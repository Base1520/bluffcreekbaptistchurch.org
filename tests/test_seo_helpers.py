"""Focused contracts for schema content and legacy-URL migration."""

from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urljoin

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from seo_helpers import LEGACY_REDIRECTS, generate_redirects, schema_json
import build


SITE = "https://www.bluffcreekbaptistchurch.org"


class RedirectDocument(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refresh = None
        self.canonical = None
        self.link = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "meta" and attributes.get("http-equiv") == "refresh":
            self.refresh = attributes["content"].split("url=", 1)[1]
        elif tag == "link" and attributes.get("rel") == "canonical":
            self.canonical = attributes["href"]
        elif tag == "a":
            self.link = attributes["href"]


class PageDocument(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.scripts = []
        self.current_script = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        self.elements.append((tag, attributes))
        if tag == "script":
            self.current_script = {"attributes": attributes, "text": ""}

    def handle_data(self, data):
        if self.current_script is not None:
            self.current_script["text"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.current_script is not None:
            self.scripts.append(self.current_script)
            self.current_script = None


class SchemaTests(unittest.TestCase):
    def test_canonicals_and_supplied_public_details(self):
        for slug, expected in (("index", SITE + "/"), ("visit", SITE + "/visit.html")):
            with self.subTest(slug=slug):
                graph = json.loads(schema_json(SITE + "/", slug, "A title", "Description"))["@graph"]
                church, page = graph
                self.assertEqual(church["@type"], "Church")
                self.assertEqual(page["@type"], "WebPage")
                self.assertEqual(page["url"], expected)
                self.assertEqual(page["about"]["@id"], church["@id"])
                self.assertEqual(church["address"]["streetAddress"], "1706 Highway 63")
                self.assertEqual(church["address"]["postalCode"], "70722")
                for field in ("telephone", "email", "geo", "openingHours", "openingHoursSpecification"):
                    self.assertNotIn(field, church)

    def test_services_are_verified_sunday_starts_not_office_hours(self):
        church = json.loads(schema_json(SITE, "times", "When We Meet", "Schedule"))["@graph"][0]
        schedules = [event["eventSchedule"] for event in church["event"]]
        self.assertEqual([schedule["startTime"] for schedule in schedules], ["10:15:00", "18:00:00"])
        for schedule in schedules:
            self.assertEqual(schedule["byDay"], "https://schema.org/Sunday")
            self.assertEqual(schedule["scheduleTimezone"], "America/Chicago")
            self.assertEqual(schedule["repeatFrequency"], "P1W")
            self.assertNotIn("endTime", schedule)

    def test_script_closing_copy_cannot_escape_json_script(self):
        title = '</script><script>alert("test")</script>'
        payload = schema_json(SITE, "visit", title, "A & B > C\u2028D")
        self.assertNotIn("<", payload)
        self.assertNotIn(">", payload)
        self.assertEqual(json.loads(payload)["@graph"][1]["name"], title)

    def test_optional_links_do_not_introduce_invalid_urls(self):
        graph = json.loads(schema_json(
            SITE, "index", "Home", "Description", app="https://app.example.org/",
            watch="javascript:alert(1)", facebook="https://facebook.com/example",
        ))["@graph"]
        self.assertEqual(graph[0]["sameAs"], ["https://facebook.com/example"])
        self.assertEqual(graph[1]["relatedLink"], "https://app.example.org/")


class GeneratedPageTests(unittest.TestCase):
    def document(self, slug):
        return PageDocument(build.layout(slug, *build.PAGES[slug]))

    def test_contact_is_a_validated_draft_with_initially_hidden_status(self):
        elements = self.document("contact").elements
        by_id = {attrs["id"]: attrs for _, attrs in elements if "id" in attrs}
        self.assertNotIn("novalidate", by_id["cform"])
        self.assertIn("hidden", by_id["cok"])
        self.assertEqual(by_id["cok"]["role"], "status")
        for field in ("cn", "ce", "cm"):
            self.assertIn("required", by_id[field])

    def test_rendered_schema_uses_public_social_profiles(self):
        script = next(script for script in self.document("index").scripts
                      if script["attributes"].get("type") == "application/ld+json")
        church = json.loads(script["text"])["@graph"][0]
        self.assertIn("https://www.youtube.com/channel/" + build.YT_CHANNEL_ID, church["sameAs"])
        self.assertIn("https://www.instagram.com/bluffcreekbaptistchurch/", church["sameAs"])
        self.assertIn("https://www.instagram.com/bluffcreekstudents/", church["sameAs"])
        self.assertTrue(all(not url.endswith("/live") for url in church["sameAs"]))

    @unittest.skipUnless(shutil.which("node"), "Node is needed to exercise generated JavaScript")
    def test_contact_handoff_keeps_draft_and_encodes_real_line_breaks(self):
        script = next(script["text"] for script in self.document("contact").scripts
                      if "getElementById('cform')" in script["text"])
        harness = r'''
const assert = require('node:assert/strict');
const vm = require('node:vm');
let submit;
const fields = ['Visitor', 'visitor@example.invalid', 'A question\nSecond line'].map(value => ({
  value, validationMessage: '', addEventListener() {},
  setCustomValidity(message) { this.validationMessage = message; }
}));
const original = fields.map(field => field.value);
const form = {
  style: {}, addEventListener(type, callback) { if(type === 'submit') submit = callback; },
  reportValidity() { return fields.every(field => !field.validationMessage); }
};
const status = { hidden: true };
const elements = { cform: form, cn: fields[0], ce: fields[1], cm: fields[2], cok: status };
const location = { href: '' };
vm.runInNewContext(SCRIPT, { document: { getElementById: id => elements[id] }, location });
submit({ preventDefault() {} });
assert.equal(status.hidden, false);
assert.deepEqual(fields.map(field => field.value), original);
assert.equal(form.style.display, undefined);
const mail = new URL(location.href);
assert.equal(mail.protocol, 'mailto:');
assert.equal(mail.searchParams.get('body'), 'From: Visitor\nContact: visitor@example.invalid\n\nA question\nSecond line');
fields[0].value = '   ';
location.href = '';
submit({ preventDefault() {} });
assert.equal(location.href, '');
assert.ok(fields[0].validationMessage);
'''.replace("SCRIPT", json.dumps(script))
        subprocess.run([shutil.which("node"), "-e", harness], check=True, capture_output=True, text=True)

    @unittest.skipUnless(shutil.which("node"), "Node is needed to exercise generated JavaScript")
    def test_nested_404_uses_host_base_and_keeps_skip_link_on_error_page(self):
        document = self.document("404")
        self.assertTrue(any(tag == "meta" and attrs.get("name") == "robots"
                            and "noindex" in attrs.get("content", "") for tag, attrs in document.elements))
        self.assertFalse(any(script["attributes"].get("type") == "application/ld+json"
                             for script in document.scripts))
        script = next(script["text"] for script in document.scripts if ".github.io" in script["text"])
        harness = r'''
const assert = require('node:assert/strict');
const vm = require('node:vm');
for (const [hostname, pathname, expectedBase] of [
  ['localhost', '/missing/nested/path', '/'],
  ['www.bluffcreekbaptistchurch.org', '/missing/nested/path', '/'],
  ['base1520.github.io', '/bluffcreekbaptistchurch.org/missing/nested/path', '/bluffcreekbaptistchurch.org/']
]) {
  let ready;
  const base = { href: '/', setAttribute(name, value) { this[name] = value; } };
  const link = { href: '#main', getAttribute(name) { return this[name]; }, setAttribute(name, value) { this[name] = value; } };
  const document = {
    querySelector() { return base; }, querySelectorAll() { return [link]; },
    addEventListener(name, callback) { ready = callback; }
  };
  vm.runInNewContext(SCRIPT, { document, location: { hostname, pathname, search: '?from=old' } });
  ready();
  assert.equal(base.href, expectedBase);
  assert.equal(link.href, pathname + '?from=old#main');
}
'''.replace("SCRIPT", json.dumps(script))
        subprocess.run([shutil.which("node"), "-e", harness], check=True, capture_output=True, text=True)


class RedirectTests(unittest.TestCase):
    def test_all_migration_targets_and_local_or_pages_resolution(self):
        self.assertEqual(len(LEGACY_REDIRECTS), 14)
        self.assertEqual(LEGACY_REDIRECTS["contact"], "times.html")
        self.assertEqual(LEGACY_REDIRECTS["contact-1"], "contact.html")
        self.assertEqual(LEGACY_REDIRECTS["college-career-1"], "ministries.html#adults")
        with tempfile.TemporaryDirectory() as directory:
            written = generate_redirects(directory, SITE, prefix="/bluffcreekbaptistchurch.org/")
            self.assertEqual(len(written), 14)
            for legacy, target in LEGACY_REDIRECTS.items():
                with self.subTest(legacy=legacy):
                    document = RedirectDocument((Path(directory) / legacy / "index.html").read_text())
                    self.assertEqual(document.refresh, "../" + target)
                    self.assertEqual(document.link, document.refresh)
                    page = target.partition("#")[0]
                    canonical = SITE + "/" + ("" if page == "index.html" else page)
                    self.assertEqual(document.canonical, canonical)
                    for base in ("http://localhost:8000/", "https://base1520.github.io/bluffcreekbaptistchurch.org/"):
                        self.assertEqual(urljoin(base + legacy + "/", document.link), base + target)

    def test_existing_unrelated_files_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            unrelated = Path(directory) / "keep.txt"
            unrelated.write_text("Keep this")
            generate_redirects(directory, SITE)
            generate_redirects(directory, SITE)
            self.assertEqual(unrelated.read_text(), "Keep this")


if __name__ == "__main__":
    unittest.main()

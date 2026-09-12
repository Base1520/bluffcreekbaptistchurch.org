"""Structured data and static legacy redirects for the church website.

These helpers perform no network requests. Content is limited to the public
church details and Sunday service start times supplied in the project brief.
"""

import html
import json
from pathlib import Path
from urllib.parse import urlsplit


CHURCH_NAME = "Bluff Creek Baptist Church"

# The old Squarespace slugs are intentionally preserved, including /contact,
# which was the meeting-times page rather than the contact page.
LEGACY_REDIRECTS = {
    "new-page": "about.html",
    "what-we-do-1": "beliefs.html",
    "contact": "times.html",
    "contact-1": "contact.html",
    "children-students-1": "ministries.html#kidz",
    "college-career-1": "ministries.html#adults",
    "women-men": "ministries.html#adults",
    "new-page-1": "ministries.html#adults",
    "church-membership": "membership.html",
    "membership": "membership.html",
    "mission": "missions.html",
    "donate": "give.html",
    "take-action": "visit.html",
    "home": "index.html",
}


def _site_base(site):
    """Return an absolute website base with one trailing slash."""
    parsed = urlsplit(site)
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        raise ValueError("site must be an absolute HTTP(S) website URL")
    if parsed.query or parsed.fragment:
        raise ValueError("site must not contain a query string or fragment")
    return site.rstrip("/") + "/"


def _canonical(site, target):
    # Fragments belong in the visitor destination, not the page canonical.
    page = target.partition("#")[0]
    return _site_base(site) + ("" if page == "index.html" else page)


def _public_url(value):
    if not value:
        return None
    parsed = urlsplit(value)
    return value if parsed.scheme in ("https", "http") and parsed.netloc else None


def schema_json(site, slug, title, desc, app=None, watch=None, facebook=None, social_urls=None):
    """Return JSON-LD text ready to place inside an application/ld+json script.

    Church service starts are recurring events, not invented office opening
    hours. End times, coordinates, individual names, email addresses, and phone
    numbers are deliberately absent. JSON escapes HTML delimiters so page copy
    cannot accidentally close the surrounding script element.
    """
    if not slug or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for character in slug):
        raise ValueError("slug must be a plain generated page name")

    base = _site_base(site)
    canonical = _canonical(base, slug + ".html")
    church_id = base + "#church"
    church = {
        "@type": "Church",
        "@id": church_id,
        "name": CHURCH_NAME,
        "url": base,
        "logo": base + "assets/logo.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "1706 Highway 63",
            "addressLocality": "Clinton",
            "addressRegion": "LA",
            "postalCode": "70722",
            "addressCountry": "US",
        },
        "event": [
            {
                "@type": "Event",
                "name": name,
                "url": base + "times.html",
                "location": {"@id": church_id},
                "eventSchedule": {
                    "@type": "Schedule",
                    "repeatFrequency": "P1W",
                    "byDay": "https://schema.org/Sunday",
                    "startTime": start,
                    "scheduleTimezone": "America/Chicago",
                },
            }
            for name, start in (
                ("Sunday worship", "10:15:00"),
                ("Sunday evening service", "18:00:00"),
            )
        ],
    }
    public_social_urls = list(dict.fromkeys(
        url for url in (_public_url(value) for value in [watch, facebook, *(social_urls or [])]) if url
    ))
    if public_social_urls:
        church["sameAs"] = public_social_urls

    page = {
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": desc,
        "inLanguage": "en-US",
        "about": {"@id": church_id},
    }
    if _public_url(app):
        page["relatedLink"] = app

    result = json.dumps(
        {"@context": "https://schema.org", "@graph": [church, page]},
        ensure_ascii=False, indent=2,
    )
    return (result.replace("&", "\\u0026").replace("<", "\\u003c")
            .replace(">", "\\u003e").replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def generate_redirects(root, site, prefix=""):
    """Write legacy-slug/index.html stubs; return their filesystem paths.

    ``root`` is the publish directory. ``prefix`` may identify its deployment
    subpath (for example /bluffcreekbaptistchurch.org); the ../ destinations
    intentionally do not depend on it, so the same output works on localhost,
    GitHub project Pages, and the custom domain. Canonicals always use ``site``.

    These are immediate HTML redirects, not HTTP 301 responses. A visible link
    remains available when automatic refresh is disabled.
    """
    _site_base(site)
    if prefix and (urlsplit(prefix).scheme or urlsplit(prefix).netloc):
        raise ValueError("prefix is a deployment path, not an absolute URL")

    root = Path(root)
    written = []
    for legacy, target in LEGACY_REDIRECTS.items():
        destination = "../" + target
        canonical = _canonical(site, target)
        link = html.escape(destination, quote=True)
        canonical_attr = html.escape(canonical, quote=True)
        content = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page moved — {CHURCH_NAME}</title>
<meta http-equiv="refresh" content="0; url={link}">
<link rel="canonical" href="{canonical_attr}">
<style>
body{{margin:0;background:#F5EFE3;color:#221F1A;font:18px/1.6 system-ui,sans-serif}}
main{{max-width:36rem;margin:12vh auto;padding:2rem}}
h1{{font-family:Georgia,serif;font-size:2.4rem;line-height:1.15}}
a{{color:#3C5A45;text-underline-offset:.2em}}
a:focus-visible{{outline:3px solid #3C5A45;outline-offset:5px}}
</style>
</head>
<body>
<main>
<p>{CHURCH_NAME}</p>
<h1>This page has moved.</h1>
<p><a href="{link}">Continue to the updated page</a>.</p>
</main>
</body>
</html>
'''
        output = root / legacy / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        written.append(output)
    return written

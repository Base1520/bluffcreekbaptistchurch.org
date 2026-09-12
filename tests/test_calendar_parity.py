"""The generator, browser, and canonical fallback must agree on verified recurrence."""
import datetime
import json
from pathlib import Path
import subprocess
import unittest
from event_helpers import expand_recurring

ROOT = Path(__file__).resolve().parents[1]

class CalendarParityTest(unittest.TestCase):
    def test_static_and_browser_calendar_match_across_seed_expiry_and_dst(self):
        data = json.loads((ROOT / 'data/events-fallback.json').read_text())
        for day in ['2026-09-06', '2026-09-18', '2026-11-01', '2028-02-27']:
            with self.subTest(day=day):
                code = "const c=require('./js/calendar-feed.js');process.stdout.write(JSON.stringify({data:c.DEFAULT_FEED,events:c.expandFeed(c.DEFAULT_FEED,process.argv[1])}));"
                js = json.loads(subprocess.check_output(['node', '-e', code, day], cwd=ROOT, text=True))
                self.assertEqual(js['data'], data)
                self.assertEqual(js['events'], expand_recurring(data, datetime.date.fromisoformat(day)))

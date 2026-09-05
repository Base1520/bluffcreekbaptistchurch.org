import datetime
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("event_helpers", ROOT / "event_helpers.py")
events = importlib.util.module_from_spec(spec)
spec.loader.exec_module(events)


def event(**overrides):
    return {"when": "2026-09-06", "time": "9:00a", "title": "Sunday School", "where": "Fellowship Building", "tag": "Weekly", **overrides}


class EventHelpersTests(unittest.TestCase):
    def test_church_day_uses_chicago_across_utc_midnight_and_dst(self):
        instant = datetime.datetime.fromisoformat("2026-09-07T01:00:00+00:00")
        self.assertEqual(events.church_today(instant).isoformat(), "2026-09-06")
        self.assertEqual(events.church_today(datetime.datetime.fromisoformat("2026-12-07T05:30:00+00:00")).isoformat(), "2026-12-06")
        with self.assertRaises(ValueError):
            events.church_today(datetime.datetime(2026, 9, 6))

    def test_sort_filters_invalid_and_expired_events_without_losing_same_day(self):
        samples = [event(time="6:00p"), event(time="10:15a"), event(time="9:00a"), event(when="2026-09-05"),
                   event(when="2026-02-30"), event(time="99:99a"), event(tag="Private"), event(title=123), None]
        result = events.upcoming_events(samples, datetime.date(2026, 9, 6))
        self.assertEqual([item["time"] for item in result], ["9:00a", "10:15a", "6:00p"])
        self.assertEqual(events.upcoming_events(samples, datetime.date(2026, 9, 7)), [])

    def test_clock_boundaries_and_real_dates(self):
        for value, expected in [("12:00a", 0), ("12:00p", 720), ("9 AM", 540), ("6p", 1080), ("10:15a", 615)]:
            self.assertEqual(events.start_minutes(value), expected)
        for value in ["00:15a", "9:60a", "13:00p", "9:00", "noon", 900]:
            self.assertIsNone(events.start_minutes(value))
        self.assertEqual(events.upcoming_events([event(when="0000-01-01")], datetime.date(1, 1, 1)), [])

    def test_render_escapes_calendar_text_and_has_permanent_noscript_fallback(self):
        markup = events.render_event_rows([event(title='<img src=x onerror="alert(1)">', where='Hall & courtyard')], today=datetime.date(2026, 9, 6))
        self.assertIn('&lt;img src=x', markup)
        self.assertNotIn('<img src=x', markup)
        self.assertIn('Hall &amp; courtyard', markup)
        self.assertIn('<noscript>', markup)
        self.assertIn('Sunday School · 9:00a', markup)
        self.assertIn('Sunday Worship · 10:15a', markup)
        self.assertIn('href="times.html"', markup)
        self.assertIn('[data-events-feed] > .event-row', markup)

    def test_empty_or_expired_calendar_keeps_weekly_schedule_link(self):
        markup = events.render_event_rows([event()], today=datetime.date(2026, 10, 1))
        self.assertNotIn('<article', markup)
        self.assertIn('class="events-empty"', markup)
        self.assertIn('href="times.html"', markup)
        self.assertIn('<noscript>', markup)


if __name__ == "__main__":
    unittest.main()

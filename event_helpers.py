"""Validate dated public events and render a dependable static calendar fallback."""

import datetime
import html
import re
from zoneinfo import ZoneInfo

CHURCH_TIMEZONE = ZoneInfo("America/Chicago")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^(1[0-2]|[1-9])(?::([0-5]\d))?\s*([ap])m?$", re.I)
EMPTY_HTML = '<p class="events-empty">Find a place in the week. <a href="times.html">View our weekly gathering times <span aria-hidden="true">→</span></a></p>'
NOSCRIPT_HTML = '''<noscript><style>[data-events-feed] > .event-row,[data-events-feed] > .events-empty{display:none}</style><p class="events-noscript">Sunday School · 9:00a<br>Sunday Worship · 10:15a<br><a href="times.html">View all weekly gathering times →</a></p></noscript>'''


def church_today(now=None):
    """The church's calendar day, independent of a builder's local timezone."""
    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Provide a timezone-aware instant")
    return now.astimezone(CHURCH_TIMEZONE).date()


def start_minutes(value):
    """Accept the feed's 12-hour clock notation (9:00a, 10:15 AM, 6p)."""
    if not isinstance(value, str):
        return None
    match = TIME_RE.fullmatch(value.strip())
    if not match:
        return None
    hour, minute, period = match.groups()
    return (int(hour) % 12 + (12 if period.lower() == "p" else 0)) * 60 + int(minute or 0)


def expand_recurring(data, today=None, horizon=42):
    """Render the same verified weekday/ordinal rules used by the shared JS feed."""
    today = today or church_today()
    events = {}
    def key(event):
        return (event["when"], " ".join(event["title"].lower().split()))
    for rule in data.get("recurring", []):
        weekday, ordinal = rule.get("weekday"), rule.get("ordinal")
        if type(weekday) is not int or not 0 <= weekday <= 6:
            continue
        if ordinal is not None and (type(ordinal) is not int or not 1 <= ordinal <= 5):
            continue
        for offset in range(max(1, min(horizon, 93))):
            day = today + datetime.timedelta(days=offset)
            if (day.weekday() + 1) % 7 != weekday or (ordinal and (day.day - 1) // 7 + 1 != ordinal):
                continue
            event = {k: rule[k] for k in ("title", "time", "where", "tag") if k in rule}
            event["when"] = day.isoformat()
            if upcoming_events([event], today):
                events[key(event)] = event
    for event in upcoming_events(data.get("events", []), today):
        events[key(event)] = event
    return upcoming_events(list(events.values()), today)


def upcoming_events(events, today=None):
    today = today or church_today()
    if not isinstance(events, list):
        return []
    accepted = []
    for event in events:
        if not isinstance(event, dict):
            continue
        if any(not isinstance(event.get(field), str) or not event[field].strip() for field in ("when", "time", "title", "where", "tag")):
            continue
        if event["tag"] not in {"Weekly", "Monthly", "Special"} or not DATE_RE.fullmatch(event["when"]):
            continue
        try:
            day = datetime.date.fromisoformat(event["when"])
        except ValueError:
            continue
        minutes = start_minutes(event["time"])
        if day < today or minutes is None:
            continue
        accepted.append(event)
    # Stable for simultaneous events: preserve the calendar editor's feed order.
    return sorted(accepted, key=lambda event: (event["when"], start_minutes(event["time"])))


def render_event_rows(events, limit=3, today=None):
    rows = []
    for event in upcoming_events(events, today)[:max(1, min(int(limit), 50))]:
        day = datetime.date.fromisoformat(event["when"])
        weekday = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[day.weekday()]
        rows.append(
            f'<article class="event-row"><time datetime="{event["when"]}">'
            f'<span>{weekday}</span>{day.day}</time><div><h3>{html.escape(event["title"])}'
            f'</h3><p>{html.escape(event["time"])} · {html.escape(event["where"])}</p></div></article>'
        )
    # Without JavaScript, show the verified weekly schedule. Dated static HTML
    # cannot stay current forever when no new build occurs.
    return ("".join(rows) or EMPTY_HTML) + NOSCRIPT_HTML

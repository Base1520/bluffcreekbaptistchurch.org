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
    if data.get("source") == "icloud":
        return upcoming_events(data.get("events", []), today)
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
        all_day = event.get("allDay") is True
        if minutes is None and event["time"] != "Time to be confirmed" and not (all_day and event["time"] == "All day"):
            continue
        end_day = None
        if "endsAt" in event:
            try:
                if all_day:
                    end_day = datetime.date.fromisoformat(event["endsAt"])
                    if end_day <= day:
                        continue
                else:
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z", event["endsAt"]):
                        continue
                    end_day = datetime.datetime.fromisoformat(event["endsAt"]).astimezone(CHURCH_TIMEZONE).date()
                    if end_day < day:
                        continue
            except (ValueError, TypeError):
                continue
        if day < today and not (end_day and (end_day > today if all_day else end_day >= today)):
            continue
        accepted.append(event)
    # Stable for simultaneous events: preserve the calendar editor's feed order.
    return sorted(accepted, key=lambda event: (event["when"], -1 if event.get("allDay") else start_minutes(event["time"]) if start_minutes(event["time"]) is not None else 1440))


def event_time_label(event):
    if not event.get("endsAt"):
        return event["time"]
    if event.get("allDay"):
        last = datetime.date.fromisoformat(event["endsAt"]) - datetime.timedelta(days=1)
        return "All day" if last.isoformat() == event["when"] else f"All day · through {last:%b} {last.day}"
    end = datetime.datetime.fromisoformat(event["endsAt"]).astimezone(CHURCH_TIMEZONE)
    end_time = f"{end.hour % 12 or 12}:{end.minute:02d}{'p' if end.hour >= 12 else 'a'}"
    return f'{event["time"]}–{end_time}' if end.date().isoformat() == event["when"] else f'{event["time"]} · through {end:%b} {end.day} {end_time}'


def render_event_rows(events, limit=3, today=None):
    rows = []
    for event in upcoming_events(events, today)[:max(1, min(int(limit), 50))]:
        day = datetime.date.fromisoformat(event["when"])
        weekday = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[day.weekday()]
        rows.append(
            f'<article class="event-row"><time datetime="{event["when"]}">'
            f'<span>{weekday}</span>{day.day}</time><div><h3>{html.escape(event["title"])}'
            f'</h3><p>{html.escape(event_time_label(event))} · {html.escape(event["where"])}</p></div></article>'
        )
    # Without JavaScript, show the verified weekly schedule. Dated static HTML
    # cannot stay current forever when no new build occurs.
    return ("".join(rows) or EMPTY_HTML) + NOSCRIPT_HTML

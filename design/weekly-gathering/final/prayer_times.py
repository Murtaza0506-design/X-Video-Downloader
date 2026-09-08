#!/usr/bin/env python3
"""Auto-compute the leaflet's programme times from the real Maghrib time for
   a given date, instead of typing them in by hand and having them drift out
   of sync with sunset as the date moves through the year.

   Maghrib comes from the Aladhan API (api.aladhan.com), calculation method 3
   (Muslim World League) — a standard astronomical method, not a specific
   local mosque timetable. If the tariqa's own committee publishes a
   timetable that differs from this by a few minutes, override MAGHRIB_OVERRIDES
   below for the dates that matter, or swap fetch_maghrib()'s method.
"""
import datetime, json, urllib.request

# Rochdale, OL12 6QG
LAT, LON = 53.6097, -2.1561
TZ = "Europe/London"
METHOD = 3  # Muslim World League

# How the rest of the evening is scheduled relative to Maghrib — inferred
# from the one example poster (29 August 2026: session 7:00, talk 8:15-8:30,
# Maghrib "8:30", ends "9:00"). Adjust these three numbers if the tariqa's
# actual practice differs — everything else derives from them.
SESSION_BEFORE_MAGHRIB = 90   # Wadhifa Dhikr and Dhikr al Faraj starts this many minutes before Maghrib
TALK_BEFORE_MAGHRIB = 15      # the talk starts this many minutes before Maghrib
EVENT_END_AFTER_MAGHRIB = 30  # refreshments/close, this many minutes after Maghrib

# Manual overrides for specific ISO dates ("YYYY-MM-DD" -> "HH:MM", 24h),
# for when the calculated time needs to be swapped for a published local
# timetable value instead of trusting the API.
MAGHRIB_OVERRIDES = {}


def fetch_maghrib(event_date: datetime.date) -> datetime.time:
    key = event_date.isoformat()
    if key in MAGHRIB_OVERRIDES:
        h, m = MAGHRIB_OVERRIDES[key].split(":")
        return datetime.time(int(h), int(m))
    url = (f"https://api.aladhan.com/v1/timings/{event_date:%d-%m-%Y}"
           f"?latitude={LAT}&longitude={LON}&method={METHOD}&timezonestring={TZ}")
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
    h, m = data["data"]["timings"]["Maghrib"].split(":")
    return datetime.time(int(h), int(m))


def _fmt(t: datetime.time) -> str:
    h = t.hour % 12 or 12
    return f"{h}:{t.minute:02d}"


def _fmt_ampm(t: datetime.time) -> str:
    return f"{_fmt(t)} {'am' if t.hour < 12 else 'pm'}"


def build_schedule(event_date: datetime.date) -> dict:
    """Returns the strings final.py's page()/bottom_html() need, computed
       from the real Maghrib time for event_date."""
    maghrib = fetch_maghrib(event_date)
    base = datetime.datetime.combine(event_date, maghrib)
    session_start = base - datetime.timedelta(minutes=SESSION_BEFORE_MAGHRIB)
    talk_start = base - datetime.timedelta(minutes=TALK_BEFORE_MAGHRIB)
    event_end = base + datetime.timedelta(minutes=EVENT_END_AFTER_MAGHRIB)

    return dict(
        weekday=event_date.strftime("%A").upper(),
        date_str=event_date.strftime("%-d %B %Y"),
        event_window=f"{_fmt(session_start)} – {_fmt_ampm(event_end)}",
        slot1_time=f"{_fmt(session_start)} – {_fmt(talk_start)}",
        slot2_time=f"{_fmt(talk_start)} – {_fmt(base)}",
        slot3_time=_fmt(base),
        maghrib_24h=f"{maghrib.hour:02d}:{maghrib.minute:02d}",
    )


if __name__ == "__main__":
    import sys
    d = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date(2026, 8, 29)
    sched = build_schedule(d)
    for k, v in sched.items():
        print(f"{k:14s} {v}")

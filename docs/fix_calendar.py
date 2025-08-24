# fix_calendar.py
import requests
from datetime import datetime, timedelta

URL = "https://maristeastwood-nsw.compass.education/download/sharedCalendar.aspx?uid=4760&key=3e2b483d-54f8-4407-b698-c3587b2bd511&c.ics"
ICAL_FILE = "docs/fixed_calendar.ics"

def convert_utc_to_aest(utc_str):
    dt = datetime.strptime(utc_str, "%Y%m%dT%H%M%SZ")
    dt += timedelta(hours=10)  # Convert UTC to AEST (+10)
    return dt.strftime("%Y%m%dT%H%M%S")

def main():
    res = requests.get(URL)
    content = res.text
    lines = content.splitlines()
    fixed_lines = []

    for line in lines:
        if line.startswith("DTSTART:"):
            time_str = line.replace("DTSTART:", "")
            fixed_lines.append(f"DTSTART;TZID=Australia/Sydney:{convert_utc_to_aest(time_str)}")
        elif line.startswith("DTEND:"):
            time_str = line.replace("DTEND:", "")
            fixed_lines.append(f"DTEND;TZID=Australia/Sydney:{convert_utc_to_aest(time_str)}")
        else:
            fixed_lines.append(line)

    with open(ICAL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(fixed_lines))

if __name__ == "__main__":
    main()

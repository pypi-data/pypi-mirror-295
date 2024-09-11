import re
from datetime import datetime, date


def parse_java_calendar(calendar_str):
    if not calendar_str or calendar_str == "null":
        return None
    pattern = r"YEAR=(\d+).*MONTH=(\d+).*DAY_OF_MONTH=(\d+).*HOUR_OF_DAY=(\d+).*MINUTE=(\d+).*SECOND=(\d+)"
    match = re.search(pattern, calendar_str)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups())
        return datetime(year, month + 1, day, hour, minute, second)
    return None


def parse_java_calendar_date(calendar_str):
    if not calendar_str or calendar_str == "null":
        return None
    pattern = r"YEAR=(\d+).*MONTH=(\d+).*DAY_OF_MONTH=(\d+)"
    match = re.search(pattern, calendar_str)
    if match:
        year, month, day = map(int, match.groups())
        return date(year, month + 1, day)
    return None

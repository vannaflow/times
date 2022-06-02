import datetime
from typing import Iterable, List

import pandas as pd
from dateutil import parser


def is_weekday(date: datetime.date) -> bool:
    return date.weekday() < 5


holiday_cache = {}


def get_holidays(date: datetime.date) -> List[datetime.date]:
    if date.year < 1990 or date.year > 2023:
        return []

    if date.year in holiday_cache:
        return holiday_cache[date.year]

    url = f"http://www.market-holidays.com/{date.year}"
    df = pd.read_html(url)

    dates = []
    for i in range(len(df[0])):
        date = parser.parse(df[0][1][i]).date()
        dates.append(date)

    holiday_cache[date.year] = dates

    return dates


def is_holiday(date: datetime.date) -> bool:
    return date in get_holidays(date)


def is_trading_day(date: datetime.date) -> bool:
    return is_weekday(date) and not is_holiday(date)


def next_trading_day(date: datetime.date) -> datetime.date:
    date += datetime.timedelta(days=1)

    while not is_trading_day(date):
        date += datetime.timedelta(days=1)

    return date


def last_trading_day(date: datetime.date) -> datetime.date:
    date -= datetime.timedelta(days=1)

    while not is_trading_day(date):
        date -= datetime.timedelta(days=1)

    return date


def date_range(start: datetime.date, end: datetime.date) -> Iterable[datetime.date]:
    for i in range((end - start).days + 1):
        yield start + datetime.timedelta(i)


def trading_days_till_expiry(start: datetime.date, end: datetime.date) -> int:
    count = 0

    for date in date_range(start, end):
        if is_trading_day(date):
            count += 1

    return count

import datetime


def next_trading_day(date: datetime.date) -> datetime.date:
    date += datetime.timedelta(days=1)

    while date.weekday() > 4:
        date += datetime.timedelta(days=1)

    return date


def last_trading_day(date: datetime.date) -> datetime.date:
    date -= datetime.timedelta(days=1)

    while date.weekday() > 4:
        date -= datetime.timedelta(days=1)

    return date

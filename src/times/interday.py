import datetime


def is_weekday(date: datetime.date) -> bool:
    return date.weekday() < 5


def is_trading_day(date: datetime.date) -> bool:
    return is_weekday(date)


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

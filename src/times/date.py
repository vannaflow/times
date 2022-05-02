import datetime
from typing import Optional, Tuple

import numpy as np
import pandas as pd


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


def last_trading_day_before_vix_expiry(
    opex_month: int, opex_year: int
) -> datetime.date:
    # Derive the last trading day before VIX expiration, given the OPEX expiry
    # month and year.
    if opex_month > 12:
        opex_year += 1
        opex_month = 1

    opex_date = datetime.date(opex_year, opex_month, 1)
    days_till_friday = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 6, 6: 5}

    return opex_date + datetime.timedelta(
        opex_date.day + days_till_friday[opex_date.weekday()] + 14 - 32
    )


def vix_expiry(start: datetime.date, maturity: int) -> datetime.date:
    month = start.month
    year = start.year

    # Get the next month's VIX expiration if this month has already passed.
    if (last_trading_day_before_vix_expiry(month + 1, year) - start).days < 0:
        month += 1

    # Rollover the date if the contract is in the new year.
    if month + maturity > 12:
        # Roll over the year and subtract 12 months.
        month -= 12
        year += 1

    return last_trading_day_before_vix_expiry(month + maturity, year)


def trading_days_till_expiry(start: datetime.date, expiry: datetime.date) -> int:
    # Find the number of days excluding weekends till expiration but count the
    # start and expiry date as days.
    return int(
        np.busday_count(pd.Timestamp(start).date(), pd.Timestamp(expiry).date()) + 1
    )


def last_trading_days_till_expiry(
    last: Optional[datetime.date] = None,
) -> Tuple[int, int]:
    # Iterate back in time from the last trading day to find a contract with
    # one or fewer days until expiry to determine the number of days in the
    # current expiration cycle.
    if not last:
        return 0, 0

    days_in_cycle = 0
    while True:
        days_till_expiry = trading_days_till_expiry(last, vix_expiry(last, 1))

        if days_till_expiry <= 1:
            break

        days_in_cycle = days_till_expiry
        last = last_trading_day(last)

    return (days_in_cycle, days_till_expiry)

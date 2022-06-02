import datetime
from typing import Optional, Tuple

from .interday import last_trading_day, trading_days_till_expiry

# VIX expiry is usually 30 days before the third Friday of the following month
# (OPEX). If there are public holidays, the expiration is on the business day
# before.


def vix_expiry_from_opex(
    opex_year: int,
    opex_month: int,
) -> datetime.date:
    if opex_month > 12:
        opex_year += opex_month // 12
        opex_month = opex_month % 12

    opex_date = datetime.date(opex_year, opex_month, 1)
    days_till_friday = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 6, 6: 5}

    return opex_date + datetime.timedelta(
        opex_date.day + days_till_friday[opex_date.weekday()] + 14 - 32
    )


def vix_expiry(start: datetime.date, maturity: int) -> datetime.date:
    month = start.month

    if (vix_expiry_from_opex(start.year, month + 1) - start).days < 0:
        month += 1

    return vix_expiry_from_opex(start.year, month + maturity)


def get_days_in_vix_cycle(
    start: Optional[datetime.date] = None,
) -> Tuple[int, int]:
    # A new cycle begins the day after there is one day to VIX expiry.

    if not start:
        return 0, 0

    next = start
    days_in_cycle = 0
    days_till_vix_expiry = None
    while True:
        days_till_expiry = trading_days_till_expiry(next, vix_expiry(next, 1))

        if days_till_vix_expiry is None:
            days_till_vix_expiry = days_till_expiry

        if days_till_expiry == 1:
            break

        days_in_cycle = days_till_expiry
        next = last_trading_day(next)

    return (days_in_cycle, days_till_vix_expiry)

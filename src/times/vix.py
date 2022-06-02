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
    year = start.year

    # Get the next month's VIX expiration if this month has already passed.
    if (vix_expiry_from_opex(year, month + 1) - start).days < 0:
        month += 1

    # Rollover the date if the contract is in the new year.
    if month + maturity > 12:
        # Roll over the year and subtract 12 months.
        month -= 12
        year += 1

    return vix_expiry_from_opex(year, month + maturity)


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

import datetime

from src.times.interday import (
    get_holidays,
    is_holiday,
    is_trading_day,
    is_weekday,
    last_trading_day,
    next_trading_day,
    trading_days_till_expiry,
)


def test_is_weekday() -> None:
    assert is_weekday(datetime.date(2022, 5, 13))

    assert not is_weekday(datetime.date(2022, 5, 14))


def test_is_trading_day() -> None:
    assert is_trading_day(datetime.date(2022, 5, 13))

    assert not is_trading_day(datetime.date(2022, 5, 14))

    assert not is_trading_day(datetime.date(2023, 2, 20))


def test_next_trading_day() -> None:
    expected = datetime.date(2022, 5, 16)
    assert next_trading_day(datetime.date(2022, 5, 13)) == expected

    expected = datetime.date(2022, 5, 2)
    assert next_trading_day(datetime.date(2022, 4, 30)) == expected


def test_last_trading_day() -> None:
    expected = datetime.date(2022, 5, 13)
    assert last_trading_day(datetime.date(2022, 5, 16)) == expected

    expected = datetime.date(2022, 4, 29)
    assert last_trading_day(datetime.date(2022, 5, 2)) == expected


def test_get_holidays() -> None:
    assert not get_holidays(datetime.date(1989, 5, 13))

    assert get_holidays(datetime.date(1990, 5, 13)) == [
        datetime.date(1990, 1, 1),
        datetime.date(1990, 1, 15),
        datetime.date(1990, 2, 19),
        datetime.date(1990, 4, 13),
        datetime.date(1990, 5, 28),
        datetime.date(1990, 7, 4),
        datetime.date(1990, 9, 3),
        datetime.date(1990, 11, 22),
        datetime.date(1990, 12, 25),
    ]

    assert get_holidays(datetime.date(2023, 5, 13)) == [
        datetime.date(2023, 1, 2),
        datetime.date(2023, 1, 16),
        datetime.date(2023, 2, 20),
        datetime.date(2023, 4, 7),
        datetime.date(2023, 5, 29),
        datetime.date(2023, 7, 4),
        datetime.date(2023, 9, 4),
        datetime.date(2023, 11, 23),
        datetime.date(2023, 12, 25),
    ]

    assert not get_holidays(datetime.date(2024, 5, 13))


def test_is_holiday() -> None:
    assert is_holiday(datetime.date(2023, 2, 20))

    assert not is_holiday(
        datetime.date(2022, 6, 1)
    ), "Counted Memorial Day as a trading day"


def test_trading_days_till_expiry() -> None:
    start = datetime.date(2022, 5, 16)
    end = datetime.date(2022, 5, 20)
    assert trading_days_till_expiry(start, end) == 5

    start = datetime.date(2022, 5, 25)
    end = datetime.date(2022, 6, 1)
    assert (
        trading_days_till_expiry(start, end) == 5
    ), "Counted Memorial Day as a trading day"

    start = datetime.date(2022, 5, 17)
    end = datetime.date(2022, 5, 23)
    assert (
        trading_days_till_expiry(start, end) == 5
    ), "Counted the weekend as trading days"

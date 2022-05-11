import datetime

from src.times.interday import is_weekday, last_trading_day, next_trading_day


def test_is_weekday() -> None:
    assert is_weekday(datetime.date(2022, 5, 13))
    assert not is_weekday(datetime.date(2022, 5, 14))


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

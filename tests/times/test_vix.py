import datetime

from src.times.vix import vix_expiry, vix_expiry_from_opex


def test_vix_expiry_from_opex() -> None:
    assert vix_expiry_from_opex(2022, 10) == datetime.date(2022, 9, 20)

    assert vix_expiry_from_opex(2022, 13) == datetime.date(2022, 12, 20)

    assert vix_expiry_from_opex(2022, 14) == datetime.date(2023, 1, 17)

    assert vix_expiry_from_opex(2021, 26) == datetime.date(2023, 1, 17)

    assert vix_expiry_from_opex(2023, 2) == datetime.date(2023, 1, 17)


def test_vix_expiry() -> None:
    start = datetime.date(2022, 6, 1)
    expected = datetime.date(2022, 9, 20)
    assert vix_expiry(start, 4) == expected

    start = datetime.date(2022, 6, 15)
    assert vix_expiry(start, 3) == expected

    expected = datetime.date(2023, 1, 17)
    assert vix_expiry(start, 7) == expected

    start = datetime.date(2020, 6, 27)
    assert vix_expiry(start, 31) == expected

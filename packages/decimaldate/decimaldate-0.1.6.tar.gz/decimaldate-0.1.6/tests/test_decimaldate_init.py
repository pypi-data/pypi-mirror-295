from datetime import datetime

import pytest

from decimaldate import DecimalDate


def test_init_no_arguments(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # WHEN
    sut: DecimalDate = DecimalDate()
    # THEN
    assert sut == DecimalDate.today()
    assert sut.as_int() == today_as_decimaldate_int


def test_init_none(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # WHEN
    sut: DecimalDate = DecimalDate(None)
    # THEN
    assert sut == DecimalDate.today()
    assert sut.as_int() == today_as_decimaldate_int


def test_init_bad_string_raises_valueerror() -> None:
    with pytest.raises(
        expected_exception=ValueError,
    ):
        _ = DecimalDate("badstring")


def test_init_int_today(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # GIVEN
    today_as_int: int = today_as_decimaldate_int
    # WHEN
    sut: DecimalDate = DecimalDate(today_as_int)
    # THEN
    assert sut.as_int() == today_as_decimaldate_int
    assert sut.as_str() == str(today_as_decimaldate_int)


def test_init_str_today(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # GIVEN
    today_as_str: str = str(today_as_decimaldate_int)
    # WHEN
    sut: DecimalDate = DecimalDate(today_as_str)
    # THEN
    assert sut.as_int() == today_as_decimaldate_int
    assert sut.as_str() == str(today_as_decimaldate_int)


def test_init_datetime_today(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # GIVEN
    today_as_dd: DecimalDate = DecimalDate(today_as_decimaldate_int)
    # WHEN
    sut: DecimalDate = DecimalDate(today_as_dd)
    # THEN
    assert sut.as_int() == today_as_decimaldate_int
    assert sut.as_str() == str(today_as_decimaldate_int)


def test_init_datetime(
    freezer,
) -> None:
    # GIVEN
    arbitrary_date = 2024_09_22
    arbitrary_dd: DecimalDate = DecimalDate(arbitrary_date)
    # WHEN
    sut: DecimalDate = DecimalDate(arbitrary_dd)
    # THEN
    assert sut.as_int() == arbitrary_date
    assert sut.as_str() == str(arbitrary_date)


def test_init_float_raises_typeerror() -> None:
    # GIVEN
    bad_arg: float = 20240534.0
    # THEN
    with pytest.raises(
        expected_exception=TypeError,
    ):
        _ = DecimalDate(bad_arg)  # type: ignore[arg-type]


def test_init_datetime_now(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # GIVEN
    today: datetime = datetime.today()  # no tzinfo
    # WHEN
    sut = DecimalDate(today)
    # THEN
    assert sut.as_int() == today_as_decimaldate_int

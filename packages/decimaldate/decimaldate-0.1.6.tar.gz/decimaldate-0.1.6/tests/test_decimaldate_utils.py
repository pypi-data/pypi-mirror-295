from typing import Literal

import pytest

from decimaldate import DecimalDate

"""
split
"""


def test_split_str_returns_ymd() -> None:
    # GIVEN
    ds: str = "20240630"
    sut: DecimalDate = DecimalDate(ds)
    # WHEN
    sut_y, sut_m, sut_d = sut.split()
    # THEN
    assert sut_y == 2024
    assert sut_m == 6
    assert sut_d == 30


def test_split_int_returns_ymd() -> None:
    # GIVEN
    dd: int = 2024_06_30
    sut: DecimalDate = DecimalDate(dd)
    # WHEN
    sut_y, sut_m, sut_d = sut.split()
    # THEN
    assert sut_y == 2024
    assert sut_m == 6
    assert sut_d == 30


"""
clone
"""


def test_clone_equal_value() -> None:
    # GIVEN
    dd_int: int = 2023_09_30
    dd: DecimalDate = DecimalDate(dd_int)
    # WHEN
    sut = dd.clone()
    # THEN
    assert sut == dd


def test_clone_not_equal_reference() -> None:
    # GIVEN
    dd_int: int = 2023_09_30
    dd: DecimalDate = DecimalDate(dd_int)
    # WHEN
    sut = dd.clone()
    # THEN
    assert sut == dd
    assert sut is not dd


def test_clone_internals() -> None:
    # GIVEN
    dd_int_29: int = 2024_09_29
    dd_int_30: int = 2023_09_30
    dd: DecimalDate = DecimalDate(dd_int_30)

    # WHEN
    dd_clone = dd.clone()
    # abuse access
    dd_clone._DecimalDate__dd_int = dd_int_29  # type: ignore[attr-defined]

    # THEN
    assert dd.as_int() == dd_int_30
    assert dd_clone.as_int() == dd_int_29
    assert dd != dd_clone


"""
next
"""


def test_next_31daymonth_1nexts_as_expected() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20201001" == sut.next().as_str()


def test_next_31daymonth_2nexts_as_expected() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20201002" == sut.next().next().as_str()


def test_next_30daymonth_1nexts_as_expected() -> None:
    # GIVEN
    ds: str = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20201031" == sut.next().as_str()


def test_next_30daymonth_2nexts_as_expected() -> None:
    # GIVEN
    ds: str = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20201101" == sut.next().next().as_str()


def test_next_next_is_two_days_previous() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.next().next() == sut.next(2)


def test_next_multiple_next() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.next(43).next(7) == sut.next(43 + 7)


def test_next_zero_is_identical() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.next(0) == sut


def test_next_none_raises_typeerror() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    with pytest.raises(expected_exception=TypeError):
        _ = sut.next(None)  # type: ignore[arg-type]  # NOSONAR


"""
previous
"""


def testprevious_31daymonth_1previous_as_expected() -> None:
    # GIVEN
    ds: str = "20201101"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20201031" == sut.previous().as_str()


def test_previous_31daymonth_2previous_as_expected() -> None:
    # GIVEN
    ds: str = "20201102"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20201031" == sut.previous().previous().as_str()


def test_previous_30daymonth_1previous_as_expected() -> None:
    # GIVEN
    ds: str = "20201001"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20200930" == sut.previous().as_str()


def test_previous_30daymonth_2previous_as_expected() -> None:
    # GIVEN
    ds: str = "20201002"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "20200930" == sut.previous().previous().as_str()


def test_previous_next_is_next_previous() -> None:
    # GIVEN
    ds: Literal["20201002"] = "20201002"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.previous().next() == sut.next().previous()
    assert sut.next().previous() == sut.previous().next()


def test_previous_previous_is_two_days_previous() -> None:
    # GIVEN
    ds: Literal["20201002"] = "20201002"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.previous().previous() == sut.previous(2)


def test_previous_multiple_previous() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.previous(43).previous(7) == sut.previous(43 + 7)


def test_previous_zero_is_identical() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.previous(0) == sut


def test_previous_none_raises_typeerror() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    with pytest.raises(expected_exception=TypeError):
        _ = sut.previous(None)  # type: ignore[arg-type]  # NOSONAR


#
#
#


def test_previous_next_are_symetrical() -> None:
    # GIVEN
    ds: Literal["20201030"] = "20201030"
    delta: int = 7
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.previous(delta) == sut.next(-delta)
    assert sut.previous(-delta) == sut.next(delta)


"""
tomorrow
"""


def test_tomorrow(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # GIVEN
    # WHEN
    sut: DecimalDate = DecimalDate(today_as_decimaldate_int)
    # THEN
    assert sut.as_int() == today_as_decimaldate_int
    assert DecimalDate.tomorrow() == sut.next()


"""
yesterday
"""


def test_yesterday(
    today_as_decimaldate_int: int,
    freezer,
) -> None:
    # GIVEN
    # WHEN
    sut: DecimalDate = DecimalDate(today_as_decimaldate_int)
    # THEN
    assert sut.as_int() == today_as_decimaldate_int
    assert DecimalDate.yesterday() == sut.previous()


"""
year
"""


def test_year() -> None:
    # GIVEN
    ds: Literal["2023_10_30"] = "2023_10_30"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.year() == 2023


"""
month
"""


def test_month() -> None:
    # GIVEN
    ds: Literal["2023_10_30"] = "2023_10_30"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.month() == 10


"""
day
"""


def test_day() -> None:
    # GIVEN
    ds: Literal["2023_10_30"] = "2023_10_30"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert sut.day() == 30


"""
last_day_of_month
"""


@pytest.mark.parametrize(
    "sut,expected",
    [
        pytest.param(DecimalDate("2023_01_06"), 31),
        pytest.param(DecimalDate("2023_02_06"), 28),
        pytest.param(DecimalDate("2024_02_06"), 29),
    ],
)
def test_last_day_of_month(sut: DecimalDate, expected: int) -> None:
    assert sut.last_day_of_month() == expected


"""
start_of_month
"""


@pytest.mark.parametrize(
    "sut,expected",
    [
        pytest.param(DecimalDate("2023_01_01"), DecimalDate("2023_01_01")),
        pytest.param(DecimalDate("2023_01_06"), DecimalDate("2023_01_01")),
        pytest.param(DecimalDate("2024_12_31"), DecimalDate("2024_12_01")),
    ],
)
def test_end_of_month(sut: DecimalDate, expected: DecimalDate) -> None:
    assert sut.end_of_month() == expected


"""
end_of_month
"""


@pytest.mark.parametrize(
    "sut,expected",
    [
        pytest.param(DecimalDate("2023_01_06"), DecimalDate("2023_01_31")),
        pytest.param(DecimalDate("2023_02_06"), DecimalDate("2023_02_28")),
        pytest.param(DecimalDate("2024_02_06"), DecimalDate("2024_02_29")),
        pytest.param(DecimalDate("2024_12_31"), DecimalDate("2024_12_31")),
    ],
)
def test_end_of_month(sut: DecimalDate, expected: DecimalDate) -> None:
    assert sut.end_of_month() == expected

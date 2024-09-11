import pytest

from decimaldate import DecimalDate, DecimalDateRange

###

dd_10_01: DecimalDate = DecimalDate(2024_10_01)
dd_10_02: DecimalDate = DecimalDate(2024_10_02)
dd_10_03: DecimalDate = DecimalDate(2024_10_03)
dd_10_04: DecimalDate = DecimalDate(2024_10_04)
dd_10_05: DecimalDate = DecimalDate(2024_10_05)
dd_10_06: DecimalDate = DecimalDate(2024_10_06)
dd_10_07: DecimalDate = DecimalDate(2024_10_07)
dd_10_08: DecimalDate = DecimalDate(2024_10_08)
dd_10_09: DecimalDate = DecimalDate(2024_10_09)
dd_10_10: DecimalDate = DecimalDate(2024_10_10)

dd_10_11: DecimalDate = DecimalDate(2024_10_11)
dd_10_12: DecimalDate = DecimalDate(2024_10_12)
dd_10_13: DecimalDate = DecimalDate(2024_10_13)
dd_10_14: DecimalDate = DecimalDate(2024_10_14)
dd_10_15: DecimalDate = DecimalDate(2024_10_15)
dd_10_16: DecimalDate = DecimalDate(2024_10_16)
dd_10_17: DecimalDate = DecimalDate(2024_10_17)
dd_10_18: DecimalDate = DecimalDate(2024_10_18)
dd_10_19: DecimalDate = DecimalDate(2024_10_19)
dd_10_20: DecimalDate = DecimalDate(2024_10_20)

dd_10_21: DecimalDate = DecimalDate(2024_10_21)
dd_10_22: DecimalDate = DecimalDate(2024_10_22)
dd_10_23: DecimalDate = DecimalDate(2024_10_23)
dd_10_24: DecimalDate = DecimalDate(2024_10_24)
dd_10_25: DecimalDate = DecimalDate(2024_10_25)
dd_10_26: DecimalDate = DecimalDate(2024_10_26)
dd_10_27: DecimalDate = DecimalDate(2024_10_27)
dd_10_28: DecimalDate = DecimalDate(2024_10_28)
dd_10_29: DecimalDate = DecimalDate(2024_10_29)
dd_10_30: DecimalDate = DecimalDate(2024_10_30)
dd_10_31: DecimalDate = DecimalDate(2024_10_31)

dd_11_01: DecimalDate = DecimalDate(2024_11_01)

sut_start_incl = dd_10_21
sut_stop_excl = dd_10_26
sut: DecimalDateRange = DecimalDateRange(sut_start_incl, sut_stop_excl)

"""
__init__
"""


def test_init_none_none_raises_valueerror() -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match=r".*None.*",
    ):
        _ = DecimalDateRange(None, None)


def test_init_dd_none_raises_valueerror() -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match=r".*None.*",
    ):
        _ = DecimalDateRange(dd_10_29, None)


def test_init_none_dd_raises_valueerror() -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match=r".*None.*",
    ):
        _ = DecimalDateRange(None, dd_10_29)


def test_init_no_arguments_raises_typeerror() -> None:
    with pytest.raises(
        expected_exception=TypeError,
        match=r".*missing 2 required positional arguments.*",
    ):
        _ = DecimalDateRange()


def test_init_none_raises_typeerror() -> None:
    with pytest.raises(
        expected_exception=TypeError,
        match=r".*missing 1 required positional argument.*",
    ):
        _ = DecimalDateRange(None)


def test_init_one_argument_raises_typeerror() -> None:
    with pytest.raises(
        expected_exception=TypeError,
        match=r".*missing 1 required positional argument.*",
    ):
        _ = DecimalDateRange(dd_10_29)


def test_init_argument_types() -> None:
    # WHEN
    rng: DecimalDateRange = DecimalDateRange(2024_10_21, "20241026")
    # THEN
    assert list(rng) == list(sut)


def test_init_argument_order() -> None:
    # GIVEN
    start: DecimalDate = dd_10_05
    stop: DecimalDate = dd_10_08
    # THEN
    assert len(DecimalDateRange(start, stop)) == 3
    assert len(DecimalDateRange(stop, start)) == 0


"""
__len__
"""


def test_len() -> None:
    # THEN
    assert len(sut) == 5


"""
__contains__
"""


def test_contains() -> None:
    # THEN
    assert dd_10_01 not in sut
    assert dd_10_20 not in sut
    assert dd_10_21 in sut
    assert dd_10_22 in sut
    assert dd_10_23 in sut
    assert dd_10_24 in sut
    assert dd_10_25 in sut
    assert dd_10_26 not in sut
    assert dd_11_01 not in sut


def test_contains_invalid_type_raises_typeerror() -> None:
    with pytest.raises(expected_exception=TypeError):
        _ = "3" in sut  # type: ignore[operator]


"""
__getitem__
"""


def test_getitem_all() -> None:
    assert sut[0] == dd_10_21
    assert sut[1] == dd_10_22
    assert sut[2] == dd_10_23
    assert sut[3] == dd_10_24
    assert sut[4] == dd_10_25


def test_getitem_zero_returns_start() -> None:
    assert sut[0] == sut_start_incl
    assert sut[-0] == sut_start_incl


def test_getitem_minus_one_returns_last_before_stop() -> None:
    assert sut[-1] == sut_stop_excl.previous(1)


def test_getitem_minus_len_returns_start() -> None:
    assert sut[-len(sut)] == sut_start_incl


def test_getitem() -> None:
    assert sut[1] == sut_start_incl.next(1)
    assert sut[-2] == sut_stop_excl.previous(2)


def test_getitem_outside_raises_indexerror() -> None:

    with pytest.raises(expected_exception=IndexError):
        _ = sut[len(sut)]

    with pytest.raises(expected_exception=IndexError):
        _ = sut[-(len(sut) + 1)]

    with pytest.raises(expected_exception=IndexError):
        _ = sut[100_000_000]

    with pytest.raises(expected_exception=IndexError):
        _ = sut[-100_000_000]


def test_getitem_invalid_type_raises_typeerror() -> None:
    with pytest.raises(expected_exception=TypeError):
        _ = sut["3"]  # type: ignore[index]


"""
__iter__
"""


def test_iter_ident_is_empty() -> None:
    # sequence 'end' is exclusive
    assert len(DecimalDateRange(dd_10_07, dd_10_07)) == 0


"""
next()
"""


def test_next() -> None:
    it = iter(sut)
    assert next(it) == dd_10_21
    assert next(it) == dd_10_22
    assert next(it) == dd_10_23
    assert next(it) == dd_10_24
    assert next(it) == dd_10_25
    with pytest.raises(expected_exception=StopIteration):
        _ = next(it)


"""
list()
"""


def test_list() -> None:
    # GIVEN
    expected: list[DecimalDate] = [
        dd_10_21,
        dd_10_22,
        dd_10_23,
        dd_10_24,
        dd_10_25,
    ]
    # THEN
    assert list(sut) == expected

from decimaldate import DecimalDate

"""
__str__
"""


def test_dunder_str_integer_prints_integer() -> None:
    # GIVEN
    dd: int = 2020_09_30
    sut: DecimalDate = DecimalDate(dd)
    # WHEN
    expected: str = str(dd)
    actual: str = str(sut)
    # THEN
    assert expected == actual


def test_dunder_str_string_prints_integer() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert int(ds) == sut.as_int()
    assert ds == str(sut)


"""
__repr__
"""


def test_dunder_repr_str() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert repr(sut) == f"DecimalDate({ds})"


def test_dunder_repr_int() -> None:
    # GIVEN
    dd: int = 2023_02_16
    # WHEN
    sut: DecimalDate = DecimalDate(dd)
    # THEN
    assert repr(sut) == f"DecimalDate({dd})"


"""
__int__
"""


def test_dunder_int_integer() -> None:
    # GIVEN
    dd: int = 2023_02_16
    # WHEN
    sut: DecimalDate = DecimalDate(dd)
    # THEN
    assert dd == sut.as_int()
    assert dd == int(sut)

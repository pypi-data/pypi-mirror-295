from decimaldate import DecimalDate

"""
as_int
"""


def test_as_int_integer_is_equal() -> None:
    # GIVEN
    dd: int = 2020_09_30
    # WHEN
    sut: DecimalDate = DecimalDate(dd)
    # THEN
    assert dd == sut.as_int()


def test_as_int_string_is_equal() -> None:
    # GIVEN
    dd: int = 2020_09_30
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert dd == sut.as_int()


"""
as_string
"""


def test_as_str_default_separator_has_no_separator() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert ds == sut.as_str()


def test_as_str_empty_separator_has_no_separator() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert ds == sut.as_str("")


def test_as_string_hyphen_separator_has_hyphen_separator() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "2020-09-30" == sut.as_str("-")


def test_as_string_dot_separator_has_dot_separator() -> None:
    # GIVEN
    ds: str = "20200930"
    # WHEN
    sut: DecimalDate = DecimalDate(ds)
    # THEN
    assert "2020.09.30" == sut.as_str(".")

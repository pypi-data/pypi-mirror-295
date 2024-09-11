from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta
from typing import Any, Literal, Self, TypeAlias

DecimalDateInitTypes: TypeAlias = int | str | datetime
"""
The regular types (excluding ``None`` and ``DecimalDate``)
that can be given as argument to 'init' methods.
"""

#
# DecimalDate
#


class DecimalDate:
    """
    A class to represent a decimal date on the form ``yyyymmdd``.

    Only dates that are valid for ``datetime`` are accepted.

    Used and exposed ``datetime`` objects in this class are *not* TimeZone aware!

    Examples::

        DecimalDate()          # today's date
        DecimalDate(None)      # today's date
        DecimalDate(20231225)
        DecimalDate("20230518")
        DecimalDate(datetime.today())
    """

    @staticmethod
    def __split(dd: int) -> tuple[int, int, int]:
        """
        A tuple with the constituent year, month, and day ``(yyyy, mm, dd)``
        from the argument decimal date on the form ``yyyymmdd``

        :param dd: A decimal date on the form ``yyyymmdd``.
        :type dd: int
        :return: A tuple with (year, month, day).
        :rtype: tuple[int, int, int]
        """
        yyyy, remain = divmod(dd, 1_00_00)
        mm, dd = divmod(remain, 1_00)
        return yyyy, mm, dd

    @staticmethod
    def __today_as_int() -> int:
        """
        Today's date as an integer on the form ``yyyymmdd``.\\
        The date is *not* TimeZone aware.

        :return: Today's date on the form ``yyyymmdd``.
        :rtype: int
        """
        today: datetime = datetime.today()  # no tzinfo
        return DecimalDate.__datetime_as_int(today)

    @staticmethod
    def __datetime_as_int(dt: datetime) -> int:
        """
        Returns an integer on the form ``yyyymmdd`` from the argument ``datetime``.

        >>> DecimalDate.__datetime_as_int(datetime.today())
            20240906

        :param dt: A ``datetime``.
        :type dt: datetime
        :return: Decimal date on the form ``yyyymmdd``.
        :rtype: int
        """
        return DecimalDate.__ymd_as_int(dt.year, dt.month, dt.day)

    @staticmethod
    def __int_as_datetime(dd: int) -> datetime:
        """
        Returns a ``datetime`` from the argument ``int`` on the form ``yyyymmdd``.

        :param dd: A decimal date on the form ``yyyymmdd``.
        :type dd: int
        :return: ``datetime`` representing the argument ``yyyymmdd``.
        :rtype: datetime
        """
        year, month, day = DecimalDate.__split(dd)
        return datetime(year, month, day)

    @staticmethod
    def __ymd_as_int(year: int, month: int, day: int) -> int:
        return year * 1_00_00 + month * 1_00 + day

    @staticmethod
    def __start_of_month(dt: datetime) -> datetime:
        """
        Start date of a year and month taken from the argument.\\
        The day will always be ``1``.

        >>> DicimalDate(DecimalDate.__start_of_month(DecimalDate("2024_02_06").as_datetime()))
            DecimalDate(20240201)

        :param dt: A ``datetime``.
        :type dt: datetime
        :return: start date of year and month.
        :rtype: datetime
        """
        return datetime.replace(day=1)  # new datetime

    @staticmethod
    def __end_of_month(dt: datetime) -> datetime:
        """
        End date of a year and month taken from the argument.

        >>> DicimalDate(DecimalDate.__end_of_month(DecimalDate("2024_02_06").as_datetime()))
            DecimalDate(20240229)

        :param dt: A ``datetime``.
        :type dt: datetime
        :return: end date of year and month.
        :rtype: datetime
        """
        # Day 28 exists in every month and 4 days later is always next month
        next_month: datetime = dt.replace(day=28) + timedelta(days=4)
        # Subtract day of next month gives last day of original month
        return next_month - timedelta(days=next_month.day)

    @staticmethod
    def __last_day_of_month(dt: datetime) -> int:
        """
        End day (1-31) of a year and month taken from the argument.

        >>> DecimalDate("2024_02_06")
            29

        :param dt: A ``datetime``.
        :type dt: datetime
        :return: End day (1-31)
        :rtype: int
        """
        return DecimalDate.__end_of_month(dt).day

    #
    # Initialization
    #

    def __init__(
        self: Self,
        dd: DecimalDateInitTypes | Self | None = None,
    ) -> None:
        """
        Construct an immutable ``DecimalDate`` instance.

        If argument is not present or ``None``, then use today's date.

        :param dd: > date representation on the form ``yyyymmdd`` or a ``datetime``, defaults to ``None``
        :type dd: DecimalDateInitTypes | Self | None, optional
        :raises ValueError: If not a valid date, that can be represented on the form ``yyyymmdd``.
        :raises TypeError: If argument type is not valid (``None``, ``DecimalDate``, ``int``, ``str``, ``datetime``).
        """

        #
        # Instance variables
        #

        self.__dd_int: int
        """ Internal instance value of the decimal date as an ``int`` on the form ``yyyymmdd``. """

        self.__dd_str: str
        """ Internal instance value of the decimal date as a ``str`` on the form ``"yyyymmdd"``. """

        self.__dd_dt: datetime
        """ Internal instance value of the decimal date as a ``datetime``. """

        self.__year: int
        """ Internal instance value of the year (1-9999). """

        self.__month: int
        """ Internal instance value of the month (1-12). """

        self.__day: int
        """ Internal instance value of the day (1-31). """

        #

        if dd is None:
            # Use the default today's date
            self.__dd_int = DecimalDate.__today_as_int()

        elif isinstance(dd, int):
            # Save argument, and validate when saving as a ``datetime``
            self.__dd_int = dd

        elif isinstance(dd, str):
            try:
                # Save argument, and validate when saving as a ``datetime``
                self.__dd_int = int(dd)
            except ValueError as e_info:
                raise ValueError(
                    f"argument {dd} is not a valid literal on the form `yyyymmdd`."
                ) from e_info

        elif isinstance(dd, datetime):
            self.__dd_int = DecimalDate.__datetime_as_int(dd)

        elif isinstance(dd, DecimalDate):
            self.__dd_int = dd.as_int()

        else:
            raise TypeError(
                f"argument {dd} is not a valid literal on the form `yyyymmdd`."
            )

        self.__dd_str = str(self.__dd_int)

        try:
            # If not a valid date, then this line raises ValueError
            self.__dd_dt = DecimalDate.__int_as_datetime(self.__dd_int)
        except ValueError as e_info:
            raise ValueError(
                f"argument {dd} is not a valid literal on the form `yyyymmdd`."
            ) from e_info

        self.__year, self.__month, self.__day = DecimalDate.__split(self.__dd_int)

    #
    # Comparisons
    #

    __UNSUPPORTED_OPERAND_TYPE: Literal["Unsupported operand type."] = (
        "Unsupported operand type."
    )

    def __eq__(self: Self, other: object) -> bool:
        """
        The equality operator, ``==``.

        :param other: the DecimalDate object to compare with.
        :type other: object
        :raises TypeError: If the object compared to is not a ``DecimalDate``.
        :return: ``True`` or ``False`` depending on the comparison.
        :rtype: bool
        """
        if isinstance(other, DecimalDate):
            return self.__dd_int == other.__dd_int
        else:
            raise TypeError(DecimalDate.__UNSUPPORTED_OPERAND_TYPE)

    def __ne__(self: Self, other: object) -> bool:
        """
        The inequality operator, ``!=``.

        :param other: Is the ``DecimalDate`` object to compare with.
        :type other: object
        :raises TypeError: If the object compared to is not a ``DecimalDate``.
        :return: ``True`` or ``False`` depending on the comparison.
        :rtype: bool
        """
        if isinstance(other, DecimalDate):
            return self.__dd_int != other.__dd_int
        else:
            raise TypeError(DecimalDate.__UNSUPPORTED_OPERAND_TYPE)

    def __gt__(self: Self, other: object) -> bool:
        """
        The greater-than operator, ``>``.

        :param other: Is the ``DecimalDate`` object to compare with.
        :type other: object
        :raises TypeError: If the object compared to is not a ``DecimalDate``.
        :return: ``True`` or ``False`` depending on the comparison.
        :rtype: bool
        """
        if isinstance(other, DecimalDate):
            return self.__dd_int > other.__dd_int
        else:
            raise TypeError(DecimalDate.__UNSUPPORTED_OPERAND_TYPE)

    def __ge__(self: Self, other: object) -> bool:
        """
        The greater-than-or-equal operator, ``>=``.

        :param other: Is the ``DecimalDate`` object to compare with.
        :type other: object
        :raises TypeError: If the object compared to is not a ``DecimalDate``.
        :return: ``True`` or ``False`` depending on the comparison.
        :rtype: bool
        """
        if isinstance(other, DecimalDate):
            return self.__dd_int >= other.__dd_int
        else:
            raise TypeError(DecimalDate.__UNSUPPORTED_OPERAND_TYPE)

    def __lt__(self: Self, other: object) -> bool:
        """
        The less-than operator, ``<``.

        :param other: Is the ``DecimalDate`` object to compare with.
        :type other: object
        :raises TypeError: If the object compared to is not a ``DecimalDate``.
        :return: ``True`` or ``False`` depending on the comparison.
        :rtype: bool
        """
        if isinstance(other, DecimalDate):
            return self.__dd_int < other.__dd_int
        else:
            raise TypeError(DecimalDate.__UNSUPPORTED_OPERAND_TYPE)

    def __le__(self: Self, other: object) -> bool:
        """
        The less-than-or-equal operator, ``<=``.

        :param other: Is the ``DecimalDate`` object to compare with.
        :type other: object
        :raises TypeError: If the object compared to is not a ``DecimalDate``.
        :return: ``True`` or ``False`` depending on the comparison.
        :rtype: bool
        """
        if isinstance(other, DecimalDate):
            return self.__dd_int <= other.__dd_int
        else:
            raise TypeError(DecimalDate.__UNSUPPORTED_OPERAND_TYPE)

    #
    # repr, str, int
    #

    def __repr__(self: Self) -> str:
        """
        When called by built-in ``repr()`` method returning a machine readable representation of ``DecimalDate``.

        >>> DecimalDate("2023_01_06")
            DecimalDate(20230106)

        :return: machine readable representation of this instance.
        :rtype: str
        """
        return f"DecimalDate({self.__dd_int})"

    def __str__(self: Self) -> str:
        """
        When ``str()`` is called on an instance of ``DecimalDate``.

        >>> str(DecimalDate(2023_01_06))
            '20230106'

        :return: string representation of this instance.
        :rtype: str
        """
        return self.__dd_str

    def __int__(self: Self) -> int:
        """
        When ``int()`` is called on an instance of ``DecimalDate``.

        >>> int(DecimalDate("2023_01_06"))
            20230106

        :return: integer representation of this instance.
        :rtype: int
        """
        return self.__dd_int

    #
    # convenience and utils
    #

    def year(self: Self) -> int:
        """
        Year (1-9999).

        >>> DecimalDate("2023_01_06").year()
            2023

        :return: Year (1-9999).
        :rtype: int
        """
        return self.__year

    def month(self: Self) -> int:
        """
        Month (1-12).

        >>> DecimalDate("2023_01_06").month()
            1

        :return: Month (1-12).
        :rtype: int
        """
        return self.__month

    def day(self: Self) -> int:
        """
        Day (0-31).

        >>> DecimalDate("2023_01_06").day()
            6

        :return: Day (0-31).
        :rtype: int
        """
        return self.__day

    def last_day_of_month(self: Self) -> int:
        """
        Day (28-31).

        >>> DecimalDate("2023_01_06").last_day_of_month()
            31

        >>> DecimalDate("2023_02_06").last_day_of_month()
            28

        >>> DecimalDate("2024_02_06").last_day_of_month()  # leap year
            29

        :return: Day (28-31).
        :rtype: int
        """
        return DecimalDate.__last_day_of_month(self.as_datetime())

    def start_of_month(self: Self) -> DecimalDate:
        """
        The start date of the month and year of this instance.\\
        The day will always be ``1``.

        :return:  A new ``DecimalDate`` with the value of start-of-month.
        :rtype: DecimalDate
        """
        return DecimalDate(DecimalDate.__start_of_month(self.as_datetime()))

    def end_of_month(self: Self) -> DecimalDate:
        """
        The end date of the month and year of this instance.\\
        For February the end day will be ``28`` or ``29`` depending on leap year.

        >>> DecimalDate("2023_01_06")
            DecimalDate(20230131)

        >>> DecimalDate("2023_02_06")
            DecimalDate(20230228)

        >>> DecimalDate("2024_02_06")
            DecimalDate(20240229)

        :return: A new ``DecimalDate`` with the value of end-of-month.
        :rtype: DecimalDate
        """
        return DecimalDate(DecimalDate.__end_of_month(self.as_datetime()))

    def split(self: Self) -> tuple[int, int, int]:
        """
        Return this object's integer value on the form ``yyyymmdd``
        as integer values for: year, month and day.

        >>> yyyy, mmm, dd = DecimalDate(2021_02_17).split()
        >>> print(yyyy, mmm, dd)
            2021 2 17

        :return: year, month, and day.
        :rtype: tuple[int, int, int]
        """
        return (self.__year, self.__month, self.__day)

    def clone(self: Self) -> DecimalDate:
        """
        Creates a new ``DecimalDate`` instance identical to original.

        Note that ``DecimalDate`` is immutable, so consider a regular assignment.

        >>> today = DecimalDate().today()
        >>> today.clone() == today
            True

        >>> today = DecimalDate().today()
        >>> today.clone() is today
            False

        :return: A new ``DecimalDate`` instance identical to original.
                 But not same reference.
        :rtype: DecimalDate
        """
        return DecimalDate(self.as_int())

    def next(self: Self, delta_days: int = 1) -> DecimalDate:
        """
        Creates a new ``DecimalDate`` instance ``delta_days`` days in the future.

        * The default argument value of ``1`` is the day after.
        * If the argument value is ``0`` then it the date of this instance.
        * If the argument is negative (<0) then it will be days in the past (opposite of future).

        :param delta_days: days in the future, defaults to ``1``.
        :type delta_days: int, optional
        :raises TypeError: if ``delta_days`` is not an ``int``.
        :return: A new ``DecimalDate`` offset with argument days.
        :rtype: DecimalDate
        """
        if not isinstance(delta_days, int):
            raise TypeError("argument for `next` is not `int`")
        next_date: datetime = self.as_datetime() + timedelta(delta_days)
        return DecimalDate(next_date)

    def previous(self: Self, delta_days: int = 1) -> DecimalDate:
        """
        Creates a new ``DecimalDate`` instance ``delta_days`` days in the past.

        * The default argument value of ``1`` is the day before.
        * If the argument value is ``0`` then it the date of this instance.
        * If the argument is negative (<0) then it will be days in the future (opposite of past).

        :param delta_days: days in the past, defaults to ``1``.
        :type delta_days: int, optional
        :raises TypeError: if ``delta_days`` is not an ``int``
        :return: A new ``DecimalDate`` offset with argument days.
        :rtype: DecimalDate
        """
        if not isinstance(delta_days, int):
            raise TypeError("argument for `previous` is not `int`")
        return self.next(-delta_days)

    #
    #
    #

    def as_int(self: Self) -> int:
        """
        This ``DecimalDate`` instance's date as a ``int`` object on the form ``yyyymmdd``.

        Convenience method similar to ``int()``.

        >>> DecimalDate(2023_04_18).as_int()
            20230418

        >>> dd = DecimalDate(2023_04_18)
        >>> int(dd) == dd.as_int()
            True

        :return: Integer representation on the form ``yyyymmdd``.
        :rtype: int
        """
        return self.__dd_int

    def as_str(
        self: Self,
        sep: str | None = None,
    ) -> str:
        """
        This ``DecimalDate`` instance's date with an optional separator as a ``str`` object.

        >>> DecimalDate(2023_04_18).as_str()
            '20230418'

        >>> DecimalDate(2023_04_18).as_str('.')
            '2023.04.18'

        :param sep: Optional separator, defaults to ``None``.
        :type sep: str | None, optional
        :return: String representation on the form ``"yyyymmdd"``.
                 Or if separator then on the form ``"yyyy_mm_dd"`` where ``_`` is the separator.
        :rtype: str
        """
        if not sep:
            # None or empty string, then return the internal string value
            return self.__dd_str
        yyyy, mm, dd = self.split()
        return f"{yyyy:04d}{sep}{mm:02d}{sep}{dd:02d}"

    def as_datetime(self: Self) -> datetime:
        """
        This ``DecimalDate`` instance's date as a ``datetime`` object.

        :return: ``datetime`` representation.
        :rtype: datetime
        """
        return self.__dd_dt

    #
    #
    #

    @staticmethod
    def today():
        """
        Todays's date as a ``DecimalDate`` instance.
        """
        return DecimalDate(DecimalDate.__today_as_int())

    @staticmethod
    def yesterday():
        """
        Yesterdays's date as a ``DecimalDate`` instance.
        """
        return DecimalDate.today().previous()

    @staticmethod
    def tomorrow():
        """
        Tomorrow's date as a ``DecimalDate`` instance.
        """
        return DecimalDate.today().next()

    @staticmethod
    def range(
        start: DecimalDate | DecimalDateInitTypes,
        stop: DecimalDate | DecimalDateInitTypes,
        step: int = 1,
        /,
    ) -> DecimalDateRange:
        """
        Return an object that produces a sequence of ``DecimalDate`` objects
        from ``start`` (inclusive) to ``stop`` (exclusive)
        by one day.

        Valid argument types are (except``None``) identical to ``DecimalDate``.

        >>> for dd in DecimalDate.range(2023_05_04, 2023_05_07):
        >>>     print(dd.as_str('.'))
            2023.05.04
            2023.05.05
            2023.05.06

        :param start: Sequence start (inclusive).
        :type start: DecimalDate | int | str | datetime
        :param stop: Sequence stop (exclusive).
        :type stop: DecimalDate | int | str | datetime
        """
        return DecimalDateRange(start, stop, step)


#
# DecimalDateRange
#

# TODO Implement step
# TODO Implement argument order (start/stop)


class DecimalDateRange:

    def __init__(
        self: Self,
        start: DecimalDate | DecimalDateInitTypes,
        stop: DecimalDate | DecimalDateInitTypes,
        step: int = 1,
        /,
    ) -> None:
        """
        Return an object that produces a sequence of ``DecimalDate`` objects
        from ``start`` (inclusive) to ``stop`` (exclusive)
        by ``step`` days
        (currently only value of step=1 is implemented).

        Valid argument types for ``start`` and ``stop``
        are identical to ``DecimalDate`` excepting ``None`` ('today').

        Start is expected to be before Stop or the sequence will be empty.

        >>> for dd in DecimalDateRange(2023_05_04, 2023_05_07):
        >>>     print(dd.as_str('.'))
            2023.05.04
            2023.05.05
            2023.05.06

        :param start: Sequence start (inclusive).
        :type start: DecimalDate | int | str | datetime
        :param stop: Sequence stop (exclusive).
        :type stop: DecimalDate | int | str | datetime
        :param step: Sequence step, defaults to 1 (on value of 1 is implemented)
        :type step: int, optional
        :raises ValueError: If any argument is None
        :raises TypeError: If step argument is not instance of ``int``
        :raises NotImplementedError: If step is other than 1
        """
        if start is None:
            raise ValueError("DecimalDateRange argument start is None.")
        if stop is None:
            raise ValueError("DecimalDateRange argument stop is None.")
        if step is None:
            raise ValueError("DecimalDateRange argument step is None.")
        if not isinstance(step, int):
            raise TypeError("DecimalDateRange step argument is not an `int`.")

        self.__start: DecimalDate = DecimalDate(start)
        self.__stop: DecimalDate = DecimalDate(stop)
        self.__step = step

        if self.__step != 1:
            raise NotImplementedError("argument step != 1 is not implemented.")

        self.__length: int = (
            0
            if self.__start > self.__stop
            else (self.__stop.as_datetime() - self.__start.as_datetime()).days
        )

    def __iter__(self) -> Generator[DecimalDate, Any, None]:
        current: DecimalDate = self.__start
        while current < self.__stop:
            yield current
            current = current.next()

    def __len__(self) -> int:
        """
        The length operator, ``len()``.

        >>> len(DecimalDateRange(DecimalDate(2023_11_11), DecimalDate(2023_11_15)))
            4

        :return: Length of sequence.
        :rtype: int
        """
        return self.__length

    def __contains__(self, dd: DecimalDate) -> bool:
        """
        The containment-check operator, ``in``.

        >>> DecimalDate(2023_11_16) in DecimalDateRange(
        >>>     DecimalDate(2023_11_11), DecimalDate(2023_11_22)
        >>> )
            True
        """
        if not isinstance(dd, DecimalDate):
            raise TypeError(
                "DecimalDateRange contains argument is not a `DecimalDate`."
            )
        return self.__start <= dd < self.__stop

    def __getitem__(self, i: int) -> DecimalDate:
        """
        The index operator, ``[]``.

        >>> DecimalDateRange(2023_05_04, 2023_05_07)[2]
            DecimalDate(20230506)

        Negative argument is not implemented!

        :param i: index into range [0..len[.
        :type i: int
        :raises TypeError: If index is not an ``int``.
        :raises NotImplementedError: If index is negative (less than 0)
        :raises IndexError: If index is outside sequence [0..len[.
        :return: Object at index in sequence.
        :rtype: DecimalDate
        """
        if not isinstance(i, int):
            raise TypeError("DecimalDateRange index argument is not an `int`.")

        if i == 0:
            return self.__start

        if i > 0:
            if not (0 <= i < self.__length):
                raise IndexError(
                    f"DecimalDateRange object index {i} out of range: [0..{self.__length}[."
                )
            return self.__start.next(i)

        if i < 0:
            if not (-self.__length <= i < 0):
                raise IndexError(
                    f"DecimalDateRange object index {i} out of range: [-{self.__length}..0[."
                )
            return self.__stop.previous(-i)

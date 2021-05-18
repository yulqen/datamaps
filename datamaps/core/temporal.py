import calendar
import datetime
import itertools
from typing import List

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


class Month:
    """An object representing a calendar Month."""

    _end_ints = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    def __init__(self, month: int, year: int):
        self.month_int = month
        self.year = year

    @property
    def start_date(self):
        return datetime.date(self.year, self.month_int, 1)

    @property
    def end_date(self):
        if self.month_int == 2 and calendar.isleap(self.year):
            return datetime.date(
                self.year, self.month_int, Month._end_ints[self.month_int] + 1
            )
        else:
            return datetime.date(
                self.year, self.month_int, Month._end_ints[self.month_int]
            )

    @property
    def name(self):
        return MONTHS[self.month_int - 1]

    def __repr__(self):
        return f"Month({self.name})"


class FinancialYear:
    """An object representing a financial year.

    Used by ``bcompiler`` internally when creating :py:class:`bcompiler.api.Master` objects.
    Can be used to calculate start and ends dates and :py:class:`bcompiler.api.Quarter` objects.

    If parameter ``year`` must be in the range 150 - 2100.

    """

    def __init__(self, year):
        if isinstance(year, int) and (year in range(150, 2100)):
            self.year = year
        else:
            raise ValueError("A year must be an integer between 1950 and 2100")
        self._generate_quarters()
        self._q1 = self.quarters[0]
        self._q2 = self.quarters[1]
        self._q3 = self.quarters[2]
        self._q4 = self.quarters[3]

        self.start_date = self.q1.start_date
        self.end_date = self.q4.end_date

    @property
    def q1(self):
        """Quarter 1 as a :py:class:`datetime.date` object"""
        return self._q1

    @property
    def q2(self):
        """Quarter 2 as a :py:class:`datetime.date` object"""
        return self._q2

    @property
    def q3(self):
        """Quarter 3 as a :py:class:`datetime.date` object"""
        return self._q3

    @property
    def q4(self):
        """Quarter 4 as a :py:class:`datetime.date` object"""
        return self._q4

    def __str__(self):
        return f"FY{str(self.year)}/{str(self.year + 1)[2:]}"

    def _generate_quarters(self):
        self.quarters = [Quarter(x, self.year) for x in range(1, 5)]

    def __repr__(self):
        return f"FinancialYear({self.year})"


class Quarter:
    """An object representing a financial quarter.

    This is mainly required for building a :py:class:`core.master.Master`
    object.

    Args:
        quarter (int): e.g.1, 2, 3 or 4
        year (int): e.g. 2013
    """

    _start_months = {
        1: (4, "April"),
        2: (7, "July"),
        3: (10, "October"),
        4: (1, "January"),
    }

    _end_months = {
        1: (6, "June", 30),
        2: (9, "September", 30),
        3: (12, "December", 31),
        4: (3, "March", 31),
    }

    def __init__(self, quarter: int, year: int) -> None:

        if isinstance(quarter, int) and (quarter >= 1 and quarter <= 4):
            self.quarter = quarter
        else:
            raise ValueError("A quarter must be either 1, 2, 3 or 4")

        if isinstance(year, int) and (year in range(1950, 2100)):
            self.year = year
        else:
            raise ValueError(
                "Year must be between 1950 and 2100 - surely that will do?"
            )

        self.start_date = self._start_date(self.quarter, self.year)
        self.end_date = self._end_date(self.quarter, self.year)
        self.months: List[Month] = []
        self._populate_months()

    def _populate_months(self):
        months_ints = []
        start_int = Quarter._start_months[self.quarter][0]
        strt = itertools.count(start_int)
        for x in range(3):
            months_ints.append(next(strt))
        for m in months_ints:
            if self.quarter == 4:
                year = self.year + 1
            else:
                year = self.year
            self.months.append(Month(m, year))

    def __str__(self):
        return f"Q{self.quarter} {str(self.year)[2:]}/{str(self.year + 1)[2:]}"

    def _start_date(self, q, y):
        if q == 4:
            y = y + 1
        return datetime.date(y, Quarter._start_months[q][0], 1)

    def _end_date(self, q, y):
        if q == 4:
            y = y + 1
        return datetime.date(y, Quarter._end_months[q][0], Quarter._end_months[q][2])

    def __repr__(self):
        return f"Quarter({self.quarter}, {self.year})"

    @property
    def fy(self):
        """Return a :py:class:`core.temporal.FinancialYear` object."""
        return FinancialYear(self.year)

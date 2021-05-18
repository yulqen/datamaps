import datetime

import pytest

from ..core.temporal import Month, Quarter


def test_quarter_month_objects_leap_years():
    q = Quarter(4, 2023)
    assert q.months[1].start_date == datetime.date(2024, 2, 1)
    assert q.months[1].end_date == datetime.date(2024, 2, 29)


def test_quarter_objects_have_months():
    q = Quarter(1, 2021)
    q2 = Quarter(4, 2021)
    assert isinstance(q.months[0], Month)
    assert q.months[0].start_date == datetime.date(2021, 4, 1)
    assert q.months[1].start_date == datetime.date(2021, 5, 1)
    assert q.months[2].start_date == datetime.date(2021, 6, 1)
    with pytest.raises(IndexError):
        q.months[4].start_date == datetime.date(2021, 6, 1)
    assert q2.months[0].start_date == datetime.date(2022, 1, 1)
    assert q2.months[1].start_date == datetime.date(2022, 2, 1)
    assert q2.months[2].start_date == datetime.date(2022, 3, 1)
    with pytest.raises(IndexError):
        q2.months[4].start_date == datetime.date(2022, 6, 1)


def test_month():
    m1 = Month(1, 2021)
    assert m1.name == "January"
    assert m1.year == 2021
    m2 = Month(9, 2021)
    assert m2.name == "September"
    assert m2.start_date == datetime.date(2021, 9, 1)
    assert m2.end_date == datetime.date(2021, 9, 30)
    # test leap year
    m3 = Month(2, 2024)
    m4 = Month(2, 2028)
    assert m3.end_date == datetime.date(2024, 2, 29)
    assert m4.end_date == datetime.date(2028, 2, 29)

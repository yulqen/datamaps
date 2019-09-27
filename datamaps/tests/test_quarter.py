import datetime

import pytest

from ..core import Quarter


def test_initialisation():
    q = Quarter(1, 2017)
    assert q.start_date == datetime.date(2017, 4, 1)
    assert q.end_date == datetime.date(2017, 6, 30)
    q = Quarter(2, 2017)
    assert q.start_date == datetime.date(2017, 7, 1)
    assert q.end_date == datetime.date(2017, 9, 30)
    q = Quarter(4, 2017)
    assert q.start_date == datetime.date(2018, 1, 1)
    assert q.end_date == datetime.date(2018, 3, 31)


def test_desc_string():
    assert str(Quarter(1, 2013)) == "Q1 13/14"
    assert str(Quarter(2, 2013)) == "Q2 13/14"
    assert str(Quarter(3, 2013)) == "Q3 13/14"
    assert str(Quarter(4, 2013)) == "Q4 13/14"

    assert str(Quarter(1, 1998)) == "Q1 98/99"
    assert str(Quarter(2, 1998)) == "Q2 98/99"
    assert str(Quarter(3, 1998)) == "Q3 98/99"
    assert str(Quarter(4, 1998)) == "Q4 98/99"

    assert str(Quarter(1, 1999)) == "Q1 99/00"
    assert str(Quarter(2, 1999)) == "Q2 99/00"
    assert str(Quarter(3, 1999)) == "Q3 99/00"
    assert str(Quarter(4, 1999)) == "Q4 99/00"


def test_errors():
    with pytest.raises(ValueError) as excinfo:
        Quarter(5, 2017)
    assert "A quarter must be either 1, 2, 3 or 4" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Quarter(3, 1921)
    assert "Year must be between 1950 and 2100 - surely that will do?" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Quarter("3", 2016)
    assert "A quarter must be either 1, 2, 3 or 4" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Quarter(3, "1921")
    assert "Year must be between 1950 and 2100 - surely that will do?" in str(excinfo.value)

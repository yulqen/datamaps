import datetime

from ..api import project_data_from_master, project_data_from_master_month
from ..core.temporal import Month


def test_get_project_data(master):
    master = project_data_from_master(master, 1, 2019)
    assert (
        master["Chutney Bridge.xlsm"]["Project/Programme Name"] == "Chutney Bridge Ltd"
    )
    assert master.quarter.quarter == 1
    assert master.quarter.end_date == datetime.date(2019, 6, 30)


def test_get_project_data_using_month(master):
    m = project_data_from_master_month(master, 7, 2021)
    m2 = project_data_from_master_month(master, 8, 2021)
    m3 = project_data_from_master_month(master, 9, 2021)
    m4 = project_data_from_master_month(master, 10, 2021)
    assert m["Chutney Bridge.xlsm"]["Project/Programme Name"] == "Chutney Bridge Ltd"
    assert isinstance(m.month, Month)
    assert m.month.name == "July"
    assert m2.month.name == "August"
    assert m3.month.name == "September"
    assert m4.month.name == "October"
    assert m.quarter.quarter == 2
    assert m2.quarter.quarter == 2
    assert m3.quarter.quarter == 2
    assert m4.quarter.quarter == 3
    assert m.quarter.end_date == datetime.date(2021, 9, 30)
    assert m2.quarter.end_date == datetime.date(2021, 9, 30)
    assert m3.quarter.end_date == datetime.date(2021, 9, 30)
    assert m4.quarter.end_date == datetime.date(2021, 12, 31)


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
    m2 = Month(9, 2021)
    assert m2.name == "September"
    assert m2.start_date == datetime.date(2021, 9, 1)
    assert m2.end_date == datetime.date(2021, 9, 30)
    # test leap year
    m3 = Month(2, 2024)
    m4 = Month(2, 2028)
    assert m3.end_date == datetime.date(2024, 2, 29)
    assert m4.end_date == datetime.date(2028, 2, 29)
    

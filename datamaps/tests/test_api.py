import datetime

from ..api import project_data_from_master, project_data_from_master_month
from ..core.temporal import Quarter, Month


def test_get_project_data(master):
    master = project_data_from_master(master, 1, 2019)
    assert (
        master["Chutney Bridge.xlsm"]["Project/Programme Name"] == "Chutney Bridge Ltd"
    )
    assert master.quarter.quarter == 1
    assert master.quarter.end_date == datetime.date(2019, 6, 30)


def test_get_project_data_using_month(master):
    master = project_data_from_master_month(master, 7, 2021)
    assert (
        master["Chutney Bridge.xlsm"]["Project/Programme Name"] == "Chutney Bridge Ltd"
    )
    assert master.month == "July"
    assert master.quarter.quarter == 2
    assert master.quarter.end_date == datetime.date(2021, 9, 30)


def test_quarter_objects_have_months():
    q = Quarter(1, 2021)
    assert q.months[0].start_date == datetime.date(2021, 4, 1)


def test_month():
    m1 = Month(1, 2021)
    assert m1.month == "January"
    m2 = Month(9, 2021)
    assert m2.month == "September"
    assert m2.start_date == datetime.date(2021, 9, 1)
    assert m2.end_date == datetime.date(2021, 9, 30)
    # test leap year
    m3 = Month(2, 2024)
    m4 = Month(2, 2028)
    assert m3.end_date == datetime.date(2024, 2, 29)
    assert m4.end_date == datetime.date(2028, 2, 29)
    

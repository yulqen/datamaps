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
    m5 = project_data_from_master_month(master, 2, 2021)  # this is q4
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

    # year should be different if using this func
    assert m.year == 2021
    assert m2.year == 2021
    assert m3.year == 2021
    assert m5.year == 2021

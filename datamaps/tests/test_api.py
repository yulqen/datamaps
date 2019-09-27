import datetime

from ..api import project_data_from_master


def test_get_project_data(master):
    master = project_data_from_master(master, 1, 2019)
    assert master["Chutney Bridge.xlsm"]["Project/Programme Name"] == "Chutney Bridge Ltd"
    assert master.quarter.quarter == 1
    assert master.quarter.end_date == datetime.date(2019, 6, 30)

import datetime
from ..process.cleansers import Cleanser


def test_cleaning_dot_date():
    ds = "25.1.72"
    ds_double = "25.01.72"
    four_year = "25.01.1972"
    c = Cleanser(ds)
    c_double = Cleanser(ds_double)
    c_four = Cleanser(four_year)
    assert c.clean() == datetime.date(1972, 1, 25)
    assert c_double.clean() == datetime.date(1972, 1, 25)
    assert c_four.clean() == datetime.date(1972, 1, 25)


def test_cleaning_slash_date():
    ds = "25/1/72"
    ds_double = "25/01/72"
    four_year = "25/01/1972"
    c = Cleanser(ds)
    c_double = Cleanser(ds_double)
    c_four = Cleanser(four_year)
    assert c.clean() == datetime.date(1972, 1, 25)
    assert c_double.clean() == datetime.date(1972, 1, 25)
    assert c_four.clean() == datetime.date(1972, 1, 25)


def test_em_dash_key():
    contains_em_dash = 'Pre 14-15 BL – Income both Revenue and Capital'
    c = Cleanser(contains_em_dash)
    assert c.clean() == 'Pre 14-15 BL - Income both Revenue and Capital'


def test_double_trailing_space():
    contains_double_trailing = 'Pre 14-15 BL - Incoming both Revenue and Capital  '
    contains_single_trailing = 'Pre 14-15 BL - Incoming both Revenue and Capital '
    c = Cleanser(contains_double_trailing)
    assert c.clean() == 'Pre 14-15 BL - Incoming both Revenue and Capital'
    c = Cleanser(contains_single_trailing)
    assert c.clean() == 'Pre 14-15 BL - Incoming both Revenue and Capital'

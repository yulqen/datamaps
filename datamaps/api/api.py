from ..core import Quarter
from ..plugins.dft.master import Master


def project_data_from_master_api(master_file: str, quarter: int, year: int):
    """Create a Master object directly without the need to explicitly pass
    a Quarter object.

    Args:
        master_file (str): the path to a master file
        quarter (int): an integer representing the financial quarter
        year (int): an integer representing the year
    """
    m = Master(Quarter(quarter, year), master_file)
    return m


def project_data_from_master_month_api(master_file: str, month: int, year: int) -> Master:
    """Create a Master object directly without the need to explicitly pass
    a Month object.

    Args:
        master_file (str): the path to a master file
        month (int): an integer representing the month
        year (int): an integer representing the year
    """
    # we need to work out what Quarter we are dealing with from the month
    if month in [1, 2, 3]:
        quarter = 4
    elif month in [4, 5, 6]:
        quarter = 1
    elif month in [7, 8, 9]:
        quarter = 2
    elif month in [10, 11, 12]:
        quarter = 3
    else:
        pass
        # TODO: raise exception here

    # from that, we can work out what quarter year we are dealing with
    if quarter == 4:
        year = year - 1
    m = Master(Quarter(quarter, year), master_file, month)
    return m

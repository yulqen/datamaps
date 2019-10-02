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

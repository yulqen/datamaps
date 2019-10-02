import re
import datetime
import logging
import unicodedata
from pathlib import Path
from typing import List, Tuple, Iterable, Optional, Any

from datamaps.plugins.dft.portfolio import project_data_from_master
from datamaps.process.cleansers import DATE_REGEX_4
from datamaps.core.temporal import Quarter

from openpyxl import load_workbook

logger = logging.getLogger('bcompiler.utils')


class ProjectData:
    """
    ProjectData class
    """
    def __init__(self, d: dict) -> None:
        """
        :py:func:`OrderedDict` is easiest to get from project_data_from_master[x]
        """
        self._data = d

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def key_filter(self, key: str) -> List[Tuple]:
        """
        Return a list of (k, v) tuples if k in master key.
        """
        data = [item for item in self._data.items() if key in item[0]]
        if not data:
            raise KeyError("Sorry, there is no matching data")
        return (data)

    def pull_keys(self, input_iter: Iterable, flat=False) -> List[Tuple[Any, ...]]:
        """
        Returns a list of (key, value) tuples from ProjectData if key matches a
        key. The order of tuples is based on the order of keys passed in the iterable.
        """
        if flat is True:
            # search and replace troublesome EN DASH character
            xs = [item for item in self._data.items()
                  for i in input_iter if item[0].strip().replace(unicodedata.lookup('EN DASH'), unicodedata.lookup('HYPHEN-MINUS')) == i]
            xs = [_convert_str_date_to_object(x) for x in xs]
            ts = sorted(xs, key=lambda x: input_iter.index(x[0].strip().replace(unicodedata.lookup('EN DASH'), unicodedata.lookup('HYPHEN-MINUS'))))
            ts = [item[1] for item in ts]
            return ts
        else:
            xs = [item for item in self._data.items()
                  for i in input_iter if item[0].replace(unicodedata.lookup('EN DASH'), unicodedata.lookup('HYPHEN-MINUS')) == i]
            xs = [item for item in self._data.items()
                  for i in input_iter if item[0] == i]
            xs = [_convert_str_date_to_object(x) for x in xs]
            ts = sorted(xs, key=lambda x: input_iter.index(x[0].replace(unicodedata.lookup('EN DASH'), unicodedata.lookup('HYPHEN-MINUS'))))
            return ts

    def __repr__(self):
        return f"ProjectData() - with data: {id(self._data)}"


def _convert_str_date_to_object(d_str: tuple) -> Tuple[str, Optional[datetime.date]]:
    try:
        if re.match(DATE_REGEX_4, d_str[1]):
            try:
                ds = d_str[1].split('-')
                return (d_str[0], datetime.date(int(ds[0]), int(ds[1]), int(ds[2])))
            except TypeError:
                return d_str
        else:
            return d_str
    except TypeError:
        return d_str


class Master:
    """A Master object, representing the main central data item in ``datamaps``.

    Args:
        quarter (:py:class:`bcompiler.api.Quarter`): creating using ``Quarter(1, 2017)`` for example.
        path (str): path to the master xlsx file

    A master object is a composition between a :py:class:`datamaps.api.Quarter` object and an
    actual master xlsx file on disk.

    You create one, either by creating the Quarter object first, and using that as the first
    parameter of the ``Master`` constructor, e.g.::

        from bcompiler.api import Quarter
        from bcompiler.api import Master

        q1 = Quarter(1, 2016)
        m1 = Master(q1, '/tmp/master_1_2016.xlsx')

    or by doing both in one::

        m1 = Master(Quarter(1, 2016), '/tmp/master_1_2016.xlsx')

    Once you have a ``Master`` object, you can access project data from it, like this::

        project_data = m1['Project Title']


    The following *attributes* are available on `m1` once created as such, e.g.::

        data = m1.data
        quarter = m1.quarter
        filename = m1.filename
        ..etc
    """
    def __init__(self, quarter: Quarter, path: str) -> None:
        self._quarter = quarter
        self.path = path
        self._data = project_data_from_master(self.path)
        self._project_titles = [item for item in self.data.keys()]
        self.year = self._quarter.year

    def __getitem__(self, project_name):
        return ProjectData(self._data[project_name])

    @property
    def data(self):
        """Return all the data contained in the master in a large, nested dictionary.

        The resulting data structure contains a dictionary of :py:class:`colletions.OrderedDict` items whose
        key is the name of a project::

            "Project Name": OrderedDict("key": "value"
                                        ...)

        This object can then be further interrogated, for example to obtain all key/values
        from a partictular project, by doing::

            d = Master.data
            project_data = d['PROJECT_NAME']

        """
        return self._data

    @property
    def quarter(self):
        """Returns the ``Quarter`` object associated with the ``Master``.

        Example::

            q1 = m.quarter

        ``q1`` can then be further interrogated as documented in :py:class:`core.temporal.Quarter`.

        """

        return self._quarter

    @property
    def filename(self):
        """The filename of the master xlsx file, e.g. ``master_1_2017.xlsx``.
        """
        p = Path(self.path)
        return p.name

    @property
    def projects(self):
        """A list of project titles derived from the master xlsx.
        """
        return self._project_titles

    def duplicate_keys(self, to_log=None):
        """Checks for duplicate keys in a master xlsx file.

        Args:
            to_log (bool): Optional True or False, depending on whether you want to see duplicates reported in a ``WARNING`` log message. This is used mainly for internal purposes within ``bcompiler``.

        Returns:
            duplicates (set): a set of duplicated keys
        """
        wb = load_workbook(self.path)
        ws = wb.active
        col_a = next(ws.iter_cols())
        col_a = [item.value for item in col_a]
        seen: set = set()
        uniq = []
        dups: set = set()
        for x in col_a:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
            else:
                dups.add(x)
        if to_log and len(dups) > 0:
            for x in dups:
                logger.warning(f"{self.path} contains duplicate key: \"{x}\". Masters cannot contain duplicate keys. Rename them.")
            return True
        elif to_log and len(dups) == 0:
            logger.info(f"No duplicate keys in {self.path}")
            return False
        elif len(dups) > 0:
            return dups
        else:
            return False

    def __repr__(self):
        return f"Master({self.path}, {self.quarter.quarter}, {self.quarter.year})"

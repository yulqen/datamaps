import os

import pytest
from pathlib import Path


@pytest.fixture
def master() -> Path:
    return Path.cwd() / "tests" / "resources" / "master.xlsx"

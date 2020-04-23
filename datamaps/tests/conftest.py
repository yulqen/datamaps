import os
import shutil
from pathlib import Path

import pytest

from engine.config import Config


@pytest.fixture
def master() -> Path:
    return Path.cwd() / "datamaps" / "tests" / "resources" / "master.xlsx"


@pytest.fixture
def mock_config(monkeypatch):
    monkeypatch.setattr(Config, "PLATFORM_DOCS_DIR", Path("/tmp/Documents/datamaps"))
    monkeypatch.setattr(
        Config, "DATAMAPS_LIBRARY_DATA_DIR", Path("/tmp/.local/share/datamaps-data")
    )
    monkeypatch.setattr(
        Config, "DATAMAPS_LIBRARY_CONFIG_DIR", Path("/tmp/.config/datamaps-data")
    )
    monkeypatch.setattr(
        Config,
        "DATAMAPS_LIBRARY_CONFIG_FILE",
        Path("/tmp/.config/datamaps-data/config.ini"),
    )
    yield Config
    try:
        shutil.rmtree(Config.DATAMAPS_LIBRARY_DATA_DIR)
        shutil.rmtree(Config.DATAMAPS_LIBRARY_CONFIG_DIR)
        shutil.rmtree(Config.PLATFORM_DOCS_DIR)
    except FileNotFoundError:
        pass


@pytest.fixture
def resource_dir():
    return Path.cwd() / "datamaps" / "tests" / "resources"

import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from datamaps.main import _import


def _copy_resources_to_input(config, directory):
    """Helper func to move files from resources into temp Docs directories."""
    for fl in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fl)):
            shutil.copy(
                Path.cwd() / "datamaps" / "tests" / "resources" / fl,
                (Path(config.PLATFORM_DOCS_DIR) / "input"),
            )


def test_error_report(mock_config, resource_dir):
    runner = CliRunner()
    mock_config.initialise()
    _copy_resources_to_input(mock_config, resource_dir)
    result = runner.invoke(_import, ["templates", "-m"])
    output = result.output.split("\n")
    assert "Import errors:" in output
    assert "\tNo sheet named Introduction in test_template.xlsm" in output



@pytest.mark.skip("Complete after error report code complete")
def test_no_expected_sheet_in_batch_import_to_master(mock_config, resource_dir):
    """If there is a batch of spreadsheet files present
    in the input directory, and at least one file is present
    that does not have a sheet as named by the datamap, we want
    the good files to process and the error file to be flagged,
    but the process to continue where it can.

    KeyError thrown by engine.parsing.query_key() needs to be handled.
    """
    runner = CliRunner()
    mock_config.initialise()
    _copy_resources_to_input(mock_config, resource_dir)
    result = runner.invoke(_import, ["templates", "-m"])
    output = result.output
    assert "Expected Sheet Missing: sheet Introduction in test_template.xlsm is expected from" \
           " datamap.csv. Not processing that file until fixed." in result.output
    # assert "Imported data from input/dft1_temp.xlsm to output/master.xlsx." in result.output
    # assert "Finished." in result.output

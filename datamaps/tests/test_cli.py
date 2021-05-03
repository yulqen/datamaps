import logging
import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner
from sys import platform

from datamaps.main import _import, export


def _copy_resources_to_input(config, directory):
    """Helper func to move files from resources into temp Docs directories."""
    for fl in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fl)):
            shutil.copy(
                Path.cwd() / "datamaps" / "tests" / "resources" / fl,
                (Path(config.PLATFORM_DOCS_DIR) / "input"),
            )


def test_can_run_validation_only_template_import(mock_config, resource_dir, caplog):
    runner = CliRunner()
    mock_config.initialise()
    caplog.set_level(logging.INFO)
    _copy_resources_to_input(mock_config, resource_dir)
    result = runner.invoke(_import, ["templates", "-v"])
    assert result.exit_code == 0
    assert "No output file produced as not requested." in [x[2] for x in caplog.record_tuples]


def test_import_from_user_defined_source_dir(
    mock_config, resource_dir, caplog, temp_input_dir
):
    runner = CliRunner()
    mock_config.initialise()
    caplog.set_level(logging.INFO)
    for fl in os.listdir(resource_dir):
        shutil.copy(
            Path.cwd() / "datamaps" / "tests" / "resources" / fl, temp_input_dir
        )
    result = runner.invoke(_import, ["templates", "-m", "--inputdir", temp_input_dir])
    assert result.exit_code == 0
    output = [x[2] for x in caplog.record_tuples]
    found = False
    for o in output:
        if f"Reading datamap {temp_input_dir}/" in o:
            found = True
            break
    if found:
        assert True
    else:
        assert False, "Cannot find correct string"


@pytest.mark.parametrize(
    "rowlimit,expected,exit_code",
    [
        (200, "Row limit is set to 200.", 0),
        (50, "Row limit is set to 50.", 0),
        (
            20,
            "Row limit is set to 20 (default is 500). This may be unintentionally low. Check datamaps import templates --help",
            0,
        ),
        (0, "Row limit cannot be 0. Quitting.", 1),
    ],
)
def test_import_with_changed_row_limit(
    mock_config, resource_dir, caplog, rowlimit, expected, exit_code
):
    runner = CliRunner()
    mock_config.initialise()
    caplog.set_level(logging.INFO)
    _copy_resources_to_input(mock_config, resource_dir)
    result = runner.invoke(_import, ["templates", "-m", "--rowlimit", rowlimit])
    assert result.exit_code == exit_code
    assert expected in [x[2] for x in caplog.record_tuples]


def test_import_with_alternative_datamap(mock_config, resource_dir, caplog):
    """
    This should fail with exit code one as we are not providing a valid datamap file.
    :param mock_config:
    :param resource_dir:
    :return:
    """
    runner = CliRunner()
    mock_config.initialise()
    caplog.set_level(logging.INFO)
    _copy_resources_to_input(mock_config, resource_dir)
    _alt_datamap_file = (
        mock_config.PLATFORM_DOCS_DIR / "input" / "datamap_alternate.csv"
    )
    result = runner.invoke(_import, ["templates", "-m", "-d", _alt_datamap_file])
    assert result.exit_code == 0
    if platform == "win32":
        assert (
            "Reading datamap \\tmp\\Documents\\datamaps\\input\\datamap_alternate.csv"
            in [x[2] for x in caplog.record_tuples]
        )
    else:
        assert (
            "Reading datamap /tmp/Documents/datamaps/input/datamap_alternate.csv"
            in [x[2] for x in caplog.record_tuples]
        )


def test_import_with_wrong_datamap(mock_config, resource_dir, caplog):
    """
    This should fail with exit code one as we are not providing a valid datamap file.
    :param mock_config:
    :param resource_dir:
    :return:
    """
    runner = CliRunner()
    mock_config.initialise()
    _copy_resources_to_input(mock_config, resource_dir)
    result = runner.invoke(
        _import, ["templates", "-m", "-d", "C:/tmp/non-existent-file.txt"]
    )
    assert result.exit_code == 1
    assert "Given datamap file is not in CSV format." in [
        x[2] for x in caplog.record_tuples
    ]


def test_export_with_alternative_datamap(mock_config, resource_dir, caplog):
    runner = CliRunner()
    mock_config.initialise()
    _copy_resources_to_input(mock_config, resource_dir)
    _master_file = os.path.join(mock_config.PLATFORM_DOCS_DIR, "input", "master.xlsx")
    result = runner.invoke(
        export, ["master", _master_file, "-d", "C:/tmp/Desktop/test.txt"]
    )
    assert result.exit_code == 1
    assert "Given datamap file is not in CSV format." in [
        x[2] for x in caplog.record_tuples
    ]


def test_export_with_alternative_datamap_not_csv(mock_config, resource_dir, caplog):
    runner = CliRunner()
    mock_config.initialise()
    _copy_resources_to_input(mock_config, resource_dir)
    _master_file = os.path.join(mock_config.PLATFORM_DOCS_DIR, "input", "master.xlsx")
    _alt_datamap_file = os.path.join(
        mock_config.PLATFORM_DOCS_DIR, "input", "datamap_alternate.csv"
    )
    _ = runner.invoke(export, ["master", _master_file, "-d", _alt_datamap_file])
    if platform == "win32":
        assert (
            "Reading datamap \\tmp\\Documents\\datamaps\\input\\datamap_alternate.csv"
            in [x[2] for x in caplog.record_tuples]
        )
    else:
        assert (
            "Reading datamap /tmp/Documents/datamaps/input/datamap_alternate.csv"
            in [x[2] for x in caplog.record_tuples]
        )


@pytest.mark.skip("Not currently passing - need to investigate")
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
    assert (
        "Expected Sheet Missing: sheet Introduction in test_template.xlsm is expected from"
        " datamap.csv. Not processing that file until fixed." in result.output
    )
    # assert "Imported data from input/dft1_temp.xlsm to output/master.xlsx." in result.output
    # assert "Finished." in result.output

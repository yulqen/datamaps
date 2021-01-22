"""
Copyright (c) 2019 Matthew Lemon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy,  modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the  Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE. """
import click
import logging
import sys
from click import version_option
from functools import partial
from pathlib import Path

from datamaps import __version__
from engine.adapters import cli as engine_cli
from engine.config import Config as engine_config
from engine.exceptions import (
    DatamapFileEncodingError,
    MalFormedCSVHeaderException,
    MissingCellKeyError,
    MissingLineError,
    MissingSheetFieldError,
    NoApplicableSheetsInTemplateFiles,
    RemoveFileWithNoSheetRequiredByDatamap,
    DatamapNotCSVException,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger(__name__)


be_logger = logging.getLogger("engine.use_cases.parsing")

# we want to pass echo func down to bcompiler-engine
output_funcs = dict(
    click_echo_green=partial(click.secho, nl=False, fg="green"),
    click_echo_yellow=partial(click.secho, nl=False, fg="yellow"),
    click_echo_red=partial(click.secho, nl=False, fg="red"),
    click_echo_white=partial(click.secho, nl=False, fg="white"),
)


class Config:
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@version_option(__version__)
@click.group()
@click.option("--verbose", is_flag=True, help="This currently has no effect.")
@pass_config
def cli(config, verbose):
    """
    datamaps is a tool for moving data to and from spreadsheets. Documentation available
    at https://www.datamaps.twentyfoursoftware.com.

    Please note: datamaps is beta software! Development is ongoing and the program
    is undergoing continuous change.

    Use --help flag after all commands to get help. For example:

        datamaps import templates --help (for
        etc...
    """
    click.secho(
        f"Welcome to datamaps {__version__} © 2021 Twenty Four Software", fg="yellow"
    )
    config.verbose = verbose
    engine_config.initialise()


@cli.group("import")
def _import():
    """
    Import something (a batch of populated templates, a datamap, etc). This command is also used
    to carry out validation tasks on populated templates.
    """


@cli.group("export")
def export():
    """
    Export data from one format to another. Current functionality allows for data
    to be exported from a Master spreadsheet to one or many blank Templates.
    """


@cli.group("report")
def report():
    """Create a report of some description. Currently only Excel cell validation
    is implemented."""


@cli.group("config")
def _config():
    """Manage datamaps configuration."""


@_config.command(
    short_help="Removes the configuration file (config.ini). It will be restored "
    "automatically with default settings when required. You will lose any custom "
    "configuration, but this is a good troubleshooting step."
)
def restart():
    """Removes the configuration file (config.ini)."""
    engine_cli.delete_config(engine_config)


@_config.command(
    short_help="Shows location of the config.ini file. This differs depending "
    "upon your operating system."
)
def show_file():
    """
    Shows location of the config file.
    """
    engine_cli.show_config_file(engine_config)


@_import.command()
@click.option(
    "--to-master",
    "-m",
    is_flag=True,
    default=False,
    help="Create master.xlsx based on populated templates and datamap.csv in input directory.",
)
@click.option(
    "--datamap", "-d", help="Path to datamap file", type=Path, metavar="CSV_FILE_PATH"
)
@click.option(
    "--rowlimit",
    type=int,
    help="Set row limit to prevent spurious Excel files with hidden rows being processed."
    "Default is 500.",
)
@click.option(
    "--inputdir",
    help="Path to input directory",
    type=Path,
    metavar="INPUT_DIRECTORY_PATH",
)
@click.option(
    "--validationonly",
    "-v",
    is_flag=True,
    default=False,
    help=(
        "Create validation report only - do not output data anywhere. Cannot be used with -m/--to-master"
        " option"
    ),
)
def templates(to_master, datamap, rowlimit, inputdir, validationonly):
    """Import data to a from populated templates.

    Import data from the template files stored in the input directory to create
    a master.xlsx file in the output directory using the datamap form the input directory.

    The default datamap file (datamap.csv) will be used unless you pass the -d flag with a
    path to a different file.

    By default there is a row limit of 500 when importing from a template, which means only cells in
    rows 1-500 will be imported, no matter what your datamap says. This prevents datamaps running out of
    memory when handling with a spreadsheet containing errenous/invisible rows, which can occur without the
    user being aware, particularly on templates that have been subjected to length edits, years of copy
    and pasting, styling changes and other chronic abuse.

    This value can be changed by passing the value using the --rowlimit option  There may be an
    imperceptible performance improvement gained by reducing this value to as low as possible, but
    its primary purpose is to prevent fatal memory leaks when processing a problematic file.

    Validation is carried out on the data when importing to a master according the 'type' column
    in the datamap. Validation output is currently exported as a CSV file which is saved in the
    output directory after import. If there is no 'type' column in the datamap, no validation
    report is produced. Any or all lines in the datamap can be given a type (currently, only TEXT,
    NUMBER and DATE are implemented) - the validation report will flag lines that do not have a
    type as UNTYPED. Cells in the template which are empty but are required by the datamap will be
    flagged as FAIL and NO VALUE RETURNED - the idea being that the inclusion of a datamap line
    suggests a value is expected.

    The validation report, being a simple CSV file, can and should be opened in a spreadsheet program
    and can be filtered and sorted to the user's needs.

    If you only require validation, use the -v flag instead of -m - no master will be produced, only
    a validation report. This may provide another almost inperceptible performance benefit as producing
    the master file is quite expensive.
    """
    if datamap:
        if not datamap.is_absolute():
            datamap = Path.cwd() / datamap
    if inputdir:
        if not inputdir.is_absolute():
            inputdir = Path.cwd() / inputdir
    if rowlimit == 0:
        logging.critical("Row limit cannot be 0. Quitting.")
        sys.exit(1)
    if to_master and validationonly:
        logging.critical(
            "Cannot select both -m/--to-master and -v/--validationonly flags."
        )
        sys.exit(1)
    if validationonly:
        try:
            engine_cli.import_and_create_master(
                echo_funcs=output_funcs,
                datamap=datamap,
                rowlimit=rowlimit,
                inputdir=inputdir,
                validationonly=validationonly,
            )
        except MalFormedCSVHeaderException as e:
            click.echo(
                click.style(
                    "Incorrect headers in datamap. {}.".format(e.args[0]),
                    bold=True,
                    reverse=True,
                    fg="cyan",
                )
            )
        except RemoveFileWithNoSheetRequiredByDatamap:
            logging.info("Import complete.")
        except RuntimeError:
            logger.critical(
                "Not completing import process due to runtime error. Please check output for CRITICAL messages to diagnose."
            )
        except NoApplicableSheetsInTemplateFiles:
            logger.critical("Not completing import process.")
        except FileNotFoundError as e:
            logger.critical(e)
            sys.exit(1)
        except MissingSheetFieldError as e:
            logger.critical(e)
            sys.exit(1)
        except MissingCellKeyError as e:
            logger.critical(e)
            sys.exit(1)
        except DatamapFileEncodingError as e:
            logger.critical(e)
            sys.exit(1)
        except DatamapNotCSVException as e:
            logger.critical(e)
            sys.exit(1)

    if to_master:
        try:
            engine_cli.import_and_create_master(
                echo_funcs=output_funcs,
                datamap=datamap,
                rowlimit=rowlimit,
                inputdir=inputdir,
            )
        except MalFormedCSVHeaderException as e:
            click.echo(
                click.style(
                    "Incorrect headers in datamap. {}.".format(e.args[0]),
                    bold=True,
                    reverse=True,
                    fg="cyan",
                )
            )
        except RemoveFileWithNoSheetRequiredByDatamap:
            logging.info("Import complete.")
        except RuntimeError:
            logger.critical(
                "Not completing import process due to runtime error. Please check output for CRITICAL messages to diagnose."
            )
        except NoApplicableSheetsInTemplateFiles:
            logger.critical("Not completing import process.")
        except FileNotFoundError as e:
            logger.critical(e)
            sys.exit(1)
        except MissingSheetFieldError as e:
            logger.critical(e)
            sys.exit(1)
        except MissingCellKeyError as e:
            logger.critical(e)
            sys.exit(1)
        except DatamapFileEncodingError as e:
            logger.critical(e)
            sys.exit(1)
        except DatamapNotCSVException as e:
            logger.critical(e)
            sys.exit(1)


@export.command()
# @click.argument("datamap")
# @click.argument("blank")
@click.argument("master", metavar="MASTER_FILE_PATH")
@click.option(
    "--datamap", "-d", help="Path to datamap (CSV) file.", metavar="CSV_FILE_PATH"
)
def master(master, datamap):
    """Export data from a Master file.

    Export data from a master file (at MASTER_FILE_PATH). A new populated template
    will be created for each project in the master.

    The default datamap file will be used unless you pass the -d flag with a path to a different file.
    """
    input_dir = engine_config.PLATFORM_DOCS_DIR / "input"

    blank_fn = engine_config.config_parser["DEFAULT"]["blank file name"]
    if datamap:
        datamap_fn = datamap
    else:
        datamap_fn = engine_config.config_parser["DEFAULT"]["datamap file name"]

    blank = input_dir / blank_fn
    datamap = input_dir / datamap_fn

    #   click.secho(f"EXPORTING master {master} to templates based on {blank}...")
    be_logger.info(f"Exporting master {master} to templates based on {blank}.")

    try:
        engine_cli.write_master_to_templates(blank, datamap, master)
    except (FileNotFoundError, RuntimeError) as e:
        logger.critical(str(e))
        sys.exit(1)
    except MissingSheetFieldError as e:
        logger.critical(e)
        sys.exit(1)
    except MissingCellKeyError as e:
        logger.critical(e)
        sys.exit(1)
    except DatamapFileEncodingError as e:
        logger.critical(e)
        sys.exit(1)
    except MissingLineError as e:
        logger.critical(e)
        sys.exit(1)
    except DatamapNotCSVException as e:
        logger.critical(e)
        sys.exit(1)
    be_logger.info("Export complete.")


@report.command()
@click.argument("target_file")
def excel_validations(target_file):
    """Shows any Excel cell-validation code in the target file.
    Requires the path to the target spreadsheet file. This is different
    from datamaps validation using the 'type' column in the datamap file."""
    logger.info(f"Getting Excel data validations from: {target_file}")
    try:
        report = engine_cli.report_data_validations_in_file(target_file)
    except FileNotFoundError as e:
        logger.critical(e)
        sys.exit(1)
    for r in report:
        logger.info(r)


@cli.command()
def check():
    """
    Checks for a correctly-named blank template in the input directory and
    a datamap file in the input directory. Checks for correct headers in datamap.
    """
    try:
        engine_cli.check_aux_files(engine_config)
    except MalFormedCSVHeaderException as e:
        logger.critical(e)
        sys.exit(1)
    except MissingSheetFieldError as e:
        logger.critical(e)
        sys.exit(1)
    except MissingCellKeyError as e:
        logger.critical(e)
        sys.exit(1)
    except DatamapFileEncodingError as e:
        logger.critical(e)
        sys.exit(1)
    except MissingLineError as e:
        logger.critical(e)
        sys.exit(1)

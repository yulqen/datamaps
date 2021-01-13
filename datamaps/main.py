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
    """
    click.secho(
        f"Welcome to datamaps {__version__} © 2021 Twenty Four Software", fg="yellow"
    )
    config.verbose = verbose
    engine_config.initialise()


@cli.group("import")
def _import():
    """
    Import something (a batch of populated templates, a datamap, etc).
    """


@cli.group("export")
def export():
    """
    Export data from one format to another. Current functionality allows for data
    to be exported from a Master spreadsheet to one or many blank Templates.
    """


@cli.group("report")
def report():
    """Create a report"""


@cli.group("config")
def _config():
    """Manage datamaps configuration."""


@_config.command(
    help="Removes the configuration file (config.ini). It will be restored "
    "automatically with default settings when required. You will lose any custom "
    "configuration, but this is a good troubleshooting step."
    )
def restart():
    """Removes the configuration file (config.ini)."""
    engine_cli.delete_config(engine_config)


@_config.command()
def show_file():
    """
    Shows location of the config.ini file.
    """
    engine_cli.show_config_file(engine_config)


@_import.command()
@click.option(
    "--to-master",
    "-m",
    is_flag=True,
    default=False,
    help="Create master.xlsx based on populated templates in output directory. "
    "Future versions will allow importing to other formats such as databases, "
    "hence the reason for this being the only option currently.",
)
@click.option("--datamap", "-d", help="Path to datamap file", metavar="CSV_FILE_PATH")
def templates(to_master, datamap):
    """Import data to a master file from a collection of populated templates.

    BASICS

    Import data from the template files stored in the input directory to create
    a master.xlsx file in the output directory.

    The default datamap file will be used unless you pass the -d flag with a path to a different file.

    TEMPLATE ROW LIMIT

    By default there is a row limit of 500 when importing from a template, which means only cells in
    rows 1-500 will be imported, no matter what your datamap says. This prevents datamaps running out of
    memory when faced with a spreadsheet containing errenous/invisible rows, which can occur without the
    user being aware, particularly on templates that have been subjected to length edits, years of copy
    and pasting, styling changes and other similar chronic abuse.

    This value can be changed in the configuration file (change the value for
    TEMPLATE_ROW_LIMIT). There may be an imperceptible performance improvement gained by reducing this
    value to as low as possible, but its primary purpose is to prevent fatal memory leaks when
    processing a problematic file.
    """
    if to_master:
        try:
            engine_cli.import_and_create_master(
                echo_funcs=output_funcs, datamap=datamap
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

    else:
        click.secho("Not implemented yet. Try --to-master/-m flag")


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
def data_validations(target_file):
    """Requires the path to the target spreadsheet file."""
    logger.info(f"Getting data validations from: {target_file}")
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

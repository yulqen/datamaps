![Tests](https://github.com/hammerheadlemon/datamaps/workflows/Tests/badge.svg)

## Introduction

`datamaps` is a command line tool, written in Python, which facilitates the collection of data using Excel as the 'form'. It accepts that Excel files are freely distributable, easy to understand and already well integrated in the non-technical office environment.

The tool uses a concept a *datamap*, which is simple, user-created CSV file which maps cell references within Excel 'templates'. The datamap concept makes it easy to design pretty Excel spreadsheets with blank cells (the 'template') intended for the user to complete - the cell references in the datamap inform the `datamaps` program where it should expect to find user-entered data. At this point, the output is another *master* spreadsheet which contains all the data from each completed template compiled into a single table. This is then used by other tools for further analysis.

The documentation found at [Datamaps - Twenty Four Software](https://datamaps.twentyfoursoftware.com) gives a more detailed explanation.

## Installation

`pip install datamaps`

## Bugs and issues

Please report bugs as [Github issues](https://github.com/yulqen/datamaps/issues).

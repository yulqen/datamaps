## v1.1.0

The first major feature release to `datamaps`.

### Simple data validation

The user is now able to stipulate the type of data expected to be
returned per cell during the `import templates` phase. Allowable types at this
stage are simply `TEXT`, `NUMBER` and `DATE`.

The types are declared in the datamap in a new column headed 'type'. Upon
import, datamaps will validate the value of the data in that particular cell
according to the required type and output the results in a CSV file in the
default output directory.

Type-validation is entirely optional: if no type column is included in the
datamap file, no validation is carried out. If a type column *is* included and
only a handful of datamap entries have types declared, a validation report is
produced, but only those cells are assessed - the rest are declared as UNTYPED.

Empty cells in the template that are expected by the datamap are flagged in the
validation report. The logic here is that if the cell is in the datamap in the
first place, we should expect a value returned.

If the user only requires validation for a single template or batch of
templates - and no master.xlsx to be produced - this can now be set using the
`-v` flag:

`datamaps import templates -v`. Please not that the `-m` and `-v` flags are
mutually exclusive.

The validation report is in CSV format to allow for rudimentary sorting and
filtering in a spreadsheet program.

This is the first iteration of validation in datamaps - more sophisticated
validation is planned for future releases, with rules-based types such as 
greater-than and less-than for numbers, date ranges and text minimum and maximum 
lengths in the frame.

### Change to setting the row limit

The row limiting feature released in `v1.0.7` must now be set using
a `--rowlimit` option to `datamaps import templates` and there is no longer any
need to change the `config.ini` file.  The default row limit remains 500.

### Configurable input directory

The input directory can now be overridden using the `--inputdir` option to
`datamaps import templates`. In future releases, it may be possible to override
the output directory also.

### Help documentation

The `--help` documentation has been improved across the board.

### Bugfixes

Some minor bugfixes introduced in recent releases.


## v1.0.9

* Bug fixes.

## v1.0.8

* Now handles `datamaps config` commands. The `config.ini` can be revealed to
  the user and deleted.

## v1.0.7

* Added a row limit in `bcompiler-engine` when importing data to prevent memory leak ([Issue #30](https://github.com/yulqen/bcompiler-engine/issues/30))

## v1.0.6

* Tracking changes in `bcompiler-engine v.1.0.6`

## v1.0.0b13

* New **check** command

### Example:

```
datamaps check
```

Checks that the necessary auxiliary files are in place so that basic
functionality can take place.

Checks for:

* Documents/input/blank_template.xlsx
* Documents/input/datamap.csv

Also carries out basic sanity checks on the datamap file, to ensure requisite
headers, number of fields, etc.

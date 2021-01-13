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

# django-spreadsheet

Validate your XLSX spreadsheet file before importing it. Export your data to a formatted XLSX spreadsheet with data validation set up.

# Requirements

- Python 3.8+
- Django 2.0+

# Installation

- run `pip install django_spreadsheets`
- add `django_spreadsheets.apps.SpreadsheetAppConfig` to your `INSTALLED_APPS`
- add `path("admin/spreadsheets/", include("django_spreadsheets.urls", namespace="spreadsheets"))` to your root `urls.py`
- run `python manage.py migrate django_spreadsheets`

# Usage

Start to create a file `spreadsheets.py` in your app. Inside this file, describe your spreadsheets configurations such as the following example:

```py
from django_spreadsheets.base_config import SpreadsheetConfig, SheetConfig
from django_spreadsheets.registry import register
from libs.bananas.models import Banana


class BananaSheetConfig(SheetConfig):
    """Describes each columns of this sheet."""

    ID = {
        "name": "Identifier",
        "required": True,
    }
    COLOR = {
        "name": "Color",
        "validation": {
            "type": "list",
            "formula1": ["yellow", "green", "brown"],
        },
        "required": True,
    }
    SIZE = {
      "name": "Size",
      "validation": {
          "type": "whole",
          "operator": "greaterThan",
          "formula1": 0,
          "error": "Please enter a positive number",
      }
    }

    def get_data_to_export(self):
        return Banana.objects.values_list("id", "color", "size")


@register
class BananaSpreadsheetConfig(SpreadsheetConfig):
    sheets_config = {
        "Banana": BananaSheetConfig()
        # the key will be used as the name of the sheet, the value is a class describing the sheet's configuration.
    }

    class Meta:
        verbose_name = "Bananas"

    def update_database(self, sheets):
        for sheet_name, rows in sheets.items():
            for row in rows:
                Banana.objects.get_or_create(
                  id=row["ID"],
                  color=row["COLOR"],
                  size=row["SIZE"],
                )
```

Then, you can go to `//localhost:8000/admin/spreadsheets/export/` to export a XSLX file and `//localhost:8000/admin/spreadsheets/import/` to import into your database.

# `SpreadsheetConfig` class

Inherit this class to describe your spreadsheets' configuration. Define a `sheets_config` dict attribute containing the name of your sheet as a key, and a `SheetConfig` class as a value.

## Validations

Several validations are run before importing a spreadsheet:

### Config version validation

Validate that the configuration version stored in the file is the same as the `SpreadsheetConfig.version` used.

### Sheets validation

Validate that all sheets in this `SpreadsheetConfig` class used, exist in imported file. Validate that all sheets in imported file, exist in this `SpreadsheetConfig` class used.

### Columns headers validation

Validate that the imported file contains the same columns headers as described in the `SheetConfig` used.

### Required data validation

Validate that there is a value in the imported file for each `required`, `required_unless`, `required_if` columns.

### Uniqueness validation [/!\ not implemented]

Validate that multiple cells in a row are unique together in the imported file.

### Types validation

Validate that each column in the imported file contains data of correct type (date, positive integer, ...).

### Data match validation

Validate that we find an object in the database matching the value in the imported file. If not, we ask the user to chose from a list of possibles values.

## Import data

If you want to import data in y our database from this spreadsheet, you need to define a `update_database(self, sheets)` method. This method is called after all data validations have been completed, and receive a python dict with an item for each sheet. The key is the name of the sheet, and the value is a python list of rows. Each row is a list containing a value for each column.

```py
def update_database(self, sheets):
    for sheet_name, rows in sheets.items():
        for row in rows:
            for value in row:
                print(value)
```


# `SheetConfig` class

Inherit this class to describe your sheets' configuration. Each attribute describes a column using a dictionary such as the following:

```py
<column_identifier> = {
  "name": str (required),  # The name of the column used in the header row
  "required": bool,  # Whether a value in the column is required when importing
  "required_unless": str,  # Whether a value in this column is required if the pointed column is empty
  "required_if": str,  # Whether a value in this column is required if the pointed column is filled
  "comment": str,  # A comment that appears in the header cell
  "admin_only": bool,  # Whether this column should be exported only when the current user is an administrator
  "validation": {  # A data validation applied to each cell of this column
    "name": str,  # A name used as header in the hidden config sheet
    "type": str (required),  # <url|date|list|range|whole...> See openpyxl documentation to get all available validation types
    ...  # Same args as openpyxl's DataValidation objects
  },
  "header_style": str,  # The name of a style that already exists in the SpreadsheetConfig to which this sheet belongs
  "style": str,  # The name of a style that already exists in the SpreadsheetConfig to which this sheet belongs
  "number_format": str # A value among FORMAT_* constants from openpyxl.styles.numbers or others values supported by XLSX spec
},
```

## Note on validation

To create a _boolean_ validation, you may use a `list` validation type with `django_spreadsheets.constants.YES_NO_CHOICES` as `formula1` value. To ensure a boolean value is displayed in your exported file, add `"number_format": "BOOLEAN"` in your column configuration.

## Note on number format

When the value in your exported file is not displayed correctly or not consistent across rows, you may define the `number_format` key in your column configuration.

Openxpyxl's format constants are not exhaustive. You may use other supported strings (eg: "BOOLEAN").

## Export data

If you want to export data to this sheet, you need to define a `get_data_to_export(self)` method. This method must return a python list containing an item by row. Each item in the list is a list containing a value for each column.

```py
def get_data_to_export(self):
  return [
    [1, "yellow", 20],
    [1, "green", 22],
  ]
```

# Settings

## `SPREADSHEET_CONFIG_SHEET_TITLE`

Default: `_("Configuration")`

The name of the (hidden) config sheet in the generated file. This special sheet is used to store data needed for validation (eg. lists of choices).

## `SPREADSHEET_MAX_VALIDATION_ROWS`

Default: `700`

When exporting data, the generated spreadsheet will have at least `SPREADSHEET_MAX_VALIDATION_ROWS` rows with data validation set up.

## `SPREADSHEET_MAX_STYLED_ROWS`

Default: `700`

When exporting data, the generated spreadsheet will have at least `SPREADSHEET_MAX_STYLED_ROWS` rows styled.

## `SPREADSHEET_COMMENT_AUTHOR`

Default: `"Django Spreadsheet"`

The name of the author used when adding comments on cells.

## `SPREADSHEET_EXPORT_FILE_NAME`

Default: `"export {config_name} {date}.xlsx"`

The name of the exported file when downloaded. Token `config_name` and `date` will be replaced respectively by the name of the configuration that is currently exported and the current date.

## `SPREADSHEET_TEMPLATE_FILE_NAME`

Default: `"{config_name} template file.xlsx"`

The name of the template file when downloaded. Token `config_name` will be replaced by the name of the configuration that is currently exported.

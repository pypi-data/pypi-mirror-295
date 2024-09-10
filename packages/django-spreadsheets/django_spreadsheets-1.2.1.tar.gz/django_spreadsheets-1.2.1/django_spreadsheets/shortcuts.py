# Standard Library
from typing import Generator, Tuple

# Django
from django.conf import settings
from django.utils import translation

# Third party
from openpyxl.worksheet.worksheet import Worksheet

# Local application / specific library imports
from .constants import (
    BOOL_XLSX_MAPPING,
    FALSE_BOOL_XLSX_VALUE,
    XLSX_BOOL_MAPPING,
    XLSX_EMPTY_VALUES,
)


def include_admin_fields_for_user(user):
    """Return True if the user is a superuser, False otherwise"""
    return user.is_superuser


def extract_rows(
    worksheet: Worksheet, columns_keys: list, min_row: int = 1
) -> Generator[Tuple[int, dict], None, None]:
    """Get a dict of values of lines of an excel sheet, keyed by header name"""

    for row in worksheet.iter_rows(min_row=min_row):
        if all(
            [cell.value in XLSX_EMPTY_VALUES or cell.data_type == "f" for cell in row]
        ):
            break  # stop parsing when empty line

        columns = {}
        for cell in row:
            column_key = columns_keys[cell.column - 1]
            value = cell.value

            if isinstance(value, str):
                value = value.strip()

            try:
                columns[column_key] = value
            except IndexError:
                ...
        yield cell.row, columns


def get_enum_choice(enum_class, enum_value, language_code=settings.LANGUAGE_CODE):
    """Get the choice of an enum value, for a given language_code"""

    with translation.override(language_code):
        return enum_class(enum_value)


def bool_to_xlsx(value: bool) -> str:
    """Convert a boolean to a string for xlsx export"""

    return BOOL_XLSX_MAPPING.get(value)


def xlsx_to_bool(value: str) -> bool:
    """Convert a string to bool for xlsx import"""

    if value == "" or value is None:
        value = FALSE_BOOL_XLSX_VALUE
    return XLSX_BOOL_MAPPING.get(value)

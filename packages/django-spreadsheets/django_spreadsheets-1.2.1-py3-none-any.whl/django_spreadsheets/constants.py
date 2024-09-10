# Django
from django.utils.translation import gettext as _

XLSX_EMPTY_VALUES = (None, "", 0, "None")

# Bools conversion
TRUE_BOOL_XLSX_VALUE = _("Yes")
FALSE_BOOL_XLSX_VALUE = _("No")

YES_NO_CHOICES = [TRUE_BOOL_XLSX_VALUE, FALSE_BOOL_XLSX_VALUE]

BOOL_XLSX_MAPPING = {True: TRUE_BOOL_XLSX_VALUE, False: FALSE_BOOL_XLSX_VALUE}

XLSX_BOOL_MAPPING = {v: k for k, v in BOOL_XLSX_MAPPING.items()}

VERSION_CUSTOM_PROPERTY_NAME = "DjangoSpreadsheetConfigVersion"

DEFAULT_HEADER_STYLE_NAME = "DefaultHeaderStyle"

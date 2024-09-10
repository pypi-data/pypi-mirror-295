# Django
from django.conf import settings
from django.utils.translation import gettext as _

CONFIG_SHEET_TITLE = getattr(
    settings, "SPREADSHEETS_CONFIG_SHEET_TITLE", _("Configuration")
)

MAX_VALIDATION_ROWS = getattr(settings, "SPREADSHEETS_MAX_VALIDATION_ROWS", 700)

MAX_STYLED_ROWS = getattr(settings, "SPREADSHEETS_MAX_STYLED_ROWS", 700)

COMMENT_AUTHOR = getattr(settings, "SPREADSHEETS_COMMENT_AUTHOR", "Django Spreadsheet")

EXPORT_FILE_NAME = getattr(
    settings, "SPREADSHEETS_EXPORT_FILE_NAME", _("export {config_name} {date}.xlsx")
)

TEMPLATE_FILE_NAME = getattr(
    settings, "SPREADSHEETS_TEMPLATE_FILE_NAME", _("{config_name} template file.xlsx")
)

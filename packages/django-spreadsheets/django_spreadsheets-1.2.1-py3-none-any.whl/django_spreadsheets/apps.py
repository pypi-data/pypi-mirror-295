# Django
from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.utils.translation import gettext_lazy as _

# Local application / specific library imports
from .autodiscover import autodiscover


class SpreadsheetAdminConfig(AdminConfig):
    default_site = "django_spreadsheets.admin.SpreadsheetAdminSite"


class SpreadsheetAppConfig(AppConfig):
    name = "django_spreadsheets"
    label = "django_spreadsheets"
    verbose_name = _("Spreadsheet")

    def ready(self) -> None:
        autodiscover()

# myproject/autodiscover.py
# Standard Library
import importlib

# Django
from django.apps import apps
from django.utils.module_loading import module_has_submodule

SPREADSHEET_CONFIG_NAME = "spreadsheets"


def autodiscover():
    discovered_classes = []

    for app in apps.get_app_configs():
        try:
            importlib.import_module(f"{app.name}.{SPREADSHEET_CONFIG_NAME}")
        except:  # NOQA
            # If something in spreadsheets.py raises an exception let that
            # exception bubble up. Only catch the exception if
            # spreadsheets.py doesn't exist
            if module_has_submodule(app.module, SPREADSHEET_CONFIG_NAME):
                raise

    return discovered_classes

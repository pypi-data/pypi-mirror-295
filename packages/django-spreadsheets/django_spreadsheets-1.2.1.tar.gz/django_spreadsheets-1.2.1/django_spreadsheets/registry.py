# Local application / specific library imports
from .base_config import SpreadsheetConfig


class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, cls):
        if not issubclass(cls, SpreadsheetConfig):
            raise ValueError("Registered class must inherit from SpreadsheetConfig")
        self._registry[cls.__name__] = cls

    def get_class(self, name):
        return self._registry.get(name)

    def get_all_classes(self):
        return self._registry


registry = Registry()


def register(cls):
    registry.register(cls)
    return cls

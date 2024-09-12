# Copyright 2024 Agnostiq Inc.
"""Arguments for Covalent blueprints."""
from pprint import pformat
from typing import Dict, Optional

from covalent_blueprints.reader.script import CovalentScript


class BlueprintInputs:
    """Provides arguments interface for Covalent blueprints."""

    def __init__(self, script: CovalentScript):
        self._docs: Dict[str, Optional[str]] = {}
        self._args, self._kwargs = script.core_function_inputs

        if not self._args == ():
            raise ValueError("Blueprints must not have positional arguments")

        if not isinstance(self._kwargs, dict):
            raise ValueError("Core function keyword arguments must be a dict")

    @property
    def kwargs(self) -> dict:
        """Default keyword arguments for the blueprint's core
        function."""
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value: dict) -> None:
        if isinstance(value, dict):
            self._kwargs = value
        else:
            raise ValueError("kwargs must be a dict")

    @property
    def docs(self) -> Dict[str, Optional[str]]:
        """Documentation for the arguments."""
        return self._docs.copy()

    @docs.setter
    def docs(self, value: dict) -> None:
        self._docs = value

    def to_dict(self):
        """Return the arguments as a dictionary."""
        return {"kwargs": self.kwargs.copy(), "docs": self.docs.copy()}

    def override_defaults(self, kwargs) -> dict:
        """Override the default arguments with the provided
        kwargs."""
        new_kwargs = self.kwargs.copy()
        new_kwargs.update(**kwargs)

        return new_kwargs

    def __getitem__(self, key):
        if key == "args":
            return self._args
        if key == "kwargs":
            return self.kwargs
        raise KeyError(f"Invalid key '{key}'")

    def __repr__(self):
        return f"BlueprintInputs({self.kwargs})"

    def __str__(self):
        return pformat(self.to_dict())

from abc import ABC, abstractmethod
import argparse
from argparse import _SubParsersAction
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type


class Subcommand(ABC):
    def __init__(self, parser, name: str, description: str, ):
        self._name = None
        self._description = None
        self._parser = None

        self.name = name
        self.description = description
        self.parser = parser

    @property
    def name(self):
        if not self._name:
            raise AttributeError("Subcommand name not set.")

        return self._name

    @name.setter
    @validate_type(str)
    def name(self, value):
        if not self._name:
            self._name = value

        else:
            raise AttributeError("Subcommand name already set.")

    @property
    def description(self):
        if not self._description:
            raise AttributeError("Subcommand description not set.")

        return self._description

    @description.setter
    @validate_type(str)
    def description(self, value):
        if not self._description:
            self._description = value

        else:
            raise AttributeError("Subcommand description already set.")

    @property
    def parser(self):
        if not self._parser:
            raise AttributeError("Subcommand parser not set.")

        return self._parser

    @parser.setter
    def parser(self, value):
        if not self._parser:
            self._parser = value

        else:
            raise AttributeError("Subcommand parser already set.")

    @property
    def help(self):
        return self.description

    @abstractmethod
    def register(self,subparser: _SubParsersAction):
        """
        Register the subcommand with the parser.

        Returns:
            None
        """
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace):
        """
        Run the subcommand.

        Parameters:
            args (argparse.Namespace):
                The parsed arguments from the command line.

        Returns:
            None
        """
        pass

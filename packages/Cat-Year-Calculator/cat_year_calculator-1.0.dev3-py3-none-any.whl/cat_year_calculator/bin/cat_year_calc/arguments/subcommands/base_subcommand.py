import argparse
from abc import abstractmethod
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.meta import Subcommand
from cat_year_calculator.lib.common.types import ParserType
from cat_year_calculator.lib.log_engine import Loggable


class BaseSubcommand(Subcommand, Loggable):
    def __init__(self, parser: ParserType, command_name: str, command_description: str, logger):
        Subcommand.__init__(self, parser, command_name, command_description)
        Loggable.__init__(self, logger)
        self.class_logger.debug(f'{self.__class__.__name__} initialized')

    def add_age_argument(self, command, help_text):
        command.add_argument(
            'age',
            type=int,
            help=help_text
        )
        self.class_logger.debug(f'Added age argument with help: {help_text}')

    def add_output_format_arguments(self, command):
        mutually_exclusive_group = command.add_mutually_exclusive_group()
        self.class_logger.debug('Added mutually exclusive group')

        mutually_exclusive_group.add_argument(
            '--as-int',
            action='store_true',
            help='Print result as an integer',
        )
        self.class_logger.debug('Added as-int argument')

        mutually_exclusive_group.add_argument(
            '--as-float',
            action='store_true',
            help='Print result as a float',
            default=True
        )
        self.class_logger.debug('Added as-float argument')

        command.add_argument(
            '--round-to',
            type=int,
            help='Rounds the result to the nearest whole number (used with --as-float)',
            default=2
        )
        self.class_logger.debug('Added round-to argument')

    @abstractmethod
    def run(self, args: argparse.Namespace):
        pass

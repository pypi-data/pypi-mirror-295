from argparse import ArgumentParser
from inspy_logger.constants import LEVELS as LOG_LEVELS
from cat_year_calculator.bin.cat_year_calc import MOD_LOGGER as PARENT_LOGGER
MOD_LOGGER = PARENT_LOGGER.get_child('arguments')
from cat_year_calculator.bin.cat_year_calc.arguments.errors import NoQueueToProcessError
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands import Subcommand, HumanToCatYears, CatToHumanYears
from cat_year_calculator.lib.common.types import ParserType




def add_arguments_to_parser(parser):
    """
    Adds basic arguments to the parser, such as log level.
    """
    parser.add_argument(
        '-l', '--log-level',
        choices=LOG_LEVELS,
        default='INFO',
        help='The level at which to output log entries to the console.'
    )


class Parser(ArgumentParser):
    _queue = []  # Queue for subcommands before the parser is instantiated
    _subcommands = []  # Holds subcommand instances
    _processed = False  # Tracks if the queue has been processed
    _instance = None  # Singleton instance tracker

    @staticmethod
    def register_subcommand(name: str, command: Subcommand):
        """
        Registers a subcommand to be processed later.
        """
        Parser._queue.append((name, command))

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Parser, cls).__new__(cls)
        return cls._instance

    def __init__(self, skip_auto_processing: bool = False, **kwargs):
        # Prevent reinitialization of the singleton instance
        if not hasattr(self, '_initialized'):
            super().__init__(**kwargs)

            # Add basic arguments to the parser
            add_arguments_to_parser(self)

            # Initialize subparsers container
            self.__subparsers = None

            # Automatically process the queue unless skipped
            if not skip_auto_processing and not Parser._processed and Parser._queue:
                self.process_registration_queue()

            # Set initialization flag
            self._initialized = True

    @property
    def subcommands(self):
        return self._subcommands

    @property
    def subparsers(self):
        if not self.__subparsers:
            self.__subparsers = self.add_subparsers(dest='subcommand')
        return self.__subparsers

    def process_registration_queue(self):
        """
        Processes the queued subcommands by registering them.
        """
        if not Parser._queue:
            raise NoQueueToProcessError("There are no subcommands to process.")

        # Process the queued subcommands
        while Parser._queue:
            name, command_cls = Parser._queue.pop(0)
            command_instance = command_cls(self)  # Instantiate the subcommand
            self._subcommands.append(command_instance)
            self._register_subcommand(name, command_instance)

        Parser._processed = True

    def _register_subcommand(self, name: str, command: Subcommand):
        """
        Registers a subcommand by adding it to the subparsers.
        """
        command = command(self)

        # Let the command define its own arguments
        command.register(self)

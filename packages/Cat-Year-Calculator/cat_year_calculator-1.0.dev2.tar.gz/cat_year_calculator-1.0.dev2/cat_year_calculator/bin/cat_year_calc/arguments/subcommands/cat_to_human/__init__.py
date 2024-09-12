from cat_year_calculator.lib.log_engine import PROG_LOGGER
from cat_year_calculator.lib.converter import cat_to_human_years
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.base_subcommand import BaseSubcommand

MOD_LOGGER = PROG_LOGGER.get_child('bin.cat_year_calc.arguments.subcommands.cat_to_human')

COMMAND_NAME = 'cat-to-human'
COMMAND_DESCRIPTION = 'Converts the age of a cat in cat years to human years'


class CatToHumanYears(BaseSubcommand):

    def __init__(self, parser):
        super().__init__(parser, COMMAND_NAME, COMMAND_DESCRIPTION, MOD_LOGGER)

    def register(self, subparser):  # subparser passed from the main parser
        # Ensure the arguments are registered uniquely for this subcommand
        self.add_age_argument(subparser, 'Age of the cat in cat years')
        subparser.set_defaults(subcommand=self.run)  # Handle subcommand action
        self.add_output_format_arguments(subparser)  # This should add arguments specific to this subcommand

    def run(self, args):
        human_years = cat_to_human_years(args.age)

        if args.as_int:
            return int(human_years)
        else:
            return round(human_years, args.round_to)

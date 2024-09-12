from cat_year_calculator.lib.log_engine import PROG_LOGGER
from cat_year_calculator.lib.converter import human_to_cat_years
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.base_subcommand import BaseSubcommand

MOD_LOGGER = PROG_LOGGER.get_child('bin.cat_year_calc.arguments.subcommands.human_to_cat')

COMMAND_NAME = 'human-to-cat'
COMMAND_DESCRIPTION = 'Converts the age of a cat in human years to cat years'


class HumanToCatYears(BaseSubcommand):

    def __init__(self, parser):
        super().__init__(parser, COMMAND_NAME, COMMAND_DESCRIPTION, MOD_LOGGER)

    def register(self, subparser):  # subparser passed from the main parser
        # Ensure the arguments are registered uniquely for this subcommand
        self.add_age_argument(subparser, 'Age of the cat in human years')
        subparser.set_defaults(subcommand=self.run)  # Handle subcommand action
        self.add_output_format_arguments(subparser)  # This should add arguments specific to this subcommand

    def run(self, args):
        cat_years = human_to_cat_years(args.age)

        if args.as_int:
            return int(cat_years)
        else:
            return round(cat_years, args.round_to)

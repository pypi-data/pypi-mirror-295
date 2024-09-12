from cat_year_calculator.lib.converter import human_to_cat_years, cat_to_human_years
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.base_subcommand import BaseSubcommand
from cat_year_calculator.lib.log_engine import PROG_LOGGER


MOD_LOGGER = PROG_LOGGER.get_child('bin.cat_year_calc.arguments.subcommands.convert')


COMMAND_NAME = 'convert'
COMMAND_DESCRIPTION = 'Converts the age of a cat in human years to cat years or vice versa'


class ConvertYears(BaseSubcommand):
    def __init__(self, parser):
        super().__init__(
                parser,
                COMMAND_NAME,
                COMMAND_DESCRIPTION,
                MOD_LOGGER
                )

    def register(self, subparser):

        print(subparser)
        subparser = subparser.subparsers.add_parser('convert', help='Converts the age of a cat in human years to cat years or vice versa')

        # Add positional argument 'conversion_type'
        subparser.add_argument(
                '--conversion-type',
                choices=['human-to-cat', 'cat-to-human'],
                help="The type of conversion to perform",
                default='human-to-cat',
                required=False
                )

        # Add the age argument, which is common to both conversions
        subparser.add_argument(
                '--age',
                type=int,
                help='Age of the cat or human in respective years (based on conversion_type)',
                required=True
                )

        # Add mutually exclusive arguments for output format
        mutually_exclusive_group = subparser.add_mutually_exclusive_group()
        mutually_exclusive_group.add_argument(
                '--as-int',
                action='store_true',
                help='Print result as an integer',
                )
        mutually_exclusive_group.add_argument(
                '--as-float',
                action='store_true',
                help='Print result as a float (default)',
                default=True
                )

        # Add optional rounding argument
        subparser.add_argument(
                '--round-to',
                type=int,
                help='Rounds the result to the nearest whole number (used with --as-float)',
                default=2
                )

    def run(self, args):
        if args.conversion_type == 'human-to-cat':
            result = human_to_cat_years(args.age)
        elif args.conversion_type == 'cat-to-human':
            result = cat_to_human_years(args.age)

            # Handle output format based on user input
        if args.as_int:
            return int(result)
        else:
            return round(result, args.round_to)

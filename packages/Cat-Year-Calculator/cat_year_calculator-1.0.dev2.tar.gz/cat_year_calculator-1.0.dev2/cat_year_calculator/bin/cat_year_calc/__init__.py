from cat_year_calculator.bin import MOD_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('cat_year_calc')

from cat_year_calculator.bin.cat_year_calc.arguments import Parser
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.convert import ConvertYears
from cat_year_calculator.lib.converter import *


def main():

    parser = Parser()
    parser._register_subcommand('convert',ConvertYears)
    args = parser.parse_args()
    print(args)

    if args.subcommand is None or args.subcommand == 'convert':
        if args.conversion_type == 'human-to-cat':
            result = human_to_cat_years(args.age, args.as_int, args.round_to)
        else:
            result = cat_to_human_years(args.age, args.as_int, args.round_to)

        print(result)



if __name__ == '__main__':
    main()

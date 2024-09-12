from cat_year_calculator.bin.cat_year_calc.arguments import MOD_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('subcommands')

from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.meta import Subcommand
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.human_to_cat import HumanToCatYears
from cat_year_calculator.bin.cat_year_calc.arguments.subcommands.cat_to_human import CatToHumanYears

def human_to_cat_years(age, as_int=False, round_to=2):
    """
    Convert human years to cat years.

    The first two human years are equivalent to 24 cat years.
    Each additional human year is roughly 4 cat years.

    Parameters:
    age (int or float): The number of human years.
    as_int (bool): Whether to return the result as an integer. Default is False.
    round_to (int): Number of decimal places to round to if not returning an integer. Default is 2.

    Returns:
    int or float: The equivalent cat years.
    """
    if age < 0:
        raise ValueError("Years cannot be negative.")

    if age <= 2:
        result = age * 12
    else:
        result = 24 + (age - 2) * 4

    if as_int:
        return int(result)
    else:
        return round(result, round_to)


def cat_to_human_years(age, as_int=False, round_to=2):
    """
    Convert cat years to human years.

    The first 24 cat years are equivalent to 2 human years.
    Each additional 4 cat years is roughly equivalent to 1 human year.

    Parameters:
    age (int or float): The number of cat years.
    as_int (bool): Whether to return the result as an integer. Default is False.
    round_to (int): Number of decimal places to round to if not returning an integer. Default is 2.

    Returns:
    int or float: The equivalent human years.
    """
    if age < 0:
        raise ValueError("Years cannot be negative.")

    if age <= 24:
        result = age / 12
    else:
        result = 2 + (age - 24) / 4

    if as_int:
        return int(result)
    else:
        return round(result, round_to)

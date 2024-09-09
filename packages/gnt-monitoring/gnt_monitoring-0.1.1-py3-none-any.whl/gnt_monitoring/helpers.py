from typing import Tuple


def percentage(part: int, whole: int) -> float:
    """
    Calculating percentage of a given numbers
    :param int part: Number for which to calculate percentage
    :param int whole: Whole number
    :returns: float
    """
    return round(100 * float(part) / float(whole), 2)


def convert_to_human(size: int) -> Tuple[float, str]:
    """
    Convert given size number to human readable format
    :param int size: number which must be converted
    :return: tuple of converted number rounded to 2 and unit
    """
    UNITS = ["MiB", "GiB", "TiB", "PiB"]
    for unit in UNITS:
        if unit == UNITS[-1]:
            break
        if float(size) < 1024.0:
            break
        size = round(float(size) / 1024.0, 2)
    return size, unit


def check_for_status(warning: int | float, critical: int | float, value: int | float) -> int:
    """
    check for value status
    :param int|float warning: Warning value
    :param int|float critical: Critical value
    :param int|float value: Value to verify
    """
    if critical > value >= warning:
        return 1
    elif value >= critical:
        return 2
    return 0

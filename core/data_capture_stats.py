from expression import Result, Ok, Error

from core.domain import (
    DataCaptureStats,
    InvalidBetweenRangeError,
    ValidNumber,
)


def less(dcs: DataCaptureStats, number: ValidNumber) -> int:
    """
    Returns the count of captured numbers less than the given number.
    :param dcs: Data capture stats instance with stats computed.
    :param number: Number to query stats.
    :return: Captured numbers count less than the number.
    """
    return dcs.stats[number.value].lesser


def greater(dcs: DataCaptureStats, number: ValidNumber) -> int:
    """
    Returns the count of captured numbers greater than the given number.
    :param dcs: Data capture stats instance with stats computed.
    :param number: Number to query stats.
    :return: Captured numbers count greater than the number.
    """
    return dcs.stats[number.value].greater


def between(dcs: DataCaptureStats, lower_number: ValidNumber, higher_number: ValidNumber)\
        -> Result[int, InvalidBetweenRangeError]:
    """
    Returns the count of captured numbers between the inclusive range.
    :param dcs: Data capture stats instance with stats computed.
    :param lower_number: Lower bound number to query stats.
    :param higher_number: Higher bound number to query stats.
    :return: Captured numbers count for the inclusive range, if range is valid, otherwise invalid range error.
    """
    if lower_number.value > higher_number.value:
        return Error(InvalidBetweenRangeError(lower_number.value, higher_number.value))

    lns = dcs.stats[lower_number.value]
    hns = dcs.stats[higher_number.value]
    return Ok(hns.lesser + hns.frequency - lns.lesser)

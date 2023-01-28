from expression import Option, effect

from core.domain import (
    CapturedNumberStats,
    DataCaptureStats,
    ValidNumber,
)


def less(dcs: DataCaptureStats, number: ValidNumber) -> Option[int]:
    """
    Returns the count of captured numbers less than the given number.
    :param dcs: Data capture stats instance with stats computed.
    :param number: Number to query stats.
    :return: Captured numbers count less than the number if captured. Otherwise, nothing.
    """
    return dcs.stats.try_find(number).map(lambda capt_num_stats: capt_num_stats.lesser)


def greater(dcs: DataCaptureStats, number: ValidNumber) -> Option[int]:
    """
    Returns the count of captured numbers greater than the given number.
    :param dcs: Data capture stats instance with stats computed.
    :param number: Number to query stats.
    :return: Captured numbers count greater than the number if captured. Otherwise, nothing.
    """
    return dcs.stats.try_find(number).map(lambda capt_num_stats: capt_num_stats.greater)


@effect.option[int]()
def between(dcs: DataCaptureStats, lower_number: ValidNumber, higher_number: ValidNumber) -> Option[int]:
    """
    Returns the count of captured numbers between the inclusive range.
    :param dcs: Data capture stats instance with stats computed.
    :param lower_number: Lower bound number to query stats.
    :param higher_number: Higher bound number to query stats.
    :return: Captured numbers count for the inclusive range if both numbers were captured. Otherwise, nothing.
    """
    lns: CapturedNumberStats = yield from dcs.stats.try_find(lower_number)
    hns: CapturedNumberStats = yield from dcs.stats.try_find(higher_number)
    return hns.lesser + hns.frequency - lns.lesser

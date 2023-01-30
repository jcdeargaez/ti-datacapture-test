from expression import Ok, Error

import core.data_capture_stats
from core.domain import ValidNumber


class DataCaptureStats:
    """Serves stats queries on captured data."""
    def __init__(self, dcs: core.domain.DataCaptureStats):
        """
        Instantiates stats on captured numbers to serve queries.
        :param dcs: Data capture stats already computed.
        """
        self.dcs = dcs

    def greater(self, number: int) -> int:
        """
        Returns the count of captured numbers greater than the given number.
        :param number: Number to query.
        :return: Greater stats for the given number.
        :raise: if number is invalid or was not captured.
        """
        return core.data_capture_stats.greater(self.dcs, ValidNumber(number))

    def less(self, number: int) -> int:
        """
        Returns the count of captured numbers less than the given number.
        :param number: Number to query.
        :return: Less than stats for the given number.
        :raise: if number is invalid or was not captured.
        """
        return core.data_capture_stats.less(self.dcs, ValidNumber(number))

    def between(self, lower_number: int, higher_number: int) -> int:
        """
        Returns the count of numbers between the inclusive range of captured numbers.
        :param lower_number: Lower bound to query.
        :param higher_number: Higher bound to query.
        :return: Captured numbers count for the inclusive range.
        :raise: if the numbers are invalid or were not captured.
        """
        match core.data_capture_stats.between(self.dcs, ValidNumber(lower_number), ValidNumber(higher_number)):
            case Ok(value):
                return value

            case Error(err):
                raise err

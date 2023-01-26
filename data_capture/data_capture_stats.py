from itertools import accumulate, islice
from typing import Callable, Tuple, Iterable

from expression import Result, Ok, Error

from data_capture import captured_number
from .domain import (
    CapturedNumber,
    CapturedNumberFrequency,
    CapturedNumberStats,
    InvalidBetweenRangeError,
    InvalidNumberError,
    NoCapturedNumberError,
    NoCapturedNumbersError
)
from .util import fst, return_ok_value_or_raise


class DataCaptureStats:
    """Serves stats queries on captured data."""

    def __init__(self, captured_numbers_frequencies: Iterable[CapturedNumberFrequency], total_frequency: int):
        """
        Instantiates stats on captured numbers to serve queries.
        :param captured_numbers_frequencies: Captured numbers frequencies.
        :param total_frequency: Accumulated frequency of captured numbers.
        :raise: If captured numbers list is None or empty.
        """
        capt_num_stats = DataCaptureStats.__scan_stats(captured_numbers_frequencies, total_frequency)
        self.stats = {cns.number: cns for cns in capt_num_stats}
        if len(self.stats) == 0:
            raise NoCapturedNumbersError()

    @staticmethod
    def __scan_stats(captured_numbers_frequencies: Iterable[CapturedNumberFrequency], total_frequency: int)\
            -> Iterable[CapturedNumberStats]:
        """
        Computes less than and greater stats for captured numbers.
        :param captured_numbers_frequencies: Captured numbers to compute stats.
        :param total_frequency: Accumulated frequency of captured numbers.
        :return: Iterator of captured numbers stats.
        """
        def map_scan_stats(acc: Tuple[CapturedNumberStats | None, int, int],
                           cnf: CapturedNumberFrequency) -> Tuple[CapturedNumberStats | None, int, int]:
            _, lesser_so_far, greater_so_far = acc
            cns = CapturedNumberStats(cnf.number, cnf.frequency, greater_so_far - cnf.frequency, lesser_so_far)
            return cns, lesser_so_far + cnf.frequency, greater_so_far - cnf.frequency

        stats_scan = accumulate(captured_numbers_frequencies, map_scan_stats, initial=(None, 0, total_frequency))
        capt_num_stats = map(fst, stats_scan)
        return islice(capt_num_stats, 1, None)

    def __map_captured_number_stats(self, number: int, mapper: Callable[[CapturedNumberStats], int])\
            -> Result[int, InvalidNumberError | NoCapturedNumberError]:
        """
        Returns a result with the stats for a captured number. If the number is invalid or not found returns an error.
        :param number: Number to map stats if its valid and was captured.
        :param mapper: Computes a value given the stats for the number.
        :return: Computed result value for the number stats or error.
        """
        def bind_captured_number_stats(capt_num: CapturedNumber):
            if (cns := self.stats.get(capt_num)) is None:
                return Error(NoCapturedNumberError(number))

            return Ok(mapper(cns))

        capt_num_result = captured_number.create(number)
        return capt_num_result.bind(bind_captured_number_stats)

    @return_ok_value_or_raise
    def greater(self, number: int) -> Result[int, InvalidNumberError | NoCapturedNumberError]:
        """
        Returns a result with the count of captured numbers greater than the given number.
        :param number: Number to query greater captured numbers stats.
        :return: Greater stats for the given number if its valid and was captured or error.
        """
        return self.__map_captured_number_stats(number, lambda cns: cns.greater)

    @return_ok_value_or_raise
    def less(self, number: int) -> Result[int, InvalidNumberError | NoCapturedNumberError]:
        """
        Returns a result with the count of captured numbers less than the given number.
        :param number: Number to query less than captured numbers stats.
        :return: Less than stats for the given number if its valid and was captured.
        """
        return self.__map_captured_number_stats(number, lambda cns: cns.lesser)

    @return_ok_value_or_raise
    def between(self, lower_number: int, higher_number: int)\
            -> Result[int, InvalidNumberError | NoCapturedNumberError | InvalidBetweenRangeError]:
        """
        Returns a result with the count of numbers between the inclusive range.
        :param lower_number: Lower bound number to compute stats.
        :param higher_number: Higher bound number to compute stats.
        :return: Captured numbers count for the inclusive range if its valid and numbers boundaries were captured.
        """
        if lower_number > higher_number:
            return Error(InvalidBetweenRangeError(lower_number, higher_number))

        def bind_between_stats(ln_lesser: int) -> Result[int, InvalidNumberError | NoCapturedNumberError]:
            hn_result = self.__map_captured_number_stats(higher_number, lambda cns: cns.frequency + cns.lesser)
            return hn_result.map(lambda hn_frequency_plus_lesser: hn_frequency_plus_lesser - ln_lesser)

        ln_result = self.__map_captured_number_stats(lower_number, lambda cns: cns.lesser)
        return ln_result.bind(bind_between_stats)

from dataclasses import replace
from typing import Dict

from expression import Result, Ok, Error

from data_capture import captured_number
from data_capture.data_capture_stats import DataCaptureStats
from data_capture.domain import (
    CapturedNumber,
    CapturedNumberFrequency,
    InvalidNumberError,
    NoCapturedNumbersError,
    MAX_VALID_NUMBER,
    MIN_VALID_NUMBER
)
from data_capture.util import return_ok_value_or_raise


class DataCapture:
    """Captures numbers and builds stats."""

    def __init__(self):
        """Instantiates an empty data capturer."""
        self.added_values: Dict[CapturedNumber, CapturedNumberFrequency] = {}
        self.total_frequency = 0

    @return_ok_value_or_raise
    def add(self, number: int) -> Result[None, InvalidNumberError]:
        """
        Captures a number and increments its frequency.
        :param number: Number to capture.
        :return: Result indicating operation success or error.
        """
        def add_or_increment_frequency(capt_num: CapturedNumber) -> None:
            capt_num_freq = self.added_values.get(capt_num, CapturedNumberFrequency(capt_num, 0))
            self.added_values[capt_num] = replace(capt_num_freq, frequency=capt_num_freq.frequency + 1)
            self.total_frequency += 1

        capt_num_result = captured_number.create(number)
        return capt_num_result.map(add_or_increment_frequency)

    @return_ok_value_or_raise
    def build_stats(self) -> Result[DataCaptureStats, NoCapturedNumbersError]:
        """
        Builds a stats object to serve queries.
        :return: Result containing CaptureDataStats instance if at least one numbers was captured or error.
        """
        def walk_captured_numbers_frequencies():
            for number in range(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1):
                capt_num = CapturedNumber(number)
                if (capt_num_freq := self.added_values.get(capt_num)) is not None:
                    yield capt_num_freq
        try:
            return Ok(DataCaptureStats(walk_captured_numbers_frequencies(), self.total_frequency))
        except NoCapturedNumbersError as ex:
            return Error(ex)

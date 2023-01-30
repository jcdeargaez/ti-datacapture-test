from typing import Iterable, Tuple

from expression import pipe, fst
from expression.collections import Map, seq

from core.domain import (
    ActiveDataCapture,
    NumberFrequency,
    NumberStats,
    EmptyDataCapture,
    DataCapture,
    DataCaptureStats,
    MAX_VALID_NUMBER,
    MIN_VALID_NUMBER,
    ValidNumber,
)


def add(dc: DataCapture, number: ValidNumber) -> ActiveDataCapture:
    """
    Captures a number and increments its frequency.
    :param dc: Either empty or active data capturer instance.
    :param number: Number to capture.
    :return: New instance of active data capturer with added number and frequency updated.
    """
    match dc:
        case EmptyDataCapture():
            captured_numbers = Map.empty().add(number, NumberFrequency(1))
            return ActiveDataCapture(captured_numbers, NumberFrequency(1))

        case ActiveDataCapture() as adc:
            new_nf = adc.captured_numbers.try_find(number)\
                .map(lambda cnf: NumberFrequency(cnf.frequency + 1))\
                .default_value(NumberFrequency(1))
            new_captured_numbers = adc.captured_numbers.add(number, new_nf)
            new_captured_frequency = NumberFrequency(adc.total_captured_numbers.frequency + 1)
            return ActiveDataCapture(new_captured_numbers, new_captured_frequency)


def build_stats(adc: ActiveDataCapture) -> DataCaptureStats:
    """
    Builds a stats object to serve queries.
    :param adc: Active data capturer with some captured numbers.
    :return: CaptureDataStats instance with computed stats.
    """
    def walk_numbers_frequencies() -> Iterable[NumberFrequency]:
        """
        Returns an iterable for the frequencies for each valid number.
        First item corresponds to MIN_VALID_NUMBER and last item to MAX_VALID_NUMBER captured frequency.
        :return: Iterable of number frequencies.
        """
        for number in range(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1):
            yield adc.captured_numbers.try_find(ValidNumber(number)).default_value(NumberFrequency(0))

    def compute_stats(acc: Tuple[NumberStats, int], nf: NumberFrequency) -> Tuple[NumberStats, int]:
        """
        Compute accumulated stats for a number.
        :param acc: Tuple of accumulated stats and lesser count so far.
        :param nf: Current number frequency.
        :return: Tuple of number stats and next lesser count.
        """
        stats_so_far, lesser = acc
        return NumberStats(nf.frequency, lesser, stats_so_far.greater - nf.frequency), lesser + nf.frequency

    stats = pipe(
        walk_numbers_frequencies(),
        seq.scan(compute_stats, (NumberStats(0, 0, adc.total_captured_numbers.frequency), 0)),
        seq.tail,
        seq.map(fst))
    return DataCaptureStats(list(stats))

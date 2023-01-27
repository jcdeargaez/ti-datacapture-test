from typing import Iterable, Tuple

from expression import Some, pipe, fst
from expression.collections import Map, seq

from core.domain import (
    ActiveDataCapture,
    CapturedNumber,
    CapturedNumberFrequency,
    CapturedNumberStats,
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
    captured_number = CapturedNumber(number.value)
    match dc:
        case EmptyDataCapture():
            captured_numbers = Map.empty().add(captured_number.value, CapturedNumberFrequency(1))
            return ActiveDataCapture(captured_numbers, CapturedNumberFrequency(1))

        case ActiveDataCapture() as adc:
            match adc.captured_numbers.try_find(captured_number.value):
                case Some(capt_num_freq):
                    new_cnf = CapturedNumberFrequency(capt_num_freq.frequency + 1)
                case Nothing:
                    new_cnf = CapturedNumberFrequency(1)
            new_captured_numbers = adc.captured_numbers.add(captured_number.value, new_cnf)
            new_captured_frequency = CapturedNumberFrequency(adc.total_captured_numbers.frequency + 1)
            return ActiveDataCapture(new_captured_numbers, new_captured_frequency)


def build_stats(dc: ActiveDataCapture) -> DataCaptureStats:
    """
    Builds a stats object to serve queries.
    :param dc: Active data capturer with some captured numbers.
    :return: CaptureDataStats instance with computed stats.
    """
    def walk_captured_numbers_frequencies() -> Iterable[Tuple[CapturedNumber, CapturedNumberFrequency]]:
        for number in range(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1):
            match dc.captured_numbers.try_find(number):
                case Some(capt_num_freq):
                    yield CapturedNumber(number), capt_num_freq

    def map_scan_stats(acc: Tuple[Tuple[int | None, CapturedNumberStats | None], Tuple[int, int]],
                       cn_cnf: Tuple[CapturedNumber, CapturedNumberFrequency])\
            -> Tuple[Tuple[int | None, CapturedNumberStats | None], Tuple[int, int]]:
        cn, cnf = cn_cnf
        _, (lesser_so_far, greater_so_far) = acc
        new_greater = greater_so_far - cnf.frequency
        cns = CapturedNumberStats(cnf.frequency, lesser_so_far, new_greater)
        return (cn.value, cns), (lesser_so_far + cnf.frequency, new_greater)

    stats = pipe(
        walk_captured_numbers_frequencies(),
        seq.scan(map_scan_stats, ((None, None), (0, dc.total_captured_numbers.frequency))),
        seq.tail,
        seq.map(fst)
    )
    return DataCaptureStats(Map.of_seq(stats))

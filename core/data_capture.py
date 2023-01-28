from typing import Iterable, Tuple

from expression import Some, pipe, fst
from expression.collections import Map, seq

from core.domain import (
    ActiveDataCapture,
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
    match dc:
        case EmptyDataCapture():
            captured_numbers = Map.empty().add(number, CapturedNumberFrequency(1))
            return ActiveDataCapture(captured_numbers, CapturedNumberFrequency(1))

        case ActiveDataCapture() as adc:
            new_cnf = adc.captured_numbers.try_find(number)\
                .map(lambda cnf: CapturedNumberFrequency(cnf.frequency + 1))\
                .default_value(CapturedNumberFrequency(1))
            new_captured_numbers = adc.captured_numbers.add(number, new_cnf)
            new_captured_frequency = CapturedNumberFrequency(adc.total_captured_numbers.frequency + 1)
            return ActiveDataCapture(new_captured_numbers, new_captured_frequency)


def build_stats(dc: ActiveDataCapture) -> DataCaptureStats:
    """
    Builds a stats object to serve queries.
    :param dc: Active data capturer with some captured numbers.
    :return: CaptureDataStats instance with computed stats.
    """
    def walk_captured_numbers_frequencies() -> Iterable[Tuple[ValidNumber, CapturedNumberFrequency]]:
        for number in range(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1):
            valid_number = ValidNumber(number)
            match dc.captured_numbers.try_find(valid_number):
                case Some(capt_num_freq):
                    yield valid_number, capt_num_freq

    def map_scan_stats(acc: Tuple[Tuple[ValidNumber | None, CapturedNumberStats | None], Tuple[int, int]],
                       vn_cnf: Tuple[ValidNumber, CapturedNumberFrequency])\
            -> Tuple[Tuple[ValidNumber | None, CapturedNumberStats | None], Tuple[int, int]]:
        vn, cnf = vn_cnf
        _, (lesser_so_far, greater_so_far) = acc
        new_greater = greater_so_far - cnf.frequency
        cns = CapturedNumberStats(cnf.frequency, lesser_so_far, new_greater)
        return (vn, cns), (lesser_so_far + cnf.frequency, new_greater)

    stats = pipe(
        walk_captured_numbers_frequencies(),
        seq.scan(map_scan_stats, ((None, None), (0, dc.total_captured_numbers.frequency))),
        seq.tail,
        seq.map(fst)
    )
    return DataCaptureStats(Map.of_seq(stats))

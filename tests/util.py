from typing import List, Tuple, Callable, Dict, Any

from hypothesis.strategies import integers, lists, tuples, composite, SearchStrategy

from data_capture import (
    MIN_VALID_NUMBER,
    MAX_VALID_NUMBER,
    DataCapture,
    DataCaptureStats,
)


@composite
def stats(draw: Callable[[SearchStrategy[List[Tuple[Any, ...]]]], List[Tuple[int, int]]],
          min_valid_number=MIN_VALID_NUMBER,
          max_valid_number=MAX_VALID_NUMBER) -> Tuple[Dict[int, int], DataCaptureStats]:
    """
    Creates a stats instance from captured random numbers.
    :param draw: Callable to generate random numbers to add with their frequencies.
    :param min_valid_number: Custom min valid number. Takes the max compared with MIN_VALID_NUMBER and min
    MAX_VALID_NUMBER.
    :param max_valid_number: Custom max valid number. Takes the min compared with MAX_VALID_NUMBER and max
    MIN_VALID_NUMBER.
    :return: Tuple of a dictionary having captured numbers and their frequencies, and stats instance.
    """
    valid_number = integers(
        min(max(min_valid_number, MIN_VALID_NUMBER), MAX_VALID_NUMBER),
        max(min(max_valid_number, MAX_VALID_NUMBER), MIN_VALID_NUMBER))
    frequency = integers(min_value=1, max_value=10)
    numbers_and_frequencies = lists(tuples(valid_number, frequency), min_size=1, max_size=100)
    some_numbers_and_frequencies = draw(numbers_and_frequencies)
    dc = DataCapture()
    added = {}
    for number, frequency in some_numbers_and_frequencies:
        for _ in range(frequency):
            dc.add(number)
        added[number] = added.get(number, 0) + frequency
    dcs = dc.build_stats()
    return added, dcs


@composite
def invalid_number(draw: Callable[[SearchStrategy[int]], int]) -> int:
    """
    Creates an invalid number.
    :param draw: Callable to generate invalid numbers randomly.
    :return: int out of the valid range.
    """
    return draw(integers().filter(lambda num: num < MIN_VALID_NUMBER or num > MAX_VALID_NUMBER))

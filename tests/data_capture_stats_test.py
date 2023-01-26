from typing import List, Tuple, Callable, Dict, Any

from hypothesis import given
from hypothesis.strategies import integers, lists, tuples, composite, SearchStrategy
import pytest

from data_capture import (
    MIN_VALID_NUMBER,
    MAX_VALID_NUMBER,
    DataCapture,
    DataCaptureStats,
    InvalidBetweenRangeError,
    InvalidNumberError,
    NoCapturedNumberError,
    NoCapturedNumbersError,
)
from .util import stats, invalid_number


def test_create_stats_with_empty_frequencies_raises_error() -> None:
    with pytest.raises(NoCapturedNumbersError):
        DataCaptureStats([], 0)


@given(stats())
def test_less_than_query(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    acc_lessers = 0
    for number, frequency in sorted(added.items()):
        assert dcs.less(number) == acc_lessers
        acc_lessers += frequency


@given(invalid_number(), stats(max_valid_number=MAX_VALID_NUMBER - 1))
def test_less_than_query_errors(number: int, numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    _, dcs = numbers_stats
    with pytest.raises(InvalidNumberError):
        dcs.less(number)

    with pytest.raises(NoCapturedNumberError):
        dcs.less(MAX_VALID_NUMBER)


@given(stats())
def test_greater_query(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    acc_greaters = sum(added.values())
    for number, frequency in sorted(added.items()):
        acc_greaters -= frequency
        assert dcs.greater(number) == acc_greaters


@given(invalid_number(), stats(max_valid_number=MAX_VALID_NUMBER - 1))
def test_greater_query_errors(number: int, numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    _, dcs = numbers_stats
    with pytest.raises(InvalidNumberError):
        dcs.greater(number)

    with pytest.raises(NoCapturedNumberError):
        dcs.greater(MAX_VALID_NUMBER)


@given(stats())
def test_between_query(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    total_frequency = sum(added.values())
    for number, frequency in added.items():
        assert dcs.between(number, number) == frequency
        assert dcs.less(number) + frequency + dcs.greater(number) == total_frequency


@given(stats(min_valid_number=MIN_VALID_NUMBER + 1, max_valid_number=MAX_VALID_NUMBER - 1))
def test_between_query_errors(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    min_added = min(added.keys())
    max_added = max(added.keys())
    with pytest.raises(InvalidBetweenRangeError):
        dcs.between(MAX_VALID_NUMBER, MIN_VALID_NUMBER)

    with pytest.raises(InvalidNumberError):
        dcs.between(MIN_VALID_NUMBER - 1, MAX_VALID_NUMBER + 1)

    with pytest.raises(InvalidNumberError):
        dcs.between(MIN_VALID_NUMBER - 1, MAX_VALID_NUMBER)

    with pytest.raises(NoCapturedNumberError):
        dcs.between(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1)

    with pytest.raises(NoCapturedNumberError):
        dcs.between(min_added, MAX_VALID_NUMBER)

    with pytest.raises(NoCapturedNumberError):
        dcs.between(MIN_VALID_NUMBER, max_added)

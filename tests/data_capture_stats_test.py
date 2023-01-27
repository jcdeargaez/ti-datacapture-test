import math
from typing import Tuple, Dict

from hypothesis import given
import pytest

from core.domain import (
    MIN_VALID_NUMBER,
    MAX_VALID_NUMBER,
    InvalidBetweenRangeError,
    InvalidNumberError,
    NoCapturedNumberError,
    NoCapturedNumbersRangeError
)
from ooapi.data_capture_stats import DataCaptureStats
from tests.util import stats, invalid_number


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
    numbers = sorted(added.keys())
    for ln, hn in ((ln, hn) for i, ln in enumerate(numbers) for j, hn in enumerate(numbers) if i <= j):
        assert dcs.less(ln) + dcs.between(ln, hn) + dcs.greater(hn) == total_frequency


@given(stats(min_valid_number=MIN_VALID_NUMBER + 1, max_valid_number=MAX_VALID_NUMBER - 1))
def test_between_query_errors(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    min_added = min(added.keys())
    max_added = max(added.keys())
    with pytest.raises(InvalidBetweenRangeError) as ex_info:
        dcs.between(MAX_VALID_NUMBER, MIN_VALID_NUMBER)
    assert ex_info.value.lower_number == MAX_VALID_NUMBER
    assert ex_info.value.higher_number == MIN_VALID_NUMBER

    with pytest.raises(InvalidNumberError) as ex_info:
        dcs.between(MIN_VALID_NUMBER - 1, MAX_VALID_NUMBER + 1)
    assert ex_info.value.number == MIN_VALID_NUMBER - 1

    with pytest.raises(InvalidNumberError) as ex_info:
        dcs.between(MIN_VALID_NUMBER - 1, MAX_VALID_NUMBER)
    assert ex_info.value.number == MIN_VALID_NUMBER - 1

    with pytest.raises(InvalidNumberError) as ex_info:
        dcs.between(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1)
    assert ex_info.value.number == MAX_VALID_NUMBER + 1

    with pytest.raises(NoCapturedNumbersRangeError) as ex_info:
        dcs.between(min_added, MAX_VALID_NUMBER)
    assert ex_info.value.lower_number == min_added
    assert ex_info.value.higher_number == MAX_VALID_NUMBER

    with pytest.raises(NoCapturedNumbersRangeError) as ex_info:
        dcs.between(MIN_VALID_NUMBER, max_added)
    assert ex_info.value.lower_number == MIN_VALID_NUMBER
    assert ex_info.value.higher_number == max_added
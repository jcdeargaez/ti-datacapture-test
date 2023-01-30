import math
from typing import Tuple, Dict

from hypothesis import given
import pytest

from core.domain import (
    MIN_VALID_NUMBER,
    MAX_VALID_NUMBER,
    InvalidBetweenRangeError,
    InvalidNumberError,
)
from ooapi.data_capture_stats import DataCaptureStats
from tests.util import stats, invalid_number


@given(stats())
def test_less_than_query(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    acc_lessers = 0
    for number in range(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1):
        assert dcs.less(number) == acc_lessers
        acc_lessers += added.get(number, 0)


@given(invalid_number(), stats())
def test_less_than_query_errors(number: int, numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    _, dcs = numbers_stats
    with pytest.raises(InvalidNumberError) as ex_info:
        dcs.less(number)
    assert ex_info.value.number == number


@given(stats())
def test_greater_query(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    acc_greaters = sum(added.values())
    for number in range(MIN_VALID_NUMBER, MAX_VALID_NUMBER + 1):
        acc_greaters -= added.get(number, 0)
        assert dcs.greater(number) == acc_greaters


@given(invalid_number(), stats())
def test_greater_query_errors(number: int, numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    _, dcs = numbers_stats
    with pytest.raises(InvalidNumberError) as ex_info:
        dcs.greater(number)
    assert ex_info.value.number == number


@given(stats())
def test_between_query(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    added, dcs = numbers_stats
    total_frequency = sum(added.values())
    for ln, hn in ((i, MAX_VALID_NUMBER - i) for i in range(MIN_VALID_NUMBER, math.ceil(MAX_VALID_NUMBER / 2))):
        assert dcs.less(ln) + dcs.between(ln, hn) + dcs.greater(hn) == total_frequency


@given(stats())
def test_between_query_errors(numbers_stats: Tuple[Dict[int, int], DataCaptureStats]) -> None:
    _, dcs = numbers_stats
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

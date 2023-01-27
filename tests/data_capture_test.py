from typing import List

from hypothesis import given
from hypothesis.strategies import integers, lists
import pytest

from core.domain import (
    MIN_VALID_NUMBER,
    MAX_VALID_NUMBER,
    DataCapture,
    InvalidNumberError,
    NoCapturedNumbersError,
)
from ooapi.data_capture import DataCapture
from tests.util import invalid_number


@given(invalid_number())
def test_add_invalid_number_raises_error(number: int) -> None:
    dc = DataCapture()
    with pytest.raises(InvalidNumberError) as ex_info:
        dc.add(number)
    assert ex_info.value.number == number


def test_build_empty_stats_raises_error() -> None:
    dc = DataCapture()
    with pytest.raises(NoCapturedNumbersError):
        dc.build_stats()


@given(lists(integers(min_value=MIN_VALID_NUMBER, max_value=MAX_VALID_NUMBER), min_size=1, max_size=100))
def test_build_stats_after_adding_numbers(numbers: List[int]) -> None:
    dc = DataCapture()
    for n in numbers:
        dc.add(n)
    assert dc.build_stats() is not None

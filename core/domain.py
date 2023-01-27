from dataclasses import dataclass

from expression.collections import Map

MIN_VALID_NUMBER = 0
MAX_VALID_NUMBER = 999


@dataclass(frozen=True)
class ValidNumber:
    """Valid numbers are in the range [MIN_VALID_NUMBER, MAX_VALID_NUMBER]"""
    value: int

    def __post_init__(self):
        """Validates that the number is in the valid range, otherwise raises error"""
        if self.value < MIN_VALID_NUMBER or self.value > MAX_VALID_NUMBER:
            raise InvalidNumberError(self.value)


@dataclass(frozen=True)
class CapturedNumber:
    """Holds the value for a captured number"""
    value: int


@dataclass(frozen=True)
class CapturedNumberFrequency:
    """Captured numbers can repeat, so a frequency is needed"""
    frequency: int

    def __post_init__(self):
        """Validates that a frequency is positive, otherwise raises error"""
        if self.frequency <= 0:
            raise Exception(f'Invalid frequency [{self.frequency}]')


@dataclass(frozen=True)
class EmptyDataCapture:
    """Represents a new data capture object without captured numbers yet"""
    pass


@dataclass(frozen=True)
class ActiveDataCapture:
    """Represents an active data capture object with captured numbers"""
    captured_numbers: Map[CapturedNumber, CapturedNumberFrequency]
    total_captured_numbers: CapturedNumberFrequency


DataCapture = EmptyDataCapture | ActiveDataCapture


@dataclass(frozen=True)
class CapturedNumberStats(CapturedNumberFrequency):
    """When stats are computed, we need to know how many numbers are lesser and greater relative to a captured number"""
    lesser: int
    greater: int

    def __post_init__(self):
        """Validates that stats are positive, otherwise raises error"""
        super().__post_init__()
        if self.lesser < 0 or self.greater < 0:
            raise Exception(f'Invalid stats lesser [{self.lesser}] greater [{self.greater}]')


@dataclass(frozen=True)
class DataCaptureStats:
    """Holds the computed stats of captured numbers"""
    stats: Map[CapturedNumber, CapturedNumberStats]

    def __post_init__(self):
        """Validates that stats are not empty"""
        if self.stats.is_empty():
            raise NoCapturedNumbersError()


@dataclass(frozen=True)
class InvalidNumberError(Exception):
    """Raised when an invalid number is found"""
    number: int


@dataclass(frozen=True)
class NoCapturedNumbersError(Exception):
    """Raised when attempting to build stats before capturing numbers"""
    pass


@dataclass(frozen=True)
class NoCapturedNumberError(Exception):
    """Raised when a number was not captured"""
    number: int


@dataclass(frozen=True)
class InvalidBetweenRangeError(Exception):
    """Raised when a between range is invalid"""
    lower_number: int
    higher_number: int


@dataclass(frozen=True)
class NoCapturedNumbersRangeError(Exception):
    """Raised when one or both numbers were not captured"""
    lower_number: int
    higher_number: int
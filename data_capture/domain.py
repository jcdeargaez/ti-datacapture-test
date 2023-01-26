from dataclasses import dataclass

MIN_VALID_NUMBER = 0
MAX_VALID_NUMBER = 999


@dataclass(frozen=True)
class CapturedNumber:
    """Captured numbers are in the range [0, 1000)"""
    value: int

    def __post_init__(self):
        """Validates that the captured number is in the valid range, otherwise raises error"""
        if self.value < MIN_VALID_NUMBER or self.value > MAX_VALID_NUMBER:
            raise InvalidNumberError(self.value)


@dataclass(frozen=True)
class CapturedNumberFrequency:
    """Captured numbers can repeat, so a frequency is needed"""
    number: CapturedNumber
    frequency: int

    def __post_init__(self):
        """Validates that a frequency is positive, otherwise raises error"""
        if self.frequency < 0:
            raise InvalidFrequencyError(self.frequency)


@dataclass(frozen=True)
class CapturedNumberStats(CapturedNumberFrequency):
    """When stats are computed, we need to know how many numbers are greater and lesser relative to the current value"""
    greater: int
    lesser: int


@dataclass(frozen=True)
class InvalidNumberError(Exception):
    """Raised when an invalid number is found"""
    number: int


@dataclass(frozen=True)
class InvalidFrequencyError(Exception):
    """Raised when a frequency is negative"""
    frequency: int


@dataclass(frozen=True)
class NoCapturedNumbersError(Exception):
    """Raised when attempting to build stats before capturing numbers"""
    pass


@dataclass(frozen=True)
class NoCapturedNumberError(Exception):
    """Raised when a number was not captured and is not found"""
    number: int


@dataclass(frozen=True)
class InvalidBetweenRangeError(Exception):
    """Raised when a between range is invalid"""
    lower_number: int
    higher_number: int

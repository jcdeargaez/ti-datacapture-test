from dataclasses import dataclass


@dataclass(frozen=True)
class NoCapturedNumbersError(Exception):
    """Raised when attempting to build stats before capturing numbers"""
    pass

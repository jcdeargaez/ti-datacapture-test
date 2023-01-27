import core.data_capture
from core.domain import (
    ActiveDataCapture,
    EmptyDataCapture,
    ValidNumber,
    NoCapturedNumbersError,
)
from ooapi.data_capture_stats import DataCaptureStats


class DataCapture:
    """Captures numbers and builds stats."""
    def __init__(self):
        """Instantiates an empty data capturer."""
        self.dc: core.domain.DataCapture = EmptyDataCapture()

    def add(self, number: int) -> None:
        """
        Captures a number and increments its frequency.
        :param number: Number to capture.
        :raise: if number is invalid.
        """
        self.dc = core.data_capture.add(self.dc, ValidNumber(number))

    def build_stats(self) -> DataCaptureStats:
        """
        Builds a stats object to serve queries.
        :return: CaptureDataStats instance if at least one numbers was captured.
        :raise: if no numbers were captured.
        """
        match self.dc:
            case EmptyDataCapture():
                raise NoCapturedNumbersError()
            case ActiveDataCapture() as adc:
                dcs = core.data_capture.build_stats(adc)
                return DataCaptureStats(dcs)

from expression import Result, Ok, Error

from data_capture.domain import CapturedNumber, InvalidNumberError


def create(number: int) -> Result[CapturedNumber, InvalidNumberError]:
    """
    Returns a captured number result if the input number is valid, otherwise returns error.
    :param number: Input number to validate as captured.
    :return: Ok result with CapturedNumber instance if validated, otherwise Error.
    """
    try:
        return Ok(CapturedNumber(number))
    except InvalidNumberError as ex:
        return Error(ex)

from typing import TypeVar, Callable, Any, Tuple

from expression import Result, Ok, Error


A = TypeVar('A')


def return_ok_value_or_raise(func: Callable[[..., Any], Result[A, Error]]) -> Callable[[..., Any], A]:
    """Decorator for Results to return unwrapped Ok value or raise Error."""
    def inner(*args, **kwargs) -> A:
        """Returns the result value if ok.
        :return: Unwrapped value for the given result.
        :raise: If result is error.
        """
        match func(*args, **kwargs):
            case Ok(value):
                return value

            case Error(err):
                raise err

    return inner


def fst(t: Tuple[..., Any]) -> Any:
    """
    Returns the first item in a tuple.
    :param t: Tuple to extract the first item.
    :return: First item in the tuple.
    """
    return t[0]

import typing as _t
from capyutils.exceptions import UnwrappedException

_T = _t.TypeVar("_T")


class Result(_t.Generic[_T]):
    """
    Util class to wrap around fallible values instead of raising Exceptions.
    """

    def __init__(self, value: _t.Union[_T, Exception]):
        self._value = value

    def __bool__(self) -> bool:
        return not self.is_err()

    def __str__(self) -> str:
        return f"{'Ok' if self.is_ok() else 'Err'}({self._value})"

    def is_ok(self) -> bool:
        """
        Returns `True` if this `Result` is of the `Ok` type
        """
        return bool(self)

    def is_err(self) -> bool:
        """
        Returns `True` if this `Result` is of the `Err` type
        """
        return isinstance(self._value, Exception)

    def unwrap(self) -> _T:
        """
        Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, then raises the UnwrappedException, instead.
        """
        if isinstance(self._value, Exception):
            raise UnwrappedException() from self._value
        else:
            return self._value

    def try_unwrap(self) -> _t.Union[_T, None]:
        """
        Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, returns `None`.
        """
        if not isinstance(self._value, Exception):
            return self._value
        else:
            return None

    def unwrap_err(self) -> Exception:
        """
        Returns the wrapped exception if this `Result` is `Err`, else, if this
        `Result` is `Ok`, then raises a `UnwrapedException`.
        """
        if isinstance(self._value, Exception):
            return self._value
        else:
            raise TypeError("Can't unwrap error type in instance of Ok result.")

    @staticmethod
    def from_call(callback: _t.Callable[[], _T]) -> "Result[_T]":
        try:
            return Ok(callback())
        except Exception as e:
            return Err(e)


@_t.overload
def Err(error: _t.Union[Exception, str], type: _t.Type[_T]) -> "Result[_T]": ...


@_t.overload
def Err(error: _t.Union[Exception, str]) -> "Result[_t.Any]": ...


def Err(
    error: _t.Union[Exception, str], type: _t.Union[None, _t.Type[_T]] = None
) -> "Result[_t.Any]":
    """
    Instantiate Error Result which wraps around exception. If `error` is a
    string, will instantiate an `Exception` with `error` as error message.

    If the wrapped type is important for type checkers, provide "type" parameter
    for the desired type.
    """
    if isinstance(error, str):
        error = Exception(error)

    return Result(error)


def Ok(value: _T) -> "Result[_T]":
    """
    Instantiate Ok Result which wraps around a `value` (use `None` if value
    is irrelevant)

    Explictly provide the type (e.g. `Result[str].Ok("A string.")`) to let
    type checkers know the type of the wrapped value
    """
    return Result(value)

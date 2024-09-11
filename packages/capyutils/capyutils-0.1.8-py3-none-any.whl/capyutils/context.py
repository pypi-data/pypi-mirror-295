import abc as _abc
import typing as _t

_T = _t.TypeVar("_T")


class ContextManager(_t.ContextManager[_T]):
    """
    Abstract class that implements dunder methods `__enter__` and `__exit__` for
    subclasses to be compatible with Python context manager semantics (`with
    ContextManagerSubclass() as val: ...`). This abstract class has a failsafe
    mechanism which calls `exit` if `enter` raises an exception, which Python
    does not do by default.
    """

    @_abc.abstractmethod
    def context_enter(self) -> _T:
        """
        Setup context manager class by allocating resources etc.

        Returns
        -------
        T
            Context manager handle, whatever it may be
        """

    @_abc.abstractmethod
    def context_exit(self, exception: _t.Optional[BaseException]) -> None:
        """
        Cleanup context manager class by releasing resources etc.

        Parameters
        ----------
        exception : Optional[BaseException]
            whatever exception may occur on enter or within `with` body. If no
            exceptions occur, this will be `None`
        """

    @_t.final
    def __enter__(self) -> _T:
        """Cannot override, override `context_enter()` instead"""
        try:
            return self.context_enter()
        except BaseException as e:
            self.__exit__(
                exception_instance=e, exception_class=None, exception_traceback=None
            )
            raise

    @_t.final
    def __exit__(
        self,
        exception_class: _t.Any,
        exception_instance: _t.Optional[BaseException],
        exception_traceback: _t.Any,
    ) -> None:
        """Cannot override, override `context_exit()` instead"""
        self.context_exit(exception_instance)

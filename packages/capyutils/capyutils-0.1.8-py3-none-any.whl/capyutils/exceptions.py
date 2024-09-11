class UnwrappedException(Exception):
    """
    Raised when unwrapping a `Result` as `Err` when it is `Ok` or vice-versa
    """

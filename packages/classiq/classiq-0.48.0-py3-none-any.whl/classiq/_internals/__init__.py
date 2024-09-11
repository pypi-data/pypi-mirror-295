import sys
import warnings

from classiq.interface.exceptions import ClassiqDeprecationWarning


def _check_python_version() -> None:
    if sys.version_info >= (3, 9):
        return
    warnings.warn(  # type: ignore[unreachable]
        "Python version 3.8 is expected to reach its end-of-life on October 2024.\n"
        "See https://devguide.python.org/versions/#supported-versions\n"
        "The Classiq SDK is expected to drop support for 3.8 around the same time.\n"
        "Please upgrade to a newer version of Python to avoid issues in the future.",
        ClassiqDeprecationWarning,
        stacklevel=2,
    )


_check_python_version()

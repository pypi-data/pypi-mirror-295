import sys
from collections.abc import Callable
from functools import wraps

from rich import print
from whenever import Instant


def now():
    return Instant.now()


def now_as_date():
    return now().py_datetime().date()


def capture(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except OSError as exc:
            print(f"[red]{exc.strerror} on {exc.filename or exc.filename2}")
            sys.exit(exc.errno)
        except ValueError as exc:
            print(f"[red]{exc}")
            sys.exit(1)
        except Exception as exc:  # noqa: BLE001
            print(f"[bold red] Unexpected error: {exc}")
            sys.exit(2)

    return wrapper

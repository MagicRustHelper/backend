from typing import Any


def exclude_exception(array: list[Any]) -> list[Any]:
    exceptions_find = lambda x: isinstance(x, Exception)
    filter_func = lambda x: not isinstance(x, Exception)
    exceptions = list(filter(exceptions_find, array))
    for exc in exceptions:
        print(exc)
    return list(filter(filter_func, array))

from typing import TypeVar, Callable, ParamSpec

FParam = ParamSpec('FParam')
FReturn = TypeVar('FReturn')
OriginalFunction = Callable[[FParam], FReturn]
RT = TypeVar('RT')


def sync(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

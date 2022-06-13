from functools import wraps
from typing import Type, Callable, Generic, TypeVar, get_args, Any


def _generic(t: type = Any) -> Callable[[object], object]:
    def decorator(f: object) -> object:
        _T = TypeVar('_T')

        @wraps(f, updated=())
        class F(f, Generic[_T]):

            def __class_getitem__(cls, item: Type[t]) -> _T:
                if t != Any and not issubclass(item, t):
                    raise TypeError(f"{item} is not a subclass of {t}")
                # noinspection PyUnresolvedReferences
                return super().__class_getitem__(item)

            @property
            def T(self) -> Type[_T]:
                try:
                    # noinspection PyUnresolvedReferences
                    return get_args(self.__orig_class__)[0]
                except Exception:
                    return Any
        return F
    return decorator
from __future__ import annotations

from types import UnionType

# noinspection PyUnresolvedReferences
from typing import Generic as TypingGeneric
from typing import TypeVar, _UnionGenericAlias, get_args

_T = TypeVar("_T")


class Generic(TypingGeneric[_T]):
    _T: type

    def __class_getitem__(cls, item: type):
        cls._T = item
        return super().__class_getitem__(item)

    # noinspection PyPep8Naming
    @classmethod
    def T(cls) -> type:
        return None if isinstance(cls._T, TypeVar) else cls._T


def is_union(ty: type) -> bool:
    return isinstance(ty, (_UnionGenericAlias, UnionType))

from __future__ import annotations

from abc import ABC
from copy import copy
from functools import singledispatch
from typing import Self

from pymcfunc.data_formats.nbt_tags import NBT
from pymcfunc.internal import base_class, _generic


@base_class
@_generic(NBT)
class Path:
    def __init__(self, root: str | None = None): # TODO maybe a source parameter for direct resolution?
        self._components = [f"\"{root}\"" if ' ' in root else (root or "")]

    def __str__(self):
        return "".join(self._components)

    def parent(self) -> Path:
        path = copy(self)
        path._components.pop()
        return path

    def copy(self) -> Self:
        return copy(self)

    def __getattr__(self, attr: str) -> NamedTag:
        tag = NamedTag("."+attr)
        tag._components = self._components + tag._components
        return tag

class RootCompoundTag(Path):
    def __init__(self, root: dict[str, NBT] | None = None):
        super().__init__(str(root) or "{}") # TODO proper parsing of dicts

class NamedTag(Path):
    def __init__(self, root: str):
        super().__init__(root)

    def __call__(self, item: dict[str, NBT] | None = None) -> NamedCompoundTag:
        tag = NamedCompoundTag("")
        tag._components = self._components + [str(item)]
        return tag

    @singledispatch
    def __getitem__(self, item):
        raise NotImplementedError

    @__getitem__.register
    def __getitem__(self, item: int) -> NamedListTag:
        tag = NamedListTag("", "")
        tag._components = self._components + ["["+str(item)+"]"]
        return tag
    @__getitem__.register
    def __getitem__(self, item: Ellipsis) -> NamedListTag:
        tag = NamedListTag("", "")
        tag._components = self._components + ["[]"]
        return tag
    @__getitem__.register
    def __getitem__(self, item: dict) -> NamedCompoundTag:
        tag = NamedCompoundTag("")
        tag._components = self._components + ["["+str(item)+"]"]
        return tag
    @__getitem__.register
    def __getitem__(self, item: str) -> NamedTag:
        return self.__getattr__(item)

class NamedCompoundTag(NamedTag, ABC):
    # noinspection PyMissingConstructor
    def __init__(self, root: str, item: dict[str, NBT] | None = None):
        self._components = NamedTag(root)(item)._components

class NamedListTag(NamedTag, ABC):
    # noinspection PyMissingConstructor
    def __init__(self, root: str, item: int | Ellipsis):
        self._components = NamedTag(root)[item]._components
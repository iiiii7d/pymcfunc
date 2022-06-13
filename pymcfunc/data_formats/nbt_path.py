from __future__ import annotations

from copy import copy
from typing import Self

from pymcfunc.data_formats.nbt_tags import NBT


class Path:
    def __init__(self, root: str | None = None):
        self._components = [f"\"{root}\"" if ' ' in root else (root or "")]

    def __str__(self):
        return "".join(self._components)

    def parent(self) -> Path:
        path = copy(self)
        path._components.pop()
        return path

    def copy(self) -> Self:
        return copy(self)

    def __getattr__(self, attr: str):
        tag = NamedTag(attr)
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

    def __getitem__(self, item: int | Ellipsis | dict) -> NamedListTag: # TODO overloading
        if item is ...:
            tag = NamedListTag("")
            tag._components = self._components + ["[]"]
        elif isinstance(item, dict):
            tag = NamedCompoundTag("")
            tag._components = self._components + ["["+str(item)+"]"]
        else:
            tag = NamedListTag("")
            tag._components = self._components + ["["+str(item)+"]"]
        return tag

class NamedCompoundTag(NamedTag):
    def __init__(self, root: str, item: dict[str, NBT] | None = None):
        self._components = NamedTag(root)(item)._components

class NamedListTag(NamedTag):
    def __init__(self, root: str, item: int | Ellipsis):
        self._components = NamedTag(root)[item]._components

class NamedListCompoundElementsTag(NamedTag):
    def __init__(self, root: str, item: dict | None):
        self._components = NamedTag(root)[item]._components
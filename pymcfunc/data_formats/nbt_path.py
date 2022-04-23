from __future__ import annotations

import re
from abc import ABC
from copy import copy
from functools import singledispatchmethod
# noinspection PyUnresolvedReferences
from typing import _LiteralGenericAlias, Any, _UnionGenericAlias, get_args, get_origin, _GenericAlias, Type, TypeVar, \
    Generic, TYPE_CHECKING

from typing_extensions import Self

from pymcfunc import JavaFunctionHandler, ExecutedCommand
from pymcfunc.data_formats.base_formats import NBTFormat
from pymcfunc.data_formats.coord import BlockCoord
from pymcfunc.data_formats.nbt_tags import Compound, NBT, List, Int, Short, Long, Float, \
    Double, Byte, String, IntArray, LongArray, ByteArray, Boolean, CompoundReprAsList
from pymcfunc.data_formats.raw_json import JavaTextComponent
if TYPE_CHECKING: from pymcfunc.data_formats.raw_json import JNBTValues
from pymcfunc.proxies.selectors import JavaSelector


class Path:
    def __init__(self, root: str | None = None,
                 fh: JavaFunctionHandler | None = None,
                 sel: JavaSelector | None = None,
                 block_pos: BlockCoord | None = None,
                 rl: str | None = None):
        self._components = [root or ""]
        self.fh = fh
        self.sel = sel
        self.block_pos = block_pos
        self.rl = rl

    def __class_getitem__(cls, item: Type[NBT] | Ellipsis) -> Type[Path]:
        if isinstance(item, TypedCompoundPath):
            return TypedCompoundPath
        elif isinstance(item, NBTFormat):
            return item._path()
        elif isinstance(item, _UnionGenericAlias):
            for anno in get_args(item):
                if issubclass(anno, NBT): return cls[anno]
            else:
                raise TypeError(f"{item} is not a valid NBT Path type")
        elif get_origin(item) == List:
            return ListPath[get_args(item)[0]]
        elif get_origin(item) == Compound or get_origin(item) == CompoundReprAsList:
            return CompoundPath[get_args(item)[0]]
        elif item == Byte:
            return BytePath
        elif item == Short:
            return ShortPath
        elif item == Int:
            return IntPath
        elif item == Long:
            return LongPath
        elif item == Float:
            return FloatPath
        elif item == Double:
            return DoublePath
        elif item == ByteArray:
            return ByteArrayPath
        elif item == String:
            return StringPath
        elif item == IntArray:
            return IntArrayPath
        elif item == LongArray:
            return LongArrayPath
        elif item == Boolean:
            return BooleanPath
        elif item is ...:
            return Collection

    def __str__(self) -> str:
        return "".join(self._components)

    def parent(self) -> Path:
        path = copy(self)
        path._components.pop()
        return path

    def copy(self) -> Self:
        return copy(self)

    @property
    def _target(self):
        return {'entity': self.sel} if self.sel \
            else {'block': self.block_pos} if self.block_pos \
            else {'storage': self.rl} if self.rl \
            else {}

    @property
    def _target_with_prefix_target(self):
        return {'target_entity': self.sel} if self.sel \
            else {'target_block': self.block_pos} if self.block_pos \
            else {'target_storage': self.rl} if self.rl \
            else {}

    @property
    def _target_with_prefix_source(self):
        return {'source_entity': self.sel} if self.sel \
            else {'source_block': self.block_pos} if self.block_pos \
            else {'source_storage': self.rl} if self.rl \
            else {}

    def raw_json(self, interpret: bool | None = None,
                 separator: JavaTextComponent | None = None) -> JNBTValues:
        from pymcfunc.data_formats.raw_json import JNBTValues
        # noinspection PyArgumentList
        return JNBTValues(nbt=self,
                          entity=self.sel,
                          interpret=interpret,
                          separator=separator)

    def get(self, scale: float | None = None) -> ExecutedCommand:
        return self.fh.r.data_get(**self._target,
                                  path=self._components,
                                  scale=scale)

    def append(self, *,
               value: _T | None = None,
               from_: TypedCompoundPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='append',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def insert(self, index: int, *,
               value: _T | None = None,
               from_: TypedCompoundPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='insert', index=index,
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def merge(self, *,
              value: _T | None = None,
              from_: TypedCompoundPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='merge',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def prepend(self, *,
                value: _T | None = None,
                from_: TypedCompoundPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='prepend',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def set(self, *,
            value: _T | None = None,
            from_: TypedCompoundPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='set',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def remove(self):
        return self.fh.r.data_remove(entity=self.sel, path=self)

    # TODO type checking for data modify
    # TODO change value into NBTTag

_T = TypeVar('_T')
class ListPath(Path, Generic[_T]):
    @property
    def T(self) -> Type[_T]:
        try:
            # noinspection PyUnresolvedReferences
            return get_args(self.__orig_class__)[0]
        except Exception:
            return Any

    @singledispatchmethod
    def __getitem__(self, index: int | Ellipsis) -> Path[_T]:
        raise NotImplementedError
    @__getitem__.register
    def _(self, index: int) -> Path[_T]:
        path = Path[self.T](None, self.fh, self.sel, self.block_pos, self.rl)
        path._components = self._components.copy()
        path._components.append("["+str(index)+"]")
        return path
    @__getitem__.register
    def _(self, _: Ellipsis) -> Path[...][_T]:
        path = Path[self.T](None, self.fh, self.sel, self.block_pos, self.rl)
        path._components = self._components.copy()
        path._components.append("[]")
        return path
    @__getitem__.register
    def _(self, index: Compound) -> Path[...][_T]:
        path = Path[self.T](None, self.fh, self.sel, self.block_pos, self.rl)
        path._components = self._components.copy()
        path._components.append("[" + str(index) + "]")
        return path

    def __setitem__(self, index: int, value: _T | None = None):
        self[index].set(value=value)

    def __delitem__(self, index: int):
        self[index].remove()

class Collection(ListPath, Generic[_T], ABC):
    pass # TODO collection class for every type

class CompoundPath(Path, Generic[_T]):
    @property
    def T(self) -> Type[_T]:
        # noinspection PyUnresolvedReferences
        try:
            return get_args(self.__orig_class__)[0]
        except Exception:
            return Any

    def __getattr__(self, attr: str) -> Path[_T]:
        if attr == '_components': return super().__getattribute__(attr)
        str_attr = attr if re.search(r"^[a-zA-Z\d]*$", attr) is not None else "\""+attr+"\""
        path = Path[self.T]()
        path._components = self._components.copy()
        self._components.append("."+str_attr)
        return path
    __getitem__ = __getattr__

    def __call__(self, tag: Compound) -> ListPath[Compound]:
        path = ListPath[Compound]()
        path._components.append(str(tag))
        return path

class BytePath(Path):
    pass

class ShortPath(Path):
    pass

class IntPath(Path):
    pass

class LongPath(Path):
    pass

class FloatPath(Path):
    pass

class DoublePath(Path):
    pass

class ByteArrayPath(Path):
    pass

class StringPath(Path):
    pass

class IntArrayPath(Path):
    pass

class LongArrayPath(Path):
    pass

class BooleanPath(Path):
    pass


class TypedCompoundPath(CompoundPath, Generic[_T]):
    @property
    def T(self) -> Type[NBTFormat]:
        # noinspection PyUnresolvedReferences
        return get_args(self.__orig_class__)[0]

    @property
    def proxy(self) -> NBTFormat.Proxy:
        return self.T.Proxy(self)
    px = proxy

    def __getattr__(self, item) -> Path:
        if item not in self.T.get_format():
            return object.__getattribute__(self, item)
        else:
            return super().__getattr__(item)

    def __setattr__(self, item, value):
        if item not in self.T.get_format():
            return object.__setattr__(self, item, value)
        else:
            return super().__setattr__(item, value)

    def __delattr__(self, item):
        if item not in self.T.get_format():
            return object.__delattr__(self, item)
        else:
            return super().__delattr__(item)
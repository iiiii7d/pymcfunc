from __future__ import annotations

import functools
import json
import re
from abc import ABC
from collections.abc import MutableSequence, Sequence
# noinspection PyUnresolvedReferences
from types import UnionType, GenericAlias
# noinspection PyUnresolvedReferences
from typing import Any, get_args, Type, TypeVar, Generic, _UnionGenericAlias, Union, get_origin, _LiteralGenericAlias, \
    _GenericAlias

from typing_extensions import Self


class Path:
    def __init__(self, root: str | None = None):
        self._components = [root or "{}"]

    def __str__(self) -> str:
        return "".join(self._components)

    def __getattr__(self, attr: str) -> Self:
        str_attr = attr if re.search(r"^[a-zA-Z\d]*$", attr) is not None else "\""+attr+"\""
        self._components.append("."+str_attr)
        return self

    def __getitem__(self, index: int | Ellipsis | NBTTag) -> Self:
        str_index = str(int) if isinstance(index, (str, NBTTag)) else ""
        self._components.append("["+str(str_index)+"]")
        return self

    def __call__(self, tag: Compound) -> Self:
        self._components.append(str(tag))
        return self

    def parent(self) -> Path:
        obj = Path()
        obj._components = self._components[:-1]
        return obj

def _numerical(min_: str | float, max_: str | float, type_: type, suffix: str=""):
    def decorator(cls):
        @functools.wraps(cls, updated=())
        class NumericalNBT(cls, type_):
            val_type = type_
            min = min_
            max = max_

            def __init__(self, val: type_):
                if not (min_ <= val <= max_):
                    raise ValueError(f"Value must be between {min_} and {max_}")
                elif not isinstance(val, self.val_type):
                    raise TypeError(f"Value must be a(n) {self.val_type.__name__} (Got {val})")
                NBTTag.__init__(self, val)

            def __str__(self):
                return str(self._val) + suffix

            @property
            def py(self) -> val_type:
                return self._val
        return NumericalNBT
    return decorator

def _sequential(type_: type, prefix: str=""):
    if prefix != "": prefix += ";"

    def decorator(cls):
        @functools.wraps(cls, updated=())
        class SequentialNBT(MutableSequence, cls, ABC, list):
            val_type = list
            content_type: type

            # noinspection PyMissingConstructor
            def __init__(self, val: Sequence[content_type], nbt_type: type=NBTTag):
                self.content_type = type_
                val = [nbt_type(v) for v in val]
                if len(val) >= 1:
                    if self.content_type != Any and not isinstance(val[0], self.content_type):
                        raise TypeError(f"Value must be of type {self.content_type.__name__} (Got {val[0]})")
                    if self.content_type == Any: self.content_type = type(val[0])
                    for v in val:
                        if not isinstance(v, type(val[0])):
                            raise TypeError(f"value must be of type {type(val[0]).__name__} (Got {v})")

                self._val = val
                self.__setattr__ = _immutable_lock

            def __str__(self):
                return "[" + prefix + ",".join(str(v) for v in self._val) + "]"

            def __iter__(self):
                for v in self._val: yield v

            def __len__(self):
                return len(self._val)

            def __getitem__(self, index: int) -> content_type:
                return self._val[index]

            def __setitem__(self, index: int, val: content_type):
                val = NBTTag(val) if not issubclass(type(val), NBTTag) else val
                if not isinstance(val, self.content_type):
                    raise TypeError(f"value must be of type {self.content_type.__name__} (Got {val})")
                self._val[index] = val

            def __delitem__(self, index: int):
                del self._val[index]

            def __contains__(self, item: content_type) -> bool:
                return item in self._val

            def insert(self, index: int, val: content_type):
                if not isinstance(val, self.content_type):
                    raise TypeError(f"value must be of type {self.content_type.__name__} (Got {val})")
                self._val.insert(index, val)

            @property
            def py(self) -> list[content_type]:
                return [i.py for i in self._val]

        return SequentialNBT
    return decorator

def _immutable_lock(*_):
    raise AttributeError("Value is immutable")


class NBT:
    @property
    def py(self) -> Any: return None

class NBTTag(NBT):
    val_type: type
    def __new__(cls, val: val_type):
        if cls != NBTTag: return super().__new__(cls)
        if isinstance(val, bool):
            return Boolean.__new__(Boolean, val)
        elif isinstance(val, int):
            if Int.min <= val <= Int.max:
                # noinspection PyArgumentList
                return Int.__new__(Int, val)
            else:
                # noinspection PyArgumentList
                return Long.__new__(Long, val)
        elif isinstance(val, float):
            # noinspection PyArgumentList
            return Double.__new__(Double, val)
        elif isinstance(val, list):
            # noinspection PyArgumentList
            return List.__new__(List, val)
        elif isinstance(val, dict):
            return Compound.__new__(Compound, val)
        elif isinstance(val, str) or hasattr(val, '__str__'):
            return String.__new__(String, str(val))
        raise TypeError(f"Type {type(val).__name__} not supported as NBTTag value (Got {val})")

    def __init__(self, val: val_type):
        if not isinstance(val, self.val_type):
            raise TypeError(f"value must be of type {self.val_type.__name__} (Got {val})")
        self._val = val

        self.__setattr__ = _immutable_lock

    def __repr__(self):
        return type(self).__name__+"("+str(self)+")"

    @property
    def py(self) -> val_type:
        return self._val

@_numerical(-128, 127, int, "b")
class Byte(NBTTag): pass

@_numerical(-32768, 32767, int, "s")
class Short(NBTTag): pass

@_numerical(-2_147_483_648, 2_147_483_647, int)
class Int(NBTTag): pass

@_numerical(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807, int, "L")
class Long(NBTTag): pass

@_numerical(-3.4e38, 3.4e38, float, "f")
class Float(NBTTag): pass

@_numerical(-1.7e308, 1.7e308, float)
class Double(NBTTag): pass

class String(NBTTag, str):
    val_type = str
    def __str__(self):
        return json.dumps(self._val)

_T = TypeVar('_T')
@_sequential(_T)
class List(NBTTag, Generic[_T]): pass

@_sequential(Byte, "B")
class ByteArray(NBTTag): pass

@_sequential(Int, "I")
class IntArray(NBTTag): pass

@_sequential(Long, "L")
class LongArray(NBTTag): pass

class Boolean(NBTTag):
    val_type = bool
    def __str__(self):
        return "true" if self._val else "false"

    @property
    def py(self) -> val_type:
        # noinspection PyTypeChecker
        return self._val

class Compound(NBTTag, dict):
    val_type = dict

    # noinspection PyMissingConstructor
    def __init__(self, val: dict[str, Any]):
        self._val = {str(k): (v if isinstance(v, NBTTag)
                              else v.as_nbt() if isinstance(v, NBTFormat)
                              else NBTTag(v)) for k, v in val.items()}

        def _immutable_lock2(self2, key: str, value: Any):
            value = NBTTag(value) if not issubclass(type(value), NBTTag) else value
            if key == "_val": _immutable_lock()
            self2._val[key] = value

        self.__setitem__ = self.__setattr__ = _immutable_lock2

    def __iter__(self):
        for i in self._val: yield i

    def __getattr__(self, item: str) -> Any:
        return self._val[item]
    __getitem__ = __getattr__

    def __delattr__(self, key: str):
        if key == "_val": _immutable_lock()
        del self._val[key]
    __delitem__ = __delattr__

    def __contains__(self, item: str) -> bool:
        return item in self._val

    def __len__(self) -> int:
        return len(self._val)

    def keys(self):
        return self._val.keys()

    def values(self):
        return self._val.values()

    def items(self):
        return self._val.items()

    def __str__(self) -> str:
        return "{"+",".join(k+": "+str(v) for k, v in self.items())+"}"

    @property
    def py(self) -> dict[str, Any]:
        return {k: v.py for k, v in self._val}

_I = TypeVar('_I')
class DictReprAsList(Generic[_I]): pass

class NBTFormat(NBT):
    @property
    def py(self) -> dict:
        d = {}
        for var, anno in type(self).__annotations__.items():
            if var not in self.NBT_FORMAT: continue
            if anno == DictReprAsList:
                d[var] = [v.as_json() for v in getattr(self, var)]
            else:
                if isinstance(getattr(self, var), NBT):
                    d[var] = getattr(self, var).py
                elif isinstance(getattr(self, var), list):
                    d[var] = [v.py for v in getattr(self, var)]
                elif isinstance(getattr(self, var), dict):
                    d[var] = {k: v.py for k, v in getattr(self, var).items()}
                else:
                    d[var] = getattr(self, var)
        return d

    def _convert_to_nbt(self, name: str,
                        val: Any,
                        py_type: type,
                        format_type: Type[NBT]) -> NBT | None:
        if not isinstance(val, py_type):
            raise TypeError(f"`{name}` must be of {py_type} (got {val})")
        if issubclass(format_type, NBTFormat) and isinstance(val, format_type):
            return val.as_nbt()
        elif issubclass(format_type, NBT) and isinstance(val, format_type):
            return val
        elif isinstance(format_type, _LiteralGenericAlias):
            if val not in get_args(format_type):
                raise ValueError(f"{val} is not in {get_args(format_type)}")
            return String(val)
        elif isinstance(format_type, _UnionGenericAlias):
            if type(None) in get_args(format_type) and val is None: return None
            for format_subtype in get_args(format_type):
                try:
                    return self._convert_to_nbt(name, val, py_type, format_subtype)
                except Exception:
                    pass
            else:
                raise TypeError(
                    f"`{name}` is not one of types {', '.join(str(a) for a in get_args(format_type))} (got {val})")
        elif isinstance(format_type, _GenericAlias):
            if isinstance(get_origin(format_type), DictReprAsList):
                val: list
                ft = get_origin(format_type)
                pt = get_origin(py_type)[0]
                return Compound({v.name: self._convert_to_nbt(name, v, pt, ft) for v in val})
            elif isinstance(get_origin(format_type), dict):
                val: dict
                kft, vft = get_args(format_type)
                _, vpt = get_args(py_type)
                if isinstance(kft, _LiteralGenericAlias):
                    for k in val.keys():
                        if not isinstance(k, kft):
                            raise TypeError(f"{k} is not of type {kft}")
                return Compound({k: self._convert_to_nbt(name, v, vpt, vft) for k, v in val.items()})
        else:
            # noinspection PyArgumentList
            return self.NBT_FORMAT[name](val)
    
    def as_nbt(self) -> Compound:
        d = {}
        for var, anno in type(self).__annotations__.items():
            var = var.removesuffix("_")
            if var not in self.NBT_FORMAT: continue
            format_type = self.NBT_FORMAT[var]
            if type(None) in get_args(anno) and getattr(self, var, None) is None: continue
            if isinstance(anno, type) and issubclass(anno, NBT):
                d[var] = getattr(self, var).as_nbt()
            elif isinstance(anno, type) and issubclass(anno, NBTTag):
                d[var] = getattr(self, var)
            elif isinstance(format_type, _LiteralGenericAlias):
                if var not in get_args(format_type):
                    raise ValueError(f"{var} is not in {get_args(format_type)}")
                d[var] = String(getattr(self, var))
            elif isinstance(format_type, _UnionGenericAlias):
                if type(None) in get_args(format_type) and getattr(self, var, None) is None: continue
                for format_subtype in get_args(format_type):
                    try:
                        d[var] = format_subtype(getattr(self, var))
                        break
                    except Exception: pass
                else:
                    raise TypeError(f"`{var}` is not one of types {', '.join(str(a) for a in get_args(format_type))} (Got {getattr(self, var)})")
            elif isinstance(format_type, _GenericAlias):
                if isinstance(get_origin(format_type), DictReprAsList):
                    d[var] = Compound({v.name: v.as_nbt() for v in getattr(self, var)})
                elif isinstance(get_origin(format_type), dict):
                    kt, vt = get_args(format_type)
                    if isinstance(kt, _LiteralGenericAlias):
                        for k in getattr(self, var).keys():
                            if not isinstance(k, kt):
                                raise TypeError(f"{k} is not of type {kt}")
                    d[var] = Compound({k: v.as_nbt() for k, v in getattr(self, var).items()})
                    for v in d[var].values():
                        if not isinstance(v, vt):
                            raise TypeError(f"{v} is not of type {vt}")
            else:
                # noinspection PyArgumentList
                d[var] = self.NBT_FORMAT[var](getattr(self, var))
            # noinspection PyTypeHints
            if (not isinstance(d[var], String if isinstance(format_type, _LiteralGenericAlias) else self.NBT_FORMAT[var])) \
                    or (issubclass(anno, NBT) and not isinstance(d[var], Compound)):
                raise TypeError(f"`{var}` is not of type {self.NBT_FORMAT[var]} (Got {getattr(self, var)})")
        return Compound(d)

    NBT_FORMAT: dict[str, Type[NBT]] | property = {}

# TODO JsonFormat wrapper around NBTFormat


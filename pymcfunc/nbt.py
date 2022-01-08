from __future__ import annotations

import functools
import json
import re
from abc import ABC
from collections.abc import MutableSequence, Sequence
from typing import Any

from typing_extensions import Self


class Path:
    def __init__(self, root: str | None = None):
        self._components = [root or "{}"]

    def __str__(self) -> str:
        return "".join(self._components)

    def __getattr__(self, attr: str) -> Self:
        str_attr = attr if re.search(r"^[a-zA-Z0-9]*$", attr) is not None else "\""+attr+"\""
        self._components.append("."+str_attr)
        return self

    def __getitem__(self, index: int | Ellipsis | NBT) -> Self:
        str_index = str(int) if isinstance(index, (str, NBT)) else ""
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

            def __init__(self, val: int):
                if not (min_ <= val <= max_):
                    raise ValueError(f"Value must be between {min_} and {max_}")
                elif not isinstance(val, self.val_type):
                    raise TypeError(f"Value must be a(n) {self.val_type.__name__} (Got {val})")
                NBT.__init__(self, val)

            def __str__(self):
                return str(self._val) + suffix
            
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
            def __init__(self, val: Sequence[content_type], nbt_type: type=NBT):
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
                val = NBT(val) if not issubclass(type(val), NBT) else val
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
                
            def py(self) -> list[content_type]:
                return [i.py() for i in self._val]

        return SequentialNBT
    return decorator

def _immutable_lock(*_):
    raise AttributeError("Value is immutable")

class NBT:
    val_type: type
    def __new__(cls, val: val_type):
        if cls != NBT: return super().__new__(cls)
        if isinstance(val, str): return String.__new__(String, val)
        elif isinstance(val, bool): return Boolean.__new__(Boolean, val)
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
        raise TypeError(f"Type {type(val).__name__} not supported as NBT value (Got {val})")

    def __init__(self, val: val_type):
        if not isinstance(val, self.val_type):
            raise TypeError(f"value must be of type {self.val_type.__name__} (Got {val})")
        self._val = val

        self.__setattr__ = _immutable_lock

    def __repr__(self):
        return type(self).__name__+"("+str(self)+")"
    
    def py(self) -> val_type:
        return self._val

@_numerical(-128, 127, int, "b")
class Byte(NBT): pass

@_numerical(-32768, 32767, int, "s")
class Short(NBT): pass

@_numerical(-2_147_483_648, 2_147_483_647, int)
class Int(NBT): pass

@_numerical(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807, int, "L")
class Long(NBT): pass

@_numerical(-3.4e38, 3.4e38, float, "f")
class Float(NBT): pass

@_numerical(-1.7e308, 1.7e308, float)
class Double(NBT): pass

class String(NBT, str):
    val_type = str
    def __str__(self):
        return json.dumps(self._val)

@_sequential(Any)
class List(NBT): pass

@_sequential(Byte, "B")
class ByteArray(NBT): pass

@_sequential(Int, "I")
class IntArray(NBT): pass

@_sequential(Long, "L")
class LongArray(NBT): pass

class Boolean(NBT):
    val_type = bool
    def __str__(self):
        return "true" if self._val else "false"
    
    def py(self) -> val_type:
        # noinspection PyTypeChecker
        return self._val

class Compound(NBT, dict):
    val_type = dict

    # noinspection PyMissingConstructor
    def __init__(self, val: dict[str, Any]):
        self._val = {str(k): NBT(v) for k, v in val.items()}

        def _immutable_lock2(self2, key: str, value: Any):
            value = NBT(value) if not issubclass(type(value), NBT) else value
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
        return "{"+",".join(k+":"+str(v) for k, v in self.items())+"}"

    def py(self) -> dict[str, Any]:
        return {k: v.py() for k, v in self._val}

class Template(Compound):
    pass
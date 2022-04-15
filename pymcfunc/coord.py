from __future__ import annotations

import re
from typing import Union

from typing_extensions import TypeAlias, Self

from pymcfunc.errors import RangeError
from pymcfunc.internal import immutable

_FloatCoord: TypeAlias = Union[float, str]
_IntCoord: TypeAlias = Union[int, str]
_FloatIntCoord: TypeAlias = Union[Union[int, float], str]

@immutable
class Coord2d: pass

@immutable
class Coord:
    x: _FloatCoord
    y: _FloatCoord
    z: _FloatCoord

    def __new__(cls, x: _FloatIntCoord, y: _FloatIntCoord, z: _FloatIntCoord):
        all_int = True
        if any(str(c).startswith("^") for c in [x, y, z]) and not all(str(c).startswith("^") for c in [x, y, z]):
            raise ValueError(f"Caret notation not used for all coordinates (Got {x}, {y} and {z})")
        for name, c in [('x', x), ('y', y), ('z', z)]:
            res = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(c))
            if res is None or len(str(res)) == 0:
                raise ValueError(f"Coordinate {name} invalid (Got {c})")
            if "." in res.group(1) or isinstance(c, float): all_int = False
        if all_int: return BlockCoord.__new__(BlockCoord, x, y, z)
        else: return super().__new__(cls)

    def __init__(self, x: _FloatIntCoord, y: _FloatIntCoord, z: _FloatIntCoord):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def __iter__(self):
        for c in (self.x, self.y, self.z): yield c

    @classmethod
    def at_executor(cls) -> Self:
        return cls("~", "~", "~")

    def to_chunk_coord(self) -> ChunkCoord:
        x = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(self.x)).group(1)
        z = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(self.z)).group(1)
        x = "" if x == "" else float(x)//8
        z = "" if z == "" else float(z)//8
        x = self.x[0]+str(x) if str(self.x)[0] in ("^", "~") else x
        z = self.x[0]+str(z) if str(self.z)[0] in ("^", "~") else z
        return ChunkCoord(x, z)

    def to_block_coord(self) -> BlockCoord:
        x = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(self.x)).group(1)
        y = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(self.y)).group(1)
        z = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(self.z)).group(1)
        x = "" if x == "" else round(float(x))
        y = "" if y == "" else round(float(y))
        z = "" if z == "" else round(float(z))
        x = self.x[0] + str(x) if str(self.x)[0] in ("^", "~") else x
        z = self.y[0] + str(y) if str(self.y)[0] in ("^", "~") else y
        z = self.x[0] + str(z) if str(self.z)[0] in ("^", "~") else z
        return BlockCoord(x, y, z)

class BlockCoord(Coord):
    x: _IntCoord
    y: _IntCoord
    z: _IntCoord

    def __new__(cls, x: _IntCoord, y: _IntCoord, z: _IntCoord):
        return object.__new__(cls)

@immutable
class ChunkCoord:
    x: _IntCoord
    z: _IntCoord
    def __init__(self, x: _IntCoord, z: _IntCoord):
        if any(str(c).startswith("^") for c in [x, z]) and not all(str(c).startswith("^") for c in [x, z]):
            raise ValueError(f"Caret notation not used for all coordinates (Got {x} and {z})")
        for name, c in [('x', x), ('z', z)]:
            res = re.search(r"^[~^]?(-?\d*(?:\.\d+)?)$", str(c))
            if res is None:
                raise ValueError(f"Coordinate {name} invalid (Got {c})")
            if "." in res.group(1) or isinstance(c, float):
                raise TypeError(f"Coordinate {name} must be an int (Got {c})")
        self.x = x
        self.z = z

    def __str__(self):
        return f"{self.x} {self.z}"

    def __iter__(self):
        for c in [self.x, self.z]: yield c

    @classmethod
    def at_executor(cls) -> Self:
        return cls("~", "~")

@immutable
class Rotation:
    yaw: _FloatCoord
    pitch: _FloatCoord
    def __init__(self, yaw: _FloatCoord, pitch: _FloatCoord):
        for name, c in [('yaw', yaw), ('pitch', pitch)]:
            if re.search(r"^~?(-?\d*(?:\.\d+)?)$", str(c)) is None:
                raise ValueError(f"Coordinate {name} invalid (Got {c})")
            if name == 'yaw' and not (-180 <= float(c.removeprefix("~")) <= 180):
                raise RangeError(f"Yaw must be -180 <= yaw <= 180")
            if name == 'pitch' and not (-90 <= float(c.removeprefix("~")) <= 90):
                raise RangeError(f"Pitch must be -90 <= pitch <= 90")
        self.yaw = yaw
        self.pitch = pitch
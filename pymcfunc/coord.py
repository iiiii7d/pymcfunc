import re
from typing import Union

from typing_extensions import TypeAlias, Self

_FloatCoord: TypeAlias = Union[float, str]
_IntCoord: TypeAlias = Union[int, str]
_FloatIntCoord: TypeAlias = Union[Union[int, float], str]

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
            if res is None:
                raise ValueError(f"Coordinate {name} invalid (Got {c})")
            if "." in res.group(1): all_int = False
        if all_int: return BlockCoord.__new__(BlockCoord, x, y, z)
        else: return super().__new__(cls)

    def __init__(self, x: _FloatIntCoord, y: _FloatIntCoord, z: _FloatIntCoord):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    @classmethod
    def at_executor(cls) -> Self:
        return cls("~", "~", "~")

class BlockCoord(Coord):
    x: _IntCoord
    y: _IntCoord
    z: _IntCoord

    def __new__(cls, x: _IntCoord, y: _IntCoord, z: _IntCoord):
        return object.__new__(cls)

class ChunkCoord:
    pass
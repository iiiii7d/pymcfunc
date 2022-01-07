import re
from typing import NamedTuple, Literal, Union

from typing_extensions import TypeAlias

_FloatCoord: TypeAlias = Union[float, str]
_IntCoord: TypeAlias = Union[int, str]
_FloatIntCoord: TypeAlias = Union[Union[int, float], str]
class Coord(NamedTuple):
    x: _FloatCoord
    y: _FloatCoord
    z: _FloatCoord

    def __new__(cls, x: _FloatIntCoord, y: _FloatIntCoord, z: _FloatIntCoord):
        if x % 1 == 0 and y % 1 == 0 and z % 1 == 0: return super(Coord, cls).__new__(BlockCoord)
        else: return super(Coord, cls).__new__(cls)

    def __init__(self, x: _FloatIntCoord, y: _FloatIntCoord, z: _FloatIntCoord):
        super().__init__(type(self).__name__)
        if any(str(c).startswith("^") for c in [x, y, z]) and not all(str(c).startswith("^") for c in [x, y, z]):
            raise ValueError(f"Caret notation not used for all coordinates (Got {x}, {y} and {z})")
        for name, c in [('x', x), ('y', y), ('z', z)]:
            if re.search(r"^[~^]?-?\d*(?:\.\d+)?$", c) is None:
                raise ValueError(f"Coordinate {name} invalid (Got {c})")
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

class BlockCoord(Coord):
    x: _IntCoord
    y: _IntCoord
    z: _IntCoord
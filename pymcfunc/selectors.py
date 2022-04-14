from __future__ import annotations

import json
from typing import Literal, Any, TypedDict, Annotated, Union

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.command import Range
from pymcfunc.coord import _FloatIntCoord, Coord
from pymcfunc.nbt import Compound, Int


@internal.base_class
@internal.immutable
class BaseSelector:
    def __init__(self, var: Literal['p', 'r', 'a', 'e', 's'], **arguments: Any):
        internal.options(var, ['p', 'r', 'a', 'e', 's']) # TODO 'c' and 'v' for edu edition, 'initiator' for bedrock
        self.var = var
        self.arguments = type(self).Arguments(**arguments)

    @property
    def singleonly(self) -> bool:
        return self.var in ['p', 'r']

    @property
    def playeronly(self) -> bool:
        return self.var in ['p', 'r', 'a']

    @classmethod
    def nearest_player(cls, **kwargs):
        """Alias of Selector('p', **kwargs)."""
        return cls('p', **kwargs)
    p = nearest_player

    @classmethod
    def random_player(cls, **kwargs):
        """Alias of Selector('r', **kwargs)."""
        return cls('r', **kwargs)
    r = random_player

    @classmethod
    def all_players(cls, **kwargs):
        """Alias of Selector('a', **kwargs)."""
        return cls('a', **kwargs)
    a = all_players

    @classmethod
    def all_entities(cls, **kwargs):
        """Alias of Selector('e', **kwargs)."""
        return cls('e', **kwargs)
    e = all_entities

    @classmethod
    def executor(cls, **kwargs):
        """Alias of Selector('s', **kwargs)."""
        return cls('s', **kwargs)
    s = executor

    def __str__(self):
        return f"@{self.var}{self.arguments}"

    class Arguments:
        def __init__(self, **kwargs): pass

        def __str__(self): pass


class JavaSelector(BaseSelector):
    @property
    def singleonly(self) -> bool:
        self.arguments: JavaSelector.Arguments
        return self.var in ['p', 'r'] or self.arguments.limit in {1, -1}

    @internal.immutable
    class Arguments:
        def __init__(self, *,
                     x: _FloatIntCoord | None = None,
                     y: _FloatIntCoord | None = None,
                     z: _FloatIntCoord | None = None,
                     coords: Coord | None = None,
                     dx: _FloatIntCoord | None = None,
                     dy: _FloatIntCoord | None = None,
                     dz: _FloatIntCoord | None = None,
                     d_coords: Coord | None = None,
                     distance: float | int | range | None = None,
                     scores: dict[str, int | range] | None = None,
                     tag: list[str] | str | None = None,
                     not_tag: list[str] | str | None = None,
                     team: str | None = None,
                     not_team: list[str] | str | None = None,
                     sort: Literal["nearest", "furthest", "random", "arbitrary"] | None = None,
                     limit: int | None = None,
                     level: int | range | None = None,
                     gamemode: Literal["spectator", "surival", "creative", "adventure"] | None = None,
                     not_gamemode: list[Literal["spectator", "surival", "creative", "adventure"]]
                     | Literal["spectator", "surival", "creative", "adventure"] | None = None,
                     name: str | None = None,
                     not_name: list[str] | None = None,
                     x_rotation: int | float | range | None = None,
                     y_rotation: int | float | range | None = None,
                     type_: str | None = None,
                     not_type: list[str] | str | None = None,
                     nbt: Compound | None = None,
                     not_nbt: Compound | None = None,
                     advancements: dict[str, bool | dict[str, bool]] | None = None, # TODO ResourceLocation
                     predicate: list[str] | str | None = None, # TODO Predicate / ResourceLocation
                     not_predicate: list[str] | str | None = None):

            if (x or y or z) and coords:
                raise ValueError("Cannot have `coords` and one of `x`, `y`, `z` selector arguments at the same time")
            elif coords:
                self.x, self.y, self.z = coords
            else:
                self.x = x
                self.y = y
                self.z = z
            if (dx or dy or dz) and d_coords:
                raise ValueError("Cannot have `d_coords` and one of `dx`, `dy`, `dz` selector arguments at the same time")
            elif d_coords:
                self.dx, self.dy, self.dz = d_coords
            else:
                self.dx = dx
                self.dy = dy
                self.dz = dz

            self.distance = distance
            self.scores = scores
            self.tag = tag if isinstance(tag, list) or tag is None else tag
            self.not_tag = not_tag if isinstance(not_tag, list) or not_tag is None else not_tag
            self.team = team
            self.not_team = not_team if isinstance(not_team, list) or not_team is None else not_team
            self.sort = sort
            self.limit = limit
            self.level = level
            self.gamemode = gamemode
            self.not_gamemode = not_gamemode if isinstance(not_gamemode, list) or not_gamemode is None else not_gamemode
            self.name = name
            self.not_name = not_name if isinstance(not_name, list) or not_name is None else not_name
            self.x_rotation = x_rotation
            self.y_rotation = y_rotation
            self.type_ = type_
            self.not_type = not_type if isinstance(not_type, list) or not_type is None else not_type
            self.nbt = nbt
            self.not_nbt = not_nbt
            self.advancements = advancements
            self.predicate = predicate if isinstance(predicate, list) or predicate is None else predicate
            self.not_predicate = not_predicate if isinstance(not_predicate, list) or not_predicate is None else not_predicate

        def __str__(self):
            s = []
            for name, value in [('x', self.x), ('y', self.y), ('z', self.z),
                                ('dx', self.dx), ('dy', self.dy), ('dz', self.dz),
                                ('distance', self.distance), ('team', self.team),
                                ('sort', self.sort), ('limit', self.limit),
                                ('level', self.level), ('gamemode', self.gamemode), ('name', self.name),
                                ('x_rotation', self.x_rotation), ('y_rotation', self.y_rotation),
                                ('type', self.type_), ('nbt', self.nbt)]:
                if value is not None: s.append(f"{name}={value}")
            for name, value in [('tag', self.tag), ('predicate', self.predicate)]:
                if value is not None:
                    for subvalue in value: s.append(f"{name}={subvalue}")

            if self.not_nbt is not None:
                s.append(f"nbt=!{self.not_nbt}")
            for name, value in [('tag', self.not_tag), ('team', self.not_team),
                                ('gamemode', self.not_gamemode), ('name', self.not_name),
                                ('type', self.not_type), ('predicate', self.not_predicate)]:
                if value is not None:
                    for subvalue in value: s.append(f"{name}=!{subvalue}")

            if self.scores is not None:
                s.append(f"scores={{{','.join(f'{k}={v}' for k, v in self.scores)}}}")
            if self.advancements is not None:
                d = ','.join(f'{k}={v if isinstance(v, bool) else ",".join(f"{sk}={sv}" for sk, sv in v)}'
                             for k, v in self.advancements)
                s.append(f"advancements={{{d}}}")
            return '['+','.join(s)+']'


class BedrockSelector(BaseSelector):
    @property
    def singleonly(self) -> bool:
        self.arguments: BedrockSelector.Arguments
        return self.var in ['p', 'r'] or self.arguments.c in {1, -1}

    @internal.immutable
    class Arguments:
        _HasItemDict = TypedDict("_HasItemDict", {
            "item": str,
            "data": Annotated[str, Range(0, Int.max)],
            "quantity": Union[int, range],
            "not_quantity": Union[int, range],
            "location": str,
            "slot": int
        }, total=False)
        def __init__(self, *,
                     x: _FloatIntCoord | None = None,
                     y: _FloatIntCoord | None = None,
                     z: _FloatIntCoord | None = None,
                     coords: Coord | None = None,
                     dx: _FloatIntCoord | None = None,
                     dy: _FloatIntCoord | None = None,
                     dz: _FloatIntCoord | None = None,
                     d_coords: Coord | None = None,
                     r: float | int | None = None,
                     rm: float | int | None = None,
                     r_range: range | None = None,
                     scores: dict[str, int | range] | None = None,
                     not_scores: dict[str, int | range] | None = None,
                     tag: list[str] | str | None = None,
                     not_tag: list[str] | str | None = None,
                     c: int | None = None,
                     l: int | None = None,
                     lm: int | None = None,
                     l_range: range | None = None,
                     gamemode: Literal["surival", "creative", "adventure", "s", "c", "a", 0, 1, 2] | None = None,
                     not_gamemode: list[Literal["surival", "creative", "adventure", "s", "c", "a", 0, 1, 2]]
                     | Literal["surival", "creative", "adventure", "s", "c", "a", 0, 1, 2] | None = None,
                     name: str | None = None,
                     not_name: list[str] | None = None,
                     rx: int | float | None = None,
                     rxm: int | float | None = None,
                     rx_range: range | None = None,
                     ry: int | float | None = None,
                     rym: int | float | None = None,
                     ry_range: range | None = None,
                     type_: str | None = None,
                     not_type: list[str] | str | None = None,
                     family: list[str] | str | None = None,
                     not_family: list[str] | str | None = None,
                     hasitem: list[_HasItemDict] | _HasItemDict | None = None):

            if (x or y or z) and coords:
                raise ValueError("Cannot have `coords` and one of `x`, `y`, `z` selector arguments at the same time")
            elif coords:
                self.x, self.y, self.z = coords
            else:
                self.x = x
                self.y = y
                self.z = z
            if (dx or dy or dz) and d_coords:
                raise ValueError("Cannot have `d_coords` and one of `dx`, `dy`, `dz` selector arguments at the same time")
            elif d_coords:
                self.dx, self.dy, self.dz = d_coords
            else:
                self.dx = dx
                self.dy = dy
                self.dz = dz

            if (r or rm) and r_range:
                raise ValueError("Cannot have `r_range` and one of `r`, `rm` selector arguments at the same time")
            elif r_range:
                self.rm = r_range.start
                self.r = r_range.stop
            else:
                self.r = r
                self.rm = rm

            self.scores = scores
            self.not_scores = not_scores
            self.tag = tag if isinstance(tag, list) or tag is None else tag
            self.not_tag = not_tag if isinstance(not_tag, list) or not_tag is None else not_tag
            self.c = c

            if (l or lm) and l_range:
                raise ValueError("Cannot have `l_range` and one of `l`, `lm` selector arguments at the same time")
            elif l_range:
                self.lm = l_range.start
                self.l = l_range.stop
            else:
                self.l = l
                self.lm = lm

            self.gamemode = gamemode if isinstance(gamemode, list) or gamemode is None else gamemode
            self.not_gamemode = not_gamemode if isinstance(not_gamemode, list) or not_gamemode is None else not_gamemode
            self.name = name
            self.not_name = not_name if isinstance(not_name, list) or not_name is None else not_name

            if (rx or rxm) and rx_range:
                raise ValueError("Cannot have `rx_range` and one of `rx`, `rxm` selector arguments at the same time")
            elif rx_range:
                self.rxm = rx_range.start
                self.rx = rx_range.stop
            else:
                self.rx = rx
                self.rxm = rxm
            if (ry or rym) and ry_range:
                raise ValueError("Cannot have `ry_range` and one of `ry`, `rym` selector arguments at the same time")
            elif ry_range:
                self.rym = ry_range.start
                self.ry = ry_range.stop
            else:
                self.ry = rx
                self.rym = rxm

            self.type_ = type_
            self.not_type = not_type if isinstance(not_type, list) or not_type is None else not_type
            self.family = family if isinstance(family, list) or family is None else family
            self.not_family = not_family if isinstance(not_family, list) or not_family is None else not_family
            self.hasitem = hasitem if isinstance(hasitem, list) or hasitem is None else hasitem

            s = []
            for name, value in [('x', self.x), ('y', self.y), ('z', self.z),
                                ('dx', self.dx), ('dy', self.dy), ('c', self.c),
                                ('l', self.l), ('lm', self.lm), ('name', self.name),
                                ('rx', self.rx), ('rxm', self.rxm),
                                ('ry', self.ry), ('rym', self.rym),
                                ('type', self.type_)]:
                if value is not None: s.append(f"{name}={value}")
            for name, value in [('tag', self.tag), ('gamemode', self.gamemode), ('family', self.family)]:
                if value is not None:
                    for subvalue in value: s.append(f"{name}={subvalue}")

            if self.not_nbt is not None:
                s.append(f"nbt=!{self.not_nbt}")
            for name, value in [('tag', self.not_tag), ('team', self.not_team),
                                ('gamemode', self.not_gamemode), ('name', self.not_name),
                                ('type', self.not_type), ('predicate', self.not_predicate)]:
                if value is not None:
                    for subvalue in value: s.append(f"{name}=!{subvalue}")

            if self.scores is not None:
                s.append(f"scores={{{','.join(f'{k}={v}' for k, v in self.scores)}}}")
            if self.advancements is not None:
                d = ','.join(f'{k}={v if isinstance(v, bool) else ",".join(f"{sk}={sv}" for sk, sv in v)}'
                             for k, v in self.advancements)
                s.append(f"advancements={{{d}}}")
            return '[' + ','.join(s) + ']'

'''
class BaseSelector:
    """The universal selector class.
       Every function has a **kwargs, which is used for selector arguments. The list of selector arguemnts are in the respective specialised classes.
       If an argument is repeatable, you can express multiple values of the same argument in lists, sets, or tuples.
       More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalSelectors"""

    @classmethod
    def select(cls, var: str, **kwargs):
        """Returns a selector, given the selector variable and optional arguments.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalSelectors.select"""
        internal.options(var, ['p', 'r', 'a', 'e', 's'])
        return "@"+var+cls._sel_args(cls, **kwargs)

    @classmethod
    def nearest_player(cls, **kwargs):
        """Alias of select('p', **kwargs)."""
        return cls.select('p', **kwargs)
    p = nearest_player

    @classmethod
    def random_player(cls, **kwargs):
        """Alias of select('r', **kwargs)."""
        return cls.select('p', **kwargs)
    r = random_player

    @classmethod
    def all_players(cls, **kwargs):
        """Alias of select('a', **kwargs)."""
        return cls.select('a', **kwargs)
    a = all_players

    @classmethod
    def all_entities(cls, **kwargs):
        """Alias of select('e', **kwargs)."""
        return cls.select('e', **kwargs)
    e = all_entities

    @classmethod
    def executor(cls, **kwargs):
        """Alias of select('s', **kwargs)."""
        return cls.select('s', **kwargs)
    s = executor

    @staticmethod
    def _sel_args(cls, **kwargs) -> str:
        args = []
        BEDROCK = ["x", "y", "z", "rmax", "rmin", "dx", "dy", "dz", "scores", "tag",
                   "c", "lmax", "lmin", "m", "name", "rxmax", "rxmin", "rymax", "rymin", "type", "family",
                   "l", "r", "rx", "ry"]
        JAVA = ["x", "y", "z", "distance", "dx", "dy", "dz", "scores", "tag",
                "team", "limit", "sort", "level", "gamemode", "name", "x_rotation", "y_rotation",
                "type", "nbt", "advancements", "predicate"]
        CAN_REPEAT = ["type", "family", "tag", "nbt", "advancements", "predicate"]
        OPTIONS_JAVA = {
            "sort": ["nearest", "furthest", "random", "arbitrary"],
            "gamemode": ["spectator", "adventure", "creative", "survival"]
        }
        OPTIONS_BEDROCK = {
            "gamemode": ["0", "1", "2", "3"]
        }
        ALIASES = {
            "lmax": "l",
            "lmin": "lm",
            "rmax": "r",
            "rmin": "rm",
            "rxmax": "rx",
            "rxmin": "rxm",
            "rymax": "ry",
            "rymin": "rym"
        }
        EXPAND = {
            "l": ("l", "lm"),
            "r": ("r", "rm"),
            "rx": ("rx", "rxm"),
            "ry": ("ry", "rym")
        }

        for k, v in kwargs.items():
            keylist = BEDROCK if type(cls) == BedrockSelector else JAVA
            optionslist = OPTIONS_BEDROCK if type(cls) == BedrockSelector else OPTIONS_JAVA
            if k not in keylist:
                raise KeyError(f"Invalid target selector argument '{k}'")
            if k in optionslist.keys():
                if not str(v) in optionslist[k]:
                    raise errors.OptionError(optionslist[k], v)
            if k in ALIASES and type(cls) == BedrockSelector:
                args.append(f"{ALIASES[k]}={v}")
            elif k in EXPAND and type(cls) == BedrockSelector:
                for i in EXPAND[k]:
                    v = json.dumps(v) if isinstance(v, dict) else v
                    args.append(f"{i}={v}")
            elif k in CAN_REPEAT and isinstance(v, (tuple, list, set)):
                for i in v:
                    i = json.dumps(i) if isinstance(i, dict) else i
                    args.append(f"{k}={i}")
            else:
                v = json.dumps(v) if isinstance(v, dict) else v
                args.append(f"{k}={v}")
        result = "["+", ".join(args)+"]"
        if result == "[]": result = ""
        return result


class BedrockSelector(BaseSelector):
    """The Bedrock Edition selector class.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockSelectors"""
    def __init__(self):
        pass


class JavaSelector(BaseSelector):
    """The Java Edition selector class.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaSelectors"""
    def __init__(self):
        pass

    @staticmethod
    def range(minv: int=0, maxv: int=inf) -> str:
        """Returns a range of values, as it is represented in Minecraft commands.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaSelectors.range"""
        if minv > maxv:
            raise ValueError(f"{maxv} is greater than {minv}")
        if minv == 0:
            minv = ""
        if maxv == inf:
            maxv = ""
        result = str(minv)+".."+str(maxv)
        if result == "..":
            raise ValueError(f"Invalid range")
        return result

def cuboid(pos1: Sequence[int], pos2: Sequence[int], dims: str='xyz') -> Dict[str, int]:
    """Finds the northwest-bottommost corner and the volume/area/length of a cuboid, area or line, given two corners.
    This function is mainly for selector arguments, namely x, y, z, dx, dy and dz.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.sel.cuboid"""
    if len(pos1) != len(pos2):
        raise ValueError("Uneven no. of dimensions")
    elif len(pos1) != len(dims) or len(pos2) != len(dims):
        raise ValueError(f"Expected {len(dims)} dimensions, got {len(pos1)} and {len(pos2)}")
    elif not re.search(r"^(?!.*(.).*\1)[xyz]+$", dims):
        raise ValueError(f"Axes are invalid (Got '{dims}')")
    out = {}
    for dim, v1, v2 in zip(dims, pos1, pos2):
        minv = min(v1, v2)
        d = max(v1, v2) - minv
        out[dim] = minv
        out['d'+dim] = d
    return out
'''
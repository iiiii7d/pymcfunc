from __future__ import annotations

from typing import Literal, Any, TypedDict, Annotated, Union, TYPE_CHECKING

import pymcfunc.internal as internal
if TYPE_CHECKING: from pymcfunc.command import ResourceLocation
from pymcfunc.data_formats.coord import _FloatIntCoord, Coord
from pymcfunc.data_formats.nbt import Compound, Int
from pymcfunc.data_formats.range import FloatRange


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
                     distance: float | int | FloatRange | None = None,
                     scores: dict[str, int | FloatRange] | None = None,
                     tag: list[str] | str | None = None,
                     not_tag: list[str] | str | None = None,
                     team: str | None = None,
                     not_team: list[str] | str | None = None,
                     sort: Literal["nearest", "furthest", "random", "arbitrary"] | None = None,
                     limit: int | None = None,
                     level: int | FloatRange | None = None,
                     gamemode: Literal["spectator", "surival", "creative", "adventure"] | None = None,
                     not_gamemode: list[Literal["spectator", "surival", "creative", "adventure"]]
                     | Literal["spectator", "surival", "creative", "adventure"] | None = None,
                     name: str | None = None,
                     not_name: list[str] | None = None,
                     x_rotation: int | float | FloatRange | None = None,
                     y_rotation: int | float | FloatRange | None = None,
                     type_: str | None = None,
                     not_type: list[str] | str | None = None,
                     nbt: Compound | None = None,
                     not_nbt: Compound | None = None,
                     advancements: dict[ResourceLocation, bool | dict[str, bool]] | None = None,
                     predicate: list[ResourceLocation] | ResourceLocation | None = None, # TODO Predicate
                     not_predicate: list[ResourceLocation] | str | None = None):

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
            "data": Annotated[str, FloatRange(0, Int.max)],
            "quantity": Union[int, FloatRange],
            "not_quantity": Union[int, FloatRange],
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
                     r_range: FloatRange | None = None,
                     scores: dict[str, int | FloatRange] | None = None,
                     not_scores: dict[str, int | FloatRange] | None = None,
                     tag: list[str] | str | None = None,
                     not_tag: list[str] | str | None = None,
                     c: int | None = None,
                     l: int | None = None,
                     lm: int | None = None,
                     l_range: FloatRange | None = None,
                     gamemode: Literal["surival", "creative", "adventure", "s", "c", "a", 0, 1, 2] | None = None,
                     not_gamemode: list[Literal["surival", "creative", "adventure", "s", "c", "a", 0, 1, 2]]
                     | Literal["surival", "creative", "adventure", "s", "c", "a", 0, 1, 2] | None = None,
                     name: str | None = None,
                     not_name: list[str] | None = None,
                     rx: int | float | None = None,
                     rxm: int | float | None = None,
                     rx_range: FloatRange | None = None,
                     ry: int | float | None = None,
                     rym: int | float | None = None,
                     ry_range: FloatRange | None = None,
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
                self.rm = r_range.lower
                self.r = r_range.upper
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
                self.lm = l_range.lower
                self.l = l_range.upper
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
                self.rxm = rx_range.lower
                self.rx = rx_range.upper
            else:
                self.rx = rx
                self.rxm = rxm
            if (ry or rym) and ry_range:
                raise ValueError("Cannot have `ry_range` and one of `ry`, `rym` selector arguments at the same time")
            elif ry_range:
                self.rym = ry_range.lower
                self.ry = ry_range.upper
            else:
                self.ry = rx
                self.rym = rxm

            self.type_ = type_
            self.not_type = not_type if isinstance(not_type, list) or not_type is None else not_type
            self.family = family if isinstance(family, list) or family is None else family
            self.not_family = not_family if isinstance(not_family, list) or not_family is None else not_family
            self.hasitem = hasitem if isinstance(hasitem, list) or hasitem is None else hasitem

        def __str__(self):
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

            for name, value in [('tag', self.not_tag),
                                ('gamemode', self.not_gamemode), ('name', self.not_name),
                                ('type', self.not_type), ('family', self.not_family)]:
                if value is not None:
                    for subvalue in value: s.append(f"{name}=!{subvalue}")

            if self.scores is not None:
                s.append(f"scores={{{','.join(f'{k}={v}' for k, v in self.scores)}}}")
            if self.not_scores is not None:
                s.append(f"scores={{{','.join(f'{k}=!{v}' for k, v in self.not_scores)}}}")
            if self.hasitem is not None:
                values = [",".join(f"{sk}={sv}" for sk, sv in v.items()) for v in self.hasitem]
                s.append(f"hasitem={values[0] if len(values) == 1 else '['+','.join(values)+']'}")
            return '[' + ','.join(s) + ']'
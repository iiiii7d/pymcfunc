from __future__ import annotations

from typing import Literal, Type, Optional, Union

from attr import define

from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.data_formats.nbt import NBTTag, Compound, NBT, DictReprAsList, Float, Double, Int
from pymcfunc.data_formats.number_providers import NumberProvider
from pymcfunc.internal import immutable


@immutable
class RangeJson(JsonFormat):
    def __new__(cls, min_: int | str, max_: int | str):
        if cls != RangeJson: return super().__new__(cls)
        if isinstance(min_, int) and Int.min <= min_ <= Int.max and \
           isinstance(max_, int) and Int.min <= max_ <= Int.max:
            return IntRangeJson.__new__(IntRangeJson, min_, max_)
        if Double.min <= min_ <= Double.max and Double.min <= max_ <= Double.max:
            return FloatRangeJson.__new__(FloatRangeJson, min_, max_)
        if Float.min <= min_ <= Float.max and Float.min <= max_ <= Float.max:
            return DoubleRangeJson.__new__(DoubleRangeJson, min_, max_)

    def __init__(self, min_: int | str, max_: int | str):
        self.min: int | str = min_
        self.max: int | str = max_

class FloatRangeJson(RangeJson):
    JSON_FORMAT = {
        'min': float,
        'max': float
    }
class IntRangeJson(RangeJson):
    JSON_FORMAT = {
        'min': int,
        'max': int
    }
class DoubleRangeJson(RangeJson):
    JSON_FORMAT = {
        'min': float,
        'max': float
    }
class NumberProviderRangeJson(RangeJson):
    JSON_FORMAT = {
        'min': NumberProvider,
        'max': NumberProvider
    }

@define(kw_only=True, init=True)
class DamageJson(JsonFormat):
    blocked: bool | None = None
    dealt: float | DoubleRangeJson | None = None
    source_entity: EntityJson | None = None
    taken: float | DoubleRangeJson | None = None
    type: DamageTypeJson | None = None

    @property
    def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'blocked': Optional[bool],
            'dealt': Optional[Union[DoubleRangeJson, float]],
            'source_entity': Optional[EntityJson],
            'taken': Optional[Union[DoubleRangeJson, float]],
            'type': Optional[DamageTypeJson]
        }

@define(kw_only=True, init=True)
class DamageTypeJson(JsonFormat):
    bypasses_armor: bool | None = None
    bypasses_invulnerability: bool | None = None
    bypasses_magic: bool | None = None
    direct_entity: EntityJson | None = None
    is_explosion: bool | None = None
    is_fire: bool | None = None
    is_magic: bool | None = None
    is_projectile: bool | None = None
    is_lightning: bool | None = None
    source_entity: EntityJson | None = None

    @property
    def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'bypasses_armor': Optional[bool],
            'bypasses_invulnerability': Optional[bool],
            'bypasses_magic': Optional[bool],
            'direct_entity': Optional[EntityJson],
            'is_explosion': Optional[bool],
            'is_fire': Optional[bool],
            'is_magic': Optional[bool],
            'is_projectile': Optional[bool],
            'is_lightning': Optional[bool],
            'source_entity': Optional[EntityJson]
        }


class EntityJson(JsonFormat):
    distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRangeJson] | None = None
    effects: list[Effect] | None = None
    equipment: dict[Literal["mainhand", "offhand", "head", "chest", "legs", "feet"], ItemJson] | None = None
    flags: dict[Literal["is_on_fire", "is_sneaking", "is_sprinting", "is_swimming", "is_baby"], bool] | None = None
    lightning_bolt: LightningBolt | None = None
    location: LocationJson | None = None
    nbt: NBTTag | None = None
    passenger: EntityJson | None = None
    player: Player | None = None
    stepping_on: LocationJson | None = None
    team: str | None = None # TODO are there specific team names?
    type: str | None = None
    targeted_entity: EntityJson | None = None
    vehicle: str | None = None
    fishing_hook_in_open_water: bool | None = None

    @property
    def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'distance': Optional[dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRangeJson]], # TODO format for distance
            'effects': Optional[DictReprAsList[self.Effect]],
            'equipment': Optional[dict[Literal["mainhand", "offhand", "head", "chest", "legs", "feet"], ItemJson]], #TODO same for below two
            'flags': Optional[dict[Literal["is_on_fire", "is_sneaking", "is_sprinting", "is_swimming", "is_baby"], bool]],
            'lightning_bolt': Optional[self.LightningBolt],
            'location': Optional[LocationJson],
            'nbt': Optional[str],
            'passenger': Optional[EntityJson],
            'player': Optional[self.Player],
            'stepping_on': Optional[LocationJson],
            'team': Optional[str],
            'type': Optional[str],
            'targeted_entity': Optional[EntityJson],
            'vehicle': Optional[str],
            'fishing_hook_in_open_water': Optional[bool]
        }

    @define(kw_only=True, init=True)
    class Effect(JsonFormat):
        name: str
        ambient: bool | None = None
        amplifier: int | IntRangeJson | None = None
        duration: int | IntRangeJson | None = None
        visible: bool | None = None

        @property
        def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
            return {
                'ambient': Optional[bool],
                'amplifier': Optional[Union[IntRangeJson, int]],
                'duration': Optional[Union[IntRangeJson, int]],
                'visible': Optional[bool]
            }

    @define(kw_only=True, init=True)
    class Player(JsonFormat):
        looking_at: EntityJson | None = None
        advancements: dict[str, bool | dict[str, bool]] | None = None
        gamemode: Literal["survival", "adventure", "creative", "spectator"] | None = None
        level: int | IntRangeJson | None = None
        recipes: dict[str, bool] | None = None
        stats: list[Statistic] | None = None

        @property
        def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
            return {
                'looking_at': Optional[EntityJson],
                'advancements': Optional[dict[str, Union[bool, dict[str, bool]]]],
                'gamemode': Optional[str],
                'level': Optional[Union[IntRangeJson, int]],
                'recipes': Optional[dict[str, bool]],
                'stats': Optional[DictReprAsList[self.Statistic]]
            }

        @define(kw_only=True, init=True)
        class Statistic:
            type: Literal["minecraft:custom", "minecraft:crafted", "minecraft:used", "minecraft:broken",
                          "minecraft:mined", "minecraft:killed", "minecraft:picked_up", "minecraft:dropped",
                          "minecraft:killed_by"] | None = None
            stat: str | None = None
            value: int | IntRangeJson | None = None

            @property
            def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
                return {
                    'type': Optional[str],
                    'stat': Optional[str],
                    'value': Optional[Union[IntRangeJson, int]]
                }

    @define(kw_only=True, init=True)
    class LightningBolt(JsonFormat):
        blocks_set_on_fire: int | None = None
        entity_struck: EntityJson | None = None

        @property
        def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
            return {
                'blocks_set_on_fire': Optional[int],
                'entity_struck': Optional[EntityJson]
            }


@define(kw_only=True, init=True)
class LocationJson(JsonFormat):
    biome: str | None = None
    block: Block | None = None
    dimension: str | None = None
    feature: str | None = None
    fluid: Fluid | None = None
    light: int | IntRangeJson | None = None
    position: dict[Literal["x", "y", "z"], float | DoubleRangeJson] | None = None
    smokey: bool | None = None

    @property
    def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'biome': Optional[str],
            'block': Optional[self.Block],
            'dimension': Optional[str],
            'feature': Optional[str],
            'fluid': Optional[self.Fluid],
            'light': Optional[Union[IntRangeJson, int]],
            'position': Optional[dict[str, Union[DoubleRangeJson, float]]],
            'smokey': Optional[bool]
        }

    @define(kw_only=True, init=True)
    class Block(JsonFormat):
        blocks: list[str] | None = None
        tag: str | None = None
        nbt: Compound | None = None
        state: dict[str, str | int | bool | IntRangeJson] | None = None

        @property
        def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
            return {
                'blocks': Optional[str],
                'tag': Optional[str],
                'nbt': Optional[Compound],
                'state': Optional[dict[str, Union[IntRangeJson, int, bool, str]]]
            }

    @define(kw_only=True, init=True)
    class Fluid(JsonFormat):
        fluid: str | None = None
        state: dict[str, str | int | bool | IntRangeJson] | None = None

        @property
        def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
            return {
                'fluid': Optional[str],
                'state': Optional[dict[str, Union[IntRangeJson, int, bool, str]]]
            }

@define(kw_only=True, init=True)
class ItemJson(JsonFormat):
    count: int | IntRangeJson | None = None
    durability: int | IntRangeJson | None = None
    enchantments: list[Enchantment] | None = None
    stored_enchantments: list[Enchantment] | None = None
    items: list[str] | None = None
    nbt: Compound | None = None
    potion: str | None = None
    tag: str | None = None

    @property
    def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'count': Optional[Union[IntRangeJson, int]],
            'durability': Optional[Union[IntRangeJson, int]],
            'enchantments': Optional[list[self.Enchantment]],
            'stored_enchantments': Optional[list[self.Enchantment]],
            'items': Optional[str],
            'nbt': Optional[Compound],
            'potion': Optional[str],
            'tag': Optional[str]
        }

    @define(kw_only=True, init=True)
    class Enchantment(JsonFormat):
        enchantment: str | None = None
        levels: int | IntRangeJson | None = None

        @property
        def JSON_FORMAT(self) -> dict[str, Type[NBT]]:
            return {
                'enchantment': Optional[str],
                'levels': Optional[Union[IntRangeJson, int]]
            }
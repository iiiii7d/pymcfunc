from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Type, Optional, Union

from pymcfunc.internal import immutable
from pymcfunc.nbt import Float, Int, Double, NBT, Compound, NBTFormat, Boolean, NBTRepresentable, List, String, \
    DictReprAsList


@immutable
class RangeJson(NBTFormat):
    def __new__(cls, min_: int | str, max_: int | str):
        if cls != RangeJson: return super().__new__(cls)
        if isinstance(min_, int) and Int.min <= min_ <= Int.max and \
           isinstance(max_, int) and Int.min <= max_ <= Int.max:
            return IntRangeJson.__new__(IntRangeJson, min_, max_)
        if Float.min <= min_ <= Float.max and Float.min <= max_ <= Float.max:
            return FloatRangeJson.__new__(FloatRangeJson, min_, max_)
        if Double.min <= min_ <= Double.max and Double.min <= max_ <= Double.max:
            return DoubleRangeJson.__new__(DoubleRangeJson, min_, max_)

    def __init__(self, min_: int | str, max_: int | str):
        self.min: int | str = min_
        self.max: int | str = max_

class FloatRangeJson(RangeJson):
    NBT_FORMAT = {
        'min': Float,
        'max': Float
    }
class IntRangeJson(RangeJson):
    NBT_FORMAT = {
        'min': Int,
        'max': Int
    }
class DoubleRangeJson(RangeJson):
    NBT_FORMAT = {
        'min': Double,
        'max': Double
    }

@dataclass(init=True)
class DamageJson(NBTFormat):
    blocked: bool | None = None
    dealt: float | DoubleRangeJson | None = None
    source_entity: EntityJson | None = None
    taken: float | DoubleRangeJson | None = None
    type: DamageTypeJson | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'blocked': Optional[Boolean],
            'dealt': Optional[Union[DoubleRangeJson, Double]],
            'source_entity': Optional[EntityJson],
            'taken': Optional[Union[DoubleRangeJson, Double]],
            'type': Optional[DamageTypeJson]
        }

@dataclass(init=True)
class DamageTypeJson(NBTFormat):
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
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'bypasses_armor': Optional[Boolean],
            'bypasses_invulnerability': Optional[Boolean],
            'bypasses_magic': Optional[Boolean],
            'direct_entity': Optional[EntityJson],
            'is_explosion': Optional[Boolean],
            'is_fire': Optional[Boolean],
            'is_magic': Optional[Boolean],
            'is_projectile': Optional[Boolean],
            'is_lightning': Optional[Boolean],
            'source_entity': Optional[EntityJson]
        }


class EntityJson(NBTFormat):
    distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRangeJson] | None = None
    effects: list[Effect] | None = None
    equipment: dict[Literal["mainhand", "offhand", "head", "chest", "legs", "feet"], ItemJson] | None = None
    flags: dict[Literal["is_on_fire", "is_sneaking", "is_sprinting", "is_swimming", "is_baby"], bool] | None = None
    lightning_bolt: LightningBolt | None = None
    location: LocationJson | None = None
    nbt: NBT | None = None
    passenger: EntityJson | None = None
    player: Player | None = None
    stepping_on: LocationJson | None = None
    team: str | None = None # TODO are there specific team names?
    type: str | None = None
    targeted_entity: EntityJson | None = None
    vehicle: str | None = None
    fishing_hook_in_open_water: bool | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'distance': Optional[dict[str, FloatRangeJson]], # TODO format for distance
            'effects': Optional[DictReprAsList[self.Effect]],
            'equipment': Optional[dict[str, ItemJson]], #TODO same for below two
            'flags': Optional[dict[str, Boolean]],
            'lightning_bolt': Optional[self.LightningBolt],
            'location': Optional[LocationJson],
            'nbt': Optional[NBT],
            'passenger': Optional[EntityJson],
            'player': Optional[self.Player],
            'stepping_on': Optional[LocationJson],
            'team': Optional[String],
            'type': Optional[String],
            'targeted_entity': Optional[EntityJson],
            'vehicle': Optional[String],
            'fishing_hook_in_open_water': Optional[Boolean]
        }

    @dataclass(init=True)
    class Effect(NBTFormat):
        name: str
        ambient: bool | None = None
        amplifier: int | IntRangeJson | None = None
        duration: int | IntRangeJson | None = None
        visible: bool | None = None

        @property
        def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
            return {
                'ambient': Optional[Boolean],
                'amplifier': Optional[Union[IntRangeJson, Int]],
                'duration': Optional[Union[IntRangeJson, Int]],
                'visible': Optional[Boolean]
            }

    @dataclass(init=True)
    class Player(NBTFormat):
        looking_at: EntityJson | None = None
        advancements: dict[str, bool | dict[str, bool]] | None = None
        gamemode: Literal["survival", "adventure", "creative", "spectator"] | None = None
        level: int | IntRangeJson | None = None
        recipes: dict[str, bool] | None = None
        stats: list[Statistic] | None = None

        @property
        def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
            return {
                'looking_at': Optional[EntityJson],
                'advancements': Optional[dict[str, Union[Boolean, dict[str, Boolean]]]],
                'gamemode': Optional[String],
                'level': Optional[Union[IntRangeJson, Int]],
                'recipes': Optional[dict[str, Boolean]],
                'stats': Optional[DictReprAsList[self.Statistic]]
            }

        @dataclass(init=True)
        class Statistic:
            type: Literal["minecraft:custom", "minecraft:crafted", "minecraft:used", "minecraft:broken",
                          "minecraft:mined", "minecraft:killed", "minecraft:picked_up", "minecraft:dropped",
                          "minecraft:killed_by"] | None = None
            stat: str | None = None
            value: int | IntRangeJson | None = None

            @property
            def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
                return {
                    'type': Optional[String],
                    'stat': Optional[String],
                    'value': Optional[Union[IntRangeJson, Int]]
                }

    @dataclass(init=True)
    class LightningBolt(NBTFormat):
        blocks_set_on_fire: int | None = None
        entity_struck: EntityJson | None = None

        @property
        def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
            return {
                'blocks_set_on_fire': Optional[Int],
                'entity_struck': Optional[EntityJson]
            }


@dataclass(init=True)
class LocationJson(NBTFormat):
    biome: str | None = None
    block: Block | None = None
    dimension: str | None = None
    feature: str | None = None
    fluid: Fluid | None = None
    light: int | IntRangeJson | None = None
    position: dict[Literal["x", "y", "z"], float | DoubleRangeJson] | None = None
    smokey: bool | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'biome': Optional[String],
            'block': Optional[self.Block],
            'dimension': Optional[String],
            'feature': Optional[String],
            'fluid': Optional[self.Fluid],
            'light': Optional[Union[IntRangeJson, Int]],
            'position': Optional[dict[str, Union[DoubleRangeJson, Double]]],
            'smokey': Optional[Boolean]
        }

    @dataclass(init=True)
    class Block(NBTFormat):
        blocks: list[str] | None = None
        tag: str | None = None
        nbt: Compound | None = None
        state: dict[str, str | int | bool | IntRangeJson] | None = None

        @property
        def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
            return {
                'blocks': Optional[String],
                'tag': Optional[String],
                'nbt': Optional[Compound],
                'state': Optional[dict[str, Union[IntRangeJson, Int, Boolean, String]]]
            }

    @dataclass(init=True)
    class Fluid(NBTFormat):
        fluid: str | None = None
        state: dict[str, str | int | bool | IntRangeJson] | None = None

        @property
        def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
            return {
                'fluid': Optional[String],
                'state': Optional[dict[str, Union[IntRangeJson, Int, Boolean, String]]]
            }

@dataclass(init=True)
class ItemJson(NBTFormat):
    count: int | IntRangeJson | None = None
    durability: int | IntRangeJson | None = None
    enchantments: list[Enchantment] | None = None
    stored_enchantments: list[Enchantment] | None = None
    items: list[str] | None = None
    nbt: Compound | None = None
    potion: str | None = None
    tag: str | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'count': Optional[Union[IntRangeJson, Int]],
            'durability': Optional[Union[IntRangeJson, Int]],
            'enchantments': Optional[List[self.Enchantment]],
            'stored_enchantments': Optional[List[self.Enchantment]],
            'items': Optional[String],
            'nbt': Optional[Compound],
            'potion': Optional[String],
            'tag': Optional[String]
        }

    @dataclass(init=True)
    class Enchantment(NBTFormat):
        enchantment: str | None = None
        levels: int | IntRangeJson | None = None

        @property
        def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
            return {
                'enchantment': Optional[String],
                'levels': Optional[Union[IntRangeJson, Int]]
            }
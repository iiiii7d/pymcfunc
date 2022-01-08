from __future__ import annotations

from typing import Literal, TypedDict

from pymcfunc.nbt import Float, Int, Double, NBT


class Range:
    def __new__(cls, min_: int | str, max_: int | str):
        if cls != Range: return super().__new__(cls)
        if isinstance(min_, int) and Int.min <= min_ <= Int.max and \
           isinstance(max_, int) and Int.min <= max_ <= Int.max:
            return IntRange.__new__(IntRange, min_, max_)
        if Float.min <= min_ <= Float.max and Float.min <= max_ <= Float.max:
            return FloatRange.__new__(FloatRange, min_, max_)
        if Double.min <= min_ <= Double.max and Double.min <= max_ <= Double.max:
            return DoubleRange.__new__(DoubleRange, min_, max_)

    def __init__(self, min_: int | str, max_: int | str):
        self.min: int | str = min_
        self.max: int | str = max_

class FloatRange(Range): pass
class IntRange(Range): pass
class DoubleRange(Range): pass

class DamageJson:
    def __init__(self, **kwargs):
        self.blocked: bool | None = None
        self.dealt: float | DoubleRange | None = None
        self.source_entity: EntityJson | None = None
        self.taken: float | DoubleRange | None = None
        self.type: DamageTypeJson | None = None

        for k, v in kwargs.items(): setattr(self, k, v)

    def json(self) -> dict:
        d = {}
        if self.blocked is not None: d["blocked"] = self.blocked
        if self.dealt is not None: d["dealt"] = self.dealt
        if self.source_entity is not None: d["source_entity"] = self.source_entity.json()
        if self.taken is not None: d["taken"] = self.taken
        if self.type is not None: d["type"] = self.type.json()
        return d

class DamageTypeJson:
    def __init__(self, **kwargs):
        self.bypasses_armor: bool | None = None
        self.bypasses_invulnerability: bool | None = None
        self.bypasses_magic: bool | None = None
        self.direct_entity: EntityJson | None = None
        self.is_explosion: bool | None = None
        self.is_fire: bool | None = None
        self.is_magic: bool | None = None
        self.is_projectile: bool | None = None
        self.is_lightning: bool | None = None
        self.source_entity: EntityJson | None = None

        for k, v in kwargs.items(): setattr(self, k, v)

    def json(self) -> dict:
        d = {}
        if self.bypasses_armor is not None: d["bypasses_armor"] = self.bypasses_armor
        if self.bypasses_invulnerability is not None: d["bypasses_invulnerability"] = self.bypasses_invulnerability.json()
        if self.bypasses_magic is not None: d["bypasses_magic"] = self.bypasses_magic
        if self.direct_entity is not None: d["direct_entity"] = self.direct_entity
        if self.is_explosion is not None: d["is_explosion"] = self.is_explosion
        if self.is_fire is not None: d["is_fire"] = self.is_fire
        if self.is_magic is not None: d["is_magic"] = self.is_magic
        if self.is_projectile is not None: d["is_projectile"] = self.is_projectile
        if self.is_lightning is not None: d["is_lightning"] = self.is_lightning
        if self.source_entity is not None: d["source_entity"] = self.source_entity.json()
        return d


class EntityJson:
    def __init__(self, **kwargs):
        self.distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRange] | None = None
        self.effects: list[EntityJson.Effect] | None = None
        self.equipment: dict[Literal["mainhand", "offhand", "head", "chest", "legs", "feet"], ItemJson] | None = None
        self.flags: dict[Literal["is_on_fire", "is_sneaking", "is_sprinting", "is_swimming", "is_baby"], bool] | None = None
        self.lightning_bolt: dict[_LightningBolt] | None = None
        self.location: LocationJson | None = None
        self.nbt: NBT | None = None
        self.passenger: EntityJson | None = None
        self.player: EntityJson.Player | None = None
        # TODO more here
    class Effect:
        pass
    class Player:
        pass
    class LightningBolt:
        pass
    # TODO classes for distance and equipment?

_LightningBolt = TypedDict("_LightningBolt", {
    "blocks_set_on_fire": int,
    "entity_struck": EntityJson
}, total=False)

class LocationJson:
    pass

class ItemJson:
    pass
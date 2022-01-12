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

    def json(self) -> dict:
        return {'min': self.min, 'max': self.max}

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
        d: dict = {}
        for attr in ['blocked', 'dealt', 'source_entity', 'taken', 'type']:
            if getattr(self, attr) is not None:
                d[attr] = getattr(self, attr)
                if 'json' in dir(d[attr]):
                    d[attr] = d[attr].json()
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
        d: dict = {}
        for attr in ['bypassess_armor', 'bypasses_invulnerability', 'bypasses_magic', 'direct_entity',
                     'is_explosion', 'is_fire', 'is_magic', 'is_projectile', 'is_lightning',
                     'source_entity']:
            if getattr(self, attr) is not None:
                d[attr] = getattr(self, attr)
                if 'json' in dir(d[attr]):
                    d[attr] = d[attr].json()
        return d


class EntityJson:
    def __init__(self, **kwargs):
        self.distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRange] | None = None
        self.effects: list[EntityJson.Effect] | None = None
        self.equipment: dict[Literal["mainhand", "offhand", "head", "chest", "legs", "feet"], ItemJson] | None = None
        self.flags: dict[Literal["is_on_fire", "is_sneaking", "is_sprinting", "is_swimming", "is_baby"], bool] | None = None
        self.lightning_bolt: EntityJson.LightningBolt | None = None
        self.location: LocationJson | None = None
        self.nbt: NBT | None = None
        self.passenger: EntityJson | None = None
        self.player: EntityJson.Player | None = None
        self.stepping_on: LocationJson | None = None
        self.team: str | None = None # TODO are there specific team names?
        self.type: str | None = None
        self.targeted_entity: EntityJson | None = None
        self.vehicle: str | None = None
        self.fishing_hook_in_open_water: bool | None = None

        for k, v in kwargs.items(): setattr(self, k, v)

    class Effect:
        def __init__(self, name: str, **kwargs):
            self.name: str = name
            self.ambient: bool | None = None
            self.amplifier: int | IntRange | None = None
            self.duration: int | IntRange | None = None
            self.visible: bool | None = None

            for k, v in kwargs.items(): setattr(self, k, v)

        def json(self) -> dict:
            d: dict = {}
            for attr in ['name', 'ambient', 'amplifier', 'duration', 'visible']:
                if getattr(self, attr) is not None:
                    d[attr] = getattr(self, attr)
                    if 'json' in dir(d[attr]):
                        d[attr] = d[attr].json()
            return d

    class Player:
        pass
    class LightningBolt:
        pass
    # TODO classes for distance and equipment?

class LocationJson:
    pass

class ItemJson:
    pass
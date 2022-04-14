from __future__ import annotations

from typing import Literal

from pymcfunc.nbt import Float, Int, Double, NBT, Compound


class RangeJson:
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

    def json(self) -> dict:
        return {'min': self.min, 'max': self.max}

class FloatRangeJson(RangeJson): pass
class IntRangeJson(RangeJson): pass
class DoubleRangeJson(RangeJson): pass

class DamageJson:
    def __init__(self, **kwargs):
        self.blocked: bool | None = None
        self.dealt: float | DoubleRangeJson | None = None
        self.source_entity: EntityJson | None = None
        self.taken: float | DoubleRangeJson | None = None
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
        self.distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRangeJson] | None = None
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
            self.amplifier: int | IntRangeJson | None = None
            self.duration: int | IntRangeJson | None = None
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
        def __init__(self, **kwargs):
            self.looking_at: EntityJson | None = None
            self.advancements: dict[str, bool | dict[str, bool]] | None = None
            self.gamemode: Literal["survival", "adventure", "creative", "spectator"] | None = None
            self.level: int | IntRangeJson | None = None
            self.recipes: dict[str, bool] | None = None
            self.stats: list[EntityJson.Player.Statistic] | None = None

            for k, v in kwargs.items(): setattr(self, k, v)

        class Statistic:
            def __init__(self, **kwargs):
                self.type: Literal["minecraft:custom", "minecraft:crafted", "minecraft:used", "minecraft:broken",
                                   "minecraft:mined", "minecraft:killed", "minecraft:picked_up", "minecraft:dropped",
                                   "minecraft:killed_by"] | None = None
                self.stat: str | None = None
                self.value: int | IntRangeJson | None = None

                for k, v in kwargs.items(): setattr(self, k, v)

            def json(self) -> dict:
                d: dict = {}
                for attr in ['type', 'stat', 'value']:
                    if getattr(self, attr) is not None:
                        d[attr] = getattr(self, attr)
                        if 'json' in dir(d[attr]):
                            d[attr] = d[attr].json()
                return d

        def json(self) -> dict:
            d: dict = {}
            for attr in ['looking_at', 'advancements', 'gamemode', 'level', 'recipes', 'stats']:
                if getattr(self, attr) is not None:
                    d[attr] = getattr(self, attr)
                    if 'json' in dir(d[attr]):
                        d[attr] = d[attr].json()
                    if isinstance(d[attr], list):
                        for i, item in enumerate(d[attr]):
                            if 'json' in dir(item):
                                d[attr][i] = item.json()
            return d

    class LightningBolt:
        def __init__(self, **kwargs):
            self.blocks_set_on_fire: int | None = None
            self.entity_struck: EntityJson | None = None

            for k, v in kwargs.items(): setattr(self, k, v)
            
        def json(self) -> dict:
            d: dict = {}
            for attr in ['blocks_set_on_fire', 'entity_struck']:
                if getattr(self, attr) is not None:
                    d[attr] = getattr(self, attr)
                    if 'json' in dir(d[attr]):
                        d[attr] = d[attr].json()
            return d
        
    def json(self) -> dict:
        d: dict = {}
        for attr in ['distance', 'effects', 'equipment', 'flags', 'lightning_bolt', 'location', 'nbt', 'passenger',
                     'player', 'stepping_on', 'team', 'type', 'targeted_entity', 'vehicle',
                     'fishing_hook_in_open_water']:
            if getattr(self, attr) is not None:
                if attr == 'effects':
                    d[attr] = {e.name: e.json for e in getattr(self, attr)}
                    continue
                elif attr == 'fishing_hook_in_open_water':
                    d['fishing_hook'] = {'in_open_water': getattr(self, attr)}
                    continue
                d[attr] = getattr(self, attr)
                if 'json' in dir(d[attr]):
                    d[attr] = d[attr].json()
                if isinstance(d[attr], list):
                    for i, item in enumerate(d[attr]):
                        if 'json' in dir(item):
                            d[attr][i] = item.json()
                elif isinstance(d[attr], dict):
                    for k, v in d[attr]:
                        if 'json' in dir(v):
                            d[attr][k] = v.json()
        return d

class LocationJson:
    def __init__(self, **kwargs):
        self.biome: str | None = None
        self.block: LocationJson.Block | None = None
        self.dimension: str | None = None
        self.feature: str | None = None
        self.fluid: LocationJson.Fluid | None = None
        self.light: int | IntRangeJson | None = None
        self.position: dict[Literal["x", "y", "z"], float | DoubleRangeJson] | None = None
        self.smokey: bool | None = None

        for k, v in kwargs.items(): setattr(self, k, v)

    class Block:
        def __init__(self, **kwargs):
            self.blocks: list[str] | None = None
            self.tag: str | None = None
            self.nbt: Compound | None = None
            self.state: dict[str, str | int | bool | IntRangeJson] | None = None

            for k, v in kwargs.items(): setattr(self, k, v)

        def json(self) -> dict:
            d: dict = {}
            for attr in ['blocks', 'tag', 'nbt', 'state']:
                if getattr(self, attr) is not None:
                    d[attr] = getattr(self, attr)
                    if 'json' in dir(d[attr]):
                        d[attr] = d[attr].json()
                    if isinstance(d[attr], dict):
                        for k, v in d[attr]:
                            if 'json' in dir(v):
                                d[attr][k] = v.json()
                    elif isinstance(d[attr], Compound):
                        d[attr] = str(d[attr])
            return d

    class Fluid:
        def __init__(self, **kwargs):
            self.fluid: str | None = None
            self.state: dict[str, str | int | bool | IntRangeJson] | None = None

            for k, v in kwargs.items(): setattr(self, k, v)

        def json(self) -> dict:
            d: dict = {}
            for attr in ['fluid', 'state']:
                if getattr(self, attr) is not None:
                    d[attr] = getattr(self, attr)
                    if 'json' in dir(d[attr]):
                        d[attr] = d[attr].json()
                    if isinstance(d[attr], dict):
                        for k, v in d[attr]:
                            if 'json' in dir(v):
                                d[attr][k] = v.json()
            return d

    def json(self) -> dict:
        d: dict = {}
        for attr in ['biome', 'block', 'dimension', 'feature', 'fluid', 'light', 'position', 'smokey']:
            if getattr(self, attr) is not None:
                d[attr] = getattr(self, attr)
                if 'json' in dir(d[attr]):
                    d[attr] = d[attr].json()
                if isinstance(d[attr], dict):
                    for k, v in d[attr]:
                        if 'json' in dir(v):
                            d[attr][k] = v.json()
        return d

class ItemJson:
    def __init__(self, **kwargs):
        self.count: int | IntRangeJson | None = None
        self.durability: int | IntRangeJson | None = None
        self.enchantments: list[ItemJson.Enchantment] | None = None
        self.stored_enchantments: list[ItemJson.Enchantment] | None = None
        self.items: list[str] | None = None
        self.nbt: Compound | None = None
        self.potion: str | None = None
        self.tag: str | None = None

        for k, v in kwargs.items(): setattr(self, k, v)

    class Enchantment:
        def __init__(self, **kwargs):
            self.enchantment: str | None = None
            self.levels: int | IntRangeJson | None = None

            for k, v in kwargs.items(): setattr(self, k, v)

        def json(self) -> dict:
            d: dict = {}
            for attr in ['enchantment', 'levels']:
                if getattr(self, attr) is not None:
                    d[attr] = getattr(self, attr)
                    if 'json' in dir(d[attr]):
                        d[attr] = d[attr].json()
            return d

    def json(self) -> dict:
        d: dict = {}
        for attr in ['count', 'durability', 'enchantments', 'stored_enchantments', 'items', 'nbt', 'potion', 'tag']:
            if getattr(self, attr) is not None:
                d[attr] = getattr(self, attr)
                if 'json' in dir(d[attr]):
                    d[attr] = d[attr].json()
                if isinstance(d[attr], list):
                    for i, item in enumerate(d[attr]):
                        if 'json' in dir(item):
                            d[attr][i] = item.json()
        return d

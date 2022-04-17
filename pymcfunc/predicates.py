from __future__ import annotations

from typing import Literal, Union, Optional

from attr import define

from pymcfunc.command import ResourceLocation
from pymcfunc.internal import base_class
from pymcfunc.json_format import DamageJson, IntRangeJson, NumberProviderRangeJson, LocationJson, ItemJson
from pymcfunc.nbt import NBTFormat, String, Int, Float, Boolean, List
from pymcfunc.number_providers import NumberProvider


@define(init=True)
@base_class
class Predicate(NBTFormat):
    condition: str = property(lambda self: "")

    NBT_FORMAT = {
        "condition": String
    }

@define(init=True)
class AlternativePredicate(Predicate):
    condition = property(lambda self: "alternative")
    terms: list[Predicate]

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "conditions": String,
        "terms": list[Predicate]
    }

@define(init=True)
class BlockStatePropertyPredicate(Predicate):
    condition = property(lambda self: "block_state_property")
    block: str
    properties: dict[str, str]

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "conditions": String,
        "block": String,
        "properties": dict[str, String]
    }

@define(init=True)
class DamageSourcePropertiesPredicate(Predicate):
    condition = property(lambda self: "damage_source_properties")
    predicate: DamageJson

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "predicate": DamageJson
    }

@define(init=True)
class EntityPropertiesPredicate(Predicate):
    condition = property(lambda self: "entity_properties")
    entity: Literal["this", "killer", "killer_player"]
    predicate: DamageJson

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "entity": Literal["this", "killer", "killer_player"],
        "predicate": DamageJson
    }

@define(init=True)
class EntityScoresPredicate(Predicate):
    condition = property(lambda self: "entity_scores")
    entity: Literal["this", "killer", "killer_player"]
    scores: dict[str, int | IntRangeJson | NumberProviderRangeJson]

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "entity": Literal["this", "killer", "killer_player"],
        "scores": dict[str, Union[Int, IntRangeJson, NumberProviderRangeJson]]
    }

@define(init=True)
class InvertedPredicate(Predicate):
    condition = property(lambda self: "inverted")
    term: Predicate

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "term": Predicate
    }

@define(init=True)
class KilledByPlayerPredicate(Predicate):
    condition = property(lambda self: "killed_by_player")
    inverse: bool

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "inverse": Boolean
    }

@define(init=True)
class LocationCheckPredicate(Predicate):
    condition = property(lambda self: "location_check")
    offsetX: int
    offsetY: int
    offsetZ: int
    predicate: LocationJson

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "offsetX": Int,
        "offsetY": Int,
        "offsetZ": Int,
        "predicate": LocationJson
    }

@define(init=True)
class MatchToolPredicate(Predicate):
    condition = property(lambda self: "match_tool")
    predicate: ItemJson

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "predicate": ItemJson
    }

@define(init=True)
class RandomChancePredicate(Predicate):
    condition = property(lambda self: "random_chance")
    chance: float

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "chance": Float
    }

@define(init=True)
class RandomChanceWithLootingPredicate(Predicate):
    condition = property(lambda self: "random_chance_with_looting")
    chance: float
    looting_multiplier: float

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "chance": Float,
        "looting_multiplier": Float,
    }

@define(init=True)
class ReferencePredicate(Predicate):
    condition = property(lambda self: "reference")
    reference: ResourceLocation | Predicate

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "reference": String
    }

@define(init=True)
class SurvivesExplosionPredicate(Predicate):
    condition = property(lambda self: "survives_explosion")

@define(init=True)
class TableBonusPredicate(Predicate):
    condition = property(lambda self: "table_bonus")
    enchantment: int
    chances: list[float]

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "enchantment": Int,
        "chances": List[Float]
    }

@define(init=True)
class TimeCheckPredicate(Predicate):
    condition = property(lambda self: "time_check")
    value: int | IntRangeJson | NumberProviderRangeJson
    period: int | None = None

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "value": Union[Int, IntRangeJson, NumberProviderRangeJson],
        "period": Optional[Int]
    }

@define(init=True)
class ValueCheckPredicate(Predicate):
    condition = property(lambda self: "value_check")
    value: int | NumberProvider
    range: int | IntRangeJson | NumberProviderRangeJson

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "value": Union[Int, NumberProvider],
        "range": Union[Int, IntRangeJson, NumberProviderRangeJson]
    }

@define(init=True)
class WeatherCheckPredicate(Predicate):
    condition = property(lambda self: "weather_check")
    raining: bool
    thundering: bool

    NBT_FORMAT = {
        **Predicate.NBT_FORMAT,
        "raining": Boolean,
        "thundering": Boolean
    }

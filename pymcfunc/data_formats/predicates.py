from __future__ import annotations

from typing import Literal, Union, Optional

from attr import s

from pymcfunc.command import ResourceLocation
from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.data_formats.json_formats import DamageJson, IntRangeJson, NumberProviderRangeJson, LocationJson, ItemJson
from pymcfunc.data_formats.number_providers import NumberProvider
from pymcfunc.internal import base_class


@s(kw_only=True, init=True)
@base_class
class Predicate(JsonFormat):
    condition: str = property(lambda self: "")

    JSON_FORMAT = {
        "condition": str
    }

@s(kw_only=True, init=True)
class AlternativePredicate(Predicate):
    condition = property(lambda self: "alternative")
    terms: list[Predicate]

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "conditions": str,
        "terms": list[Predicate]
    }

@s(kw_only=True, init=True)
class BlockStatePropertyPredicate(Predicate):
    condition = property(lambda self: "block_state_property")
    block: str
    properties: dict[str, str]

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "conditions": str,
        "block": str,
        "properties": dict[str, str]
    }

@s(kw_only=True, init=True)
class DamageSourcePropertiesPredicate(Predicate):
    condition = property(lambda self: "damage_source_properties")
    predicate: DamageJson

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "predicate": DamageJson
    }

@s(kw_only=True, init=True)
class EntityPropertiesPredicate(Predicate):
    condition = property(lambda self: "entity_properties")
    entity: Literal["this", "killer", "killer_player"]
    predicate: DamageJson

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "entity": Literal["this", "killer", "killer_player"],
        "predicate": DamageJson
    }

@s(kw_only=True, init=True)
class EntityScoresPredicate(Predicate):
    condition = property(lambda self: "entity_scores")
    entity: Literal["this", "killer", "killer_player"]
    scores: dict[str, int | IntRangeJson | NumberProviderRangeJson]

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "entity": Literal["this", "killer", "killer_player"],
        "scores": dict[str, Union[int, IntRangeJson, NumberProviderRangeJson]]
    }

@s(kw_only=True, init=True)
class InvertedPredicate(Predicate):
    condition = property(lambda self: "inverted")
    term: Predicate

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "term": Predicate
    }

@s(kw_only=True, init=True)
class KilledByPlayerPredicate(Predicate):
    condition = property(lambda self: "killed_by_player")
    inverse: bool

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "inverse": bool
    }

@s(kw_only=True, init=True)
class LocationCheckPredicate(Predicate):
    condition = property(lambda self: "location_check")
    offsetX: int
    offsetY: int
    offsetZ: int
    predicate: LocationJson

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "offsetX": int,
        "offsetY": int,
        "offsetZ": int,
        "predicate": LocationJson
    }

@s(kw_only=True, init=True)
class MatchToolPredicate(Predicate):
    condition = property(lambda self: "match_tool")
    predicate: ItemJson

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "predicate": ItemJson
    }

@s(kw_only=True, init=True)
class RandomChancePredicate(Predicate):
    condition = property(lambda self: "random_chance")
    chance: float

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "chance": float
    }

@s(kw_only=True, init=True)
class RandomChanceWithLootingPredicate(Predicate):
    condition = property(lambda self: "random_chance_with_looting")
    chance: float
    looting_multiplier: float

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "chance": float,
        "looting_multiplier": float,
    }

@s(kw_only=True, init=True)
class ReferencePredicate(Predicate):
    condition = property(lambda self: "reference")
    reference: ResourceLocation | Predicate

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "reference": str
    }

@s(kw_only=True, init=True)
class SurvivesExplosionPredicate(Predicate):
    condition = property(lambda self: "survives_explosion")

@s(kw_only=True, init=True)
class TableBonusPredicate(Predicate):
    condition = property(lambda self: "table_bonus")
    enchantment: int
    chances: list[float]

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "enchantment": int,
        "chances": list[float]
    }

@s(kw_only=True, init=True)
class TimeCheckPredicate(Predicate):
    condition = property(lambda self: "time_check")
    value: int | IntRangeJson | NumberProviderRangeJson
    period: int | None = None

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "value": Union[int, IntRangeJson, NumberProviderRangeJson],
        "period": Optional[int]
    }

@s(kw_only=True, init=True)
class ValueCheckPredicate(Predicate):
    condition = property(lambda self: "value_check")
    value: int | NumberProvider
    range: int | IntRangeJson | NumberProviderRangeJson

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "value": Union[int, NumberProvider],
        "range": Union[int, IntRangeJson, NumberProviderRangeJson]
    }

@s(kw_only=True, init=True)
class WeatherCheckPredicate(Predicate):
    condition = property(lambda self: "weather_check")
    raining: bool
    thundering: bool

    JSON_FORMAT = {
        **Predicate.JSON_FORMAT,
        "raining": bool,
        "thundering": bool
    }

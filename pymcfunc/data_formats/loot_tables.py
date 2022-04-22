from __future__ import annotations

from typing import Union, Optional

from attr import s

from pymcfunc.command import ResourceLocation
from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.data_formats.item_modifiers import ItemModifier
from pymcfunc.data_formats.number_providers import NumberProvider
from pymcfunc.data_formats.predicates import Predicate
from pymcfunc.internal import base_class


@s(kw_only=True, init=True)
@base_class
class Entry(JsonFormat):
    conditions: list[Predicate]
    functions: list[ItemModifier]
    type = property(lambda self: "")
    weight: int
    quality: int

    JSON_FORMAT = {
        "conditions": list[Predicate],
        "functions": list[ItemModifier],
        "type": str,
        "weight": int,
        "quality": int
    }

@s(kw_only=True, init=True)
class ItemEntry(Entry):
    type = property(lambda self: "item")
    name: ResourceLocation

    JSON_FORMAT = {
        **Entry.JSON_FORMAT,
        "name": str
    }

@s(kw_only=True, init=True)
class TagEntry(Entry):
    type = property(lambda self: "tag")
    name: ResourceLocation
    expand: bool

    JSON_FORMAT = {
        **Entry.JSON_FORMAT,
        "name": str,
        "expand": bool
    }

@s(kw_only=True, init=True)
class LootTableEntry(JsonFormat):
    type = property(lambda self: "loot_table")
    name: ResourceLocation | LootTable

    JSON_FORMAT = {
        **Entry.JSON_FORMAT,
        "type": str,
        "name": str
    }

@s(kw_only=True, init=True)
@base_class
class ChildrenEntry(JsonFormat):
    children: list[Entry]

    JSON_FORMAT = {
        **Entry.JSON_FORMAT,
        "type": str,
        "children": list[Entry]
    }

@s(kw_only=True, init=True)
class GroupEntry(ChildrenEntry):
    type = property(lambda self: "group")

@s(kw_only=True, init=True)
class AlternativesEntry(ChildrenEntry):
    type = property(lambda self: "alternatives")

@s(kw_only=True, init=True)
class SequenceEntry(ChildrenEntry):
    type = property(lambda self: "group")

@s(kw_only=True, init=True)
class DynamicEntry(Entry):
    type = property(lambda self: "dynamic")
    name: str

    JSON_FORMAT = {
        **ChildrenEntry.JSON_FORMAT,
        "type": str,
        "name": str,
    }

@s(kw_only=True, init=True)
class EmptyEntry(Entry):
    type = property(lambda self: "empty")

    JSON_FORMAT = {
        **Entry.JSON_FORMAT
    }

@s(kw_only=True, init=True)
class Pool(JsonFormat):
    conditions: list[Predicate]
    functions: list[ItemModifier]
    rolls: int | NumberProvider
    bonus_rolls: float | NumberProvider
    entries: list[Entry]

    JSON_FORMAT = {
        "conditions": list[Predicate],
        "functions": list[ItemModifier],
        "rolls": Union[int, NumberProvider],
        "bonus_rolls": Union[float, NumberProvider],
        "entries": list[str]
    }

@s(kw_only=True, init=True)
@base_class
class LootTable(JsonFormat):
    functions: list[ItemModifier]
    pools: list[Pool]
    type: str | None = None

    JSON_FORMAT = {
        "type": Optional[str],
        "functions": list[ItemModifier],
        "pools": list[Pool]
    }
from __future__ import annotations

from typing import Union, Optional

from attr import define

from pymcfunc.command import ResourceLocation
from pymcfunc.internal import base_class
from pymcfunc.item_modifiers import ItemModifier
from pymcfunc.nbt import NBTFormat, List, String, Int, Float, Boolean
from pymcfunc.number_providers import NumberProvider
from pymcfunc.predicates import Predicate


@define(init=True)
@base_class
class Entry(NBTFormat):
    conditions: list[Predicate]
    functions: list[ItemModifier]
    type = property(lambda self: "")
    weight: int
    quality: int

    NBT_FORMAT = {
        "conditions": List[Predicate],
        "functions": List[ItemModifier],
        "type": String,
        "weight": Int,
        "quality": Int
    }

@define(init=True)
class ItemEntry(Entry):
    type = property(lambda self: "item")
    name: ResourceLocation

    NBT_FORMAT = {
        **Entry.NBT_FORMAT,
        "name": String
    }

@define(init=True)
class TagEntry(Entry):
    type = property(lambda self: "tag")
    name: ResourceLocation
    expand: bool

    NBT_FORMAT = {
        **Entry.NBT_FORMAT,
        "name": String,
        "expand": Boolean
    }

@define(init=True)
class LootTableEntry(NBTFormat):
    type = property(lambda self: "loot_table")
    name: ResourceLocation | LootTable

    NBT_FORMAT = {
        **Entry.NBT_FORMAT,
        "type": String,
        "name": String
    }

@define(init=True)
@base_class
class ChildrenEntry(NBTFormat):
    children: list[Entry]

    NBT_FORMAT = {
        **Entry.NBT_FORMAT,
        "type": String,
        "children": list[Entry]
    }

@define(init=True)
class GroupEntry(ChildrenEntry):
    type = property(lambda self: "group")

@define(init=True)
class AlternativesEntry(ChildrenEntry):
    type = property(lambda self: "alternatives")

@define(init=True)
class SequenceEntry(ChildrenEntry):
    type = property(lambda self: "group")

@define(init=True)
class DynamicEntry(Entry):
    type = property(lambda self: "dynamic")
    name: str

    NBT_FORMAT = {
        **ChildrenEntry.NBT_FORMAT,
        "type": String,
        "name": String,
    }

@define(init=True)
class EmptyEntry(Entry):
    type = property(lambda self: "empty")

    NBT_FORMAT = {
        **Entry.NBT_FORMAT
    }

@define(init=True)
class Pool(NBTFormat):
    conditions: list[Predicate]
    functions: list[ItemModifier]
    rolls: int | NumberProvider
    bonus_rolls: float | NumberProvider
    entries: list[Entry]

    NBT_FORMAT = {
        "conditions": List[Predicate],
        "functions": List[ItemModifier],
        "rolls": Union[Int, NumberProvider],
        "bonus_rolls": Union[Float, NumberProvider],
        "entries": List[String]
    }

@define(init=True)
@base_class
class LootTable(NBTFormat):
    functions: list[ItemModifier]
    pools: list[Pool]
    type: str | None = None

    NBT_FORMAT = {
        "type": Optional[String],
        "functions": List[ItemModifier],
        "pools": List[Pool]
    }
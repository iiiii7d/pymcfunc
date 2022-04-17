from __future__ import annotations

from typing import Union

from attr import define, field

from pymcfunc.command import ResourceLocation
from pymcfunc.internal import base_class
from pymcfunc.nbt import NBTFormat, List, String, Int, Float, Boolean
from pymcfunc.number_providers import NumberProvider

ItemModifier = str
Predicate = str

@define(init=True)
@base_class
class Entry(NBTFormat):
    conditions: list[Predicate]
    functions: list[ItemModifier]
    type: str = field(init=False)
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
    type: str = "item"
    name: ResourceLocation

    NBT_FORMAT = {
        **Entry.NBT_FORMAT,
        "name": String
    }

@define(init=True)
class TagEntry(Entry):
    type: str = "tag"
    name: ResourceLocation
    expand: bool

    NBT_FORMAT = {
        **Entry.NBT_FORMAT,
        "name": String,
        "expand": Boolean
    }

@define(init=True)
class LootTableEntry(NBTFormat):
    type: str = "loot_table"
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
    type: str = "group"

@define(init=True)
class AlternativesEntry(ChildrenEntry):
    type: str = "alternatives"

@define(init=True)
class SequenceEntry(ChildrenEntry):
    type: str = "group"

@define(init=True)
class DynamicEntry(Entry):
    type: str = "dynamic"
    name: str

    NBT_FORMAT = {
        **ChildrenEntry.NBT_FORMAT,
        "type": String,
        "name": String,
    }

@define(init=True)
class EmptyEntry(Entry):
    type: str = "empty"

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
    type: str = field(init=False)
    functions: list[ItemModifier]
    pools: list[Pool]

    NBT_FORMAT = {
        "type": String,
        "functions": List[ItemModifier],
        "pools": List[Pool]
    }
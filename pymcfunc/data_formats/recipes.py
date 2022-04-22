from __future__ import annotations

from typing import Optional, Union, Sequence, Literal

from attr import s

from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.data_formats.nbt import Compound, DictReprAsList
from pymcfunc.internal import base_class, immutable


@s(kw_only=True, init=True)
@base_class
class Recipe(JsonFormat):
    name: str
    namespace: str
    type = property(lambda self: "")

    @property
    def namespaced(self) -> str: return f'{self.namespace}:{self.name}'

    NBT_FORMAT = {
        'type': str
    }

@s(kw_only=True, init=True)
@base_class
class GroupedRecipe(Recipe):
    group: str | None = None

    NBT_FORMAT = {
        'type': str,
        'group': Optional[str],
    }

@s(kw_only=True, init=True)
@base_class
class CookingRecipe(GroupedRecipe):
    ingredient: Ingredient | list[Ingredient]
    result: str
    experience: float
    cookingtime: int | None = None

    @s(kw_only=True, init=True)
    class Ingredient(JsonFormat):
        item: str
        tag: str

        JSON_FORMAT = {
            'item': str,
            'tag': str,
        }

    NBT_FORMAT = {
        **GroupedRecipe.NBT_FORMAT,
        'ingredient': Union[Ingredient, list[Ingredient]],
        'result': str,
        'experience': float,
        'cookingtime': Optional[int],
    }


@s(kw_only=True, init=True)
class BlastingRecipe(CookingRecipe):
    type = property(lambda self: "blasting")

@s(kw_only=True, init=True)
class CampfireCookingRecipe(CookingRecipe):
    type = property(lambda self: "campfire_cooking")

@s(kw_only=True, init=True)
@base_class
class CraftingRecipe(GroupedRecipe):
    result: Result

    @s(kw_only=True, init=True)
    class Result(JsonFormat):
        item: str
        count: int = 1

        JSON_FORMAT = {
            **GroupedRecipe.NBT_FORMAT,
            'count': int,
            'item': str,
        }

    @immutable
    class Key(JsonFormat):
        key: str
        item: str | None = None
        tag: str | None = None

        def __init__(self, key: str, *,
                     item: str | None = None, tag: str | None = None):
            if len(key) != 1: raise ValueError("Key must be of a single character")
            if item is not None:
                self.item = item
            else:
                self.tag = tag
            self.key = key

        JSON_FORMAT = {
            'item': Optional[str],
            'tag': Optional[str],
        }

    @immutable
    class KeyGroup(JsonFormat):
        key: str
        values: list[CraftingRecipe.Key]

        def __init__(self, key: str, items: Optional[Sequence[str]] = None, tags: Optional[Sequence[str]] = None):
            if len(key) != 1: raise ValueError("Key must be of a single character")
            self.values = []
            if items is not None:
                for item in items:
                    self.values.append(CraftingRecipe.Key(key, item=item))
            if tags is not None:
                for tag in tags:
                    self.values.append(CraftingRecipe.Key(key, tag=tag))
            self.key = key

        def as_json(self) -> list[dict]:
            return [a.as_json() for a in self.values]

@s(kw_only=True, init=True)
class CraftingShapedRecipe(CraftingRecipe):
    type = property(lambda self: "crafting_shaped")
    _pattern: list[str]
    key: list[CraftingRecipe.Key | CraftingRecipe.KeyGroup]

    @property
    def pattern(self) -> list[str]: return self._pattern
    @pattern.setter
    def pattern(self, value: tuple[tuple[CraftingRecipe.Key | CraftingRecipe.KeyGroup,
                                         CraftingRecipe.Key | CraftingRecipe.KeyGroup,
                                         CraftingRecipe.Key | CraftingRecipe.KeyGroup],
                                   tuple[CraftingRecipe.Key | CraftingRecipe.KeyGroup,
                                         CraftingRecipe.Key | CraftingRecipe.KeyGroup,
                                         CraftingRecipe.Key | CraftingRecipe.KeyGroup],
                                   tuple[CraftingRecipe.Key | CraftingRecipe.KeyGroup,
                                         CraftingRecipe.Key | CraftingRecipe.KeyGroup,
                                         CraftingRecipe.Key | CraftingRecipe.KeyGroup]]) -> None:
        self._pattern = [''.join(a.key for a in row for row in col) for col in value]
        self.key = list({*value[0], *value[1], *value[2]})

    JSON_FORMAT = {
        **CraftingRecipe.NBT_FORMAT,
        'pattern': list[str],
        'key': DictReprAsList[CraftingRecipe.Key | CraftingRecipe.KeyGroup]
    }

@s(kw_only=True, init=True)
class CraftingShapelessRecipe(CraftingRecipe):
    type = property(lambda self: "crafting_shapeless")
    ingredients: list[CraftingRecipe.Key | CraftingRecipe.KeyGroup]

    JSON_FORMAT = {
        **CraftingRecipe.NBT_FORMAT,
        'ingredients': list[Compound],
    }

@s(kw_only=True, init=True)
class CraftingSpecialRecipe(Recipe):
    special_type: Literal['armordye', 'bannerduplicate', 'bookcloning', 'fireworks_rocket', 'fireworks_star',
                          'fireworks_star_fade', 'mapcloning', 'mapextending', 'repairitem', 'shielddecoration',
                          'shulkerboxcoloring', 'tippedarrow', 'suspiciousstew']

    @property
    def type(self) -> str: return "crafting_special_"+self.special_type


@s(kw_only=True, init=True)
class SmeltingRecipe(CookingRecipe):
    type = property(lambda self: "smelting")

@s(kw_only=True, init=True)
class SmithingRecipe(GroupedRecipe):
    base: Item
    addition: Item
    result: Item

    @immutable
    class Item(JsonFormat):
        item: str | None = None
        tag: str | None = None

        def __init__(self, *,
                     item: str | None = None, tag: str | None = None):
            if item is not None:
                self.item = item
            else:
                self.tag = tag

        JSON_FORMAT = {
            'item': Optional[str],
            'tag': Optional[str],
        }

    JSON_FORMAT = {
        **GroupedRecipe.NBT_FORMAT,
        'base': Item,
        'addition': Item,
        'result': Item,
    }

@s(kw_only=True, init=True)
class SmokingRecipe(CookingRecipe):
    type = property(lambda self: "smoking")


@s(kw_only=True, init=True)
class StonecuttingRecipe(CraftingRecipe):
    ingredient: CraftingRecipe.Key | list[CraftingRecipe.Key]
    result: str
    count: int

    JSON_FORMAT = {
        **CraftingRecipe.NBT_FORMAT,
        'ingredient': Union[CraftingRecipe.Key, list[CraftingRecipe.Key]],
        'result': str,
        'count': int,
    }
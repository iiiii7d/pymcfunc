from __future__ import annotations

from typing import Optional, Union, Sequence, Literal

from attr import define, field

from pymcfunc.internal import base_class, immutable
from pymcfunc.nbt import NBTFormat, String, Double, Int, Compound, List, DictReprAsList


@define(init=True)
@base_class
class Recipe(NBTFormat):
    name: str
    namespace: str
    type: str = field(init=False)

    @property
    def namespaced(self) -> str: return f'{self.namespace}:{self.name}'

    NBT_FORMAT = {
        'type': String
    }

@define(init=True)
@base_class
class GroupedRecipe(Recipe):
    group: str | None = None

    NBT_FORMAT = {
        'type': String,
        'group': Optional[String],
    }

@define(init=True)
@base_class
class CookingRecipe(GroupedRecipe):
    ingredient: Ingredient | list[Ingredient]
    result: str
    experience: float
    cookingtime: int | None = None

    @define(init=True)
    class Ingredient(NBTFormat):
        item: str
        tag: str

        NBT_Format = {
            'item': String,
            'tag': String,
        }

    NBT_FORMAT = {
        **GroupedRecipe.NBT_FORMAT,
        'ingredient': Union[Ingredient, list[Ingredient]],
        'result': String,
        'experience': Double,
        'cookingtime': Optional[Int],
    }


@define(init=True)
class BlastingRecipe(CookingRecipe):
    type: str = 'blasting'

@define(init=True)
class CampfireCookingRecipe(CookingRecipe):
    type: str = 'campfire_cooking'

@define(init=True)
@base_class
class CraftingRecipe(GroupedRecipe):
    result: Result

    @define(init=True)
    class Result(NBTFormat):
        count: int = 1
        item: str

        NBT_Format = {
            **GroupedRecipe.NBT_FORMAT,
            'count': Int,
            'item': String,
        }

    @immutable
    class Key(NBTFormat):
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

        NBT_Format = {
            'item': Optional[String],
            'tag': Optional[String],
        }

    @immutable
    class KeyGroup(NBTFormat):
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

        def as_nbt(self) -> List[Compound]:
            return List[Compound](a.as_nbt() for a in self.values)

@define(init=True)
class CraftingShapedRecipe(CraftingRecipe):
    type: str = 'crafting_shaped'
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

    NBT_Format = {
        **CraftingRecipe.NBT_FORMAT,
        'pattern': List[String],
        'key': DictReprAsList[CraftingRecipe.Key | CraftingRecipe.KeyGroup]
    }

@define(init=True)
class CraftingShapelessRecipe(CraftingRecipe):
    type: str = 'crafting_shapeless'
    ingredients: list[CraftingRecipe.Key | CraftingRecipe.KeyGroup]

    NBT_Format = {
        **CraftingRecipe.NBT_FORMAT,
        'ingredients': List[Compound],
    }

@define(init=True)
class CraftingSpecialRecipe(Recipe):
    special_type: Literal['armordye', 'bannerduplicate', 'bookcloning', 'fireworks_rocket', 'fireworks_star',
                          'fireworks_star_fade', 'mapcloning', 'mapextending', 'repairitem', 'shielddecoration',
                          'shulkerboxcoloring', 'tippedarrow', 'suspiciousstew']

    @property
    def type(self) -> str: return "crafting_special_"+self.special_type


@define(init=True)
class SmeltingRecipe(CookingRecipe):
    type: str = 'smelting'

@define(init=True)
class SmithingRecipe(GroupedRecipe):
    base: Item
    addition: Item
    result: Item

    @immutable
    class Item(NBTFormat):
        item: str | None = None
        tag: str | None = None

        def __init__(self, *,
                     item: str | None = None, tag: str | None = None):
            if item is not None:
                self.item = item
            else:
                self.tag = tag

        NBT_Format = {
            'item': Optional[String],
            'tag': Optional[String],
        }

    NBT_Format = {
        **GroupedRecipe.NBT_FORMAT,
        'base': Item,
        'addition': Item,
        'result': Item,
    }

@define(init=True)
class SmokingRecipe(CookingRecipe):
    type: str = 'smoking'


@define(init=True)
class StonecuttingRecipe(CraftingRecipe):
    ingredient: CraftingRecipe.Key | list[CraftingRecipe.Key]
    result: str
    count: int

    NBT_Format = {
        **CraftingRecipe.NBT_FORMAT,
        'ingredient': Union[CraftingRecipe.Key, List[CraftingRecipe.Key]],
        'result': String,
        'count': Int,
    }
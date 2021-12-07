from typing import Optional, Tuple, Sequence, Union
import pymcfunc_old.internal as internal

class Recipe:
    """The base class for all Recipes.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.Recipe"""
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        self.p = p
        self.name = name
        self.namespaced = self.p.name + ":" + self.name
        self.p.recipes[name] = {
            "type_": type_
        }
        self.value = self.p.recipes[name]
        if group is not None: self.value['group'] = group

class CookingRecipe(Recipe):
    """A recipe for furnaces, blast furnaces, smokers and campfires.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.CookingRecipe"""
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['ingredient'] = []
        self.value['result'] = ""
        self.value['experience'] = 0

    def ingredient(self, item: Optional[str]=None, tag: Optional[str]=None):
        """Sets the ingredient of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.CookingRecipe.ingredient"""
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['ingredient'].append({'item': item})
        else:
            self.value['ingredient'].append({'tag': tag})

    def result(self, item: str):
        """Sets the result of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.CookingRecipe.result"""
        self.value['result'] = item

    def experience(self, exp: int):
        """Sets the amount of experience obtained from the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.CookingRecipe.experience"""
        self.value['experience'] = exp
    
    def cooking_time(self, time: int):
        """Sets the amount of cooking time the recipe would take.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.CookingRecipe.cooking_time"""
        self.value['cookingTime'] = time

class ShapedCraftingRecipe(Recipe):
    """A shaped recipe for crafting tables and inventory crafting.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapedCraftingRecipe"""
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['pattern'] = ['   ', '   ', '   ']
        self.value['key'] = {}
        self.value['result'] = {}

    class Key:
        """A key, or a representation of an item.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapedCraftingRecipe.Key"""
        def __init__(self, key: str, item: Optional[str]=None, tag: Optional[str]=None):
            internal.pick_one_arg(
                (item, None, 'item'),
                (tag, None, 'tag'),
                optional=False
            )
            if len(key) != 1: raise ValueError("Key must be of a single character")
            if item is not None:
                self.value = {'item': item}
            else:
                self.value = {'tag': tag}
            self.key = key

    class KeyGroup:
        """A group of keys, or a representation of a group of items.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapedCraftingRecipe.KeyGroup"""
        def __init__(self, key: str, items: Optional[Sequence[str]]=None, tags: Optional[Sequence[str]]=None):
            if len(key) != 1: raise ValueError("Key must be of a single character")
            self.values = []
            if items is not None:
                for item in items:
                    self.values.append({'item': item})
            if tags is not None:
                for tag in tags:
                    self.values.append({'tag': tag})
            self.key = key

    def pattern(self, pattern: Tuple[Tuple[Optional[Union[KeyGroup, Key]], Optional[Union[KeyGroup, Key]], Optional[Union[KeyGroup, Key]]],
                                     Tuple[Optional[Union[KeyGroup, Key]], Optional[Union[KeyGroup, Key]], Optional[Union[KeyGroup, Key]]],
                                     Tuple[Optional[Union[KeyGroup, Key]], Optional[Union[KeyGroup, Key]], Optional[Union[KeyGroup, Key]]]]):
        """Sets the pattern of the crafting recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapedCraftingRecipe.pattern"""
        keys = []
        for rown in range(3):
            col = []
            for elen in range(3):
                if pattern[rown][elen] is None:
                    col.append(" ")
                else:
                    col.append(pattern[rown][elen].key)
                    if pattern[rown][elen] not in keys:
                        keys.append(pattern[rown][elen])
            self.value['pattern'][rown] = ''.join(col)
        
        for key in keys:
            if isinstance(key, self.KeyGroup):
                self.value[key.key] = []
                for value in key.values:
                    self.value[key.key].append(value)
            else:
                self.value[key.key] = key.value

    def result(self, item: str, count: int=1):
        """Sets the result of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapedCraftingRecipe.result"""
        self.value['result'] = {"item": item}
        if count != 1: self.value['result']['count'] = count

class ShapelessCraftingRecipe(Recipe):
    """A shapeless recipe for crafting tables and inventory crafting.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapelessCraftingRecipe"""
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['ingredients'] = []
        self.value['result'] = {}

    def ingredient(self, item: Optional[str]=None, tag: Optional[str]=None):
        """Adds an ingredient to the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapelessCraftingRecipe.ingredient"""
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['ingredients'].append({'item': item})
        else:
            self.value['ingredients'].append({'tag': tag})

    def ingredient_group(self, items: Optional[Sequence[str]]=None, tags: Optional[Sequence[str]]=None):
        """Adds a group of ingredients to the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapelessCraftingRecipe.ingredient_group"""
        group = []
        if items is not None:
            for item in items: group.append({'item': item})
        if tags is not None:
            for tag in tags: group.append({'tag': tag})
        self.value['ingredients'].append(group)

    def result(self, item: str, count: int=1):
        """Sets the result of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ShapelessCraftingRecipe.result"""
        self.value['result'] = {"item": item}
        if count != 1: self.value['result']['count'] = count

class SmithingRecipe(Recipe):
    """A recipe for smithing tables.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.SmithingRecipe"""
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['base'] = {}
        self.value['addition'] = {}
        self.value['result'] = ""

    def base(self, item: Optional[str]=None, tag: Optional[str]=None):
        """Sets the base item of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.SmithingRecipe.base"""
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['base']['item'] = item
        else:
            self.value['base']['tag'] = tag

    def addition(self, item: Optional[str]=None, tag: Optional[str]=None):
        """Sets the additional item of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.SmithingRecipe.addition"""
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['addition']['item'] = item
        else:
            self.value['addition']['tag'] = tag

    def result(self, result: str):
        """Sets the result of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.SmithingRecipe.result"""
        self.value['result'] = result

class StonecuttingRecipe(Recipe):
    """A recipe for stonecutters.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.StonecuttingRecipe"""
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['ingredients'] = []

    def ingredient(self, item: Optional[str]=None, tag: Optional[str]=None):
        """Sets the ingredient of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.ingredient"""
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['ingredients'].append({'item': item})
        else:
            self.value['ingredients'].append({'tag': tag})

    def result(self, item: str, count: int=1):
        """Sets the result of the recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.recipes.result"""
        self.value['result'] = {'item': item, 'count': count}
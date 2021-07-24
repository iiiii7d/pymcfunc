from typing import Optional, Tuple, Sequence, Union
import pymcfunc.internal as internal

class Recipe:
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        self.p = p
        self.p.recipes[name] = {
            "type_": type_
        }
        self.value = self.p.recipes[name]
        if group is not None: self.value['group'] = group

class CookingRecipe(Recipe):
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['ingredient'] = []
        self.value['result'] = ""
        self.value['experience'] = 0

    def ingredient(self, item: Optional[str]=None, tag: Optional[str]=None):
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
        self.value['result'] = item

    def experience(self, exp: int):
        self.value['experience'] = exp
    
    def cooking_time(self, time: int):
        self.value['cookingTime'] = time

class ShapedCraftingRecipe(Recipe):
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['pattern'] = ['   ', '   ', '   ']
        self.value['key'] = {}
        self.value['result'] = {}

    class Key:
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

    def pattern(self, pattern: Tuple[Tuple[Union[KeyGroup, Key], Union[KeyGroup, Key], Union[KeyGroup, Key]],
                                     Tuple[Union[KeyGroup, Key], Union[KeyGroup, Key], Union[KeyGroup, Key]],
                                     Tuple[Union[KeyGroup, Key], Union[KeyGroup, Key], Union[KeyGroup, Key]]]):
        keys = []
        for rown in range(3):
            col = []
            for elen in range(3):
                col.append(pattern[rown][elen].key)
                self.value['pattern'][rown] = str(col)
                if pattern[rown][elen] not in keys:
                    keys.append(pattern[rown][elen])
        
        for key in keys:
            if isinstance(key, self.KeyGroup):
                self.value[key.key] = []
                for value in key.values:
                    self.value[key.key].append(value)
            else:
                self.value[key.key] = key.value

    def result(self, item: str, count: int=1):
        self.value['result'] = {"item": item}
        if count != 1: self.value['result']['count'] = count

class ShapelessCraftingRecipe(Recipe):
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['ingredients'] = []
        self.value['result'] = {}

    def ingredient(self, item: Optional[str]=None, tag: Optional[str]=None):
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
        group = []
        if items is not None:
            for item in items: group.append({'item': item})
        if tags is not None:
            for tag in tags: group.append({'tag': tag})
        self.value['ingredients'].append(group)

    def result(self, item: str, count: int=1):
        self.value['result'] = {"item": item}
        if count != 1: self.value['result']['count'] = count

class SmithingRecipe(Recipe):
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['base'] = {}
        self.value['addition'] = {}
        self.value['result'] = ""

    def base(self, item: Optional[str]=None, tag: Optional[str]=None):
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['base'].append({'item': item})
        else:
            self.value['base'].append({'tag': tag})

    def addition(self, item: Optional[str]=None, tag: Optional[str]=None):
        internal.pick_one_arg(
            (item, None, 'item'),
            (tag, None, 'tag'),
            optional=False
        )
        if item is not None:
            self.value['addition'].append({'item': item})
        else:
            self.value['addition'].append({'tag': tag})

    def result(self, result: str):
        self.value['result'] = result

class StonecuttingRecipe(Recipe):
    def __init__(self, p, name: str, type_: str, group: Optional[str]=None):
        super().__init__(p, name, type_, group)
        self.value['ingredient'] = []

    def ingredient(self, item: Optional[str]=None, tag: Optional[str]=None):
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
        self.value['result'] = {'item': item, 'count': count}
from typing import Optional
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
        self.value['ingredients'] = []
        self.value['result'] = ""
        self.value['experience'] = 0

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

    
        

from typing import Callable, Any, Optional, Union
from functools import wraps
import pathlib
import os
import json
import ntpath
import re

import pymcfunc_old.errors as errors
import pymcfunc_old.internal as internal
from pymcfunc_old.func_handlers import JavaFuncHandler, BedrockFuncHandler, UniversalFuncHandler
import pymcfunc.proxies.selectors as selectors
from pymcfunc_old.advancements import Advancement
from pymcfunc_old.loot_tables import LootTable
from pymcfunc_old.predicates import Predicate
from pymcfunc_old.recipes import CookingRecipe, ShapedCraftingRecipe, ShapelessCraftingRecipe, SmithingRecipe, StonecuttingRecipe, Recipe
from pymcfunc_old.item_modifiers import ItemModifier

class Pack:
    """A container for all functions.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack"""

    def __init__(self, name: str, edition: str="j"):
        internal.options(edition, ['j', 'b'])
        if edition not in ['j', 'b']:
            raise errors.OptionError(['j', 'b'], edition)
        self.edition = edition
        self.name = name
        self.funcs = {}
        self.tags = {'blocks': {}, 'entity_types': {}, 'fluids': {}, 'functions': {}, 'items': {}}
        self.minecraft_tags = {'load': [], 'tick': []}
        self.advancements = {}
        self.loot_tables = {}
        self.predicates = {}
        self.recipes = {}
        self.item_modifiers = {}
        self.sel = selectors.BedrockSelectors() if edition == "b" else selectors.JavaSelectors()
        if edition == 'j':
            self.t = JavaFunctionTags(self)

    def tag(self, group: str, tag_name: str, *items: str):
        """Adds items to a tag.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.tag"""
        internal.options(group, ['blocks', 'entity_types', 'fluids', 'functions', 'items'])
        if tag_name not in self.tags[group]:
            self.tags[group][tag_name] = []
        self.tags[group][tag_name].extend(list(items))

    def function(self, func: Callable[[UniversalFuncHandler], Any]):
        """Registers a Python function and translates it into a Minecraft function.    
        The decorator will run the function so you do not need to run the function again.
        The name of the Python function will be the name of the Minecraft function.
        The decorator calls the function being decorated with one argument being a PackageHandler.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.function"""
        m = JavaFuncHandler() if self.edition == 'j' else BedrockFuncHandler()
        func(m)
        fname = func.__name__
        self.funcs.update({fname: str(m)})

    def advancement(self, name: str, parent: Union[str, Advancement]) -> Advancement:
        """Registers and returns an advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.advancement"""
        if self.edition == 'b':
            raise TypeError('No advancements in Bedrock')
        return Advancement(self, name, parent)

    def loot_table(self, name: str, type_: Optional[str]=None) -> LootTable:
        """Registers and returns a loot table.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.loot_table"""
        if self.edition == 'b':
            raise TypeError('No loot tables in Bedrock')
        return LootTable(self, name, type_=type_)

    def predicate(self, name: str) -> Predicate:
        """Registers and returns a predicate.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.predicate"""
        if self.edition == 'b':
            raise TypeError('No predicates in Bedrock')
        return Predicate(self, name)

    def recipe(self, name: str, type_: str, group: Optional[str]=None) -> Recipe:
        """Registers and returns a recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.recipe"""
        if self.edition == 'b':
            raise TypeError('No recipes in Bedrock')
        internal.options(type_, ['blasting', 'campfire_cooking', 'crafting_shaped', 'crafting_shapeless', 'smelting', 'smithing', 'smoking', 'stonecutting'])
        r = None
        if type_ in ['blasting', 'campfire_cooking', 'smelting', 'smoking']: r = CookingRecipe
        elif type_ == "crafting_shaped": r = ShapedCraftingRecipe
        elif type_ == "crafting_shapeless": r = ShapelessCraftingRecipe
        elif type_ == "smithing": r = SmithingRecipe
        elif type_ == "stonecutting": r = StonecuttingRecipe
        return r(self, name, type_, group=group)

    def item_modifier(self, name: str) -> ItemModifier:
        """Registers and returns an item_modifier.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.item_modifier"""
        if self.edition == 'b':
            raise TypeError('No item modifiers in Bedrock')
        return ItemModifier(self, name)

    def import_function(self, directory: str):
        """Imports and registers a function.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.import_function"""
        name = re.sub(r"\.mcfunction$", "", ntpath.basename(directory))
        with open(directory) as f:
            self.funcs[name] = f.read()

    def import_advancement(self, directory: str):
        """Imports and registers an advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.import_advancement"""
        name = re.sub(r"\.json$", "", ntpath.basename(directory))
        with open(directory) as f:
            self.advancements[name] = json.load(f)

    def import_loot_table(self, directory: str):
        """Imports and registers a loot table.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.import_loot_table"""
        name = re.sub(r"\.json$", "", ntpath.basename(directory))
        with open(directory) as f:
            self.loot_tables[name] = json.load(f)

    def import_predicate(self, directory: str):
        """Imports and registers a predicate.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.import_predicate"""
        name = re.sub(r"\.json$", "", ntpath.basename(directory))
        with open(directory) as f:
            self.predicates[name] = json.load(f)

    def import_recipe(self, directory: str):
        """Imports and registers a recipe.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.import_recipe"""
        name = re.sub(r"\.json$", "", ntpath.basename(directory))
        with open(directory) as f:
            self.recipes[name] = json.load(f)

    def import_item_modifier(self, directory: str):
        """Imports and registers an item modifier.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.import_item_modifier"""
        name = re.sub(r"\.json$", "", ntpath.basename(directory))
        with open(directory) as f:
            self.item_modifiers[name] = json.load(f)

    def build(self, pack_format: int, description: str, datapack_folder: str='.', indent: int=2):
        """Builds the pack. Java Edition only.\n
        **Format numbering**
        * **4** - 1.13–1.14.4
        * **5** - 1.15–1.16.1
        * **6** - 1.16.2–1.16.5
        * **7** - 1.17\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.build"""
        if self.edition == 'b':
            raise TypeError('Cannot build Bedrock packs')
        name = self.name.lower()
        #create pack dir
        pathlib.Path(datapack_folder+'/'+self.name).mkdir(parents=True, exist_ok=True)
        os.chdir(datapack_folder+'/'+self.name)

        #make pack.mcmeta
        mcmeta = {
            'pack': {
                'pack_format': pack_format,
                'description': description
            }
        }
        with open('pack.mcmeta', 'w') as f:
            json.dump(mcmeta, f)

        #create data dir
        pathlib.Path(os.getcwd()+'/data/'+self.name).mkdir(parents=True, exist_ok=True)

        #minecraft tags
        if any([v != [] for v in self.minecraft_tags.values()]):
            pathlib.Path(os.getcwd()+f'/data/minecraft/tags/functions').mkdir(parents=True, exist_ok=True)
            for tag, funcs in self.minecraft_tags.items():
                if funcs:
                    tagJson = {
                        'values': [self.name+':'+i.lower() for i in funcs]
                    }
                    with open(os.getcwd()+f'/data/minecraft/tags/functions/{tag}.json', 'w') as f:
                        json.dump(tagJson, f, indent=indent)

        #cd to custom namespace
        os.chdir('data/'+self.name)

        #functions
        pathlib.Path(os.getcwd()+'/functions').mkdir(exist_ok=True)
        for k, v in self.funcs.items():
            funcName, function = k.lower(), v[:]
            subfuncs = f"\n{function}\n".count('\n***\n')+1
            func_count = 1
            func_list = function.split('\n')
            for n, line in enumerate(func_list):
                if line == "***": func_count += 1
                line = line.replace('/pymcfunc_old:first/', self.name+':'+funcName+("0" if subfuncs != 1 else "")) \
                           .replace('/pymcfunc_old:prev/', self.name+':'+funcName+str(func_count-1)) \
                           .replace('/pymcfunc_old:this/', self.name+':'+funcName+str(func_count if subfuncs != 1 else "")) \
                           .replace('/pymcfunc_old:next/', self.name+':'+funcName+str(func_count+1)) \
                           .replace('/pymcfunc_old:last/', self.name+':'+funcName+(str(subfuncs-1) if subfuncs != 1 else ""))
                func_list[n] = line
            function = '\n'.join(func_list)
            for n, subfunc in enumerate([x.strip() for x in function.split("***")]):
                if subfuncs == 1: n = ""
                with open(f'functions/{funcName}{n}.mcfunction', 'w') as f:
                    f.write(subfunc)

        #advancements
        if self.advancements != {}:
            pathlib.Path(os.getcwd()+'/advancements').mkdir(exist_ok=True)
            for k, v in self.advancements.items():
                with open(f'advancements/{k}.json', 'w') as f:
                    print(v)
                    json.dump(v, f, indent=indent)

        #loot tables
        if self.loot_tables != {}:
            pathlib.Path(os.getcwd()+'/loot_tables').mkdir(exist_ok=True)
            for k, v in self.loot_tables.items():
                with open(f'loot_tables/{k}.json', 'w') as f:
                    json.dump(v, f, indent=indent)

        #predicates
        if self.predicates != {}:
            pathlib.Path(os.getcwd()+'/predicates').mkdir(exist_ok=True)
            for k, v in self.predicates.items():
                with open(f'predicates/{k}.json', 'w') as f:
                    json.dump(v, f, indent=indent)

        #recipes
        if self.recipes != {}:
            pathlib.Path(os.getcwd()+'/recipes').mkdir(exist_ok=True)
            for k, v in self.recipes.items():
                with open(f'recipes/{k}.json', 'w') as f:
                    json.dump(v, f, indent=indent)

        #item modifiers
        if self.item_modifiers != {}:
            pathlib.Path(os.getcwd() + '/item_modifiers').mkdir(exist_ok=True)
            for k, v in self.item_modifiers.items():
                with open(f'item_modifiers/{k}.json', 'w') as f:
                    json.dump(v, f, indent=indent)

        #structures
        #dimension types
        #dimensions
        #worldgen

        #tags
        for group, tags in self.tags.items():
            if tags != {}:
                pathlib.Path(os.getcwd()+f'/tags/{group}').mkdir(parents=True, exist_ok=True)
                for tag, funcs in tags.items():
                    tagJson = {
                        'values': [self.name+':'+i.lower() for i in funcs]
                    }
                    with open(f'tags/{group}/{tag}.json', 'w') as f:
                        json.dump(tagJson, f, indent=indent)

class JavaFunctionTags:
    def __init__(self, p):
        self.p = p

    def tag(self, tag: str, minecraft_tag: bool=False):
        """Applies a tag to the function. When the tag is run with /function, all functions under this tag will run.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFunctionTags.tag"""
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                if minecraft_tag:
                    self.p.minecraft_tags[tag].append(func.__name__)
                else:
                    if tag not in self.p.tags:
                        self.p.tags['functions'][tag] = []
                    self.p.tags['functions'][tag].append(func.__name__)
                func(m)
            return wrapper
        return decorator

    def on_load(self, func: Callable[[UniversalFuncHandler], Any]):
        """Applies a ‘load’ tag to the function. Alias of @pmf.JavaFunctionTags.tag('load', minecraft_tag=True).
        Functions with the tag will be run when the datapack is loaded.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFunctionTags.on_load"""
        return self.tag('load', minecraft_tag=True)(func)

    def repeat_every_tick(self, func: Callable[[UniversalFuncHandler], Any]):
        """Applies a ‘tick’ tag to the function. Alias of @pmf.JavaFunctionTags.tag('tick', minecraft_tag=True).
        Functions with the tag will be run every tick.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFunctionTags.repeat_every_tick"""
        return self.tag('tick', minecraft_tag=True)(func)

    def repeat_every(self, ticks: int):
        """The function will be run on a defined interval.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFunctionTags.repeat_every"""
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                self.on_load(func)(m)
                m.r.schedule('/pymcfunc_old:first/', duration=ticks, mode='append')
            return wrapper
        return decorator

    @staticmethod
    def repeat(n: int):
        """The function will be run a defined number of times.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFunctionTags.repeat"""
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                for i in range(n):
                    func(m)
            return wrapper
        return decorator
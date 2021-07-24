from typing import Callable, Any, Optional
from functools import wraps
import pathlib
import os
import json

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handlers import JavaFuncHandler, BedrockFuncHandler, UniversalFuncHandler
import pymcfunc.selectors as selectors
from pymcfunc.advancements import Advancement
from pymcfunc.loot_tables import LootTable
from pymcfunc.predicates import Predicate
from pymcfunc.recipes import CookingRecipe, ShapedCraftingRecipe, ShapelessCraftingRecipe, SmithingRecipe, StonecuttingRecipe

class Pack:
    """A container for all functions.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack"""

    def __init__(self, edition: str="j"):
        internal.options(edition, ['j','b'])
        if not edition in ['j', 'b']:
            raise errors.OptionError(['j', 'b'], edition)
        self.edition = edition
        self.funcs = {}
        self.tags = {'functions':{}}
        self.minecraft_tags = {'load': [], 'tick': []}
        self.advancements = {}
        self.loot_tables = {}
        self.predicates = {}
        self.recipes = {}
        self.sel = selectors.BedrockSelectors() if edition == "b" else selectors.JavaSelectors()
        if edition == 'j':
            self.t = JavaTags(self)

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

    def advancement(self, name: str, parent: str):
        if self.edition == 'b':
            raise TypeError('No advancements in Bedrock')
        return Advancement(self, name, parent)

    def loot_table(self, name: str):
        if self.edition == 'b':
            raise TypeError('No loot tables in Bedrock')
        return LootTable(self, name)

    def predicate(self, name: str):
        if self.edition == 'b':
            raise TypeError('No predicates in Bedrock')
        return Predicate(self, name)

    def recipe(self, name: str, type_: str, group: Optional[str]=None):
        internal.options(type_, ['blasting', 'campfire_cooking', 'crafting_shaped', 'crafting_shapeless', 'smelting', 'smithing', 'smoking', 'stonecutting'])
        if type_ in ['blasting', 'campfire_cooking', 'smelting', 'smoking']: recipe = CookingRecipe
        elif type_ == "crafting_shaped": recipe = ShapedCraftingRecipe
        elif type_ == "crafting_shapeless": recipe = ShapelessCraftingRecipe
        elif type_ == "smithing": recipe = SmithingRecipe
        elif type_ == "stonecutting": recipe = StonecuttingRecipe
        return recipe(self, name, type_, group=group)
        

    def build(self, name: str, pack_format: int, description: str, datapack_folder: str='.'):
        """Builds the pack. Java Edition only.\n
        **Format numbering**
        * **4** - 1.13–1.14.4
        * **5** - 1.15–1.16.1
        * **6** - 1.16.2–1.16.5
        * **7** - 1.17\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.build"""
        if self.edition == 'b':
            raise TypeError('Cannot build Bedrock packs')
        name = name.lower()
        #create pack dir
        pathlib.Path(datapack_folder+'/'+name).mkdir(exist_ok=True)
        os.chdir(datapack_folder+'/'+name)

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
        pathlib.Path(os.getcwd()+'/data/'+name).mkdir(parents=True, exist_ok=True)
        os.chdir('data/'+name)

        #functions
        pathlib.Path(os.getcwd()+'/functions').mkdir(exist_ok=True)
        for k, v in self.funcs.items():
            funcName, function = k.lower(), v[:]
            subfuncs = f"\n{function}\n".count('\n***\n')+1
            func_count = 1
            for line in function:
                if line == "***": func_count += 1
                line = line.replace('/pymcfunc:first/', name+':'+funcName+("0" if subfuncs != 1 else "")) \
                           .replace('/pymcfunc:prev/', name+':'+funcName+str(func_count-1)) \
                           .replace('/pymcfunc:next/', name+':'+funcName+str(func_count+1)) \
                           .replace('/pymcfunc:last/', name+':'+funcName+(str(subfuncs-1) if subfuncs != 1 else ""))
            for n, subfunc in enumerate(function.split("***").strip()):
                if subfuncs == 1: n = ""
                with open(f'functions/{funcName}{n}.mcfunction', 'w') as f:
                    f.write(subfunc)
            
        #advancements
        pathlib.Path(os.getcwd()+'/advancements').mkdir(exist_ok=True)
        for k, v in self.advancements.items():
            with open(f'advancements/{k}.json', 'w') as f:
                    json.dump(f, v)

        #loot tables
        pathlib.Path(os.getcwd()+'/loot_tables').mkdir(exist_ok=True)
        for k, v in self.loot_tables.items():
            with open(f'loot_tables/{k}.json', 'w') as f:
                    json.dump(f, v)

        #predicates
        pathlib.Path(os.getcwd()+'/predicates').mkdir(exist_ok=True)
        for k, v in self.predicates.items():
            with open(f'predicates/{k}.json', 'w') as f:
                    json.dump(f, v)

        #recipes
        pathlib.Path(os.getcwd()+'/recipes').mkdir(exist_ok=True)
        for k, v in self.recipes.items():
            with open(f'recipes/{k}.json', 'w') as f:
                    json.dump(f, v)

        #structures
        #tags
        #dimension types
        #dimensions
        #item modifiers
        #worldgen
        
        #tags
        for group, tags in self.tags.items():
            pathlib.Path(os.getcwd()+f'/tags/{group}').mkdir(parents=True, exist_ok=True)
            for tag, funcs in tags.items():
                tagJson = {
                    'values': [name+':'+i.lower() for i in funcs]
                }
                with open(f'tags/{group}/{tag}.json', 'w') as f:
                    json.dump(tagJson, f)

class JavaTags:
    def __init__(self, p):
        self.pack = p
    
    def tag(self, tag: str, minecraft_tag: bool=False):
        """Applies a tag to the function. When the tag is run with /function, all functions under this tag will run.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaTags.tag"""
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                if minecraft_tag:
                    self.pack.minecraft_tags[tag].append(func.__name__)
                else:
                    if tag not in self.pack.tags:
                        self.pack.tags['functions'][tag] = []
                    self.pack.tags['functions'][tag].append(func.__name__)
                func(m)
            return wrapper
        return decorator

    def on_load(self, func: Callable[[UniversalFuncHandler], Any]):
        """Applies a ‘load’ tag to the function. Alias of @pmf.JavaTags.tag('load').
        Functions with the tag will be run when the datapack is loaded.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaTags.on_load"""
        return self.tag('load')(func)

    def repeat_every_tick(self, func: Callable[[UniversalFuncHandler], Any]):
        """Applies a ‘tick’ tag to the function. Alias of @pmf.JavaTags.tag('tick').
        Functions with the tag will be run every tick.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaTags.repeat_every_tick"""
        return self.tag('tick')(func)

    def repeat_every(self, ticks: int):
        """The function will be run on a defined interval.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaTags.repeat_every"""
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                self.on_load(func)(m)
                m.r.schedule('/pymcfunc:first/', duration=ticks, mode='append')
            return wrapper
        return decorator
    
    def repeat(self, n: int):
        """The function will be run a defined number of times.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaTags.repeat"""
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                for i in range(n):
                    func(m)
            return wrapper
        return decorator
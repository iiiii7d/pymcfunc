from functools import wraps
import pathlib
import os
import json

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_java import JavaFuncHandler
from pymcfunc.func_handler_bedrock import BedrockFuncHandler
import pymcfunc.selectors as selectors

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
        self.sel = selectors.BedrockSelectors() if edition == "b" else selectors.JavaSelectors()
        if edition == 'j':
            self.t = JavaTags(self)

    def function(self, func):
        """Registers a Python function and translates it into a Minecraft function.    
        The decorator will run the function so you do not need to run the function again.
        The name of the Python function will be the name of the Minecraft function.
        The decorator calls the function being decorated with one argument being a PackageHandler.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.function"""
        m = JavaFuncHandler() if self.edition == 'j' else BedrockFuncHandler()
        func(m)
        fname = func.__name__
        self.funcs.update({fname: str(m)})

    def build(self, name: str, pack_format: int, description: str, datapack_folder: str='.'):
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
            function = function.replace('/pymcfunc:first/', name+':'+funcName)
            with open(f'functions/{funcName}.mcfunction', 'w') as f:
                f.write(function)
            
        #advancements
        #loot tables
        #predicates
        #recipes
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
    
    def tag(self, tag: str):
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                if tag not in self.pack.tags:
                    self.pack.tags['functions'][tag] = []
                self.pack.tags['functions'][tag].append(func.__name__)
                func(m)
            return wrapper
        return decorator

    def on_load(self, func):
        return self.tag('load')(func)

    def repeat_every_tick(self, func):
        return self.tag('tick')(func)

    def repeat_every(self, ticks: int):
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                self.on_load(func)(m)
                m.r.schedule('/pymcfunc:first/', duration=ticks, mode='append')
            return wrapper
        return decorator
    
    def repeat(self, n: int):
        def decorator(func):
            @wraps(func)
            def wrapper(m):
                for i in range(n):
                    func(m)
            return wrapper
        return decorator
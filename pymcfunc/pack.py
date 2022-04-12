from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from pymcfunc import selectors
from pymcfunc.func_handler import JavaFunctionHandler
from pymcfunc.version import JavaVersion


class JavaPack:
    """Represents a Java Edition Datapack."""

    def __init__(self, name: str, version: Union[str, JavaVersion]):
        """
        Initialises the pack.
        
        :param str name: The name of the pack
        :param version: The version of the pack
        :type version: str | JavaVersion
        """
        self.name = name
        self.funcs: Dict[str, str] = {}
        self.tags: Dict[str, Dict[str, List[str]]] = {'blocks': {}, 'entity_types': {}, 'fluids': {}, 'functions': {}, 'items': {}}
        self.minecraft_tags: Dict[str, List] = {'load': [], 'tick': []}
        self.advancements: dict = {}
        self.loot_tables: dict = {}
        self.predicates: dict = {}
        self.recipes: dict = {}
        self.item_modifiers: dict = {}
        self.sel = selectors.JavaSelector()
        self.version = JavaVersion(version) if isinstance(version, str) else version

    def function(self, name: Optional[str]=None):
        """
        Registers a Python function and translates it into a Minecraft function.

        The decorator calls the function being decorated with one argument being a PackageHandler.

        :param name: The name of the Minecraft function, if it isn't the name of the Python function.
        :type name: [type] | None
        """
        def decorator(func: Callable[[JavaFunctionHandler], Any]):
            m = JavaFunctionHandler(self)
            func(m)
            fname = func.__name__ if name is None else name
            self.funcs.update({fname: str(m)})
        return decorator

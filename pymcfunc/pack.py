from __future__ import annotations

from typing import Any, Callable, Optional

from pymcfunc import selectors
from pymcfunc.data_formats.advancements import Advancement
from pymcfunc.functions import JavaFunctionHandler, Function
from pymcfunc.internal import base_class
from pymcfunc.data_formats.loot_tables import LootTable
from pymcfunc.data_formats.predicates import Predicate
from pymcfunc.data_formats.recipes import Recipe
from pymcfunc.version import JavaVersion
from pymcfunc.data_formats.item_modifiers import ItemModifier


@base_class
class BasePack: pass


class JavaPack(BasePack):
    """Represents a Java Edition Datapack."""

    def __init__(self, name: str, version: str | JavaVersion):
        """
        Initialises the pack.
        
        :param str name: The name of the pack
        :param version: The version of the pack
        :type version: str | JavaVersion
        """
        self.name = name
        self.functions: list[Function] = []
        self.tags: dict[str, dict[str, list[str]]] = {'blocks': {}, 'entity_types': {}, 'fluids': {}, 'functions': {}, 'items': {}}
        self.minecraft_tags: dict[str, list] = {'load': [], 'tick': []}
        self.advancements: list[Advancement] = []
        self.loot_tables: list[LootTable] = []
        self.predicates: list[Predicate] = []
        self.recipes: list[Recipe] = []
        self.item_modifiers: list[ItemModifier] = []
        self.sel = selectors.JavaSelector
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
            function = Function(self, m, "", fname)
            self.funcs.append(function)
            return function
        return decorator

    def build(self): pass

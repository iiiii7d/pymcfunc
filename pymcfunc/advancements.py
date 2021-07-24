from typing import Union, Optional, Any, Callable, List, Tuple
from functools import wraps
import pymcfunc.internal as internal
import pymcfunc.func_handlers as func_handler

class Advancement:
    def __init__(self, p, name: str, parent: str):
        self.p = p
        self.name = name
        self.p.advancements[name] = {
            "criteria": {},
            "rewards": {}
        }
        self.value = self.p.advancements[self.name]
        if parent is not None:
            self.value['parent'] = parent

    def set_icon(self, item_name: str, nbt: Optional[dict]=None):
        if 'display' not in self.value.keys():
            self.value['display'] = {}
        self.value['display']['item'] = item_name
        if nbt is not None:
            self.value['display']['nbt'] = nbt

    def set_display(self, attr: str, value: Any):
        internal.options(attr, ['icon', 'title', 'frame', 'background', 'description', 'show_toast', 'announce_to_chat', 'hidden'])
        if 'display' not in self.value.keys():
            self.value['display'] = {}
        self.value['display'][attr] = value

    def set_parent(self, parent: Union[str, 'Advancement']):
        if isinstance(parent, type(self)):
            self.value['parent'] = parent.name
        else:
            self.value['parent'] = parent

    def criterion(self, name: str, trigger: str, conditions: dict):
        if 'criteria' not in self.value.keys():
            self.value['criteria'] = {}
        criterion_dict = {'trigger': trigger, 'conditions': conditions}
        self.value['criteria'][name] = criterion_dict

    def set_requirements(self, *criterion_lists: Tuple[List[str]]):
        self.value['requirements'] = list(criterion_lists)

    def reward(self, item: str, value: Any):
        internal.options(item, ['recipes', 'loot', 'experience', 'function'])
        self.value['rewards'][item] = value

    def on_reward(self, func: Callable[[func_handler.JavaFuncHandler], Any]):
        @wraps(func)
        def wrapper(m):
            self.value['rewards']['function'] = func.__name__
            func(m)
        return wrapper
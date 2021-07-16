from typing import Union, Optional, Any, Callable, List, Tuple
from functools import wraps
import pymcfunc.internal as internal
import pymcfunc.func_handlers as func_handler

class Advancement:
    def __init__(self, p, name: str, parent: str):
        self.p = p
        self.name = name
        self.p.advancements[name] = {}
        if parent is not None:
            self.p.advancements[name]['parent'] = parent

    def set_icon(self, itemName: str, nbt: Optional[dict]=None):
        if not 'display' in self.p.advancements[self.name].keys():
            self.p.advancements[self.name]['display'] = {}
        self.p.advancements[self.name]['display']['item'] = itemName
        if nbt is not None:
            self.p.advancements[self.name]['display']['nbt'] = nbt

    def set_display(self, attr: str, value: Any):
        internal.options(attr, ['icon', 'title', 'frame', 'background', 'description', 'show_toast', 'announce_to_chat', 'hidden'])
        if not 'display' in self.p.advancements[self.name].keys():
            self.p.advancements[self.name]['display'] = {}
        self.p.advancements[self.name]['display'][attr] = value

    def set_parent(self, parent: Union[str, 'Advancement']):
        if isinstance(parent, type(self)):
            self.p.advancements[self.name]['parent'] = parent.name
        else:
            self.p.advancements[self.name]['parent'] = parent

    def criterion(self, name: str, trigger: str, conditions: dict):
        if not 'criteria' in self.p.advancements[self.name].keys():
            self.p.advancements[self.name]['criteria'] = {}
        criterion_dict = {'trigger': trigger, 'conditions': conditions}
        self.p.advancements[self.name]['criteria'][name] = criterion_dict

    def set_requirements(self, *criterion_lists: Tuple[List[str]]):
        self.p.advancements[self.name]['requirements'] = list(criterion_lists)

    def reward(self, item: str, value: Any):
        internal.options(item, ['recipes', 'loot', 'experience', 'function'])
        if not 'reward' in self.p.advancements[self.name].keys():
            self.p.advancements[self.name]['reward'] = {}
        self.p.advancements[self.name]['reward'][item] = value

    def on_reward(self, func: Callable[[func_handler.JavaFuncHandler], Any]):
        @wraps(func)
        def wrapper(m):
            if not 'reward' in self.p.advancements[self.name].keys():
                self.p.advancements[self.name]['reward'] = {}
            self.p.advancements[self.name]['reward']['function'] = func.__name__
            func(m)
        return wrapper
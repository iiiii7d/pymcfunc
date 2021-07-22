from typing import Optional, Tuple
import pymcfunc.internal as internal

class LootTable:
    def __init__(self, p, name: str, type_: Optional[str]=None):
        self.p = p
        self.name = name
        self.p.loot_tables[name] = {}
        if type_ is not None:
            internal.options(type_, ['empty', 'entity', 'block', 'chest', 'fishing', 'gift', 'advancement_reward', 'barter', 'command', 'selector', 'advancement_entity', 'generic'])
            self.p.loot_tables[name]['type'] = type_

    def add_item_modifier(self, name: str, *predicates: Tuple[str]):
        if 'functions' not in self.p.loot_tables[self.name].keys():
            self.p.loot_tables[self.name]['functions'] = []
        self.p.loot_tables[self.name]['functions'].append({
            'function': name,
            'conditions': [{'condition': i} for i in predicates]
        })
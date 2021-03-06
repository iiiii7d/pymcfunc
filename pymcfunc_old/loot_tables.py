from typing import Optional, Union
import pymcfunc_old.internal as internal
from pymcfunc_old.predicates import Predicate
from pymcfunc_old.item_modifiers import ItemModifier
NumberProvider = dict

class LootTable:
    """A loot table.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.LootTable"""
    def __init__(self, p, name: str, type_: Optional[str]=None):
        self.p = p
        self.name = name
        self.namespaced = self.p.name + ":" + self.name
        self.p.loot_tables[name] = {
            'functions': [],
            'pools': []
        }
        if type_ is not None:
            internal.options(type_, ['empty', 'entity', 'block', 'chest', 'fishing', 'gift', 'advancement_reward', 'barter', 'command', 'selector', 'advancement_entity', 'generic'])
            self.p.loot_tables[name]['type'] = type_

    def item_modifier(self, name: Union[str, ItemModifier], *predicates: Union[str, Predicate]):
        """Sets an item modifier of the loot table as the function.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.LootTable.item_modifier"""
        self.p.loot_tables[self.name]['functions'].append({
            'function': name.namespaced if isinstance(name, ItemModifier) else name,
            'conditions': [{'condition': i.namespaced if isinstance(i, Predicate) else i} for i in predicates]
        })

    def pool(self, rolls: Union[int, NumberProvider], bonus_rolls: Union[float, NumberProvider]) -> 'Pool':
        """Sets a pool of the loot table.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.LootTable.pool"""
        return Pool(self, rolls, bonus_rolls, len(self.p.loot_tables[self.name]['pools']))

class Pool:
    """A pool for a loot table.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Pool"""
    def __init__(self, lt, rolls: Union[int, NumberProvider], bonus_rolls: Union[float, NumberProvider], index: int):
        self.lt = lt
        self.name = self.lt.name
        self.lt.p.loot_tables[self.name]['pools'].append({
            'conditions': [],
            'functions': [],
            'rolls': rolls,
            'bonus_rolls': bonus_rolls,
            'entries': []
        })
        self.index = index
        self.value = self.lt.p.loot_tables[self.name]['pools'][self.index]

    def item_modifier(self, name: Union[str, ItemModifier], *predicates: Union[str, Predicate]):
        """Sets an item modifier of the loot table as the function.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Pool.item_modifier"""
        self.value['functions'].append({
            'function': name.namespaced if isinstance(name, ItemModifier) else name,
            'conditions': [{'condition': i.namespaced if isinstance(i, Predicate) else i} for i in predicates]
        })

    def predicate(self, predicate: Union[str, Predicate]):
        """Sets a predicate of the pool as the condition for the pool to be used.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Pool.predicate"""
        self.value['conditions'].append({
            'condition': predicate.namespaced if isinstance(predicate, Predicate) else predicate
        })

    def entry(self, type_: str, weight: int, quality: int, expand: Optional[bool]=None, name: Optional[str]=None) -> 'Entry':
        """An entry of things in the pool.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Pool.entry"""
        return Entry(self, type_, weight, quality, pool_index=self.index, entry_index=len(self.value['entries']), expand=expand, name=name)

class Entry:
    """An entry for a pool.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Entry"""
    def __init__(self, pl, type_: str, weight: int, quality: int, pool_index: Optional[int]=None, entry_index: Optional[int]=None, expand: Optional[bool]=None, name: Optional[str]=None, value: Optional[dict]=None):
        self.pl = pl
        self.name = self.pl.lt.name
        internal.options(type_, ['item', 'tag', 'loot_table', 'group', 'alternatives', 'sequence', 'dynamic', 'empty'])
        template = {
            'conditions': [],
            'functions': [],
            'children': [],
            'type': type_,
            'weight': weight,
            'quality': quality
        }
        if value is None:
            self.pool_index = pool_index
            self.index = entry_index
            self.pl.lt.p.loot_tables[self.name]['pools'][self.pool_index]['entries'].append(template)
            self.value = self.pl.lt.p.loot_tables[self.name]['pools'][self.pool_index]['entries'][self.index]
        else:
            self.value = template
        if expand is not None:
            self.value['expand'] = expand
        if name is not None:
            self.value['name'] = name

    def item_modifier(self, name: Union[str, ItemModifier], *predicates: Union[str, Predicate]):
        """Sets an item modifier of the entry as the function.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Entry.item_modifier"""
        self.value['functions'].append({
            'function': name.namespaced if isinstance(name, ItemModifier) else name,
            'conditions': [{'condition': i.namespaced if isinstance(i, Predicate) else i} for i in predicates]
        })

    def predicate(self, predicate: Union[str, Predicate]):
        """Sets a predicate of the entry as the condition for the entry to be used.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Entry.predicate"""
        self.value['conditions'].append({
            'condition': predicate.namespaced if isinstance(predicate, Predicate) else predicate
        })

    def child(self, type_: str, weight: int, quality: int, expand: Optional[bool]=None, name: Optional[str]=None) -> 'Entry':
        """Sets a child entry in the entry.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.loot_tables.Entry.child"""
        self.value['children'].append([])
        index = int(len(self.value['children'])-1)
        return Entry(self.pl, type_, weight, quality, expand=expand, name=name, value=self.value['children'][index])

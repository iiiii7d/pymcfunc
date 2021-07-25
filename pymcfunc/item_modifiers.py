from typing import Optional, Sequence, Tuple, Union, Dict, List
import pymcfunc.internal as internal
NumberProvider = dict

class ItemModifier:
    def __init__(self, p, name: str):
        self.p = p
        self.name = name
        self.namespaced = self.p.name + ":" + self.name
        self.p.item_modifiers[name] = {}
        self.value = self.p.item_modifiers[self.name]

    def apply_bonus(self, enchantment: str, formula: str, extra: int, probability: float, bonus_multiplier: float):
        internal.options(formula, ['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops'])
        self.value = {
            'function': 'apply_bonus',
            'enchantment': enchantment,
            'formula': formula,
            'parameters': [
                extra,
                probability,
                bonus_multiplier
            ]
        }

    def copy_name(self):
        self.value = {
            'function': 'copy_name',
            'source': 'block_entity'
        }

    def copy_nbt_source(self, source: Optional[str]=None, type_: Optional[str]=None, target: Optional[str]=None):
        self.value['function'] = 'copy_nbt'
        internal.unstated("type", type_, ['context'], 'target', target, None)
        internal.pick_one_arg(
            (source, None, 'source'),
            (target, None, 'target'),
            optional=False
        )
        if type_ is None: self.value['source'] = source
        else:
            if 'source' not in self.value.keys(): self.value['source'] = {}
            internal.options(type_, ['context', 'storage'])
            self.value['source']['type'] = type_
            if target is not None: self.value['source']['target'] = target
            else: self.value['source']['source'] = source

    def copy_nbt_operation(self, source: str, target: str, op: str):
        self.value['function'] = 'copy_nbt'
        internal.options(op, ['replace', 'append', 'merge'])
        if 'ops' not in self.value.keys(): self.value['ops'] = []
        self.value['ops'].append({
            'source': source,
            'target': target,
            'op': op
        })

    def copy_state(self, block: str, properties: Sequence[str]):
        self.value = {
            "function": 'copy_state',
            "block": block,
            "properties": list(properties)
        }

    def enchant_randomly(self, *enchantments: str):
        self.value['function'] = 'enchant_randomly'
        if len(enchantments) != 0: self.value['enchantments'] = list(enchantments)
    
    def enchant_with_levels(self, treasure: bool, levels: Union[int, NumberProvider]):
        self.value = {
            'function': "enchant_with_levels",
            'treasure': treasure,
            'levels': levels
        }

    def exploration_map(self, dest: str, icon: str, zoom: int=2, search_radius: int=50, skip_existing_chunks: bool=True):
        self.value = {
            'function': 'exploration_map',
            'destination': dest,
            'decoration': icon,
            'zoom': zoom,
            'search_radius': search_radius,
            'skip_existing_chunks': skip_existing_chunks
        }

    def explosion_decay(self):
        self.value['function'] = 'explosion_decay'

    def furnace_smelt(self):
        self.value['function'] = 'furnace_smelt'

    def fill_player_head(self, entity: str):
        self.value['function'] = 'fill_player_head'
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value['entity'] = entity

    def limit_count(self, limit: Union[Union[int, NumberProvider], Dict[str, Union[int, NumberProvider]]]):
        internal.check_range(limit)
        self.value = {
            'function': 'limit_count',
            'limit': limit
        }
        
    def looting_enchant(self, count: Union[int, NumberProvider], limit: int):
        self.value = {
            'function': 'looting_enchant',
            'count': count,
            'limit': limit
        }
        
    def set_attributes_modifier(self, name: str, attribute: str, operation: str, amount: Union[float, NumberProvider], slot: Union[str, List[str]], id_: Optional[str]=None):
        internal.options(operation, ['add', 'multiply_base', 'multiply_total'])
        if isinstance(slot, list):
            for s in slot:
                internal.options(s, ['mainhand', 'offhand', 'feet', 'legs', 'chest', 'head'])
        else:
            internal.options(slot, ['mainhand', 'offhand', 'feet', 'legs', 'chest', 'head'])
        self.value['function'] = "set_attributes"
        if 'modifiers' not in self.value.keys():
            self.value['modifiers'] = []
        self.value['modifiers'].append({
            'name': name,
            'attribute': attribute,
            'operation': operation,
            'amount': amount,
            'slot': slot
        })
        if id_ is not None: self.value['modifiers'][-1]['id'] = id_
        
    def set_banner_pattern(self, *patterns: Tuple[str, str], append: Optional[bool]=None):
        for _, c in patterns:
            internal.options(c, ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
                                 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'])
            
        self.value = {
            'function': 'set_banner_pattern',
            'patterns': [{'pattern': p, 'color': c} for p, c in patterns]
        }
        if append is not None: self.value['append'] = append

    def set_contents(self, *entries: str):
        self.value = {
            'function': 'set_contents',
            'entries': list(entries)
        }
        
    def set_count(self, count: Union[int, NumberProvider], add: Optional[bool]=None):
        self.value = {
            'function': 'set_count',
            'count': count
        }
        if add is not None: self.value['add'] = add

    def set_damage(self, damage: Union[float, NumberProvider], add: Optional[bool]=None):
        self.value = {
            'function': 'set_damage',
            'damage': damage
        }
        if add is not None: self.value['add'] = add

    def add_enchantments(self, enchantments: Dict[str, Union[int, NumberProvider]], add: Optional[bool]=None):
        self.value = {
            'function': 'add_enchantments',
            'enchantments': enchantments
        }
        if add is not None: self.value['add'] = add

    def set_loot_table(self, name: str, seed: int=0):
        self.value = {
            'function': 'add_enchantments',
            'name': name
        }
        if seed != 0: self.value['seed'] = seed

    def set_lore(self, lore: List[dict], entity: str, replace: bool):
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value = {
            'function': 'set_lore',
            'lore': lore,
            'entity': entity,
            'replace': replace
        }

    def set_name(self, name: dict, entity: str):
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value = {
            'function': 'set_lore',
            'name': name,
            'entity': entity,
        }

    def set_nbt(self, tag: str):
        self.value = {
            'function': 'set_lore',
            'tag': tag
        }

    def set_stew_effect(self, *effects: Tuple[str, Union[int, NumberProvider]]):
        self.value = {
            'function': 'set_stew_effect',
            'effects': [{'type': t, 'duration': d} for t, d in effects]
        }
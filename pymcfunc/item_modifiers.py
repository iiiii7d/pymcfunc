from typing import Optional, Sequence, Tuple
import pymcfunc.internal as internal

class ItemModifier:
    def __init__(self, p, name: str):
        self.p = p
        self.name = name
        self.p.item_modifiers[name] = {}
        self.value = self.p.item_modifiers[self.name]

    def apply_bonus(self, enchantment: str, formula: str, extra: int, probability: float, bonusMultiplier: float):
        internal.options(formula, ['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops'])
        self.value = {
            'function': 'apply_bonus',
            'formula': formula,
            'parameters': [
                extra,
                probability,
                bonusMultiplier
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
            internal.options(type_, ['context', 'storage'])
            self.value['source']['type'] = type_
            if target is not None: self.value['source']['target'] = target
            else: self.value['source']['source'] = source

    def copy_nbt_operation(self, source: str, target: str, op: str):
        self.value['function'] = 'copy_nbt'
        internal.options(op, ['replace', 'append', 'merge'])
        if not 'ops' in self.value.keys(): self.value['ops'] = []
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

    def enchant_randomly(self, *enchantments: Tuple[str]):
        self.value['function'] = 'enchant_randomly'
        if len(enchantments) != 0: self.value['enchantments'] = list(enchantments)
    
    def enchant_with_levels(self, treasure: bool, levels: int):
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

    def limit_count(self, )
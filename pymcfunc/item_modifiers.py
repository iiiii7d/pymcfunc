from typing import Optional, Sequence, Tuple, Union, Dict, List
import pymcfunc.internal as internal

NumberProvider = dict

class ItemModifier:
    """An item modifier in Java Edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier"""

    def __init__(self, p, name: str):
        self.p = p
        self.name = name
        self.namespaced = self.p.name + ":" + self.name
        self.p.item_modifiers[name] = {}
        self.value = self.p.item_modifiers[self.name]

    def apply_bonus(self, enchantment: str, formula: str, extra: int, probability: float, bonus_multiplier: float):
        """Sets the item modifier's function to ``apply_bonus``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.apply_bonus"""
        internal.options(formula, ['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops'])
        self.value.update({
            'function': 'apply_bonus',
            'enchantment': enchantment,
            'formula': formula,
            'parameters': [
                extra,
                probability,
                bonus_multiplier
            ]
        })

    def copy_name(self):
        """Sets the item modifier's function to ``copy_name``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.copy_name"""
        self.value.update({
            'function': 'copy_name',
            'source': 'block_entity'
        })

    def copy_nbt_source(self, source: Optional[str] = None, type_: Optional[str] = None, target: Optional[str] = None):
        """Sets the source of the item modifier for when its function to ``copy_nbt``. Used together with ``copy_nbt_operation()``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.copy_nbt_source"""
        self.value['function'] = 'copy_nbt'
        internal.unstated("type", type_, ['context'], 'target', target, None)
        internal.pick_one_arg(
            (source, None, 'source'),
            (target, None, 'target'),
            optional=False
        )
        if type_ is None:
            self.value['source'] = source
        else:
            if 'source' not in self.value.keys(): self.value['source'] = {}
            internal.options(type_, ['context', 'storage'])
            self.value['source']['type'] = type_
            if target is not None:
                self.value['source']['target'] = target
            else:
                self.value['source']['source'] = source

    def copy_nbt_operation(self, source: str, target: str, op: str):
        """Sets the target of the item modifier for when its function to ``copy_nbt``. Used together with ``copy_nbt_source()``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.copy_nbt_operation"""
        self.value['function'] = 'copy_nbt'
        internal.options(op, ['replace', 'append', 'merge'])
        if 'ops' not in self.value.keys(): self.value['ops'] = []
        self.value['ops'].append({
            'source': source,
            'target': target,
            'op': op
        })

    def copy_state(self, block: str, properties: Sequence[str]):
        """Sets the item modifier's function to ``copy_state``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.copy_state"""
        self.value.update({
            "function": 'copy_state',
            "block": block,
            "properties": list(properties)
        })

    def enchant_randomly(self, *enchantments: str):
        """Sets the item modifier's function to ``enchant_randomly``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.enchant_randomly"""
        self.value['function'] = 'enchant_randomly'
        if len(enchantments) != 0: self.value['enchantments'] = list(enchantments)

    def enchant_with_levels(self, treasure: bool, levels: Union[int, NumberProvider]):
        """Sets the item modifier's function to ``enchant_with_levels``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.enchant_with_levels"""
        self.value.update({
            'function': "enchant_with_levels",
            'treasure': treasure,
            'levels': levels
        })

    def exploration_map(self, dest: str, icon: str, zoom: int = 2, search_radius: int = 50,
                        skip_existing_chunks: bool = True):
        """Sets the item modifier's function to ``exploration_map``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.exploration_map"""
        self.value.update({
            'function': 'exploration_map',
            'destination': dest,
            'decoration': icon,
            'zoom': zoom,
            'search_radius': search_radius,
            'skip_existing_chunks': skip_existing_chunks
        })

    def explosion_decay(self):
        """Sets the item modifier's function to ``explosion_decay``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.explosion_decay"""
        self.value['function'] = 'explosion_decay'

    def furnace_smelt(self):
        """Sets the item modifier's function to ``furnace_smelt``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.furnace_smelt"""
        self.value['function'] = 'furnace_smelt'

    def fill_player_head(self, entity: str):
        """Sets the item modifier's function to ``fill_player_head``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.fill_player_head"""
        self.value['function'] = 'fill_player_head'
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value['entity'] = entity

    def limit_count(self, limit: Union[Union[int, NumberProvider], Dict[str, Union[int, NumberProvider]]]):
        """Sets the item modifier's function to ``limit_count``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.limit_count"""
        internal.check_range(limit)
        self.value.update({
            'function': 'limit_count',
            'limit': limit
        })

    def looting_enchant(self, count: Union[int, NumberProvider], limit: int):
        """Sets the item modifier's function to ``looting_enchant``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.looting_enchant"""
        self.value.update({
            'function': 'looting_enchant',
            'count': count,
            'limit': limit
        })

    def set_attributes_modifier(self, name: str, attribute: str, operation: str, amount: Union[float, NumberProvider],
                                slot: Union[str, List[str]], id_: Optional[str] = None):
        """Sets the item modifier's function to ``set_attributes_modifier``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_attributes_modifier"""
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

    def set_banner_pattern(self, *patterns: Tuple[str, str], append: Optional[bool] = None):
        """Sets the item modifier's function to ``set_banner_pattern``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_banner_pattern"""
        for _, c in patterns:
            internal.options(c, ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
                                 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'])

        self.value.update({
            'function': 'set_banner_pattern',
            'patterns': [{'pattern': p, 'color': c} for p, c in patterns]
        })
        if append is not None: self.value['append'] = append

    def set_contents(self, *entries: dict):
        """Sets the item modifier's function to ``set_contents``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_contents"""
        self.value.update({
            'function': 'set_contents',
            'entries': list(entries)
        })

    def set_count(self, count: Union[int, NumberProvider], add: Optional[bool] = None):
        """Sets the item modifier's function to ``set_count``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_count"""
        self.value.update({
            'function': 'set_count',
            'count': count
        })
        if add is not None: self.value['add'] = add

    def set_damage(self, damage: Union[float, NumberProvider], add: Optional[bool] = None):
        """Sets the item modifier's function to ``set_damage``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_damage"""
        self.value.update({
            'function': 'set_damage',
            'damage': damage
        })
        if add is not None: self.value['add'] = add

    def set_enchantments(self, enchantments: Dict[str, Union[int, NumberProvider]], add: Optional[bool] = None):
        """Sets the item modifier's function to ``set_enchantments``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_enchantments"""
        self.value.update({
            'function': 'set_enchantments',
            'enchantments': enchantments
        })
        if add is not None: self.value['add'] = add

    def set_loot_table(self, name: str, seed: int = 0):
        """Sets the item modifier's function to ``set_loot_table``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_loot_table"""
        self.value.update({
            'function': 'set_loot_table',
            'name': name
        })
        if seed != 0: self.value['seed'] = seed

    def set_lore(self, lore: List[dict], entity: str, replace: bool):
        """Sets the item modifier's function to ``set_lore``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_lore"""
        self.value.update({
            'function': 'set_lore',
            'lore': lore,
            'entity': entity,
            'replace': replace
        })

    def set_name(self, name: dict, entity: str):
        """Sets the item modifier's function to ``set_name``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_name"""
        self.value.update({
            'function': 'set_name',
            'name': name,
            'entity': entity,
        })

    def set_nbt(self, tag: str):
        """Sets the item modifier's function to ``set_nbt``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_nbt"""
        self.value.update({
            'function': 'set_nbt',
            'tag': tag
        })

    def set_stew_effect(self, *effects: Tuple[str, Union[int, NumberProvider]]):
        """Sets the item modifier's function to ``set_stew_effect``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.item_modifiers.ItemModifier.set_stew_effect"""
        self.value.update({
            'function': 'set_stew_effect',
            'effects': [{'type': t, 'duration': d} for t, d in effects]
        })
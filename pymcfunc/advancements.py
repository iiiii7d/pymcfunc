from typing import Union, Optional, Any, Callable, List, Dict
from functools import wraps
import pymcfunc.internal as internal
import pymcfunc.func_handlers as func_handler

class Advancement:
    def __init__(self, p, name: str, parent: str):
        self.p = p
        self.name = name
        self.namespaced = self.p.name+":"+self.name
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

    '''def criterion(self, name: str, trigger: str, conditions: dict):
        if 'criteria' not in self.value.keys():
            self.value['criteria'] = {}
        criterion_dict = {'trigger': trigger, 'conditions': conditions}
        self.value['criteria'][name] = criterion_dict'''

    def criterion(self, name: str):
        return Criterion(self, name)

    def set_requirements(self, *criterion_lists: List[str]):
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

class Criterion:
    def __init__(self, ad, name: str):
        self.name = name
        self.ad = ad
        if 'name' not in self.ad.value['criteria']: self.ad.value['criteria'][name] = {}
        self.value = self.ad.value['criteria'][name]

    def bee_nest_destroyed(self, block: Optional[str]=None, item: Optional[dict]=None, num_bees_inside: Optional[int]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:bee_nest_destroyed',
            'conditions': {}
        }
        if block.startswith("minecraft:"): internal.options(block, ["minecraft:bee_nest", "minecraft:beehive"])
        if block is not None: self.value['conditions']['block'] = block
        if item is not None: self.value['conditions']['item'] = item
        if num_bees_inside is not None: self.value['conditions']['num_bees_inside'] = num_bees_inside
        if player is not None: self.value['conditions']['player'] = player

    def bred_animals(self, child: Optional[Union[List[str], dict]]=None, parent: Optional[Union[List[str], dict]]=None, partner: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:bred_animals',
            'conditions': {}
        }
        if child is not None: self.value['conditions']['child'] = child
        if parent is not None: self.value['conditions']['parent'] = parent
        if partner is not None: self.value['conditions']['partner'] = partner
        if player is not None: self.value['conditions']['player'] = player

    def brewed_potion(self, potion: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:brewed_potion',
            'conditions': {}
        }
        if potion is not None: self.value['conditions']['potion'] = potion
        if player is not None: self.value['conditions']['player'] = player

    def changed_dimension(self, from_: Optional[str]=None, to: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:changed_dimension',
            'conditions': {}
        }
        for d in (from_, to):
            if d is not None: internal.options(d, ['overworld', 'the_nether', 'the_end'])
        if from_ is not None: self.value['conditions']['from_'] = from_
        if to is not None: self.value['conditions']['to'] = to
        if player is not None: self.value['conditions']['player'] = player

    def channeled_lightning(self, *victims: Union[List[str], dict], player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:channeled_lightning',
            'conditions': {}
        }
        if len(victims) != 0: self.value['conditions']['victims'] = list(victims)
        if player is not None: self.value['conditions']['player'] = player

    def construct_beacon(self, level: Optional[Union[int, Dict[str, int]]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:construct_beacon',
            'conditions': {}
        }
        if isinstance(level, dict):
            for k, v in level:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if level is not None: self.value['conditions']['level'] = level
        if player is not None: self.value['conditions']['player'] = player

    def consume_item(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:consume_item',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def defcured_zombie_villager(self, villager: Optional[Union[List[str], dict]]=None, zombie: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:defcured_zombie_villager',
            'conditions': {}
        }
        if villager is not None: self.value['conditions']['villager'] = villager
        if zombie is not None: self.value['conditions']['zombie'] = zombie
        if player is not None: self.value['conditions']['player'] = player

    def effects_changed(self, source: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value['trigger'] = 'minecraft:effects_changed'
        if 'conditions' not in self.value.keys(): self.value['conditions'] = {}
        if source is not None: self.value['conditions']['source'] = source
        if player is not None: self.value['conditions']['player'] = player

    def effects_changed_effect(self, effect_name: Optional[str]=None, amplifier: Optional[Union[int, Dict[str, int]]]=None, duration: Optional[Union[int, Dict[str, int]]]=None):
        self.value['trigger'] = 'minecraft:effects_changed'
        if 'conditions' not in self.value.keys(): self.value['conditions'] = {}
        if 'effects' not in self.value['conditions'].keys(): self.value['conditions']['effects'] = {}
        self.value['conditions']['effects'][effect_name] = {}
        if isinstance(amplifier, dict):
            for k, v in amplifier:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if isinstance(duration, dict):
            for k, v in duration:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if amplifier is not None: self.value['conditions']['amplifier'] = amplifier
        if duration is not None: self.value['conditions']['duration'] = duration

    def enchanted_item(self, item: Optional[dict]=None, levels: Optional[Union[int, Dict[str, int]]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:enchanted_item',
            'conditions': {}
        }
        if isinstance(levels, dict):
            for k, v in levels:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if item is not None: self.value['conditions']['item'] = item
        if levels is not None: self.value['conditions']['levels'] = levels
        if player is not None: self.value['conditions']['player'] = player

    def enter_block(self, block: Optional[str]=None, state: Optional[Dict[str, str]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:enter_block',
            'conditions': {}
        }
        if block is not None: self.value['conditions']['block'] = block
        if state is not None: self.value['conditions']['state'] = state
        if player is not None: self.value['conditions']['player'] = player

    def entity_hurt_player(self, damage: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:entity_hurt_player',
            'conditions': {}
        }
        if damage is not None: self.value['conditions']['damage'] = damage
        if player is not None: self.value['conditions']['player'] = player

    def entity_killed_player(self, entity: Optional[Union[List[str], dict]]=None, killing_blow: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:entity_killed_player',
            'conditions': {}
        }
        if entity is not None: self.value['conditions']['entity'] = entity
        if killing_blow is not None: self.value['conditions']['killing_blow'] = killing_blow
        if player is not None: self.value['conditions']['player'] = player

    def filled_bucket(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:filled_bucket',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def fishing_rod_hooked(self, entity: Optional[Union[List[str], dict]]=None, item: Optional[dict]=None, rod: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:fishing_rod_hooked',
            'conditions': {}
        }
        if entity is not None: self.value['conditions']['entity'] = entity
        if item is not None: self.value['conditions']['item'] = item
        if rod is not None: self.value['conditions']['rod'] = rod
        if player is not None: self.value['conditions']['player'] = player

    def hero_of_the_village(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:hero_of_the_village',
            'conditions': {}
        }
        if location is not None: self.value['conditions']['location'] = location
        if player is not None: self.value['conditions']['player'] = player

    def impossible(self):
        self.value = {
            'trigger': 'minecraft:impossible',
            'conditions': {}
        }

    def inventory_changed(self, *items: dict, empty_slots: Optional[Union[int, Dict[str, int]]]=None, full_slots: Optional[Union[int, Dict[str, int]]]=None, occupied_slots: Optional[Union[int, Dict[str, int]]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:inventory_changed',
            'conditions': {}
        }
        if isinstance(empty_slots, dict):
            for k, v in empty_slots:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if isinstance(full_slots, dict):
            for k, v in full_slots:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if isinstance(occupied_slots, dict):
            for k, v in occupied_slots:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if items is not None: self.value['conditions']['items'] = items
        if empty_slots is not None or full_slots is not None or occupied_slots is not None: self.value['conditions']['slots'] = {}
        if empty_slots is not None: self.value['conditions']['slots']['empty'] = empty_slots
        if full_slots is not None: self.value['conditions']['slots']['full'] = full_slots
        if occupied_slots is not None: self.value['conditions']['slots']['occupied'] = occupied_slots
        if player is not None: self.value['conditions']['player'] = player

    def item_durability_changed(self, delta: Optional[Union[int, Dict[str, int]]]=None, durability: Optional[Union[int, Dict[str, int]]]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:item_durability_changed',
            'conditions': {}
        }
        if isinstance(delta, dict):
            for k, v in delta:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if isinstance(durability, dict):
            for k, v in durability:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        if delta is not None: self.value['conditions']['delta'] = delta
        if durability is not None: self.value['conditions']['durability'] = durability
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def item_used_on_block(self, location: Optional[dict]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:item_used_on_block',
            'conditions': {}
        }
        if location is not None: self.value['conditions']['location'] = location
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def killed_by_crossbow(self, *victims: Union[List[str], dict], unique_entity_types: Optional[Union[int, Dict[str, int]]], player: Optional[Union[List[str], dict]]=None):
        pass
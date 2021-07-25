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

    def set_requirements(self, *criterion_lists: List[Union[str, 'Criterion']]):
        for li, criterion_list in enumerate(criterion_lists):
            for ei, criterion in enumerate(criterion_list):
                if isinstance(criterion, Criterion):
                    criterion_lists[li][ei] = criterion.name
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

RangeDict = Dict[str, int]
class Criterion:
    def __init__(self, ad, name: str):
        self.name = name
        self.ad = ad
        if 'name' not in self.ad.value['criteria']: self.ad.value['criteria'][self.name] = {}
        self.value = self.ad.value['criteria'][self.name]
        print(self.value is self.ad.value['criteria'][self.name])

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

    def construct_beacon(self, level: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:construct_beacon',
            'conditions': {}
        }
        internal.check_range(level)
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

    def effects_changed_effect(self, effect_name: Optional[str]=None, amplifier: Optional[Union[int, RangeDict]]=None, duration: Optional[Union[int, RangeDict]]=None):
        self.value['trigger'] = 'minecraft:effects_changed'
        if 'conditions' not in self.value.keys(): self.value['conditions'] = {}
        if 'effects' not in self.value['conditions'].keys(): self.value['conditions']['effects'] = {}
        self.value['conditions']['effects'][effect_name] = {}
        internal.check_range(amplifier)
        internal.check_range(duration)
        if amplifier is not None: self.value['conditions']['amplifier'] = amplifier
        if duration is not None: self.value['conditions']['duration'] = duration

    def enchanted_item(self, item: Optional[dict]=None, levels: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:enchanted_item',
            'conditions': {}
        }
        internal.check_range(levels)
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
        self.value['trigger'] = 'minecraft:impossible'
        self.value['conditions'] = {}

    def inventory_changed(self, *items: dict, empty_slots: Optional[Union[int, RangeDict]]=None, full_slots: Optional[Union[int, RangeDict]]=None, occupied_slots: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:inventory_changed',
            'conditions': {}
        }
        for l in (empty_slots, full_slots, occupied_slots): internal.check_range(l)
        if any([x is not None for x in (empty_slots, full_slots, occupied_slots)]): self.value['conditions']['slots'] = {}
        if empty_slots is not None: self.value['conditions']['slots']['empty'] = empty_slots
        if full_slots is not None: self.value['conditions']['slots']['full'] = full_slots
        if occupied_slots is not None: self.value['conditions']['slots']['occupied'] = occupied_slots
        if player is not None: self.value['conditions']['player'] = player

    def item_durability_changed(self, delta: Optional[Union[int, RangeDict]]=None, durability: Optional[Union[int, RangeDict]]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:item_durability_changed',
            'conditions': {}
        }
        internal.check_range(delta)
        internal.check_range(durability)
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

    def killed_by_crossbow(self, *victims: Union[List[str], dict], unique_entity_types: Optional[Union[int, RangeDict]], player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:killed_by_crossbow',
            'conditions': {}
        }
        internal.check_range(unique_entity_types)
        if len(victims) != 0: self.value['victims'] = list(victims)
        if unique_entity_types is not None: self.value['unique_entity_types'] = unique_entity_types
        if player is not None: self.value['conditions']['player'] = player

    def levitation(self, absolute_distance: Optional[RangeDict]=None, horizontal_distance: Optional[RangeDict]=None, x_distance: Optional[RangeDict]=None, y_distance: Optional[RangeDict]=None,
                   z_distance: Optional[RangeDict]=None, duration: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:levitation',
            'conditions': {}
        }
        for l in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance, duration): internal.check_range(l)
        if any([x is not None for x in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance)]): self.value['distance']
        if absolute_distance is not None: self.value['distance']['absolute'] = absolute_distance
        if horizontal_distance is not None: self.value['distance']['horizontal'] = horizontal_distance
        if x_distance is not None: self.value['distance']['x'] = x_distance
        if y_distance is not None: self.value['distance']['y'] = y_distance
        if z_distance is not None: self.value['distance']['z'] = z_distance
        if duration is not None: self.value['duration'] = duration
        if player is not None: self.value['player'] = player

    def lightning_strike(self, lightning: Optional[Union[List[str], dict]]=None, bystander: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:lightning_strike',
            'conditions': {}
        }
        if lightning is not None: self.value['lightning'] = lightning
        if bystander is not None: self.value['bystander'] = bystander
        if player is not None: self.value['player'] = player

    def location(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:location',
            'conditions': {}
        }
        if location is not None: self.value['location'] = location
        if player is not None: self.value['player'] = player
    
    def nether_travel(self, entered: Optional[dict]=None, exited: Optional[dict]=None, absolute_distance: Optional[RangeDict]=None, horizontal_distance: Optional[RangeDict]=None,
                      x_distance: Optional[RangeDict]=None, y_distance: Optional[RangeDict]=None, z_distance: Optional[RangeDict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:nether_travel',
            'conditions': {}
        }
        for l in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance): internal.check_range(l)
        if any([x is not None for x in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance)]): self.value['distance']
        if absolute_distance is not None: self.value['distance']['absolute'] = absolute_distance
        if horizontal_distance is not None: self.value['distance']['horizontal'] = horizontal_distance
        if x_distance is not None: self.value['distance']['x'] = x_distance
        if y_distance is not None: self.value['distance']['y'] = y_distance
        if z_distance is not None: self.value['distance']['z'] = z_distance
        if entered is not None: self.value['entered'] = entered
        if exit is not None: self.value['exit'] = exit
        if player is not None: self.value['player'] = player

    def placed_block(self, block: Optional[str]=None, item: Optional[dict]=None, location: Optional[dict]=None, state: Optional[Dict[str, str]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:placed_block',
            'conditions': {}
        }
        if block is not None: self.value['block'] = block
        if item is not None: self.value['item'] = item
        if location is not None: self.value['location'] = location
        if state is not None: self.value['state'] = state
        if player is not None: self.value['player'] = player

    def player_generates_container_loot(self, loot_table: Optional[str], player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:player_generates_container_loot',
            'conditions': {}
        }
        if loot_table is not None: self.value['loot_table'] = loot_table
        if player is not None: self.value['player'] = player

    def player_hurt_entity(self, damage: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:player_hurt_entity',
            'conditions': {}
        }
        if damage is not None: self.value['conditions']['damage'] = damage
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def player_interacted_with_entity(self, item: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:player_interacted_with_entity',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def player_killed_entity(self, entity: Optional[Union[List[str], dict]]=None, killing_blow: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:player_killed_entity',
            'conditions': {}
        }
        if entity is not None: self.value['conditions']['entity'] = entity
        if killing_blow is not None: self.value['conditions']['killing_blow'] = killing_blow
        if player is not None: self.value['conditions']['player'] = player

    def recipe_unlocked(self, recipe: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:recipe_unlocked',
            'conditions': {}
        }
        if recipe is not None: self.value['conditions']['recipe'] = recipe
        if player is not None: self.value['conditions']['player'] = player

    def shot_crossbow(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:shot_crossbow',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def slept_in_bed(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:slept_in_bed',
            'conditions': {}
        }
        if location is not None: self.value['conditions']['location'] = location
        if player is not None: self.value['conditions']['player'] = player

    def slide_down_block(self, block: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:slide_down_block',
            'conditions': {}
        }
        if block is not None: self.value['conditions']['block'] = block
        if player is not None: self.value['conditions']['player'] = player

    def start_riding(self, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:start_riding',
            'conditions': {}
        }
        if player is not None: self.value['conditions']['player'] = player

    def summoned_entity(self, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:summoned_entity',
            'conditions': {}
        }
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def tame_animal(self, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:tame_animal',
            'conditions': {}
        }
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player 

    def target_hit(self, signal_strength: Optional[int]=None, projectile: Optional[str]=None, shooter: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:target_hit',
            'conditions': {}
        }
        if signal_strength is not None: self.value['conditions']['signal_strength'] = signal_strength
        if projectile is not None: self.value['conditions']['projectile'] = projectile
        if shooter is not None: self.value['conditions']['shooter'] = shooter
        if player is not None: self.value['conditions']['player'] = player

    def thrown_item_picked_up_by_entity(self, item: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:thrown_item_picked_up_by_entity',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def tick(self, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:tick',
            'conditions': {}
        }
        if player is not None: self.value['conditions']['player'] = player

    def used_ender_eye(self, distance: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:used_ender_eye',
            'conditions': {}
        }
        internal.check_range(distance)
        if distance is not None: self.value['conditions']['distance'] = distance
        if player is not None: self.value['conditions']['player'] = player

    def used_totem(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:used_totem',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def using_item(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:using_item',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def villager_trade(self, item: Optional[dict]=None, vilager: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:villager_trade',
            'conditions': {}
        }
        if item is not None: self.value['conditions']['item'] = item
        if vilager is not None: self.value['conditions']['vilager'] = vilager
        if player is not None: self.value['conditions']['player'] = player

    def voluntary_exile(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        self.value = {
            'trigger': 'minecraft:voluntary_exile',
            'conditions': {}
        }
        if location is not None: self.value['conditions']['location'] = location
        if player is not None: self.value['conditions']['player'] = player
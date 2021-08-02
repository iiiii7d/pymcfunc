from typing import Union, Optional, Any, Callable, List, Dict
from functools import wraps
import pymcfunc.internal as internal
import pymcfunc.func_handlers as func_handler

class Advancement:
    """An advancement in Java Edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement"""

    def __init__(self, p, name: str, parent: Union[str, 'Advancement']):
        """Initialises the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.__init__"""
        self.p = p
        self.name = name
        self.namespaced = self.p.name+":"+self.name
        self.p.advancements[name] = {
            "criteria": {},
            "rewards": {}
        }
        self.value = self.p.advancements[self.name]
        if parent is not None:
            if isinstance(parent, type(self)):
                self.value['parent'] = parent.name
            else:
                self.value['parent'] = parent

    def set_icon(self, item_name: str, nbt: Optional[dict]=None):
        """Sets the icon of the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.set_icon"""
        if 'display' not in self.value.keys():
            self.value['display'] = {}
        self.value['display']['item'] = item_name
        if nbt is not None:
            self.value['display']['nbt'] = nbt

    def set_display(self, attr: str, value: Any):
        """Sets display parameters for the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.set_display"""
        internal.options(attr, ['icon', 'title', 'frame', 'background', 'description', 'show_toast', 'announce_to_chat', 'hidden'])
        if 'display' not in self.value.keys():
            self.value['display'] = {}
        self.value['display'][attr] = value

    def set_parent(self, parent: Union[str, 'Advancement']):
        """Sets the parent for the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.set_parent"""
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
        """Creates and returns a new criterion for the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.criterion"""
        return Criterion(self, name)

    def set_requirements(self, *criterion_lists: List[Union[str, 'Criterion']]):
        """Sets the requirements for the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.set_requirements"""
        for li, criterion_list in enumerate(criterion_lists):
            for ei, criterion in enumerate(criterion_list):
                if isinstance(criterion, Criterion):
                    criterion_lists[li][ei] = criterion.name
        self.value['requirements'] = list(criterion_lists)

    def reward(self, item: str, value: Any):
        """Sets the reward for the advancement.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.reward"""
        internal.options(item, ['recipes', 'loot', 'experience', 'function'])
        self.value['rewards'][item] = value

    def on_reward(self, func: Callable[[func_handler.JavaFuncHandler], Any]):
        """The function with the tag will be called when the achievement is gotten.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.on_reward"""
        @wraps(func)
        def wrapper(m):
            self.value['rewards']['function'] = func.__name__
            func(m)
        return wrapper

RangeDict = Dict[str, int]
class Criterion:
    """A criterion for an advancement.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion"""

    def __init__(self, ach, name: str):
        """Initialises the criterion.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.__init__"""
        self.name = name
        self.ach = ach
        if 'name' not in self.ach.value['criteria']: self.ach.value['criteria'][self.name] = {}
        self.value = self.ach.value['criteria'][self.name]

    def _setup(self, trigger):
        self.value['trigger'] = "minecraft:"+trigger
        self.value['conditions'] = {}

    def bee_nest_destroyed(self, block: Optional[str]=None, item: Optional[dict]=None, num_bees_inside: Optional[int]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `bee_nest_destroyed`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.bee_nest_destroyed"""
        """Sets the criterion’s trigger to `bee_nest_destroyed`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.bee_nest_destroyed"""
        self._setup("bee_nest_destroyed")
        if block is not None and block.startswith("minecraft:"): internal.options(block, ["minecraft:bee_nest", "minecraft:beehive"])
        if block is not None: self.value['conditions']['block'] = block
        if item is not None: self.value['conditions']['item'] = item
        if num_bees_inside is not None: self.value['conditions']['num_bees_inside'] = num_bees_inside
        if player is not None: self.value['conditions']['player'] = player

    def bred_animals(self, child: Optional[Union[List[str], dict]]=None, parent: Optional[Union[List[str], dict]]=None, partner: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `bred_animals`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.bred_animals"""
        self._setup("bred_animals")
        if child is not None: self.value['conditions']['child'] = child
        if parent is not None: self.value['conditions']['parent'] = parent
        if partner is not None: self.value['conditions']['partner'] = partner
        if player is not None: self.value['conditions']['player'] = player

    def brewed_potion(self, potion: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `brewed_potion`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.brewed_potion"""
        self._setup("brewed_potion")
        if potion is not None: self.value['conditions']['potion'] = potion
        if player is not None: self.value['conditions']['player'] = player

    def changed_dimension(self, from_: Optional[str]=None, to: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `changed_dimension`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.changed_dimension"""
        self._setup("changed_dimension")
        for d in (from_, to):
            if d is not None: internal.options(d, ['overworld', 'the_nether', 'the_end'])
        if from_ is not None: self.value['conditions']['from_'] = from_
        if to is not None: self.value['conditions']['to'] = to
        if player is not None: self.value['conditions']['player'] = player

    def channeled_lightning(self, *victims: Union[List[str], dict], player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `channeled_lightning`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.channeled_lightning"""
        self._setup("channeled_lightning")
        if len(victims) != 0: self.value['conditions']['victims'] = list(victims)
        if player is not None: self.value['conditions']['player'] = player

    def construct_beacon(self, level: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `construct_beacon`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.construct_beacon"""
        self._setup("construct_beacon")
        internal.check_range(level)
        if level is not None: self.value['conditions']['level'] = level
        if player is not None: self.value['conditions']['player'] = player

    def consume_item(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `consume_item`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.consume_item"""
        self._setup("consume_item")
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def cured_zombie_villager(self, villager: Optional[Union[List[str], dict]]=None, zombie: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `cured_zombie_villager`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.cured_zombie_villager"""
        self._setup("cured_zombie_villager")
        if villager is not None: self.value['conditions']['villager'] = villager
        if zombie is not None: self.value['conditions']['zombie'] = zombie
        if player is not None: self.value['conditions']['player'] = player

    def effects_changed(self, source: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `effects_changed`. Used together with `effects_changed_effect()`
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.effects_changed"""
        self.value['trigger'] = 'minecraft:effects_changed'
        if 'conditions' not in self.value.keys(): self.value['conditions'] = {}
        if source is not None: self.value['conditions']['source'] = source
        if player is not None: self.value['conditions']['player'] = player

    def effects_changed_effect(self, effect_name: Optional[str]=None, amplifier: Optional[Union[int, RangeDict]]=None, duration: Optional[Union[int, RangeDict]]=None):
        """An effect, for when the criterion is `effects_changed`. Used together with `effects_changed()`
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.effects_changed_effect"""
        self.value['trigger'] = 'minecraft:effects_changed'
        if 'conditions' not in self.value.keys(): self.value['conditions'] = {}
        if 'effects' not in self.value['conditions'].keys(): self.value['conditions']['effects'] = {}
        self.value['conditions']['effects'][effect_name] = {}
        internal.check_range(amplifier)
        internal.check_range(duration)
        if amplifier is not None: self.value['conditions']['amplifier'] = amplifier
        if duration is not None: self.value['conditions']['duration'] = duration

    def enchanted_item(self, item: Optional[dict]=None, levels: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `enchanted_item`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.enchanted_item"""
        self._setup("enchanted_item")
        internal.check_range(levels)
        if item is not None: self.value['conditions']['item'] = item
        if levels is not None: self.value['conditions']['levels'] = levels
        if player is not None: self.value['conditions']['player'] = player

    def enter_block(self, block: Optional[str]=None, state: Optional[Dict[str, str]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `enter_block`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.enter_block"""
        self._setup("enter_block")
        if block is not None: self.value['conditions']['block'] = block
        if state is not None: self.value['conditions']['state'] = state
        if player is not None: self.value['conditions']['player'] = player

    def entity_hurt_player(self, damage: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `entity_hurt_player`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.entity_hurt_player"""
        self._setup("entity_hurt_player")
        if damage is not None: self.value['conditions']['damage'] = damage
        if player is not None: self.value['conditions']['player'] = player

    def entity_killed_player(self, entity: Optional[Union[List[str], dict]]=None, killing_blow: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `entity_killed_player`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.entity_killed_player"""
        self._setup("entity_killed_player")
        if entity is not None: self.value['conditions']['entity'] = entity
        if killing_blow is not None: self.value['conditions']['killing_blow'] = killing_blow
        if player is not None: self.value['conditions']['player'] = player

    def filled_bucket(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `filled_bucket`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.filled_bucket"""
        self._setup("filled_bucket")
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def fishing_rod_hooked(self, entity: Optional[Union[List[str], dict]]=None, item: Optional[dict]=None, rod: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `fishing_rod_hooked`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.fishing_rod_hooked"""
        self._setup("fishing_rod_hooked")
        if entity is not None: self.value['conditions']['entity'] = entity
        if item is not None: self.value['conditions']['item'] = item
        if rod is not None: self.value['conditions']['rod'] = rod
        if player is not None: self.value['conditions']['player'] = player

    def hero_of_the_village(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `hero_of_the_village`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.hero_of_the_village"""
        self._setup("hero_of_the_village")
        if location is not None: self.value['conditions']['location'] = location
        if player is not None: self.value['conditions']['player'] = player

    def impossible(self):
        """Sets the criterion’s trigger to `impossible`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.impossible"""
        self.value['trigger'] = 'minecraft:impossible'
        self.value['conditions'] = {}

    def inventory_changed(self, *items: dict, empty_slots: Optional[Union[int, RangeDict]]=None, full_slots: Optional[Union[int, RangeDict]]=None, occupied_slots: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `inventory_changed`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.inventory_changed"""
        self._setup("inventory_changed")
        for l in (empty_slots, full_slots, occupied_slots): internal.check_range(l)
        if any([x is not None for x in (empty_slots, full_slots, occupied_slots)]): self.value['conditions']['slots'] = {}
        if len(items) != 0: self.value['conditions']['slots']['items'] = list(items)
        if empty_slots is not None: self.value['conditions']['slots']['empty'] = empty_slots
        if full_slots is not None: self.value['conditions']['slots']['full'] = full_slots
        if occupied_slots is not None: self.value['conditions']['slots']['occupied'] = occupied_slots
        if player is not None: self.value['conditions']['player'] = player

    def item_durability_changed(self, delta: Optional[Union[int, RangeDict]]=None, durability: Optional[Union[int, RangeDict]]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `item_durability_changed`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.item_durability_changed"""
        self._setup("item_durability_changed")
        internal.check_range(delta)
        internal.check_range(durability)
        if delta is not None: self.value['conditions']['delta'] = delta
        if durability is not None: self.value['conditions']['durability'] = durability
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def item_used_on_block(self, location: Optional[dict]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `item_used_on_block`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.item_used_on_block"""
        self._setup("item_used_on_block")
        if location is not None: self.value['conditions']['location'] = location
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def killed_by_crossbow(self, *victims: Union[List[str], dict], unique_entity_types: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `killed_by_crossbow`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.killed_by_crossbow"""
        self._setup("killed_by_crossbow")
        internal.check_range(unique_entity_types)
        if len(victims) != 0: self.value['victims'] = list(victims)
        if unique_entity_types is not None: self.value['unique_entity_types'] = unique_entity_types
        if player is not None: self.value['conditions']['player'] = player

    def levitation(self, absolute_distance: Optional[RangeDict]=None, horizontal_distance: Optional[RangeDict]=None, x_distance: Optional[RangeDict]=None, y_distance: Optional[RangeDict]=None,
                   z_distance: Optional[RangeDict]=None, duration: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `levitation`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.levitation"""
        self._setup("levitation")
        for l in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance, duration): internal.check_range(l)
        if any([x is not None for x in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance)]): self.value['distance'] = {}
        if absolute_distance is not None: self.value['distance']['absolute'] = absolute_distance
        if horizontal_distance is not None: self.value['distance']['horizontal'] = horizontal_distance
        if x_distance is not None: self.value['distance']['x'] = x_distance
        if y_distance is not None: self.value['distance']['y'] = y_distance
        if z_distance is not None: self.value['distance']['z'] = z_distance
        if duration is not None: self.value['duration'] = duration
        if player is not None: self.value['player'] = player

    def lightning_strike(self, lightning: Optional[Union[List[str], dict]]=None, bystander: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `lightning_strike`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.lightning_strike"""
        self._setup("lightning_strike")
        if lightning is not None: self.value['lightning'] = lightning
        if bystander is not None: self.value['bystander'] = bystander
        if player is not None: self.value['player'] = player

    def location(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `location`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.location"""
        self._setup("location")
        if location is not None: self.value['location'] = location
        if player is not None: self.value['player'] = player

    def nether_travel(self, entered: Optional[dict]=None, exited: Optional[dict]=None, absolute_distance: Optional[RangeDict]=None, horizontal_distance: Optional[RangeDict]=None,
                      x_distance: Optional[RangeDict]=None, y_distance: Optional[RangeDict]=None, z_distance: Optional[RangeDict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `nether_travel`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.nether_travel"""
        self._setup("nether_travel")
        for l in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance): internal.check_range(l)
        if any([x is not None for x in (absolute_distance, horizontal_distance, x_distance, y_distance, z_distance)]): self.value['distance'] = {}
        if absolute_distance is not None: self.value['distance']['absolute'] = absolute_distance
        if horizontal_distance is not None: self.value['distance']['horizontal'] = horizontal_distance
        if x_distance is not None: self.value['distance']['x'] = x_distance
        if y_distance is not None: self.value['distance']['y'] = y_distance
        if z_distance is not None: self.value['distance']['z'] = z_distance
        if entered is not None: self.value['entered'] = entered
        if exited is not None: self.value['exit'] = exited
        if player is not None: self.value['player'] = player

    def placed_block(self, block: Optional[str]=None, item: Optional[dict]=None, location: Optional[dict]=None, state: Optional[Dict[str, str]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `placed_block`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.placed_block"""
        self._setup("placed_block")
        if block is not None: self.value['block'] = block
        if item is not None: self.value['item'] = item
        if location is not None: self.value['location'] = location
        if state is not None: self.value['state'] = state
        if player is not None: self.value['player'] = player

    def player_generates_container_loot(self, loot_table: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `player_generates_container_loot`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.player_generates_container_loot"""
        self._setup("player_generates_container_loot")
        if loot_table is not None: self.value['loot_table'] = loot_table
        if player is not None: self.value['player'] = player

    def player_hurt_entity(self, damage: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `player_hurt_entity`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.player_hurt_entity"""
        self._setup("player_hurt_entity")
        if damage is not None: self.value['conditions']['damage'] = damage
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def player_interacted_with_entity(self, item: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `player_interacted_with_entity`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.player_interacted_with_entity"""
        self._setup("player_interacted_with_entity")
        if item is not None: self.value['conditions']['item'] = item
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def player_killed_entity(self, entity: Optional[Union[List[str], dict]]=None, killing_blow: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `player_killed_entity`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.player_killed_entity"""
        self._setup("player_killed_entity")
        if entity is not None: self.value['conditions']['entity'] = entity
        if killing_blow is not None: self.value['conditions']['killing_blow'] = killing_blow
        if player is not None: self.value['conditions']['player'] = player

    def recipe_unlocked(self, recipe: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `recipe_unlocked`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.recipe_unlocked"""
        self._setup("recipe_unlocked")
        if recipe is not None: self.value['conditions']['recipe'] = recipe
        if player is not None: self.value['conditions']['player'] = player

    def shot_crossbow(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `shot_crossbow`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.shot_crossbow"""
        self._setup("shot_crossbow")
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def slept_in_bed(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `slept_in_bed`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.slept_in_bed"""
        self._setup("slept_in_bed")
        if location is not None: self.value['conditions']['location'] = location
        if player is not None: self.value['conditions']['player'] = player

    def slide_down_block(self, block: Optional[str]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `slide_down_block`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.slide_down_block"""
        self._setup("slide_down_block")
        if block is not None: self.value['conditions']['block'] = block
        if player is not None: self.value['conditions']['player'] = player

    def start_riding(self, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `start_riding`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.start_riding"""
        self._setup("start_riding")
        if player is not None: self.value['conditions']['player'] = player

    def summoned_entity(self, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `summoned_entity`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.summoned_entity"""
        self._setup("summoned_entity")
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def tame_animal(self, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `tame_animal`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.tame_animal"""
        self._setup("tame_animal")
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def target_hit(self, signal_strength: Optional[int]=None, projectile: Optional[str]=None, shooter: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `target_hit`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.target_hit"""
        self._setup("target_hit")
        if signal_strength is not None: self.value['conditions']['signal_strength'] = signal_strength
        if projectile is not None: self.value['conditions']['projectile'] = projectile
        if shooter is not None: self.value['conditions']['shooter'] = shooter
        if player is not None: self.value['conditions']['player'] = player

    def thrown_item_picked_up_by_entity(self, item: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `thrown_item_picked_up_by_entity`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.thrown_item_picked_up_by_entity"""
        self._setup("thrown_item_picked_up_by_entity")
        if item is not None: self.value['conditions']['item'] = item
        if entity is not None: self.value['conditions']['entity'] = entity
        if player is not None: self.value['conditions']['player'] = player

    def tick(self, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `tick`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.tick"""
        self._setup("tick")
        if player is not None: self.value['conditions']['player'] = player

    def used_ender_eye(self, distance: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `used_ender_eye`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.used_ender_eye"""
        self._setup("used_ender_eye")
        internal.check_range(distance)
        if distance is not None: self.value['conditions']['distance'] = distance
        if player is not None: self.value['conditions']['player'] = player

    def used_totem(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `used_totem`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.used_totem"""
        self._setup("used_totem")
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def using_item(self, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `using_item`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.using_item"""
        self._setup("using_item")
        if item is not None: self.value['conditions']['item'] = item
        if player is not None: self.value['conditions']['player'] = player

    def villager_trade(self, item: Optional[dict]=None, villager: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `villager_trade`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.villager_trade"""
        self._setup("villager_trade")
        if item is not None: self.value['conditions']['item'] = item
        if villager is not None: self.value['conditions']['villager'] = villager
        if player is not None: self.value['conditions']['player'] = player

    def voluntary_exile(self, location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None):
        """Sets the criterion’s trigger to `voluntary_exile`.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Criterion.voluntary_exile"""
        self._setup("voluntary_exile")
        if location is not None: self.value['conditions']['location'] = location
        if player is not None: self.value['conditions']['player'] = player
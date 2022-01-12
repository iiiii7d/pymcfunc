from __future__ import annotations

import inspect
from functools import wraps
from typing import TypeAlias, Union, Literal, Callable, Any

from pymcfunc import func_handler
from pymcfunc.json_format import ItemJson, EntityJson, DamageJson, DamageTypeJson, LocationJson, IntRange, FloatRange, \
    DoubleRange
from pymcfunc.nbt import Compound, NBT

RawJson: TypeAlias = Union[dict, list]

class Advancement:
    def __init__(self, namespace: str, name: str, **kwargs):
        self.name: str = name
        self.namespace: str = namespace

        self.display: AdvancementDisplay | None = None
        self.parent: str | Advancement | None = None
        self.criteria: list[Criterion] = []
        self.requirements: list[list[Criterion]] | None = None
        self.rewards: Rewards | None = None

        for k, v in kwargs.items(): setattr(self, k, v)

    def namespaced(self) -> str: return self.namespace+":"+self.name

    def on_advancement_get(self, func: Callable[[func_handler.JavaFuncHandler, ...], Any]):
        """The function with the tag will be called when the achievement is gotten.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.on_reward"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.rewards is None: self.rewards = Rewards()
            self.rewards.function = func.__name__ # TODO namespace
            return func(*args, **kwargs)
        return wrapper

    def json(self) -> dict:
        d: dict = {}
        if self.display is not None: d['display'] = self.display.json()
        if self.parent is not None: d['display'] = self.parent.namespaced() if isinstance(self.parent, Advancement) else self.parent
        if self.criteria is not None: d['criteria'] = {c.name: c.json for c in self.criteria}
        if self.requirements is not None: d['requirements'] = [[c.name for c in cs] for cs in self.requirements]
        if self.rewards is not None: d['rewards'] = self.rewards.json()
        return d

class AdvancementDisplay:
    def __init__(self, **kwargs):
        self.icon_item: str = "air"
        self.icon_nbt: Compound = Compound({})
        self.title: str | RawJson = ""
        self.frame: Literal["challenge", "goal", "task"] = "task"
        self.background: str | None = None
        self.description: str | RawJson = ""
        self.show_toast: bool = True
        self.announce_to_chat: bool = True
        self.hidden: bool = False

        for k, v in kwargs.items(): setattr(self, k, v)

    def __setattr__(self, key: str, value):
        if key == "icon_nbt" and not isinstance(value, Compound):
            value = Compound(value)
        super().__setattr__(key, value)

    def json(self) -> dict:
        d = {
            "icon_item": self.icon_item,
            "icon_nbt": str(self.icon_nbt),
            "title": str(self.title),
            "frame": self.frame,
            "description": str(self.description)
        }
        if self.background is not None: d['background'] = self.background
        if not self.show_toast: d['show_toast'] = self.show_toast
        if not self.announce_to_chat: d['announce_to_chat'] = self.announce_to_chat
        if self.hidden: d['hidden'] = self.hidden
        return d

Recipe: TypeAlias = str # TODO Recipe and LootTable and Function and Predicate class
LootTable: TypeAlias = str
Function: TypeAlias = str
Predicate: TypeAlias = str
class Rewards:
    def __init__(self, **kwargs):
        self.recipes: list[Recipe] = []
        self.loot: list[LootTable] = []
        self.experience: int = 0
        self.function: Function | str = ""

        for k, v in kwargs.items(): setattr(self, k, v)

    def json(self) -> dict:
        return {
            "recipes": self.recipes,
            "loot": self.loot,
            "experience": self.experience,
            "function": self.function
        }


class Criterion:
    def __init__(self, name: str):
        self.name = name
        self.json: dict = {}
        self.trigger: str = ""

    @staticmethod
    def _trigger(func: Callable[..., Criterion]):
        def wrapper(*args, **kwargs) -> Criterion:
            crit = Criterion(args[0])
            crit.trigger = "minecraft:"+func.__name__
            for arg, param in inspect.signature(func).parameters.items():
                if arg in ("self", "name"): continue
                if arg not in kwargs or kwargs[arg] == param.default: continue

                def convert(in_):
                    if issubclass(type(in_), NBT): return in_.py()
                    elif issubclass(type(in_), list): return [convert(i) for i in in_]
                    elif issubclass(type(in_), dict): return {k: convert(v) for k, v in in_}
                    elif 'json' in dir(in_): return in_.json()
                    else: return in_
                crit.json[arg] = convert(kwargs[arg])
            return crit
        return wrapper

    # Don't worry if all the functions are empty. See _trigger for the logic.
    @classmethod
    @_trigger
    def bee_nest_destroyed(cls, name: str, *,
                           block: str | None = None,
                           item: ItemJson | None = None,
                           num_bees_inside: int | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def bred_animals(cls, name: str, *,
                     child: EntityJson | list[Predicate] | None = None,
                     parent: EntityJson | list[Predicate] | None = None,
                     partner: EntityJson | list[Predicate] | None = None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def brewed_potion(cls, name: str, *,
                      potion: str | None = None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def changed_dimension(cls, name: str, *,
                          from_: Literal["overworld", "the_nether", "the_end"] | None = None,
                          to: Literal["overworld", "the_nether", "the_end"] | None = None,
                          player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def channeled_lightning(cls, name: str, *,
                            victims: list[EntityJson | list[Predicate]] | None = None,
                            player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def construct_beacon(cls, name: str, *,
                         level: int | IntRange | None = None,
                         player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def consume_item(cls, name: str, *,
                     item: ItemJson | None = None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def cured_zombie_villager(cls, name: str, *,
                              villager: EntityJson | list[Predicate] | None = None,
                              zombie: EntityJson | list[Predicate] | None = None,
                              player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def effects_changed(cls, name: str, *,
                        effects: dict[str, dict[Literal["amplifier", "duration"], int | IntRange]] | None = None,
                        source: EntityJson | list[Predicate] | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def enchanted_item(cls, name: str, *,
                       item: ItemJson | None = None,
                       levels: int | IntRange | None = None,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def enter_block(cls, name: str, *,
                    block: str | None = None,
                    state: dict[str, Any] | None = None,
                    player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def entity_hurt_player(cls, name: str, *,
                           damage: DamageJson | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def entity_killed_player(cls, name: str, *,
                             entity: EntityJson | list[Predicate] | None = None,
                             killing_blow: DamageTypeJson | None = None,
                             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def filled_bucket(cls, name: str, *,
                      item: ItemJson | None = None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def fishing_rod_hooked(cls, name: str, *,
                           entity: EntityJson | list[Predicate] | None = None,
                           item: ItemJson | None = None,
                           rod: ItemJson | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def hero_of_the_village(cls, name: str, *,
                            location: LocationJson | None = None,
                            player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def impossible(cls, name: str) -> Criterion: pass

    @classmethod
    @_trigger
    def inventory_changed(cls, name: str, *,
                          items: list[ItemJson] | None = None,
                          slots: dict[Literal["empty", "full", "occupied"], int | IntRange] | None = None,
                          player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def item_durability_changed(cls, name: str, *,
                                delta: int | IntRange | None = None,
                                durability: int | IntRange | None = None,
                                item: ItemJson | None = None,
                                player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def item_used_on_block(cls, name: str, *,
                           location: LocationJson | None = None,
                           item: ItemJson | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def killed_by_crossbow(cls, name: str, *,
                           unique_entity_types: int | IntRange | None = None,
                           victims: EntityJson | list[EntityJson | list[Predicate]] | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def levitation(cls, name: str, *,
                   distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], IntRange] | None = None,
                   duration: int | IntRange | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def lightning_strike(cls, name: str, *,
                         lightning: EntityJson | list[Predicate] | None = None,
                         bystander: EntityJson | list[Predicate] | None = None,
                         player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def location(cls, name: str, *,
                 location: LocationJson | None = None,
                 player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def nether_travel(cls, name: str, *,
                      entered: LocationJson | None = None,
                      exited: LocationJson | None = None,
                      distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRange] | None = None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def placed_block(cls, name: str, *,
                     block: str | None = None,
                     item: ItemJson | None = None,
                     location: LocationJson | None = None,
                     state: dict[str, Any] | None = None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_generates_container_loot(cls, name: str, *,
                                        loot_table: LootTable | None = None,
                                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_hurt_entity(cls, name: str, *,
                           damage: DamageJson | None = None,
                           entity: EntityJson | list[Predicate] | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_interacted_with_entity(cls, name: str, *,
                                      item: ItemJson | None = None,
                                      entity: EntityJson | list[Predicate] | None = None,
                                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_killed_entity(cls, name: str, *,
                             entity: EntityJson | list[Predicate] | None = None,
                             killing_blow: DamageTypeJson | None = None,
                             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def recipe_unlocked(cls, name: str, *,
                        recipe: Recipe | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def shot_crossbow(cls, name: str, *,
                      item: ItemJson | None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def slept_in_bed(cls, name: str, *,
                     location: LocationJson | None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def slide_down_block(cls, name: str, *,
                         block: str,
                         player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def started_riding(cls, name: str, *,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def summoned_entity(cls, name: str, *,
                        entity: EntityJson | list[Predicate] | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def tame_animal(cls, name: str, *,
                    entity: EntityJson | list[Predicate] | None = None,
                    player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def target_hit(cls, name: str, *,
                   signal_strength: int | None = None,
                   projectile: int | None = None,
                   shooter: EntityJson | list[Predicate] | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def thrown_item_picked_up_by_entity(cls, name: str, *,
                                        item: ItemJson | None = None,
                                        entity: EntityJson | list[Predicate] | None = None,
                                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def tick(cls, name: str, *,
             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def used_ender_eye(cls, name: str, *,
                       distance: DoubleRange | None = None,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def used_totem(cls, name: str, *,
                   item: ItemJson | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def using_item(cls, name: str, *,
                   item: ItemJson | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def villager_trade(cls, name: str, *,
                       item: ItemJson | None = None,
                       villager: EntityJson | list[Predicate] | None = None,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def voluntary_exile(cls, name: str, *,
                        location: LocationJson | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    # TODO Deprecation warnings for below three

    @classmethod
    @_trigger
    def arbitrary_player_tick(cls, name: str) -> Criterion: pass

    @classmethod
    @_trigger
    def player_damaged(cls, name: str, *,
                       damage: DamageJson | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def safely_harvest_honey(cls, name: str, *,
                             block: dict[Literal["block", "tag"], str],
                             item: ItemJson | None,
                             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

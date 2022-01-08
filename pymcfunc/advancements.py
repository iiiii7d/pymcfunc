from __future__ import annotations

import inspect
from collections import Sequence
from typing import TypeAlias, Union, Literal, Callable, TypedDict, Any

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
                    elif issubclass(type(in_), Sequence): return [convert(i) for i in in_]
                    else: return in_
                crit.json[arg] = convert(kwargs[arg])
            return crit
        return wrapper

    # Don't worry if all the functions are empty. See _trigger for the logic.
    @classmethod
    @_trigger
    def bee_nest_destroyed(cls, name: str, *,
                           block: str | None = None,
                           item: Compound | None = None,
                           num_bees_inside: int | None = None,
                           player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def bred_animals(cls, name: str, *,
                     child: Compound | list[Predicate] | None = None,
                     parent: Compound | list[Predicate] | None = None,
                     partner: Compound | list[Predicate] | None = None,
                     player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def brewed_potion(cls, name: str, *,
                      potion: str | None = None,
                      player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def changed_dimension(cls, name: str, *,
                          from_: Literal["overworld", "the_nether", "the_end"] | None = None,
                          to: Literal["overworld", "the_nether", "the_end"] | None = None,
                          player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def channeled_lightning(cls, name: str, *,
                            victims: list[Compound | list[Predicate]] | None = None,
                            player: Compound | list[Predicate] | None = None) -> Criterion: pass

    _Range = TypedDict("_Range", {"min": int, "max": int}, total=False)
    @classmethod
    @_trigger
    def construct_beacon(cls, name: str, *,
                         level: str | _Range | None = None,
                         player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def consume_item(cls, name: str, *,
                     item: Compound | None = None,
                     player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def cured_zombie_villager(cls, name: str, *,
                              villager: Compound | list[Predicate] | None = None,
                              zombie: Compound | list[Predicate] | None = None,
                              player: Compound | list[Predicate] | None = None) -> Criterion: pass

    _Effect = TypedDict("_Effect", {
        "amplifier": Union[int, _Range],
        "duration": Union[int, _Range]},
                        total=False)
    @classmethod
    @_trigger
    def effects_changed(cls, name: str, *,
                        effects: dict[str, _Effect] | None = None,
                        source: Compound | list[Predicate] | None = None,
                        player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def enchanted_item(cls, name: str, *,
                       item: Compound | None = None,
                       levels: int | _Range | None = None,
                       player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def enter_block(cls, name: str, *,
                    block: str | None = None,
                    state: dict[str, Any] | None = None,
                    player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def entity_hurt_player(cls, name: str, *,
                           damage: Compound | None = None,
                           player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def entity_killed_player(cls, name: str, *,
                             entity: Compound | list[Predicate] | None = None,
                             killing_blow: Compound | None = None,
                             player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def filled_bucket(cls, name: str, *,
                      item: Compound | None = None,
                      player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def fishing_rod_hooked(cls, name: str, *,
                           entity: Compound | list[Predicate] | None = None,
                           item: Compound | None = None,
                           rod: Compound | None = None,
                           player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def hero_of_the_village(cls, name: str, *,
                            location: Compound | None = None,
                            player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def impossible(cls, name: str) -> Criterion: pass

    _Slots = TypedDict("_Slots", {
        "empty": Union[int, _Range],
        "full": Union[int, _Range],
        "occupied": Union[int, _Range],
    }, total=False)
    @classmethod
    @_trigger
    def inventory_changed(cls, name: str, *,
                          items: list[Compound] | None = None,
                          slots: _Slots | None = None,
                          player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def item_durability_changed(cls, name: str, *,
                                delta: str | _Range | None = None,
                                durability: str | _Range | None = None,
                                item: Compound | None = None,
                                player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def item_used_on_block(cls, name: str, *,
                           location: Compound | None = None,
                           item: Compound | None = None,
                           player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def killed_by_crossbow(cls, name: str, *,
                           unique_entity_types: int | _Range | None = None,
                           victims: Compound | list[Compound | list[Predicate]] | None = None,
                           player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def levitation(cls, name: str, *,
                   distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], _Range] | None = None,
                   duration: int | _Range | None = None,
                   player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def lightning_strike(cls, name: str, *,
                         lightning: Compound | list[Predicate] | None = None,
                         bystander: Compound | list[Predicate] | None = None,
                         player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def location(cls, name: str, *,
                 location: Compound | None = None,
                 player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def nether_travel(cls, name: str, *,
                      entered: Compound | None = None,
                      exited: Compound | None = None,
                      distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], _Range] | None = None,
                      player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def placed_block(cls, name: str, *,
                     block: str | None = None,
                     item: Compound | None = None,
                     location: Compound | None = None,
                     state: dict[str, Any] | None = None,
                     player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_generates_container_loot(cls, name: str, *,
                                        loot_table: LootTable | None = None,
                                        player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_hurt_entity(cls, name: str, *,
                           damage: Compound | None = None,
                           entity: Compound | list[Predicate] | None = None,
                           player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_interacted_with_entity(cls, name: str, *,
                                      item: Compound | None = None,
                                      entity: Compound | list[Predicate] | None = None,
                                      player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def player_killed_entity(cls, name: str, *,
                             entity: Compound | list[Predicate] | None = None,
                             killing_blow: Compound | None = None,
                             player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def recipe_unlocked(cls, name: str, *,
                        recipe: Recipe | None = None,
                        player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def shot_crossbow(cls, name: str, *,
                      item: Compound | None,
                      player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def slept_in_bed(cls, name: str, *,
                     location: Compound | None,
                     player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def slide_down_block(cls, name: str, *,
                         block: str,
                         player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def started_riding(cls, name: str, *,
                       player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def summoned_entity(cls, name: str, *,
                        entity: Compound | list[Predicate] | None = None,
                        player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def tame_animal(cls, name: str, *,
                    entity: Compound | list[Predicate] | None = None,
                    player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def target_hit(cls, name: str, *,
                   signal_strength: int | None = None,
                   projectile: int | None = None,
                   shooter: Compound | list[Predicate] | None = None,
                   player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def thrown_item_picked_up_by_entity(cls, name: str, *,
                                        item: Compound | None = None,
                                        entity: Compound | list[Predicate] | None = None,
                                        player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def tick(cls, name: str, *,
             player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def used_ender_eye(cls, name: str, *,
                       distance: _Range | None = None,
                       player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def used_totem(cls, name: str, *,
                   item: Compound | None = None,
                   player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def using_item(cls, name: str, *,
                   item: Compound | None = None,
                   player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def villager_trade(cls, name: str, *,
                       item: Compound | None = None,
                       villager: Compound | list[Predicate] | None = None,
                       player: Compound | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def voluntary_exile(cls, name: str, *,
                        location: Compound | None = None,
                        player: Compound | list[Predicate] | None = None) -> Criterion: pass

    # TODO Deprecation warnings for below three

    @classmethod
    @_trigger
    def arbitrary_player_tick(cls, name: str) -> Criterion: pass

    @classmethod
    @_trigger
    def player_damaged(cls, name: str, *,
                       damage: Compound | None = None) -> Criterion: pass

    @classmethod
    @_trigger
    def safely_harvest_honey(cls, name: str, *,
                             block: dict[Literal["block", "tag"], str],
                             item: Compound | None,
                             player: Compound | list[Predicate] | None = None) -> Criterion: pass

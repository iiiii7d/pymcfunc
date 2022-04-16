from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import TypeAlias, Union, Literal, Callable, Any, TYPE_CHECKING, Type, Optional

if TYPE_CHECKING: from pymcfunc.functions import Function
from pymcfunc.json_format import ItemJson, EntityJson, DamageJson, DamageTypeJson, LocationJson, IntRangeJson, FloatRangeJson, \
    DoubleRangeJson
from pymcfunc.nbt import Compound, NBT, List, NBTFormat, String, NBTRepresentable, Boolean, Int, make_nbt_representable, \
    DictReprAsList

RawJson: TypeAlias = Union[dict, list]

@dataclass(init=True)
class Advancement(NBTFormat):
    namespace: str
    name: str
    display: AdvancementDisplay | None = None
    parent: str | Advancement | None = None
    criteria: list[Criterion] = field(default_factory=list)
    requirements: list[list[Criterion]] | None = None
    rewards: Rewards | None = None

    @property
    def namespaced(self) -> str: return f'{self.namespace}:{self.name}'
    def __str__(self): return self.namespaced

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'display': AdvancementDisplay,
            'parent': Optional[String],
            'criteria': DictReprAsList[Criterion],
            'requirements': Optional[List[DictReprAsList[Criterion]]],
            'rewards': Optional[Rewards]
        }

    def on_advancement_get(self, func: Function) -> Function:
        """The function with the tag will be called when the achievement is gotten.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.advancements.Advancement.on_reward"""
        if self.rewards is None: self.rewards = Rewards()
        self.rewards.function = func
        return func

@dataclass(init=True)
class Icon(NBTFormat):
    item: str = "air"
    nbt: Compound | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'item': String,
            'nbt': Compound,
        }

@dataclass(init=True)
class AdvancementDisplay(NBTFormat):
    icon_: Icon = Icon("")
    title: str | RawJson = ""
    frame: Literal["challenge", "goal", "task"] | None = None
    background: str | None = None
    description: str | RawJson = ""
    show_toast: bool = True
    announce_to_chat: bool = True
    hidden: bool = False

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'icon': Icon,
            'title': Union[String, List[Compound], Compound],
            'frame': Optional[String],
            'background': Optional[String],
            'description': String,
            'show_toast': Boolean,
            'announce_to_chat': Boolean,
            'hidden': Boolean,
        }

Recipe: TypeAlias = str # TODO Recipe and LootTable and Predicate class
LootTable: TypeAlias = str
Predicate: TypeAlias = str
@dataclass(init=True)
class Rewards(NBTFormat):
    recipes: list[Recipe] | None = None
    loot: list[LootTable] | None = None
    experience: int | None = None
    function: Function | None = None

    def json(self) -> dict:
        return {
            "recipes": self.recipes,
            "loot": self.loot,
            "experience": self.experience,
            "function": self.function
        }

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBTRepresentable, NBT]]:
        return {
            'recipes': List[String],
            'loot': List[String],
            'experience': Optional[Int],
            'function': Optional[String]
        }

class Criterion(NBTFormat):
    def __init__(self, name: str):
        self.name = name
        self.trigger: str = ""

    @staticmethod
    def _trigger(**nbt_fmt: Type[NBTRepresentable, NBT]) -> Callable:
        def decorator(func: Callable[..., Criterion]) -> Callable:
            def wrapper(_, name, *__, **kwargs) -> Criterion:
                crit = Criterion(name)
                crit.trigger = "minecraft:" + func.__name__
                annos = {}
                for arg, param in inspect.signature(func).parameters.items():
                    if arg in ("self", "name"): continue
                    crit.__annotations__[arg] = param
                    annos[arg] = param

                    if arg in kwargs and kwargs[arg] != param.default:
                        crit.__dict__[arg] = kwargs[arg]

                crit.NBT_FORMAT = property(lambda self: {
                    **{k: make_nbt_representable(v) for k, v in annos},
                    **{k: Optional[v] for k, v in nbt_fmt}})

                def _immutable_lock(self, *_):
                    raise AttributeError(f"{type(self).__name__} is immutable")
                crit.__setattr__ = _immutable_lock
                return crit
            return wrapper
        return decorator

    @classmethod
    @_trigger()
    def bee_nest_destroyed(cls, name: str, *,
                           block: str | None = None,
                           item: ItemJson | None = None,
                           num_bees_inside: int | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def bred_animals(cls, name: str, *,
                     child: EntityJson | list[Predicate] | None = None,
                     parent: EntityJson | list[Predicate] | None = None,
                     partner: EntityJson | list[Predicate] | None = None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def brewed_potion(cls, name: str, *,
                      potion: str | None = None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def changed_dimension(cls, name: str, *,
                          from_: Literal["overworld", "the_nether", "the_end"] | None = None,
                          to: Literal["overworld", "the_nether", "the_end"] | None = None,
                          player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def channeled_lightning(cls, name: str, *,
                            victims: list[EntityJson | list[Predicate]] | None = None,
                            player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def construct_beacon(cls, name: str, *,
                         level: int | IntRangeJson | None = None,
                         player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def consume_item(cls, name: str, *,
                     item: ItemJson | None = None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def cured_zombie_villager(cls, name: str, *,
                              villager: EntityJson | list[Predicate] | None = None,
                              zombie: EntityJson | list[Predicate] | None = None,
                              player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def effects_changed(cls, name: str, *,
                        effects: dict[str, dict[Literal["amplifier", "duration"], int | IntRangeJson]] | None = None,
                        source: EntityJson | list[Predicate] | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def enchanted_item(cls, name: str, *,
                       item: ItemJson | None = None,
                       levels: int | IntRangeJson | None = None,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def enter_block(cls, name: str, *,
                    block: str | None = None,
                    state: dict[str, Any] | None = None,
                    player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def entity_hurt_player(cls, name: str, *,
                           damage: DamageJson | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def entity_killed_player(cls, name: str, *,
                             entity: EntityJson | list[Predicate] | None = None,
                             killing_blow: DamageTypeJson | None = None,
                             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def filled_bucket(cls, name: str, *,
                      item: ItemJson | None = None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def fishing_rod_hooked(cls, name: str, *,
                           entity: EntityJson | list[Predicate] | None = None,
                           item: ItemJson | None = None,
                           rod: ItemJson | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def hero_of_the_village(cls, name: str, *,
                            location: LocationJson | None = None,
                            player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def impossible(cls, name: str) -> Criterion: pass

    @classmethod
    @_trigger()
    def inventory_changed(cls, name: str, *,
                          items: list[ItemJson] | None = None,
                          slots: dict[Literal["empty", "full", "occupied"], int | IntRangeJson] | None = None,
                          player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def item_durability_changed(cls, name: str, *,
                                delta: int | IntRangeJson | None = None,
                                durability: int | IntRangeJson | None = None,
                                item: ItemJson | None = None,
                                player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def item_used_on_block(cls, name: str, *,
                           location: LocationJson | None = None,
                           item: ItemJson | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def killed_by_crossbow(cls, name: str, *,
                           unique_entity_types: int | IntRangeJson | None = None,
                           victims: EntityJson | list[EntityJson | list[Predicate]] | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def levitation(cls, name: str, *,
                   distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], IntRangeJson] | None = None,
                   duration: int | IntRangeJson | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def lightning_strike(cls, name: str, *,
                         lightning: EntityJson | list[Predicate] | None = None,
                         bystander: EntityJson | list[Predicate] | None = None,
                         player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def location(cls, name: str, *,
                 location: LocationJson | None = None,
                 player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def nether_travel(cls, name: str, *,
                      entered: LocationJson | None = None,
                      exited: LocationJson | None = None,
                      distance: dict[Literal["absolute", "horizontal", "x", "y", "z"], FloatRangeJson] | None = None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def placed_block(cls, name: str, *,
                     block: str | None = None,
                     item: ItemJson | None = None,
                     location: LocationJson | None = None,
                     state: dict[str, Any] | None = None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def player_generates_container_loot(cls, name: str, *,
                                        loot_table: LootTable | None = None,
                                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def player_hurt_entity(cls, name: str, *,
                           damage: DamageJson | None = None,
                           entity: EntityJson | list[Predicate] | None = None,
                           player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def player_interacted_with_entity(cls, name: str, *,
                                      item: ItemJson | None = None,
                                      entity: EntityJson | list[Predicate] | None = None,
                                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def player_killed_entity(cls, name: str, *,
                             entity: EntityJson | list[Predicate] | None = None,
                             killing_blow: DamageTypeJson | None = None,
                             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def recipe_unlocked(cls, name: str, *,
                        recipe: Recipe | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def shot_crossbow(cls, name: str, *,
                      item: ItemJson | None,
                      player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def slept_in_bed(cls, name: str, *,
                     location: LocationJson | None,
                     player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def slide_down_block(cls, name: str, *,
                         block: str,
                         player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def started_riding(cls, name: str, *,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def summoned_entity(cls, name: str, *,
                        entity: EntityJson | list[Predicate] | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def tame_animal(cls, name: str, *,
                    entity: EntityJson | list[Predicate] | None = None,
                    player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def target_hit(cls, name: str, *,
                   signal_strength: int | None = None,
                   projectile: int | None = None,
                   shooter: EntityJson | list[Predicate] | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def thrown_item_picked_up_by_entity(cls, name: str, *,
                                        item: ItemJson | None = None,
                                        entity: EntityJson | list[Predicate] | None = None,
                                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def tick(cls, name: str, *,
             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def used_ender_eye(cls, name: str, *,
                       distance: DoubleRangeJson | None = None,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def used_totem(cls, name: str, *,
                   item: ItemJson | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def using_item(cls, name: str, *,
                   item: ItemJson | None = None,
                   player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def villager_trade(cls, name: str, *,
                       item: ItemJson | None = None,
                       villager: EntityJson | list[Predicate] | None = None,
                       player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def voluntary_exile(cls, name: str, *,
                        location: LocationJson | None = None,
                        player: EntityJson | list[Predicate] | None = None) -> Criterion: pass

    # TODO Deprecation warnings for below three

    @classmethod
    @_trigger()
    def arbitrary_player_tick(cls, name: str) -> Criterion: pass

    @classmethod
    @_trigger()
    def player_damaged(cls, name: str, *,
                       damage: DamageJson | None = None) -> Criterion: pass

    @classmethod
    @_trigger()
    def safely_harvest_honey(cls, name: str, *,
                             block: dict[Literal["block", "tag"], str],
                             item: ItemJson | None,
                             player: EntityJson | list[Predicate] | None = None) -> Criterion: pass
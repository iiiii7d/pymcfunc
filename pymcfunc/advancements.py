from __future__ import annotations

from typing import TypeAlias, Union, Literal, Any, TYPE_CHECKING, Type, Optional

from attr import define, field

from pymcfunc.internal import base_class
from pymcfunc.loot_tables import LootTable
from pymcfunc.predicates import Predicate
from pymcfunc.recipes import Recipe

if TYPE_CHECKING: from pymcfunc.functions import Function
from pymcfunc.json_format import ItemJson, EntityJson, DamageJson, DamageTypeJson, LocationJson, IntRangeJson, FloatRangeJson, \
    DoubleRangeJson
from pymcfunc.nbt import Compound, List, NBTFormat, String, NBT, Boolean, Int, DictReprAsList

RawJson: TypeAlias = Union[dict, list]

@define(init=True)
class Advancement(NBTFormat):
    namespace: str
    name: str
    display: AdvancementDisplay | None = None
    parent: str | Advancement | None = None
    criteria: list[Criterion] = field(factory=list)
    requirements: list[list[Criterion]] | None = None
    rewards: Rewards | None = None

    @property
    def namespaced(self) -> str: return f'{self.namespace}:{self.name}'
    def __str__(self): return self.namespaced

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBT]]:
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

@define(init=True)
class Icon(NBTFormat):
    item: str = "air"
    nbt: Compound | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'item': String,
            'nbt': Compound,
        }

@define(init=True)
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
    def NBT_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'icon': Icon,
            'title': Union[String, List[Compound], Compound],
            'frame': Optional[Literal["challenge", "goal", "task"]],
            'background': Optional[String],
            'description': String,
            'show_toast': Boolean,
            'announce_to_chat': Boolean,
            'hidden': Boolean,
        }

@define(init=True)
class Rewards(NBTFormat):
    recipes: list[Recipe] | None = None
    loot: list[LootTable] | None = None
    experience: int | None = None
    function: Function | None = None

    @property
    def NBT_FORMAT(self) -> dict[str, Type[NBT]]:
        return {
            'recipes': List[String],
            'loot': List[String],
            'experience': Optional[Int],
            'function': Optional[String]
        }

@define(init=True)
class Criterion(NBTFormat):
    conditions: Trigger

    @property
    def trigger(self) -> str: return self.conditions.type

    NBT_FORMAT = {
        'trigger': String
    }

@define(init=True, frozen=True)
@base_class
class Trigger(NBTFormat):
    type = property(lambda self: "")

@define(init=True, frozen=True)
@base_class
class PlayerTrigger(Trigger):
    player: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        'player': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class AllayDropItemOnBlockTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:allay_drop_item_on_block")
    location: LocationJson | None = None
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'location': Optional[LocationJson],
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class AvoidVibrationTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:avoid_vibration")

@define(init=True, frozen=True)
class BeeNestDestroyedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:bee_nest_destroyed")
    block: str | None = None
    item: ItemJson | None = None
    num_bees_inside: int | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'block': Optional[String],
        'item': Optional[ItemJson],
        'num_bees_inside': Optional[Int]
    }

@define(init=True, frozen=True)
class BredAnimalsTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:bred_animals")
    child: EntityJson | list[Predicate] | None = None
    parent: EntityJson | list[Predicate] | None = None
    partner: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'child': Optional[Union[EntityJson, list[Predicate]]],
        'parent': Optional[Union[EntityJson, list[Predicate]]],
        'partner': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class BrewedPotionTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:brewed_potion")
    potion: str | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'potion': Optional[String]
    }

@define(init=True, frozen=True)
class ChangedDimensionTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:changed_dimension")
    from_: Literal['overworld', 'the_nether', 'the_end'] | None = None
    to: Literal['overworld', 'the_nether', 'the_end'] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'from': Optional[String],
        'to': Optional[String]
    }

@define(init=True, frozen=True)
class ChanelledLightningTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:chanelled_lightning")
    victims: list[EntityJson | list[Predicate]] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'victims': Optional[List[Union[EntityJson, List[Predicate]]]]
    }

@define(init=True, frozen=True)
class ConstructBeaconTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:construct_beacon")
    level: int | IntRangeJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'level': Optional[Union[IntRangeJson, Int]]
    }

@define(init=True, frozen=True)
class ConsumeItemTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:consume_item")
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class CuredZombieVillagerTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:cured_zombie_villager")
    villager: EntityJson | list[Predicate] | None = None
    zombie: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'villager': Optional[Union[EntityJson, list[Predicate]]],
        'zombie': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class EffectsChangedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:effects_changed")
    effect: list[Effect] | None = None
    source: EntityJson | list[Predicate] | None = None

    @define(init=True)
    class Effect(NBTFormat):
        name: str
        amplifier: int | IntRangeJson | None = None
        duration: int | IntRangeJson | None = None

        NBT_FORMAT = {
            'amplifier': Optional[Union[IntRangeJson, Int]],
            'duration': Optional[Union[IntRangeJson, Int]]
        }

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'effect': Optional[DictReprAsList[Effect]],
        'source': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class EnchantedItemTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:enchanted_item")
    item: ItemJson | None = None
    levels: int | IntRangeJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson],
        'levels': Optional[Union[IntRangeJson, Int]]
    }

@define(init=True, frozen=True)
class EnterBlockTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:enter_block")
    block: str | None = None
    state: dict[str, Any] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'block': Optional[String],
        'state': Optional[dict[str, Any]]
    }

@define(init=True, frozen=True)
class EntityHurtPlayerTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:entity_hurt_player")
    damage: DamageJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'damage': Optional[DamageJson]
    }

@define(init=True, frozen=True)
class EntityKilledPlayerTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:entity_killed_player")
    entity: EntityJson | list[Predicate] | None = None
    killing_blow: DamageJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]],
        'killing_blow': Optional[DamageJson]
    }

@define(init=True, frozen=True)
class FallFromHeightTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:fall_from_height")
    start_position: LocationJson | None = None
    distance: dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], FloatRangeJson] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'start_position': Optional[LocationJson],
        'distance': Optional[dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], FloatRangeJson]]
    }

@define(init=True, frozen=True)
class FilledBucketTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:filled_bucket")
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class FishingRodHookedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:fishing_rod_hooked")
    entity: EntityJson | list[Predicate] | None = None
    item: ItemJson | None = None
    rod: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]],
        'item': Optional[ItemJson],
        'rod': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class HeroOfTheVillageTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:hero_of_the_village")
    location: LocationJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'location': Optional[LocationJson]
    }

@define(init=True, frozen=True)
class ImpossibleTrigger(Trigger):
    type = property(lambda self: "minecraft:impossible")

@define(init=True, frozen=True)
class InventoryChangedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:inventory_changed")
    items: list[ItemJson] | None = None
    slots: dict[Literal['empty', 'full', 'occupied'], Union[Int, IntRangeJson]] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'items': Optional[list[ItemJson]],
        'slots': Optional[dict[Literal['empty', 'full', 'occupied'], Union[Int, IntRangeJson]]]
    }

@define(init=True, frozen=True)
class ItemDurabilityChangedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:item_durability_changed")
    delta: int | IntRangeJson | None = None
    durability: int | IntRangeJson | None = None
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'delta': Optional[Union[Int, IntRangeJson]],
        'durability': Optional[Union[Int, IntRangeJson]],
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class ItemUsedOnBlockTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:item_used_on_block")
    location: LocationJson | None = None
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'location': Optional[LocationJson],
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class KillMobNearSculkCatalystTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:kill_mob_near_sculk_catalyst")
    entity: EntityJson | list[Predicate] | None = None
    killing_blow: DamageTypeJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]],
        'killing_blow': Optional[DamageTypeJson]
    }

@define(init=True, frozen=True)
class KilledByCrossbowTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:killed_by_crossbow")
    unique_entity_types: int | IntRangeJson | None = None
    victims: EntityJson | list[EntityJson | list[Predicate]] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'unique_entity_types': Optional[Union[Int, IntRangeJson]],
        'victims': Optional[Union[EntityJson, list[Union[EntityJson, list[Predicate]]]]]
    }

@define(init=True, frozen=True)
class LevitationTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:levitation")
    distance: dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], IntRangeJson] | None = None
    duration: int | IntRangeJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'distance': Optional[dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], IntRangeJson]],
        'duration': Optional[Union[int, IntRangeJson]]
    }

@define(init=True, frozen=True)
class LightningStrikeTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:lightning_strike")
    lightning: EntityJson | list[Predicate] | None = None
    bystander: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'lightning': Optional[Union[EntityJson, list[Predicate]]],
        'bystander': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class LocationTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:location")
    location: LocationJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'location': Optional[LocationJson]
    }

@define(init=True, frozen=True)
class NetherTravelTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:nether_travel")
    start_position: LocationJson | None = None
    distance: dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], FloatRangeJson] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'start_position': Optional[LocationJson],
        'distance': Optional[dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], FloatRangeJson]]
    }

@define(init=True, frozen=True)
class PlacedBlockTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:placed_block")
    block: str | None = None
    item: ItemJson | None = None
    location: LocationJson | None = None
    state: dict[str, Any] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'block': Optional[String],
        'item': Optional[ItemJson],
        'location': Optional[LocationJson],
        'state': Optional[dict[str, Any]]
    }

@define(init=True, frozen=True)
class PlayerGeneratesContainerLootTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:player_generates_container_loot")
    loot_table: str | LootTable

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'loot_table': String
    }

@define(init=True, frozen=True)
class PlayerHurtEntityTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:player_hurt_entity")
    damage: DamageJson | None = None
    entity: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'damage': Optional[DamageJson],
        'entity': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class PlayerInteractedWithEntityTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:player_interacted_with_entity")
    item: ItemJson | None = None
    entity: EntityJson | list[Predicate] | None = None
    
    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson],
        'entity': Optional[Union[EntityJson, list[Predicate]]]
    }
    
@define(init=True, frozen=True)
class PlayerKilledEntityTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:player_killed_entity")
    entity: EntityJson | list[Predicate] | None = None
    killing_blow: DamageTypeJson | None = None
    
    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]],
        'killing_blow': Optional[DamageTypeJson]
    }
    
@define(init=True, frozen=True)
class RecipeUnlockedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:recipe_unlocked")
    recipe: str | Recipe

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'recipe': String
    }

@define(init=True, frozen=True)
class RideEntityInLavaTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:ride_entity_in_lava")
    start_position: LocationJson | None = None
    distance: dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], FloatRangeJson] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'start_position': Optional[LocationJson],
        'distance': Optional[dict[Literal['absolute', 'horizontal', 'x', 'y', 'z'], FloatRangeJson]]
    }

@define(init=True, frozen=True)
class ShotCrossbowTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:shot_crossbow")
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class SleptInBedTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:slept_in_bed")
    location: LocationJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'location': Optional[LocationJson]
    }

@define(init=True, frozen=True)
class SlideDownBlockTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:slide_down_block")
    block: str | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'block': Optional[String]
    }

@define(init=True, frozen=True)
class StartedRidingTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:started_riding")

@define(init=True, frozen=True)
class SummonedEntityTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:summoned_entity")
    entity: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class TameAnimalTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:tame_animal")
    entity: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class TargetHitTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:target_hit")
    signal_strength: int | None = None
    projectile: str | None = None
    shooter: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'signal_strength': Optional[Int],
        'projectile': Optional[String],
        'shooter': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class ThrownItemPickedUpByEntityTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:thrown_item_picked_up_by_entity")
    item: ItemJson | None = None
    entity: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson],
        'entity': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class ThrownItemPickedUpByPlayerTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:thrown_item_picked_up_by_player")
    entity: EntityJson | list[Predicate] | None = None
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'entity': Optional[Union[EntityJson, list[Predicate]]],
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class TickTrigger(Trigger):
    type = property(lambda self: "minecraft:tick")

@define(init=True, frozen=True)
class UsedEnderEyeTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:used_ender_eye")
    distance: Int | DoubleRangeJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'distance': Optional[Union[Int, DoubleRangeJson]]
    }

@define(init=True, frozen=True)
class UsedTotemTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:used_totem")
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class UsingItemTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:using_item")
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson]
    }

@define(init=True, frozen=True)
class VillagerTradeTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:villager_trade")
    item: ItemJson | None = None
    villager: EntityJson | list[Predicate] | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'item': Optional[ItemJson],
        'villager': Optional[Union[EntityJson, list[Predicate]]]
    }

@define(init=True, frozen=True)
class VoluntaryExileTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:voluntary_exile")
    location: LocationJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'location': Optional[LocationJson]
    }

# TODO deprecation notices for below triggers

@define(init=True, frozen=True)
class ArbitraryPlayerTickTrigger(Trigger):
    type = property(lambda self: "minecraft:arbitrary_player_tick")

@define(init=True, frozen=True)
class ItemDeliveredToPlayerTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:item_delivered_to_player")

@define(init=True, frozen=True)
class PlayerDamagedTrigger(Trigger):
    type = property(lambda self: "minecraft:player_damaged")
    damage: DamageJson | None = None

    NBT_FORMAT = {
        **Trigger.NBT_FORMAT,
        'damage': Optional[DamageJson]
    }

@define(init=True, frozen=True)
class SafelyHarvestHoneyTrigger(PlayerTrigger):
    type = property(lambda self: "minecraft:safely_harvest_honey")
    block: dict[Literal['block', 'tag'], str] | None = None
    item: ItemJson | None = None

    NBT_FORMAT = {
        **PlayerTrigger.NBT_FORMAT,
        'block': Optional[dict[Literal['block', 'tag'], String]],
        'item': Optional[ItemJson]
    }
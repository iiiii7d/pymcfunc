from __future__ import annotations

from typing import Annotated

from beartype.vale import Is

from pkmc.formats.entity import Entity
from pkmc.formats.item import SlottedItem
from pkmc.formats.level import GameType
from pkmc.formats.mob import Mob
from pkmc.nbt import (
    Boolean,
    Case,
    Double,
    Float,
    Int,
    IntArray,
    List,
    Short,
    String,
    TypedCompound,
    TypedFile,
)


class DoubleCoords(TypedCompound):
    x: Double
    y: Double
    z: Double


class LastDeathLocation(TypedCompound):
    dimension: String  # TODO dimension enum
    pos: IntArray


class Abilities(TypedCompound):
    flying: Boolean
    fly_speed: Annotated[Float, Case.CAMEL]
    instabuild: Boolean
    invulnerable: Boolean
    may_build: Annotated[Boolean, Case.CAMEL]
    may_fly: Annotated[Boolean, Case.NOCASE]
    walk_speed: Annotated[Float, Case.CAMEL]


class RecipeBook(TypedCompound):
    recipes: List[String]
    to_be_displayed: Annotated[List[String], Case.CAMEL]
    is_filtering_craftable: Annotated[Boolean, Case.CAMEL]
    is_gui_open: Annotated[Boolean, Case.CAMEL]
    is_furnace_filtering_craftable: Annotated[Boolean, Case.CAMEL]
    is_furnace_gui_open: Annotated[Boolean, Case.CAMEL]
    is_blasting_furnace_filtering_craftable: Annotated[Boolean, Case.CAMEL]
    is_blasting_furnace_gui_open: Annotated[Boolean, Case.CAMEL]
    is_smoker_filtering_craftable: Annotated[Boolean, Case.CAMEL]
    is_smoker_gui_open: Annotated[Boolean, Case.CAMEL]


class RootVehicle(TypedCompound):
    attach: Annotated[IntArray, Case.PASCAL]
    entity: Annotated[Entity, Case.PASCAL]


class WardenSpawnTracker(TypedCompound):
    cooldown_ticks: Int
    ticks_since_last_warning: Int
    warning_level: Annotated[Int, Is[lambda x: 0 <= x.value <= 3]]


class Player(Entity, Mob, TypedFile):
    abilities: Abilities
    data_version: Annotated[Int, Case.PASCAL]
    dimension: Annotated[String, Case.PASCAL]
    ender_items: Annotated[List[SlottedItem], Case.PASCAL]
    entered_nether_position: Annotated[DoubleCoords, Case.CAMEL]
    food_exhaustion_level: Annotated[Float, Case.CAMEL]
    food_level: Annotated[Int, Case.CAMEL]
    food_saturation_level: Annotated[Float, Case.CAMEL]
    food_tick_timer: Annotated[Int, Case.CAMEL]
    inventory: Annotated[List[SlottedItem], Case.PASCAL]
    last_death_location: Annotated[LastDeathLocation, Case.PASCAL]
    player_game_type: Annotated[GameType, Case.CAMEL]
    previous_player_game_type: Annotated[GameType, Case.CAMEL]
    recipe_book: Annotated[RecipeBook, Case.CAMEL]
    root_vehicle: Annotated[RootVehicle | None, Case.PASCAL]
    score: Annotated[Int, Case.PASCAL]
    seen_credits: Annotated[Boolean, Case.CAMEL]
    selected_item: Annotated[SlottedItem, Case.PASCAL]
    selected_item_slot: Annotated[Int, Case.PASCAL]
    shoulder_entity_left: Annotated[Entity, Case.PASCAL]
    shoulder_entity_right: Annotated[Entity, Case.PASCAL]
    sleep_timer: Annotated[Short, Case.PASCAL]
    spawn_dimension: Annotated[String | None, Case.PASCAL]  # TODO Dimension enum
    spawn_forced: Annotated[Boolean, Case.PASCAL]
    spawn_x: Annotated[Int | None, Case.PASCAL]
    spawn_y: Annotated[Int | None, Case.PASCAL]
    spawn_z: Annotated[Int | None, Case.PASCAL]
    warden_spawn_tracker: WardenSpawnTracker
    xp_level: Annotated[Int, Case.PASCAL]
    xp_p: Annotated[Float, Case.PASCAL]
    xp_seed: Annotated[Int, Case.PASCAL]
    xp_total: Annotated[Int, Case.PASCAL]

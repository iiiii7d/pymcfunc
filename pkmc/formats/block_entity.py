from __future__ import annotations

from enum import Enum
from typing import Annotated

from pkmc.formats.entity import Entity
from pkmc.formats.item import IntCoords, Item, ItemTag, SlottedItem
from pkmc.nbt import (
    Boolean,
    Byte,
    Case,
    Compound,
    Float,
    Int,
    IntArray,
    List,
    Long,
    Short,
    String,
    TypedCompound,
)


class BlockEntity(TypedCompound):
    id: String | None
    keep_packed: Annotated[Boolean, Case.CAMEL]
    x: Int | None
    y: Int | None
    z: Int | None


class _CustomNameLock(BlockEntity):
    custom_name: Annotated[String | None, Case.PASCAL]  # TODO Json Text Component
    lock: Annotated[String, Case.PASCAL]
    items: Annotated[List[SlottedItem], Case.PASCAL]


class _Container(_CustomNameLock):
    items: Annotated[List[SlottedItem], Case.PASCAL]
    loot_table: Annotated[String, Case.PASCAL]  # TODO Loot Table
    loot_table_seed: Annotated[Long | None, Case.PASCAL]


class _FurnaceDerivative(_CustomNameLock):
    burn_time: Annotated[Short, Case.PASCAL]
    cook_time: Annotated[Short, Case.PASCAL]
    cook_time_total: Annotated[Short, Case.PASCAL]
    items: Annotated[List[SlottedItem], Case.PASCAL]
    recipes_used: Annotated[Compound[Int], Case.PASCAL]


class Banner(BlockEntity):
    class Pattern(TypedCompound):
        class Color(Enum):
            WHITE = Int(0)
            ORANGE = Int(1)
            MAGENTA = Int(2)
            LIGHT_BLUE = Int(3)
            YELLOW = Int(4)
            LIME = Int(5)
            PINK = Int(6)
            GRAY = Int(7)
            LIGHT_GRAY = Int(8)
            CYAN = Int(9)
            PURPLE = Int(10)
            BLUE = Int(11)
            BROWN = Int(12)
            GREEN = Int(13)
            RED = Int(14)
            BLACK = Int(15)

        class Pattern(Enum):
            pass  # TODO

        color: Annotated[Color, Case.PASCAL]
        pattern: Annotated[String, Case.PASCAL]

    custom_name: Annotated[String | None, Case.PASCAL]  # TODO JSON Text Component
    patterns: Annotated[List[Pattern], Case.PASCAL]


class Barrel(_Container):
    pass


class Beacon(_CustomNameLock):
    levels: Annotated[Int, Case.PASCAL]
    primary: Annotated[Int, Case.PASCAL]  # TODO potion effect
    secondary: Annotated[Int, Case.PASCAL]  # same


class Bed(BlockEntity):
    pass


class Beehive(BlockEntity):
    class Bee(TypedCompound):
        entity_data: Annotated[Entity, Case.PASCAL]
        min_occupation_ticks: Annotated[Int, Case.PASCAL]
        ticks_in_hive: Annotated[Int, Case.PASCAL]

    bees: Annotated[List[Bee], Case.PASCAL]
    flower_pos: Annotated[IntCoords, Case.PASCAL]


class Bell(BlockEntity):
    pass


class BlastFurnace(_FurnaceDerivative):
    pass


class BrewingStand(BlockEntity):
    brew_time: Annotated[Short, Case.PASCAL]
    fuel: Annotated[Byte, Case.PASCAL]
    items: Annotated[List[SlottedItem], Case.PASCAL]


class Campfire(BlockEntity):
    cooking_times: Annotated[IntArray, Case.PASCAL]
    cooking_total_times: Annotated[IntArray, Case.PASCAL]
    items: Annotated[List[Item], Case.PASCAL]


class ChiseledBookshelf(BlockEntity):
    items: Annotated[List[SlottedItem], Case.PASCAL]


class Chest(_Container):
    pass


class Comparator(BlockEntity):
    output_signal: Annotated[Int, Case.PASCAL]


class CommandBlock(BlockEntity):
    auto: Boolean
    command: Annotated[String, Case.PASCAL]  # TODO Command type
    condition_met: Annotated[Boolean, Case.CAMEL]
    custom_name: Annotated[String | None, Case.CAMEL]
    last_execution: Annotated[Long, Case.CAMEL]
    last_output: Annotated[String, Case.PASCAL]
    powered: Boolean
    success_count: Annotated[Int, Case.PASCAL]
    track_output: Annotated[Boolean, Case.PASCAL]
    update_last_execution: Annotated[Boolean, Case.PASCAL]


class Conduit(BlockEntity):
    target: Annotated[IntArray, Case.PASCAL]


class DaylightDetector(BlockEntity):
    pass


class Dispenser(_Container):
    pass


class Dropper(_Container):
    pass


class EnchantingTable(BlockEntity):
    custom_name: Annotated[String | None, Case.PASCAL]


class EnderChest(BlockEntity):
    pass


class EndGateway(BlockEntity):
    age: Annotated[Long, Case.PASCAL]
    exact_teleport: Annotated[Boolean, Case.PASCAL]
    exit_portral: Annotated[IntCoords, Case.PASCAL]


class EndPortal(BlockEntity):
    pass


class Furnace(_FurnaceDerivative):
    pass


class Hopper(_CustomNameLock):
    transfer_cooldown: Annotated[Int, Case.PASCAL]


class Jigsaw(BlockEntity):
    class Joint(Enum):
        ROLLABLE = String("Rollable")
        ALIGNED = String("Aligned")

    final_state: String  # TODO Block
    joint: Joint
    name: String
    pool: String
    target: String


class Jukebox(BlockEntity):
    is_playing: Annotated[Boolean, Case.PASCAL]
    record_item: Annotated[Item, Case.PASCAL]
    record_start_tick: Annotated[Long, Case.PASCAL]
    tick_count: Annotated[Long, Case.PASCAL]


class Lectern(BlockEntity):
    book: Annotated[Item, Case.PASCAL]
    page: Annotated[Int, Case.PASCAL]


class MobSpawner(BlockEntity):
    class PotentialSpawn(TypedCompound):
        class Data(TypedCompound):
            class CustomSpawnRules(TypedCompound):
                block_light_limit: Int
                block_sky_limit: Int

            entity: Entity
            custom_spawn_rules: CustomSpawnRules

        weight: Int
        data: Data

    delay: Annotated[Short, Case.PASCAL]
    max_nearby_entities: Annotated[Short, Case.PASCAL]
    max_spawned_delay: Annotated[Short, Case.PASCAL]
    min_spawn_delay: Annotated[Short, Case.PASCAL]
    required_player_range: Annotated[Short, Case.PASCAL]
    spawn_count: Annotated[Short, Case.PASCAL]
    spawn_data: Annotated[Compound, Case.PASCAL]  # TODO Partial classes?
    spawn_potentials: Annotated[List[PotentialSpawn], Case.PASCAL]
    spawn_range: Annotated[Short, Case.PASCAL]


class Piston(BlockEntity):
    class BlockState(TypedCompound):  # TODO move somewhere
        name: Annotated[String, Case.PASCAL]
        properties: Annotated[Compound[String], Case.PASCAL]

    class Facing(Enum):
        DOWN = Int(0)
        UP = Int(1)
        NORTH = Int(2)
        SOUTH = Int(3)
        WEST = Int(4)
        EAST = Int(5)

    block_state: Annotated[BlockState, Case.CAMEL]
    extending: Boolean
    facing: Facing
    progress: Float
    source: Boolean


class ShulkerBox(_Container):
    pass


class Sign(BlockEntity):
    class Color(Enum):
        WHITE = String("white")
        ORANGE = String("orange")
        MAGENTA = String("magenta")
        LIGHT_BLUE = String("light_blue")
        YELLOW = String("yellow")
        LIME = String("lime")
        PINK = String("pink")
        GRAY = String("gray")
        LIGHT_GRAY = String("light_gray")
        CYAN = String("cyan")
        PURPLE = String("purple")
        BLUE = String("blue")
        BROWN = String("brown")
        GREEN = String("green")
        RED = String("red")
        BLACK = String("black")

    glowing_text: Annotated[Boolean, Case.PASCAL]
    color: Annotated[Color, Case.PASCAL]
    text_1: Annotated[String, Case.PASCAL]  # TODO Json Text
    text_2: Annotated[String, Case.PASCAL]  # TODO Json Text
    text_3: Annotated[String, Case.PASCAL]  # TODO Json Text
    text_4: Annotated[String, Case.PASCAL]  # TODO Json Text


class Skull(BlockEntity, ItemTag.SkullOwner):
    pass


class Smoker(_FurnaceDerivative):
    pass


class SoulCampfire(Campfire):
    pass


class StructureBlock(BlockEntity):
    class Mirror(Enum):
        NONE = String("NONE")
        LEFT_RIGHT = String("LEFT_RIGHT")
        FRONT_BACK = String("FRONT_BACK")

    class Mode(Enum):
        SAVE = String("SAVE")
        LOAD = String("LOAD")
        CORNER = String("CORNER")
        DATA = String("DATA")

    class Rotation(Enum):
        NONE = String("NONE")
        CLOCKWISE_90 = String("CLOCKWISE_90")
        CLOCKWISE_180 = String("CLOCKWISE_180")
        COUNTERCLOCKWISE_90 = String("COUNTERCLOCKWISE_90")

    author: String
    ignore_entities: Annotated[Boolean, Case.CAMEL]
    integrity: Float
    metadata: String
    mirror: Mirror
    mode: Mode
    name: String
    pos_x: Annotated[Int, Case.PASCAL]
    pos_y: Annotated[Int, Case.PASCAL]
    pos_z: Annotated[Int, Case.PASCAL]
    powered: Annotated[Boolean, Case.PASCAL]
    rotation: Rotation
    seed: Long
    show_bounding_box: Annotated[Boolean, Case.NOCASE]
    size_x: Annotated[Int, Case.PASCAL]
    size_y: Annotated[Int, Case.PASCAL]
    size_z: Annotated[Int, Case.PASCAL]


class TrappedChest(_Container):
    pass

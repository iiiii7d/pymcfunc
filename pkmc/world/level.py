from enum import Enum
from typing import Annotated

from beartype.vale import Is

from pkmc.nbt import (
    Boolean,
    Byte,
    Case,
    Compound,
    Double,
    Int,
    IntArray,
    List,
    Long,
    LongArray,
    String,
    TypedCompound,
    TypedFile,
)


class Difficulty(Enum):
    PEACEFUL = Byte(0, "Difficulty")
    EASY = Byte(1, "Difficulty")
    NORMAL = Byte(2, "Difficulty")
    HARD = Byte(3, "Difficulty")


class GameType(Enum):
    SURVIVAL = Byte(0, "GameType")
    CREATIVE = Byte(1, "GameType")
    ADVENTURE = Byte(2, "GameType")
    SPECTATOR = Byte(3, "GameType")


class GeneratorName(Enum):
    DEFAULT = String("default", "GeneratorName")
    FLAT = String("flat", "GeneratorName")
    LARGE_BIOMES = String("largebiomes", "GeneratorName")
    AMPLIFIED = String("amplified", "GeneratorName")
    BUFFET = String("buffet", "GeneratorName")
    DEBUG_ALL_BLOCK_STATES = String("debug_all_block_states", "GeneratorName")
    DEFAULT_1_1 = String("default_1_1", "GeneratorName")
    CUSTOMIZED = String("customized", "GeneratorName")


class Overlay(Enum):
    PROGRESS = String("progress", "Overlay")
    NOTCHED_6 = String("notched_6", "Overlay")
    NOTCHED_10 = String("notched_10", "Overlay")
    NOTCHED_12 = String("notched_12", "Overlay")
    NOTCHED_20 = String("notched_20", "Overlay")


class BossBar(TypedCompound):
    players: Annotated[List[IntArray], Case.PASCAL]
    color: Annotated[String, Case.PASCAL]  # TODO color code enum
    create_world_fog: Annotated[Boolean, Case.PASCAL]
    darken_screen: Annotated[Boolean, Case.PASCAL]
    max: Annotated[Int, Case.PASCAL]
    value: Annotated[Int, Case.PASCAL]
    name: Annotated[String, Case.PASCAL]  # TODO JSON text component
    overlay: Annotated[Overlay, Case.PASCAL]
    play_boss_music: Annotated[Boolean, Case.PASCAL]
    visible: Annotated[Boolean, Case.PASCAL]


class DataPacks(TypedCompound):
    disabled: Annotated[List[String], Case.PASCAL]
    enabled: Annotated[List[String], Case.PASCAL]


class ByteCoord(TypedCompound):
    x: Annotated[Byte, Case.PASCAL]
    y: Annotated[Byte, Case.PASCAL]
    z: Annotated[Byte, Case.PASCAL]


class DragonFlight(TypedCompound):
    exit_portal_location: Annotated[ByteCoord, Case.PASCAL]
    gateways: Annotated[List[Annotated[Int, Is[lambda x: 0 <= x <= 19]]], Case.PASCAL]
    dragon_killed: Annotated[Boolean, Case.PASCAL]
    dragon_uuid_least: Annotated[LongArray, "DragonUUIDLeast"]
    dragon_uuid_most: Annotated[LongArray, "DragonUUIDMost"]
    previously_killed: Annotated[Boolean, Case.PASCAL]


class _EndDimensionData(TypedCompound):
    dragon_flight: Annotated[DragonFlight, Case.PASCAL]


class _DimensionData(TypedCompound):
    end: Annotated[_EndDimensionData, "1"]


class WorldGenSettigs(TypedCompound):
    bonus_chest: Boolean
    seed: Long
    generate_features: Boolean
    dimensions: Compound[GeneratorSetting]


class Version(TypedCompound):
    id: Annotated[Int, Case.PASCAL]
    name: Annotated[String, Case.PASCAL]
    series: Annotated[String, Case.PASCAL]
    snapshot: Annotated[Boolean, Case.PASCAL]


class GeneratorOptions(TypedCompound):
    class BiomeSource(TypedCompound):
        pass


class LevelFile(TypedFile):
    allow_commands: Annotated[Boolean, Case.CAMEL]
    border_center_x: Annotated[Double, Case.PASCAL]
    border_center_z: Annotated[Double, Case.PASCAL]
    border_damage_per_block: Annotated[Double, Case.PASCAL]
    border_size: Annotated[Double, Case.PASCAL]
    border_safe_zone: Annotated[Double, Case.PASCAL]
    border_size_lerp_target: Annotated[Double, Case.PASCAL]
    border_size_lerp_time: Annotated[Long, Case.PASCAL]
    border_warning_blocks: Annotated[Double, Case.PASCAL]
    border_warning_time: Annotated[Double, Case.PASCAL]
    clear_weather_time: Annotated[Int, Case.CAMEL]
    custom_boss_events: Annotated[Compound[BossBar], Case.PASCAL]
    data_packs: Annotated[DataPacks, Case.PASCAL]
    data_version: Annotated[Int, Case.PASCAL]
    day_time: Annotated[Long, Case.PASCAL]
    difficulty: Annotated[Difficulty, Case.PASCAL]
    difficulty_locked: Annotated[Boolean, Case.PASCAL]
    _dimension_data: Annotated[_DimensionData, "DimensionData"]
    game_rules: Annotated[Compound[String], Case.PASCAL]
    world_gen_settings: Annotated[WorldGenSettigs, Case.PASCAL]
    game_type: Annotated[GameType, Case.PASCAL]
    generator_name: Annotated[GeneratorName, Case.CAMEL]
    generator_options: Annotated[GeneratorOptions, Case.CAMEL]
    generator_version: Annotated[Int, Case.CAMEL]
    hardcore: Boolean
    initialized: Boolean
    last_played: Annotated[Long, Case.PASCAL]
    level_name: Annotated[String, Case.PASCAL]
    map_features: Annotated[Boolean, Case.PASCAL]
    player: Annotated[Player | None, Case.PASCAL]
    raining: Boolean
    rain_time: Annotated[Int, Case.CAMEL]
    random_seed: Annotated[Long, Case.PASCAL]
    size_on_disk: Annotated[Long, Case.PASCAL]
    spawn_x: Annotated[Int, Case.PASCAL]
    spawn_y: Annotated[Int, Case.PASCAL]
    spawn_z: Annotated[Int, Case.PASCAL]
    thundering: Boolean
    thunderTime: Annotated[Int, Case.CAMEL]
    time: Annotated[Long, Case.PASCAL]
    level_version: Annotated[Int, "version"]
    mc_version: Annotated[Version, "Version"]
    wandering_trader_id: Annotated[IntArray, Case.PASCAL]
    wandering_trader_spawn_chance: Annotated[Int, Case.PASCAL]
    wandering_trader_spawn_delay: Annotated[Int, Case.PASCAL]
    was_modded: Annotated[Boolean, Case.PASCAL]

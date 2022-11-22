from enum import Enum
from typing import Annotated

from pkmc.nbt import Boolean, Byte, Case, Compound, Double, Int, Long, String, TypedFile


class LevelFile(TypedFile):
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
    custom_boss_events: Annotated[Compound[Bossbar], Case.PASCAL]
    data_packs: Annotated[DataPacks, Case.PASCAL]
    data_version: Annotated[Int, Case.PASCAL]
    day_time: Annotated[Long, Case.PASCAL]
    difficulty: Annotated[Difficulty, Case.PASCAL]
    difficulty_locked: Annotated[Boolean, Case.PASCAL]
    dimension_data: Annotated[DimensionData, Case.PASCAL]
    game_rules: Annotated[Compound[String], Case.PASCAL]
    world_gen_settings: Annotated[WorldGenSettigs, Case.PASCAL]
    game_type: Annotated[GameType, Case.PASCAL]

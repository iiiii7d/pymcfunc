from __future__ import annotations

from enum import Enum
from typing import Annotated

from beartype.vale import Is

from pkmc.formats.block import BlockState
from pkmc.formats.block_entity import BlockEntity, StructureBlock
from pkmc.formats.entity import Entity
from pkmc.nbt import (
    Boolean,
    Byte,
    ByteArray,
    Case,
    Compound,
    Float,
    Int,
    IntArray,
    List,
    Long,
    LongArray,
    Short,
    String,
    TypedCompound,
)


class Section(TypedCompound):
    class BlockStates(TypedCompound):
        palette: List[BlockState]
        data: LongArray

    class Biomes(TypedCompound):
        palette: List[String]  # TODO resource location
        data: LongArray

    y: Annotated[Byte, Case.PASCAL]
    block_states: BlockStates
    biomes: Biomes
    block_light: Annotated[ByteArray, Case.PASCAL]
    sky_light: Annotated[ByteArray, Case.PASCAL]


class InvalidStructure(TypedCompound):
    id: String = String("INVALID")


class Structure(TypedCompound):
    class Children(TypedCompound):
        class BiomeType(Enum):
            WARM = String("WARM")
            COLD = String("COLD")

        class Junction(TypedCompound):
            class DestProj(Enum):
                TERRAIN_MATCHING = String("terrain_matching")
                RIGID = String("rigid")

            source_x: Int
            source_ground_y: Int
            source_z: Int
            delta_y: Int
            dest_proj: DestProj

        class VillageType(Enum):
            PLAINS = Byte(0)
            DESERT = Byte(1)
            SAVANNAH = Byte(2)
            TAIGA = Byte(3)

        bounding_box: Annotated[IntArray | None, "BB"]
        biome_type: Annotated[BiomeType | None, Case.PASCAL]
        hut_roof_type: Annotated[Byte | None, "C"]  # TODO verify
        farm_crop_1: Annotated[BlockState | None, "CA"]  # TODO verify
        farm_crop_2: Annotated[BlockState | None, "CB"]  # TODO verify
        farm_crop_3: Annotated[BlockState | None, "CC"]  # TODO verify
        farm_crop_4: Annotated[BlockState | None, "CD"]  # TODO verify
        chest: Annotated[Boolean | None, Case.PASCAL]
        incoming_crossing_direction: Annotated[Int | None, "D"]
        depth: Annotated[Int | None, Case.PASCAL]
        entrances: Annotated[List[IntArray] | None, Case.PASCAL]
        entry_door: Annotated[String | None, Case.PASCAL]  # TODO block resource
        distance_from_origin: Annotated[Int | None, "GD"]  # TODO verify
        has_placed_chest_0: Annotated[Boolean | None, Case.PASCAL]
        has_placed_chest_1: Annotated[Boolean | None, Case.PASCAL]
        has_placed_chest_2: Annotated[Boolean | None, Case.PASCAL]
        has_placed_chest_3: Annotated[Boolean | None, Case.PASCAL]
        height: Annotated[Int | None, Case.PASCAL]
        h_pos: Annotated[Int | None, Case.PASCAL]
        hps: Boolean | None
        hr: Boolean | None
        id: String | None
        integrity: Float | None
        is_large: Annotated[Boolean | None, Case.CAMEL]
        junctions: List[Junction] | None  # TODO verify
        left: Annotated[Boolean | None, Case.PASCAL]
        left_high: Annotated[Boolean | None, Case.CAMEL]
        left_low: Annotated[Boolean | None, Case.CAMEL]
        length: Annotated[Int | None, Case.PASCAL]  # TODO verify
        mob: Annotated[Boolean | None, Case.PASCAL]
        corridor_length: Annotated[Int | None, "Num"]
        orientation: Annotated[Int | None, "O"]
        placed_hidden_chest: Annotated[Boolean | None, Case.CAMEL]
        placed_main_chest: Annotated[Boolean | None, Case.CAMEL]
        placed_trap_1: Annotated[Boolean | None, Case.CAMEL]
        placed_trap_2: Annotated[Boolean | None, Case.CAMEL]
        pos_x: Annotated[Int | None, Case.PASCAL]
        pos_y: Annotated[Int | None, Case.PASCAL]
        pos_z: Annotated[Int | None, Case.PASCAL]
        right: Annotated[Boolean | None, Case.PASCAL]
        right_high: Annotated[Boolean | None, Case.CAMEL]
        right_low: Annotated[Boolean | None, Case.CAMEL]
        rot: Annotated[StructureBlock.Rotation | None, Case.PASCAL]
        cobwebs: Annotated[Boolean | None, "sc"]
        seed: Annotated[Int | None, Case.PASCAL]
        source: Annotated[Boolean | None, Case.PASCAL]
        steps: Annotated[Int | None, Case.CAMEL]
        table: Annotated[Annotated[Int, Is[lambda x: 0 <= x <= 2]] | None, "T"]
        tall: Annotated[Boolean | None, Case.PASCAL]
        template: Annotated[String | None, Case.PASCAL]
        terrace: Annotated[Boolean | None, Case.PASCAL]  # TODO verify
        two_floors: Annotated[Boolean | None, "tf"]
        tpx: Annotated[Int | None, Case.UPPER]
        tpy: Annotated[Int | None, Case.UPPER]
        tpz: Annotated[Int | None, Case.UPPER]
        type: Annotated[VillageType | Int | None, Case.PASCAL]  # TODO verify
        villager_count: Annotated[Int | None, "VCount"]  # TODO verify
        width: Annotated[Int | None, Case.UPPER]
        witch: Annotated[Boolean | None, Case.PASCAL]
        zombie: Annotated[Boolean | None, Case.PASCAL]  # TODO verify

    class ProcessedChunk(TypedCompound):
        x: Annotated[Int, Case.PASCAL]
        z: Annotated[Int, Case.PASCAL]

    bounding_box: Annotated[IntArray, "BB"]
    biome: String
    children: Annotated[List[Children], Case.PASCAL]
    chunk_x: Annotated[Int, Case.PASCAL]
    chunk_z: Annotated[Int, Case.PASCAL]
    id: String
    processed: Annotated[List[ProcessedChunk] | None, Case.PASCAL]
    valud: Annotated[Boolean | None, Case.PASCAL]


class StructureData(TypedCompound):
    references: Annotated[Compound[LongArray], Case.PASCAL]
    starts: Compound[Structure | InvalidStructure]


class Chunk(TypedCompound):
    class Status(Enum):
        EMPTY = String("empty")
        STRUCTURE_STARTS = String("structure_starts")
        STRUCTURE_REFERENCES = String("structure_references")
        BIOMES = String("biomes")
        NOISE = String("noise")
        SURFACE = String("surface")
        CARVERS = String("carvers")
        LIQUID_CARVERS = String("liquid_carvers")
        FEATURES = String("features")
        LIGHT = String("light")
        SPAWN = String("spawn")
        HEIGHTMAPS = String("heightmaps")
        FULL = String("full")

    class CarvingMasks(TypedCompound):
        air: Annotated[ByteArray, Case.UPPER]
        liquid: Annotated[ByteArray, Case.UPPER]

    class Heightmaps(TypedCompound):
        motion_blocking: Annotated[LongArray, Case.UPPER]
        motion_blocking_no_leaves: Annotated[LongArray, Case.UPPER]
        ocean_floor: Annotated[LongArray, Case.UPPER]
        ocean_floor_wg: Annotated[LongArray, Case.UPPER]
        world_surface: Annotated[LongArray, Case.UPPER]
        world_surface_wg: Annotated[LongArray, Case.UPPER]

    class TileTick(TypedCompound):
        i: String  # TODO Block ID
        p: Int
        t: Int
        x: Int
        y: Int
        z: Int

    data_version: Annotated[Int, Case.PASCAL]
    x_pos: Annotated[Int, Case.PASCAL]
    z_pos: Annotated[Int, Case.PASCAL]
    entity_tag: Annotated[Int, Case.PASCAL]
    status: Annotated[Status, Case.PASCAL]
    last_update: Annotated[Long, Case.PASCAL]
    sections: List[Section]
    block_entities: List[BlockEntity]
    carving_masks: Annotated[CarvingMasks | None, Case.PASCAL]
    heightmaps: Annotated[Heightmaps, Case.PASCAL]
    lights: Annotated[List[List[Short]] | None, Case.PASCAL]
    entities: Annotated[List[Entity] | None, Case.PASCAL]
    fluid_ticks: List[TileTick]
    block_ticks: List[TileTick]
    inhabited_time: Annotated[Long, Case.PASCAL]
    post_process_time: Annotated[List[Short], Case.PASCAL]  # TODO ToBeTicked
    structures: StructureData

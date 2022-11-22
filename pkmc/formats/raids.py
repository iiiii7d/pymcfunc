from enum import Enum
from typing import Annotated

from pkmc.nbt import (
    Boolean,
    Case,
    Float,
    Int,
    List,
    Long,
    String,
    TypedCompound,
    TypedFile,
)


class Status(Enum):
    ONGOING = String("ongoing")
    VICTORY = String("victory")
    LOSS = String("loss")
    STOPPED = String("stopped")


class NbtUuid(TypedCompound):
    least: Annotated[Long, "UUIDLeast"]
    most: Annotated[Long, "UUIDMost"]


class Raid(TypedCompound):
    active: Annotated[Boolean, Case.PASCAL]
    bad_omen_level: Annotated[Int, Case.PASCAL]
    cx: Annotated[Int, Case.UPPER]
    cy: Annotated[Int, Case.UPPER]
    cz: Annotated[Int, Case.UPPER]
    groups_spawned: Annotated[Int, Case.PASCAL]
    heroes_of_the_village: Annotated[List[NbtUuid], Case.PASCAL]
    id: Annotated[Int, Case.PASCAL]
    num_groups: Annotated[Int, Case.PASCAL]
    pre_raid_ticks: Annotated[Int, Case.PASCAL]
    post_raid_ticks: Annotated[Int, Case.PASCAL]
    started: Annotated[Boolean, Case.PASCAL]
    status: Annotated[Status, Case.PASCAL]
    ticks_active: Annotated[Long, Case.PASCAL]
    total_health: Annotated[Float, Case.PASCAL]


class Raids(TypedCompound):
    next_available_id: Annotated[Int, "NextAvailableID"]
    raids: Annotated[List[Raid], Case.PASCAL]
    tick: Annotated[Int, Case.PASCAL]


class RaidFile(TypedFile):
    data: Raids
    data_version: Annotated[Int, Case.PASCAL]

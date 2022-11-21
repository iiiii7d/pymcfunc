from enum import Enum
from typing import Annotated

from pkmc.nbt import Boolean, Int, List, Long, String, TypedCompound, TypedFile


class Status(Enum):
    ONGOING = String("ongoing", "Status")
    VICTORY = String("victory", "Status")
    LOSS = String("loss", "Status")
    STOPPED = String("stopped", "Status")


class NbtUuid(TypedCompound):
    least: Annotated[Long, "UUIDLeast"]
    most: Annotated[Long, "UUIDMost"]


class Raid(TypedCompound):
    active: Annotated[Boolean, "Active"]
    bad_omen_level: Annotated[Int, "BadOmenLevel"]
    cx: Annotated[Int, "CX"]
    cy: Annotated[Int, "CY"]
    cz: Annotated[Int, "CZ"]
    groups_spawned: Annotated[Int, "GroupsSpawned"]
    heroes_of_the_village: Annotated[List[NbtUuid], "HeroesOfTheVillage"]
    id: Annotated[Int, "Id"]
    num_groups: Annotated[Int, "NumGroups"]
    pre_raid_ticks: Annotated[Int, "PreRaidTicks"]
    post_raid_ticks: Annotated[Int, "PostRaidTicks"]
    started: Annotated[Boolean, "Started"]
    status: Annotated[Status, "Status"]


class Raids(TypedCompound):
    next_available_id: Annotated[Int, "NextAvailableID"]
    raids: Annotated[List[Raid], "Raids"]
    tick: Annotated[Int, "Tick"]


class RaidFile(TypedFile):
    data: Raids
    data_version: Annotated[Int, "DataVersion"]

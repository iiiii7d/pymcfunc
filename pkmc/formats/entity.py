from __future__ import annotations

from typing import Annotated

from beartype.vale import Is

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
)


class Entity(TypedCompound):
    air: Annotated[Short, Case.PASCAL]
    fall_distance: Annotated[Float, Case.PASCAL]
    fire: Annotated[Short, Case.PASCAL]
    glowing: Annotated[Boolean, Case.PASCAL]
    has_visual_fire: Annotated[Boolean, Case.PASCAL]
    invulnerable: Annotated[Boolean, Case.PASCAL]
    motion: Annotated[List[Double], Case.PASCAL]
    no_gravity: Annotated[Boolean, Case.PASCAL]
    on_ground: Annotated[Boolean, Case.PASCAL]
    passengers: Annotated[List[Entity], Case.PASCAL]
    portal_cooldown: Annotated[Int, Case.PASCAL]
    pos: Annotated[List[Double], Case.PASCAL]
    rotation: Annotated[List[Float], Case.PASCAL]
    silent: Annotated[Boolean, Case.PASCAL]
    tags: Annotated[List[Annotated[String, Is[lambda x: " " not in x]]], Case.PASCAL]
    ticks_frozen: Annotated[Int | None, Case.PASCAL]
    uuid: Annotated[IntArray, Case.UPPER]


class EntityNotPlayer(Entity):
    custom_name: Annotated[String, Case.PASCAL]
    custom_name_visible: Annotated[Boolean, Case.PASCAL]
    id: String

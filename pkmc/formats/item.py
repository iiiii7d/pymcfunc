from __future__ import annotations

from enum import Enum
from struct import Struct
from typing import Annotated

from beartype.vale import Is

from pkmc.formats.block_entity import BlockEntity
from pkmc.formats.entity import Entity
from pkmc.formats.mob import Attribute
from pkmc.nbt import (
    Boolean,
    Byte,
    Case,
    Compound,
    Double,
    Int,
    IntArray,
    List,
    Short,
    String,
    TypedCompound,
)


class IntCoords(TypedCompound):
    x: Int
    y: Int
    z: Int


class ItemTag(TypedCompound):
    damage: Annotated[Int | None, Case.PASCAL]
    unbreakable: Annotated[Byte | None, Case.PASCAL]
    can_destroy: Annotated[List[Int] | None, Case.PASCAL]
    custom_model_data: Annotated[Int | None, Case.PASCAL]

    class AttributeModifier(Attribute.Modifier, TypedCompound):
        class Slot(Enum):
            MAIN_HAND = String("mainhand")
            OFF_HAND = String("offhand")
            FEET = String("feet")
            LEGS = String("legs")
            CHEST = String("chest")
            HEAD = String("head")

        attribute_name: Annotated[String, Case.PASCAL]
        slot: Annotated[Slot, Case.PASCAL]

    attribute_modifiers: Annotated[List[AttributeModifier] | None, Case.PASCAL]

    can_place_on: Annotated[List[String] | None, Case.PASCAL]
    block_entity_tag: Annotated[BlockEntity | None, Case.PASCAL]
    block_state_tag: Annotated[Compound[String] | None, Case.PASCAL]

    class Display(TypedCompound):
        color: Int  # TODO color
        name: Annotated[String, Case.PASCAL]  # TODO Json Text component
        lore: Annotated[List[String], Case.PASCAL]

    display: Display | MapDisplay | None
    hide_flags: Annotated[
        Annotated[Int, Is[lambda x: 0 <= x.value <= 127]] | None, Case.PASCAL
    ]  # TODO IntField

    class Enchantment(TypedCompound):
        id: String
        lvl: Short

    enchantments: Annotated[List[Enchantment] | None, Case.PASCAL]
    stored_enchantments: Annotated[List[Enchantment] | None, Case.PASCAL]
    repair_cost: Annotated[Int | None, Case.PASCAL]

    class PotionEffect(TypedCompound):
        ambient: Annotated[Boolean, Case.PASCAL]
        amplifier: Annotated[Byte, Case.PASCAL]
        duration: Annotated[Int, Case.PASCAL]
        id: Annotated[Byte, Case.PASCAL]
        show_icon: Annotated[Boolean, Case.PASCAL]
        show_particles: Annotated[Boolean, Case.PASCAL]

    custom_potion_effects: Annotated[List[PotionEffect] | None, Case.PASCAL]
    potion: Annotated[String | None, Case.PASCAL]  # TODO potion effect names
    custom_potion_color: Annotated[Int | None, Case.PASCAL]  # TODO color

    entity_tag: Annotated[Entity | None, Case.PASCAL]

    pages: List[String] | None

    class Generation(Enum):
        ORIGINAL = Int(0)
        COPY = Int(1)
        COPY_COPY = Int(2)
        TATTERED = Int(3)

    filtered_pages: Compound | None
    filtered_titie: String | None
    resolved: Boolean | None
    generation: Generation | None
    author: String | None
    title: String | None
    pages: List[String] | None  # TODO Json text

    bucket_variant_tag: Annotated[Int | None, Case.PASCAL]
    entity_tag: Annotated[Entity | None, Case.PASCAL]

    items: Annotated[List[Item] | None, Case.PASCAL]

    lodestone_tracked: Annotated[Boolean | None, Case.PASCAL]
    lodestone_dimension: Annotated[String | None, Case.PASCAL]
    lodestone_pos: Annotated[IntCoords | None, Case.PASCAL]

    charged_projectiles: Annotated[List[Item] | None, Case.PASCAL]
    charged: Annotated[Boolean | None, Case.PASCAL]

    debug_property: Annotated[Compound[String] | None, Case.PASCAL]

    class FireworkExplosionEffect(TypedCompound):
        class Type(Enum):
            SMALL_BALL = Byte(0)
            LARGE_BALL = Byte(1)
            STAR = Byte(2)
            CREEPER = Byte(3)
            BURST = Byte(4)

        colors: Annotated[IntArray, Case.PASCAL]
        fade_colors: Annotated[IntArray, Case.PASCAL]
        flicker: Annotated[Boolean, Case.PASCAL]
        trail: Annotated[Type, Case.PASCAL]

    class Fireworks(TypedCompound):
        explosions: Annotated[List[ItemTag.FireworkExplosionEffect], Case.PASCAL]
        flight: Annotated[Byte, Case.PASCAL]

    fireworks: Annotated[Fireworks | None, Case.PASCAL]

    explosions: Annotated[FireworkExplosionEffect | None, Case.PASCAL]

    class Decorations(TypedCompound):
        id: String
        type: Byte
        x: Double
        z: Double
        rot: Annotated[Double, Is[lambda x: 0.0 <= x.value <= 360.0]]

    class MapDisplay(TypedCompound):
        map_color: Annotated[Int, Case.PASCAL]

    map: Int | None
    map_scale_direction: Int | None
    map_to_lock: Boolean | None
    decorations: Annotated[List[Decorations] | None, Case.PASCAL]

    class SkullOwner(TypedCompound):
        class Value(Struct):
            pass  # TODO https://minecraft.fandom.com/wiki/Player.dat_format#Item_structure

        class Texture(TypedCompound):
            value: Annotated[ItemTag.SkullOwner.Value, Case.PASCAL]
            signature: Annotated[String, Case.PASCAL]

        class _Properties(TypedCompound):
            textures: List[ItemTag.SkullOwner.Texture]

        id: Annotated[IntArray | None, Case.PASCAL]
        name: Annotated[String | None, Case.PASCAL]
        properties: Annotated[_Properties, Case.PASCAL]

    skull_owner: Annotated[String | SkullOwner, Case.PASCAL]

    class Effect(TypedCompound):
        effect_id: Annotated[Byte, Case.PASCAL]
        effect_duration: Annotated[Int | None, Case.PASCAL]

    effects: List[Effect]


class Item(TypedCompound):
    count: Annotated[Byte, Case.PASCAL]
    id: String | None
    tag: ItemTag | None


class SlottedItem(Item):
    slot: Byte | None

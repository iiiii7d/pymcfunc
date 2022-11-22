from __future__ import annotations

from enum import Enum
from typing import Annotated

from pkmc.formats.item import Item
from pkmc.nbt import (
    Boolean,
    Byte,
    Case,
    Compound,
    Double,
    Float,
    Int,
    IntArray,
    List,
    Long,
    Short,
    String,
    TypedCompound,
)


class PotionEffect(TypedCompound):
    ambient: Annotated[Boolean, Case.PASCAL]
    amplifier: Annotated[Byte, Case.PASCAL]
    duration: Annotated[Int, Case.PASCAL]
    hidden_effect: Annotated[PotionEffect, Case.PASCAL]
    id: Annotated[Int, Case.PASCAL]
    show_icon: Annotated[Boolean, Case.PASCAL]
    show_particles: Annotated[Boolean, Case.PASCAL]


class Attribute(TypedCompound):
    class Modifier(TypedCompound):
        class Operation(Enum):
            OPR_0 = Int(0)
            OPR_1 = Int(1)
            OPR_2 = Int(2)

        amount: Annotated[Double, Case.PASCAL]
        name: Annotated[String, Case.PASCAL]
        operation: Annotated[Operation, Case.PASCAL]
        uuid: Annotated[IntArray, Case.UPPER]

    base: Annotated[Double, Case.PASCAL]
    modifiers: Annotated[List[Modifier], Case.PASCAL]
    name: Annotated[String, Case.PASCAL]


class _Brain(TypedCompound):
    memories: Memories


class Memories(TypedCompound):
    class AdmiringDisabled(TypedCompound):
        value: Boolean
        ttl: Long

    class AdmiringItem(TypedCompound):
        value: Boolean
        ttl: Long

    class AngryAt(TypedCompound):
        value: IntArray
        ttl: Long

    class DigCooldown(TypedCompound):
        value: Compound
        ttl: Long

    class GolemDetectedRecently(TypedCompound):
        value: Boolean
        ttl: Long

    class HasHuntingCooldown(TypedCompound):
        value: Boolean
        ttl: Long

    class Home(TypedCompound):
        class _Value(TypedCompound):
            dimension: String  # TODO NBT dimensions
            pos: IntArray

        _value: Annotated[_Value, "value"]

    class HuntedRecently(TypedCompound):
        value: Boolean
        ttl: Long

    class IsEmerging(TypedCompound):
        value: Compound

    class IsInWater(TypedCompound):
        value: Compound

    class IsPregnant(TypedCompound):
        value: Compound

    class IsSniffing(TypedCompound):
        value: Compound

    class IsTempted(TypedCompound):
        value: Boolean

    class ItemPickupCooldownTicks(TypedCompound):
        value: Int

    class JobSite(TypedCompound):
        class _Value(TypedCompound):
            dimension: String  # TODO NBT dimensions
            pos: IntArray

        _value: Annotated[_Value, "value"]

    class LastSlept(TypedCompound):
        value: Long

    class LastWoken(TypedCompound):
        value: Long

    class LastWorkedAtPoi(TypedCompound):
        value: Long

    class LikedNoteblock(TypedCompound):
        class _Value(TypedCompound):
            dimension: String  # TODO NBT dimensions
            pos: IntArray

        _value: Annotated[_Value, "value"]

    class LikedNoteblockCooldownTicks(TypedCompound):
        value: Int

    class LikedPlayer(TypedCompound):
        value: IntArray

    class LongJumpCoolingDown(TypedCompound):
        value: Int

    class MeetingPoint(TypedCompound):
        class _Value(TypedCompound):
            dimension: String  # TODO NBT dimensions
            pos: IntArray

        _value: Annotated[_Value, "value"]

    class PlayDeadTricks(TypedCompound):
        value: Int

    class PotentialJobSite(TypedCompound):
        class _Value(TypedCompound):
            dimension: String  # TODO NBT dimensions
            pos: IntArray

        _value: Annotated[_Value, "value"]

    class RamCooldownTicks(TypedCompound):
        value: Int

    class RecentProjectile(TypedCompound):
        value: Compound
        ttl: Long

    class RoarSoundCooldown(TypedCompound):
        value: Compound
        ttl: Long

    class RoarSoundDelay(TypedCompound):
        value: Compound
        ttl: Long

    class SniffCooldown(TypedCompound):
        value: Compound
        ttl: Long

    class TemptationCooldownTicks(TypedCompound):
        value: Int

    class TouchCooldown(TypedCompound):
        value: Compound
        ttl: Long

    class UniversalAnger(TypedCompound):
        value: Boolean
        ttl: Long

    class VibrationCooldown(TypedCompound):
        value: Compound
        ttl: Long

    admiring_disabled: Annotated[AdmiringDisabled | None, "minecraft:admiring_disabled"]
    admiring_item: Annotated[AdmiringItem | None, "minecraft:admiring_item"]
    angry_at: Annotated[AngryAt | None, "minecraft:angry_at"]
    dig_cooldown: Annotated[DigCooldown | None, "minecraft:dig_cooldown"]
    golem_detected_recently: Annotated[
        GolemDetectedRecently | None, "minecraft:golem_detected_recently"
    ]
    has_hunting_cooldown: Annotated[
        HasHuntingCooldown | None, "minecraft:has_hunting_cooldown"
    ]
    home: Annotated[Home | None, "minecraft:home"]
    hunted_recently: Annotated[HuntedRecently | None, "minecraft:hunted_recently"]
    is_emerging: Annotated[IsEmerging | None, "minecraft:is_emerging"]
    is_in_water: Annotated[IsInWater | None, "minecraft:is_in_water"]
    is_pregnant: Annotated[IsPregnant | None, "minecraft:is_pregnant"]
    is_sniffing: Annotated[IsSniffing | None, "minecraft:is_sniffing"]
    is_tempted: Annotated[IsTempted | None, "minecraft:is_tempted"]
    item_pickup_cooldown_ticks: Annotated[
        ItemPickupCooldownTicks | None, "minecraft:item_pickup_cooldown_ticks"
    ]
    job_site: Annotated[JobSite | None, "minecraft:job_site"]
    last_slept: Annotated[LastSlept | None, "minecraft:last_slept"]
    last_woken: Annotated[LastWoken | None, "minecraft:last_woken"]
    last_worked_at_poi: Annotated[
        LastWorkedAtPoi | None, "minecraft:last_worked_at_poi"
    ]
    liked_noteblock: Annotated[LikedNoteblock | None, "minecraft:liked_noteblock"]
    liked_noteblock_cooldown_ticks: Annotated[
        LikedNoteblockCooldownTicks | None, "minecraft:liked_noteblock_cooldown_ticks"
    ]
    liked_player: Annotated[LikedPlayer | None, "minecraft:liked_player"]
    long_jump_cooling_down: Annotated[
        LongJumpCoolingDown | None, "minecraft:long_jump_cooling_down"
    ]
    meeting_point: Annotated[MeetingPoint | None, "minecraft:meeting_point"]
    play_dead_tricks: Annotated[PlayDeadTricks | None, "minecraft:play_dead_tricks"]
    potential_job_site: Annotated[
        PotentialJobSite | None, "minecraft:potential_job_site"
    ]
    ram_cooldown_ticks: Annotated[
        RamCooldownTicks | None, "minecraft:ram_cooldown_ticks"
    ]
    recent_projectile: Annotated[RecentProjectile | None, "minecraft:recent_projectile"]
    roar_sound_cooldown: Annotated[
        RoarSoundCooldown | None, "minecraft:roar_sound_cooldown"
    ]
    roar_sound_delay: Annotated[RoarSoundDelay | None, "minecraft:roar_sound_delay"]
    sniff_cooldown: Annotated[SniffCooldown | None, "minecraft:sniff_cooldown"]
    temptation_cooldown_ticks: Annotated[
        TemptationCooldownTicks | None, "minecraft:temptation_cooldown_ticks"
    ]
    touch_cooldown: Annotated[TouchCooldown | None, "minecraft:touch_cooldown"]
    universal_anger: Annotated[UniversalAnger | None, "minecraft:universal_anger"]
    vibration_cooldown: Annotated[
        VibrationCooldown | None, "minecraft:vibration_cooldown"
    ]


class Mob(TypedCompound):
    absorption_amount: Annotated[Float, Case.PASCAL]
    active_effects: Annotated[List[PotionEffect] | None, Case.PASCAL]
    attributes: Annotated[List[Attribute], Case.PASCAL]
    _brain: Annotated[_Brain, "Brain"]
    death_loot_table: Annotated[String, Case.PASCAL]  # TODO loot table name
    death_loot_table_seed: Annotated[Long, Case.PASCAL]
    death_time: Annotated[Short, Case.PASCAL]
    fall_flying: Annotated[Boolean, Case.PASCAL]
    health: Annotated[Float, Case.PASCAL]
    hurt_by_timestamp: Annotated[Int, Case.PASCAL]
    hurt_time: Annotated[Short, Case.PASCAL]
    left_handed: Annotated[Boolean, Case.PASCAL]
    no_ai: Annotated[Boolean, "NoAI"]
    sleeping_x: Annotated[Int, Case.PASCAL]
    sleeping_y: Annotated[Int, Case.PASCAL]
    sleeping_z: Annotated[Int, Case.PASCAL]
    team: Annotated[String, Case.PASCAL]  # TODO scoreboard team


class UuidLeash(TypedCompound):
    uuid: Annotated[IntArray, Case.UPPER]


class XyzLeash(TypedCompound):
    x: Annotated[Int, Case.UPPER]
    y: Annotated[Int, Case.UPPER]
    z: Annotated[Int, Case.UPPER]


class MobNotPlayer(Mob):
    armor_drop_chances: Annotated[List[Float], Case.PASCAL]
    armor_items: Annotated[List[Item], Case.PASCAL]
    can_pick_up_loot: Annotated[Boolean, Case.PASCAL]
    hand_drop_chances: Annotated[List[Float], Case.PASCAL]
    hand_items: Annotated[List[Item], Case.PASCAL]
    leash: Annotated[UuidLeash | XyzLeash, Case.PASCAL]
    persistence_required: Annotated[Boolean, Case.PASCAL]

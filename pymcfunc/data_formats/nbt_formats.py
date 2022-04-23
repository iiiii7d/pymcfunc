from __future__ import annotations

from pymcfunc.data_formats.base_formats import NBTFormat
from pymcfunc.data_formats.nbt_tags import Byte, Int, String, CompoundReprAsList, Long, IntArray, Compound, Double, List
from pymcfunc.internal import base_class


class PotionEffectNBT(NBTFormat):
    ambient: Byte
    amplifier: Byte
    duration: Int
    id: Byte
    show_icon: Byte
    show_particles: Byte

class HideablePotionEffectNBT(PotionEffectNBT):
    hidden_effect: HideablePotionEffectNBT

class ItemNBT(NBTFormat): # TODO move this to its own page maybe?
    count: Byte
    id: String
    tag: ItemTagNBT

class SlottedItemNBT(ItemNBT):
    slot: Byte

class ItemTagNBT(NBTFormat):
    pass

class LocationNBT(NBTFormat):
    dimension: String
    pos: IntArray

class BrainNBT(NBTFormat):
    memories: CompoundReprAsList[Memory]

    @base_class
    class Memory(NBTFormat, do_pascal_case_ify=False):
        name = property(lambda self: "")

    class AdmiringDisabledMemory(Memory):
        name = property(lambda self: "minecraft:admiring_disabled")
        value: Byte
        ttl: Long

    class AdmiringItemMemory(Memory):
        name = property(lambda self: "minecraft:admiring_item")
        value: Byte
        ttl: Long

    class AngryAtMemory(Memory):
        name = property(lambda self: "minecraft:angry_at")
        value: IntArray
        ttl: Long

    class DigCooldownMemory(Memory):
        name = property(lambda self: "minecraft:dig_cooldown")
        value: Compound
        ttl: Long

    class GolemDetectedRecentlyMemory(Memory):
        name = property(lambda self: "minecraft:golem_detected_recently")
        value: Byte
        ttl: Long

    class HasHuntingCooldownMemory(Memory):
        name = property(lambda self: "minecraft:has_hunting_cooldown")
        value: Byte
        ttl: Long

    class HomeMemory(Memory):
        name = property(lambda self: "minecraft:home")
        value: BrainNBT.LocationNBT

    class HuntedRecentlyMemory(Memory):
        name = property(lambda self: "minecraft:hunted_recently")
        value: Byte
        ttl: Long

    class IsEmergingMemory(Memory):
        name = property(lambda self: "minecraft:is_emerging")
        value: Compound

    class IsInWaterMemory(Memory):
        name = property(lambda self: "minecraft:is_in_water")
        value: Compound

    class IsPregnantMemory(Memory):
        name = property(lambda self: "minecraft:is_pregnant")
        value: Compound

    class IsSniffingMemory(Memory):
        name = property(lambda self: "minecraft:is_sniffing")
        value: Compound

    class IsTemptedMemory(Memory):
        name = property(lambda self: "minecraft:is_tempted")
        value: Byte

    class ItemPickupCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:item_pickup_cooldown_ticks")
        value: Int

    class JobSiteMemory(Memory):
        name = property(lambda self: "minecraft:job_site")
        value: BrainNBT.LocationNBT

    class LastSleptMemory(Memory):
        name = property(lambda self: "minecraft:last_slept")
        value: Long

    class LastWokenMemory(Memory):
        name = property(lambda self: "minecraft:last_woken")
        value: Long

    class LastWorkedAtPoiMemory(Memory):
        name = property(lambda self: "minecraft:last_worked_at_poi")
        value: Long

    class LikedNoteblockMemory(Memory):
        name = property(lambda self: "minecraft:liked_noteblock")
        value: BrainNBT.LocationNBT

    class LikedNoteblockCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:liked_noteblock_cooldown_ticks")
        value: Int

    class LikedPlayerMemory(Memory):
        name = property(lambda self: "minecraft:liked_player")
        value: IntArray

    class LongJumpCoolingDownMemory(Memory):
        name = property(lambda self: "minecraft:long_jump_cooling_down")
        value: Int

    class MeetingPointMemory(Memory):
        name = property(lambda self: "minecraft:meeting_point")
        value: BrainNBT.LocationNBT

    class PlayDeadTicksMemory(Memory):
        name = property(lambda self: "minecraft:play_dead_ticks")
        value: Int

    class PotentialJobSiteMemory(Memory):
        name = property(lambda self: "minecraft:potential_job_site")
        value: BrainNBT.LocationNBT

    class RamCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:ram_cooldown_ticks")
        value: Int

    class RecentProjectileMemory(Memory):
        name = property(lambda self: "minecraft:recent_projectile")
        value: Compound
        ttl: Long

    class RoarSoundCooldownMemory(Memory):
        name = property(lambda self: "minecraft:roar_sound_cooldown")
        value: Compound
        ttl: Long

    class RoarSoundDelayemory(Memory):
        name = property(lambda self: "minecraft:roar_sound_delay")
        value: Compound
        ttl: Long

    class SniffCooldownMemory(Memory):
        name = property(lambda self: "minecraft:sniff_cooldown")
        value: Compound
        ttl: Long

    class TemptationCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:temptation_cooldown_ticks")
        value: Int

    class TouchCooldownMemory(Memory):
        name = property(lambda self: "minecraft:touch_cooldown")
        value: Compound
        ttl: Long

    class UniversalAngerMemory(Memory):
        name = property(lambda self: "minecraft:universal_anger")
        value: Byte
        ttl: Long

    class VibrationCooldownMemory(Memory):
        name = property(lambda self: "minecraft:vibration_cooldown")
        value: Compound
        ttl: Long

class AttributeNBT(NBTFormat):
    base: Double
    modifiers: List[Modifier]
    name: String

    class Modifier(NBTFormat):
        amount: Double
        name: String
        operation: Int
        uuid: IntArray


class LeashNBT:
    uuid: IntArray
    x: Int
    y: Int
    z: Int
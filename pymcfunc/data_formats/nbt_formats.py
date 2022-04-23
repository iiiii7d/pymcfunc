from __future__ import annotations

from uuid import UUID

from pymcfunc.data_formats.base_formats import NBTFormat
from pymcfunc.data_formats.coord import Coord
from pymcfunc.data_formats.nbt_path import Path
from pymcfunc.data_formats.nbt_tags import Byte, Int, String, CompoundReprAsList, Long, IntArray, Compound, Double, List
from pymcfunc.internal import base_class


class PotionEffectNBT(NBTFormat):
    ambient: Byte
    amplifier: Byte
    duration: Int
    id: Byte
    show_icon: Byte
    show_particles: Byte

    class Proxy(NBTFormat.Proxy):
        @property
        def ambient(self) -> Path[Byte]:
            return self.nbt.ambient
        @ambient.setter
        def ambient(self, value: bool):
            self.nbt.ambient = value

        @property
        def amplifier(self) -> Path[Byte]:
            return self.nbt.amplifier
        @amplifier.setter
        def amplifier(self, value: bool):
            self.nbt.amplifier = value

        @property
        def duration(self) -> Path[Int]:
            return self.nbt.duration
        @duration.setter
        def duration(self, value: int):
            self.nbt.duration = value

        @property
        def id(self) -> Path[Byte]:
            return self.nbt.id
        @id.setter
        def id(self, value: int):
            self.nbt.id = value

        @property
        def show_icon(self) -> Path[Byte]:
            return self.nbt.show_icon
        @show_icon.setter
        def show_icon(self, value: bool):
            self.nbt.show_icon = value

        @property
        def show_particles(self) -> Path[Byte]:
            return self.nbt.show_particles
        @show_particles.setter
        def show_particles(self, value: bool):
            self.nbt.show_particles = value

class HideablePotionEffectNBT(PotionEffectNBT):
    hidden_effect: HideablePotionEffectNBT

    class Proxy(PotionEffectNBT.Proxy):
        @property
        def hidden_effect(self) -> Path[HideablePotionEffectNBT]:
            return self.nbt.hidden_effect
        @hidden_effect.setter
        def hidden_effect(self, value: HideablePotionEffectNBT):
            self.nbt.hidden_effect = value

class ItemNBT(NBTFormat): # TODO move this to its own page maybe?
    count: Byte
    id: String
    tag: ItemTagNBT

    class Proxy(NBTFormat.Proxy):
        @property
        def count(self) -> Path[Byte]:
            return self.nbt.count
        @count.setter
        def count(self, value: int):
            self.nbt.count = value

        @property
        def id(self) -> Path[String]:
            return self.nbt.id
        @id.setter
        def id(self, value: str):
            self.nbt.id = value

        @property
        def tag(self) -> Path[ItemTagNBT]:
            return self.nbt.tag
        @tag.setter
        def tag(self, value: ItemTagNBT):
            self.nbt.tag = value


class SlottedItemNBT(ItemNBT):
    slot: Byte

    class Proxy(ItemNBT.Proxy):
        @property
        def slot(self) -> Path[Byte]:
            return self.nbt.slot
        @slot.setter
        def slot(self, value: int):
            self.nbt.slot = value

class ItemTagNBT(NBTFormat):
    pass

class LocationNBT(NBTFormat):
    dimension: String
    pos: IntArray

    class Proxy(NBTFormat.Proxy):
        @property
        def dimension(self) -> Path[String]:
            return self.nbt.dimension
        @dimension.setter
        def dimension(self, value: str):
            self.nbt.dimension = value

        @property
        def pos(self) -> Path[IntArray]:
            return self.nbt.pos
        @property
        def pos_x(self) -> Path[Int]:
            return self.nbt.pos[0]
        @property
        def pos_y(self) -> Path[Int]:
            return self.nbt.pos[1]
        @property
        def pos_z(self) -> Path[Int]:
            return self.nbt.pos[2]
        def set_pos(self, *,
                    coord: Coord | None = None,
                    x: int | None = None,
                    y: int | None = None,
                    z: int | None = None):
            if coord is not None:
                self.nbt.pos[0] = coord.x
                self.nbt.pos[1] = coord.y
                self.nbt.pos[2] = coord.z
            else:
                if x is not None: self.nbt.pos[0] = x
                if y is not None: self.nbt.pos[1] = y
                if z is not None: self.nbt.pos[2] = z


class BrainNBT(NBTFormat):
    memories: CompoundReprAsList[Memory] # TODO fix CompoundReprAsLists

    @base_class
    class Memory(NBTFormat, do_pascal_case_ify=False):
        name = property(lambda self: "")

    @base_class
    class TtlMemory(Memory):
        ttl: Long

        class Proxy(NBTFormat.Proxy):
            @property
            def ttl(self) -> Path[Long]:
                return self.nbt.ttl
            @ttl.setter
            def ttl(self, value: int):
                self.nbt.ttl = value

    @base_class
    class CompoundTtlMemory(TtlMemory):
        value: Compound

    @base_class
    class ByteTtlMemory(TtlMemory):
        value: Byte

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Byte]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    @base_class
    class IntArrayTtlMemory(TtlMemory):
        value: IntArray

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[IntArray]:
                return self.nbt.value
            @value.setter
            def value(self, value: UUID):
                self.nbt.value = IntArray(value)

    @base_class
    class LocationMemory(Memory):
        location: LocationNBT

        class Proxy(NBTFormat.Proxy):
            @property
            def location(self) -> Path[LocationNBT]:
                return self.nbt.location
            @location.setter
            def location(self, value: LocationNBT):
                self.nbt.location = value

    class AdmiringDisabledMemory(ByteTtlMemory):
        name = property(lambda self: "minecraft:admiring_disabled")

    class AdmiringItemMemory(ByteTtlMemory):
        name = property(lambda self: "minecraft:admiring_item")

    class AngryAtMemory(IntArrayTtlMemory):
        name = property(lambda self: "minecraft:angry_at")

    class DigCooldownMemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:dig_cooldown")

    class GolemDetectedRecentlyMemory(ByteTtlMemory):
        name = property(lambda self: "minecraft:golem_detected_recently")

    class HasHuntingCooldownMemory(ByteTtlMemory):
        name = property(lambda self: "minecraft:has_hunting_cooldown")

    class HomeMemory(LocationMemory):
        name = property(lambda self: "minecraft:home")

    class HuntedRecentlyMemory(ByteTtlMemory):
        name = property(lambda self: "minecraft:hunted_recently")

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

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Byte]:
                return self.nbt.value
            @value.setter
            def value(self, value: bool):
                self.nbt.value = Byte(value)

    class ItemPickupCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:item_pickup_cooldown_ticks")
        value: Int

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Int]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    class JobSiteMemory(LocationMemory):
        name = property(lambda self: "minecraft:job_site")

    class LastSleptMemory(Memory):
        name = property(lambda self: "minecraft:last_slept")
        value: Long

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Long]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Long(value)

    class LastWokenMemory(Memory):
        name = property(lambda self: "minecraft:last_woken")
        value: Long

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Long]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Long(value)

    class LastWorkedAtPoiMemory(Memory):
        name = property(lambda self: "minecraft:last_worked_at_poi")
        value: Long

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Long]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Long(value)

    class LikedNoteblockMemory(LocationMemory):
        name = property(lambda self: "minecraft:liked_noteblock")

    class LikedNoteblockCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:liked_noteblock_cooldown_ticks")
        value: Int

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Int]:
                return self.nbt.value

            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    class LikedPlayerMemory(Memory):
        name = property(lambda self: "minecraft:liked_player")
        value: IntArray

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[IntArray]:
                return self.nbt.value
            @value.setter
            def value(self, value: UUID):
                self.nbt.value = IntArray(value)

    class LongJumpCoolingDownMemory(Memory):
        name = property(lambda self: "minecraft:long_jump_cooling_down")
        value: Int

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Int]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    class MeetingPointMemory(LocationMemory):
        name = property(lambda self: "minecraft:meeting_point")

    class PlayDeadTicksMemory(Memory):
        name = property(lambda self: "minecraft:play_dead_ticks")
        value: Int

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Int]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    class PotentialJobSiteMemory(LocationMemory):
        name = property(lambda self: "minecraft:potential_job_site")

    class RamCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:ram_cooldown_ticks")
        value: Int

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Int]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    class RecentProjectileMemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:recent_projectile")

    class RoarSoundCooldownMemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:roar_sound_cooldown")

    class RoarSoundDelayemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:roar_sound_delay")

    class SniffCooldownMemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:sniff_cooldown")

    class TemptationCooldownTicksMemory(Memory):
        name = property(lambda self: "minecraft:temptation_cooldown_ticks")
        value: Int

        class Proxy(NBTFormat.Proxy):
            @property
            def value(self) -> Path[Int]:
                return self.nbt.value
            @value.setter
            def value(self, value: int):
                self.nbt.value = Int(value)

    class TouchCooldownMemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:touch_cooldown")

    class UniversalAngerMemory(ByteTtlMemory):
        name = property(lambda self: "minecraft:universal_anger")

    class VibrationCooldownMemory(CompoundTtlMemory):
        name = property(lambda self: "minecraft:vibration_cooldown")

class AttributeNBT(NBTFormat):
    base: Double
    modifiers: List[Modifier]
    name: String

    class Modifier(NBTFormat):
        amount: Double
        name: String
        operation: Int
        uuid: IntArray

        class Proxy(NBTFormat.Proxy):
            @property
            def amount(self) -> Path[Double]:
                return self.nbt.amount
            @amount.setter
            def amount(self, value: float):
                self.nbt.amount = Double(value)

            @property
            def name(self) -> Path[String]:
                return self.nbt.name
            @name.setter
            def name(self, value: str):
                self.nbt.name = String(value)

            @property
            def operation(self) -> Path[Int]:
                return self.nbt.operation
            @operation.setter
            def operation(self, value: int):
                self.nbt.operation = Int(value)

            @property
            def uuid(self) -> Path[IntArray]:
                return self.nbt.uuid
            @uuid.setter
            def uuid(self, value: UUID):
                self.nbt.uuid = IntArray(value)

    class Proxy(NBTFormat.Proxy):
        @property
        def base(self) -> Path[Double]:
            return self.nbt.base
        @base.setter
        def base(self, value: int):
            self.nbt.base = Double(value)

        @property
        def modifiers(self) -> Path[List[AttributeNBT.Modifier]]:
            return self.nbt.modifiers
        @modifiers.setter
        def modifiers(self, value: List[AttributeNBT.Modifier]):
            self.nbt.modifiers = List(value)

        @property
        def name(self) -> Path[String]:
            return self.nbt.name
        @name.setter
        def name(self, value: str):
            self.nbt.name = String(value)


class LeashNBT(NBTFormat):
    uuid: IntArray
    x: Int
    y: Int
    z: Int

    class Proxy(NBTFormat.Proxy):
        @property
        def uuid(self) -> Path[IntArray]:
            return self.nbt.uuid
        @uuid.setter
        def uuid(self, value: UUID):
            self.nbt.uuid = IntArray(value)

        @property
        def x(self) -> Path[Int]:
            return self.nbt.x
        @property
        def y(self) -> Path[Int]:
            return self.nbt.y
        @property
        def z(self) -> Path[Int]:
            return self.nbt.z
        def set_pos(self, *,
                    coord: Coord | None = None,
                    x: int | None = None,
                    y: int | None = None,
                    z: int | None = None):
            if coord is not None:
                self.nbt.x = coord.x
                self.nbt.y = coord.y
                self.nbt.z = coord.z
            else:
                if x is not None: self.nbt.x = Int(x)
                if y is not None: self.nbt.y = Int(y)
                if z is not None: self.nbt.z = Int(z)

class StateNBT(NBTFormat):
    name: String
    properties: Compound

    class Proxy(NBTFormat.Proxy):
        @property
        def name(self) -> Path[String]:
            return self.nbt.name
        @name.setter
        def name(self, value: str):
            self.nbt.name = String(value)

        @property
        def properties(self) -> Path[Compound]:
            return self.nbt.properties
        @properties.setter
        def properties(self, value: dict):
            self.nbt.properties = Compound(value)
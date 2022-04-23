from __future__ import annotations

from typing import Literal, Any
from uuid import UUID

from pymcfunc import JavaFunctionHandler
from pymcfunc.data_formats.base_formats import NBTFormat
from pymcfunc.data_formats.coord import Rotation, Coord
from pymcfunc.data_formats.loot_tables import LootTable
from pymcfunc.data_formats.nbt_path import Path
from pymcfunc.data_formats.nbt_tags import String, Short, Byte, IntArray, Int, List, Double, Float, Long
from pymcfunc.data_formats.nbt_formats import HideablePotionEffectNBT, ItemNBT, BrainNBT, AttributeNBT, LeashNBT, \
    PotionEffectNBT, SlottedItemNBT, LocationNBT, StateNBT
from pymcfunc.proxies.selectors import JavaSelector

class JavaEntity(JavaSelector):
    class NBT(NBTFormat):
        air: Short
        custom_name: String
        custom_name_visible: Byte | None
        fall_distance: Float
        fire: Short
        glowing: Byte
        has_visual_fire: Byte
        id: String
        invulnerable: Byte
        motion: List[Double]
        no_gravity: Byte
        on_ground: Byte
        passengers: List[JavaEntity.NBT]
        portal_cooldown: Int
        pos: List[Double]
        rotation: List[Float]
        silent: Byte | None
        tags: List[String]
        ticks_frozen: Int
        uuid: IntArray

        class Proxy(NBTFormat.Proxy):
            @property
            def air(self) -> Path[Short]:
                return self.nbt.air
    
            @air.setter
            def air(self, value: int):
                self.nbt.air = Short(value)
    
            @property
            def custom_name(self) -> Path[String]:
                return self.nbt.custom_name
    
            @custom_name.setter
            def custom_name(self, value: str | None):
                if value is None:
                    self.nbt.custom_name = String("")
                else:
                    self.nbt.custom_name = String(value)
    
            @property
            def custom_name_visible(self) -> Path[Byte]:
                return self.nbt.custom_name_visible
    
            @custom_name_visible.setter
            def custom_name_visible(self, value: bool):
                self.nbt.custom_name_visible = Byte(int(value))
    
            @custom_name_visible.deleter
            def custom_name_visible(self):
                del self.nbt.custom_name_visible
    
            @property
            def fall_distance(self) -> Path[Float]:
                return self.nbt.fall_distance
    
            @fall_distance.setter
            def fall_distance(self, value: float):
                self.nbt.fall_distance = Float(value)
    
            @property
            def fire(self) -> Path[Short]:
                return self.nbt.fire
    
            @fire.setter
            def fire(self, value: int):
                self.nbt.fire = Short(value)
    
            @property
            def glowing(self) -> Path[Byte]:
                return self.nbt.glowing
    
            @glowing.setter
            def glowing(self, value: bool):
                self.nbt.glowing = Byte(int(value))
    
            @property
            def has_visual_fire(self) -> Path[Byte]:
                return self.nbt.has_visual_fire
    
            @has_visual_fire.setter
            def has_visual_fire(self, value: bool):
                self.nbt.has_visual_fire = Byte(int(value))
    
            @property
            def id(self) -> Path[String]:
                return self.nbt.id
    
            @id.setter
            def id(self, value: str):
                self.nbt.id = String(value)
    
            @property
            def invulnerable(self) -> Path[Byte]:
                return self.nbt.invulnerable
    
            @invulnerable.setter
            def invulnerable(self, value: bool):
                self.nbt.invulnerable = Byte(int(value))
    
            @property
            def motion(self) -> Path[List[Double]]:
                return self.nbt.motion
    
            @property
            def motion_x(self) -> Path[Double]:
                return self.nbt.motion[0]
    
            @property
            def motion_y(self) -> Path[Double]:
                return self.nbt.motion[1]
    
            @property
            def motion_z(self) -> Path[Double]:
                return self.nbt.motion[2]
    
            def set_motion(self, *,
                           x: float | None = None,
                           y: float | None = None,
                           z: float | None = None):
                if x is not None:
                    self.nbt.motion[0] = Double(x)
                if y is not None:
                    self.nbt.motion[1] = Double(y)
                if z is not None:
                    self.nbt.motion[2] = Double(z)
    
            @property
            def no_gravity(self) -> Path[Byte]:
                return self.nbt.no_gravity
    
            @no_gravity.setter
            def no_gravity(self, value: bool):
                self.nbt.no_gravity = Byte(int(value))
    
            @property
            def passengers(self) -> Path[List[JavaEntity.NBT]]:
                return self.nbt.passengers
    
            @passengers.setter
            def passengers(self, value: list[JavaEntity.NBT]):
                self.nbt.passengers = List[JavaEntity.NBT](value)
    
            @property
            def portal_cooldown(self) -> Path[Int]:
                return self.nbt.portal_cooldown
    
            @portal_cooldown.setter
            def portal_cooldown(self, value: float):
                self.nbt.portal_cooldown = Int(value)
    
            @property
            def pos(self) -> Path[List[Double]]:
                return self.nbt.pos
    
            @property
            def pos_x(self) -> Path[Double]:
                return self.nbt.pos[0]
    
            @property
            def pos_y(self) -> Path[Double]:
                return self.nbt.pos[1]
    
            @property
            def pos_z(self) -> Path[Double]:
                return self.nbt.pos[2]
    
            def set_pos(self, *,
                        position: Coord | None = None,
                        x: float | None = None,
                        y: float | None = None,
                        z: float | None = None):
                if position:
                    self.nbt.pos[0] = Double(position.x)
                    self.nbt.pos[1] = Double(position.y)
                    self.nbt.pos[2] = Double(position.z)
                else:
                    if x: self.nbt.pos[0] = Double(x)
                    if y: self.nbt.pos[1] = Double(y)
                    if z: self.nbt.pos[2] = Double(z)
    
            @property
            def rotation(self) -> Path[List[Float]]:
                return self.nbt.rotation
    
            @property
            def pitch(self) -> Path[Float]:
                return self.nbt.rotation[0]
    
            @property
            def yaw(self) -> Path[Float]:
                return self.nbt.rotation[1]
    
            def set_rotation(self, *,
                             rotation: Rotation | None = None,
                             pitch: float | None = None,
                             yaw: float | None = None):
                if rotation is not None:
                    self.nbt.rotation[0] = Float(rotation.pitch)
                    self.nbt.rotation[1] = Float(rotation.yaw)
                else:
                    if pitch is not None: self.nbt.rotation[0] = Float(pitch)
                    if yaw is not None: self.nbt.rotation[1] = Float(yaw)
    
            @property
            def silent(self) -> Path[Byte]:
                return self.nbt.silent
    
            @silent.setter
            def silent(self, value: bool):
                self.nbt.silent = Byte(int(value))
    
            @silent.deleter
            def silent(self):
                del self.nbt.silent
    
            @property
            def tags(self) -> Path[List[String]]:
                return self.nbt.tags
    
            @tags.setter
            def tags(self, value: list[str]):
                self.nbt.tags = List[String](value)
    
            @property
            def ticks_frozen(self) -> Path[Int]:
                return self.nbt.ticks_frozen
    
            @ticks_frozen.setter
            def ticks_frozen(self, value: float):
                self.nbt.ticks_frozen = Int(value)
    
            @property
            def uuid(self) -> Path[IntArray]:
                return self.nbt.uuid
    
            @uuid.setter
            def uuid(self, value: UUID):
                self.nbt.uuid = IntArray(value)  # TODO see if this works

    def __init__(self, var: Literal['p', 'r', 'a', 'e', 's'],
                 fh: JavaFunctionHandler | None = None,
                 **arguments: Any):
        super().__init__(var, fh, **arguments)
        self.nbt = self.NBT.as_path(fh=fh)
        self.proxy = self.NBT.Proxy(self.nbt)
        self.px = self.proxy


class JavaMob(JavaEntity):
    class NBT(JavaEntity.NBT):
        absorption_amount: Float
        active_effects: List[HideablePotionEffectNBT] | None
        armor_drop_chances: List[Float]
        armor_items: List[ItemNBT]
        attributes: List[AttributeNBT]
        brain: BrainNBT
        can_pick_up_loot: Byte
        death_loot_table: String | None
        death_loot_table_seed: Long | None
        death_time: Short
        fall_flying: Byte
        health: Float
        hurt_by_timestamp: Int
        hurt_time: Short
        hand_drop_chances: List[Float]
        hand_items: List[ItemNBT]
        leash: LeashNBT
        left_handed: Byte
        no_ai: Byte
        persistence_required: Byte
        sleeping_x: Int
        sleeping_y: Int
        sleeping_z: Int
        team: String

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def absorption_amount(self) -> Path[Float]:
                return self.nbt.absorption_amount
            @absorption_amount.setter
            def absorption_amount(self, value: float):
                self.nbt.absorption_amount = Float(value)
    
            @property
            def active_effects(self) -> Path[List[HideablePotionEffectNBT]]:
                return self.nbt.active_effects
            @active_effects.setter
            def active_effects(self, value: list[HideablePotionEffectNBT]):
                self.nbt.active_effects = List[HideablePotionEffectNBT](value)
            @active_effects.deleter
            def active_effects(self):
                del self.nbt.active_effects
    
            @property
            def armor_drop_chances(self) -> Path[List[Float]]:
                return self.nbt.armor_drop_chances
            @property
            def feet_armor_drop_chances(self) -> Path[Float]:
                return self.nbt.armor_drop_chances[0]
            @property
            def legs_armor_drop_chances(self) -> Path[Float]:
                return self.nbt.armor_drop_chances[1]
            @property
            def chest_armor_drop_chances(self) -> Path[Float]:
                return self.nbt.armor_drop_chances[2]
            @property
            def head_armor_drop_chances(self) -> Path[Float]:
                return self.nbt.armor_drop_chances[3]
            def set_armour_drop_chances(self, *,
                                        feet: float | None = None,
                                        legs: float | None = None,
                                        chest: float | None = None,
                                        head: float | None = None):
                if feet is not None: self.nbt.armor_drop_chances[0] = Float(feet)
                if legs is not None: self.nbt.armor_drop_chances[1] = Float(legs)
                if chest is not None: self.nbt.armor_drop_chances[2] = Float(chest)
                if head is not None: self.nbt.armor_drop_chances[3] = Float(head)
    
            @property
            def armor_items(self) -> Path[List[ItemNBT]]:
                return self.nbt.armor_items
            @property
            def feet_armor_item(self) -> Path[ItemNBT]:
                return self.nbt.armor_items[0]
            @property
            def legs_armor_item(self) -> Path[ItemNBT]:
                return self.nbt.armor_items[1]
            @property
            def chest_armor_item(self) -> Path[ItemNBT]:
                return self.nbt.armor_items[2]
            @property
            def head_armor_item(self) -> Path[ItemNBT]:
                return self.nbt.armor_items[3]
            def set_armour_items(self, *,
                                 feet: ItemNBT | None = None,
                                 legs: ItemNBT | None = None,
                                 chest: ItemNBT | None = None,
                                 head: ItemNBT | None = None):
                if feet is not None: self.nbt.armor_items[0] = feet
                if legs is not None: self.nbt.armor_items[1] = legs
                if chest is not None: self.nbt.armor_items[2] = chest
                if head is not None: self.nbt.armor_items[3] = head
    
            @property
            def attributes(self) -> Path[List[AttributeNBT]]:
                return self.nbt.attributes
            @attributes.setter
            def attributes(self, value: list[AttributeNBT]):
                self.nbt.attributes = List[AttributeNBT](value)
    
            @property
            def brain(self) -> Path[BrainNBT]:
                return self.nbt.brain
            @brain.setter
            def brain(self, value: BrainNBT):
                self.nbt.brain = value
            @property
            def memories(self) -> Path[List[BrainNBT.Memory]]:
                return self.nbt.brain.memories
            @memories.setter
            def memories(self, value: list[BrainNBT.Memory]):
                self.nbt.brain.memories = List[BrainNBT.Memory](value)
    
            @property
            def can_pick_up_loot(self) -> Path[Byte]:
                return self.nbt.can_pick_up_loot
            @can_pick_up_loot.setter
            def can_pick_up_loot(self, value: bool):
                self.nbt.can_pick_up_loot = Byte(value)
    
            @property
            def death_loot_table(self) -> Path[String]:
                return self.nbt.death_loot_table
            @death_loot_table.setter
            def death_loot_table(self, value: str | LootTable):
                self.nbt.death_loot_table = String(value)
            @death_loot_table.deleter
            def death_loot_table(self):
                del self.nbt.death_loot_table
    
            @property
            def death_loot_table_seed(self) -> Path[Long]:
                return self.nbt.death_loot_table_seed
            @death_loot_table_seed.setter
            def death_loot_table_seed(self, value: int):
                self.nbt.death_loot_table_seed = Long(value)
            @death_loot_table_seed.deleter
            def death_loot_table_seed(self):
                del self.nbt.death_loot_table_seed
    
            @property
            def death_time(self) -> Path[Short]:
                return self.nbt.death_time
            @death_time.setter
            def death_time(self, value: int):
                self.nbt.death_time = Short(value)
    
            @property
            def fall_flying(self) -> Path[Byte]:
                return self.nbt.fall_flying
            @fall_flying.setter
            def fall_flying(self, value: bool):
                self.nbt.fall_flying = Byte(value)
    
            @property
            def health(self) -> Path[Float]:
                return self.nbt.health
            @health.setter
            def health(self, value: float):
                self.nbt.health = Float(value)
    
            @property
            def hurt_by_timestamp(self) -> Path[Int]:
                return self.nbt.hurt_by_timestamp
            @hurt_by_timestamp.setter
            def hurt_by_timestamp(self, value: int):
                self.nbt.hurt_by_timestamp = Int(value)
    
            @property
            def hurt_time(self) -> Path[Short]:
                return self.nbt.hurt_time
            @hurt_time.setter
            def hurt_time(self, value: int):
                self.nbt.hurt_time = Short(value)
    
            @property
            def hand_drop_chances(self) -> Path[List[Float]]:
                return self.nbt.hand_drop_chances
            @property
            def mainhand_drop_chances(self) -> Path[Float]:
                return self.nbt.hand_drop_chances[0]
            @property
            def offhand_drop_chances(self) -> Path[Float]:
                return self.nbt.hand_drop_chances[1]
            def set_hand_drop_chances(self, *,
                                      mainhand: float | None = None,
                                      offhand: float | None = None):
                if mainhand is not None: self.nbt.hand_drop_chances[0] = mainhand
                if offhand is not None: self.nbt.hand_drop_chances[1] = offhand
    
            @property
            def hand_items(self) -> Path[List[ItemNBT]]:
                return self.nbt.hand_items
            @property
            def mainhand_item(self) -> Path[ItemNBT]:
                return self.nbt.hand_items[0]
            @property
            def offhand_item(self) -> Path[ItemNBT]:
                return self.nbt.hand_items[1]
            def set_hand_items(self, *,
                               mainhand: ItemNBT | None = None,
                               offhand: ItemNBT | None = None):
                if mainhand is not None: self.nbt.hand_items[0] = mainhand
                if offhand is not None: self.nbt.hand_items[1] = offhand
    
            @property
            def leash(self) -> Path[LeashNBT]:
                return self.nbt.leash
            @leash.setter
            def leash(self, value: LeashNBT):
                self.nbt.leash = value
    
            @property
            def left_handed(self) -> Path[Byte]:
                return self.nbt.left_handed
            @left_handed.setter
            def left_handed(self, value: bool):
                self.nbt.left_handed = Byte(value)
    
            @property
            def no_ai(self) -> Path[Byte]:
                return self.nbt.no_ai
            @no_ai.setter
            def no_ai(self, value: bool):
                self.nbt.no_ai = Byte(value)
    
            @property
            def persistence_required(self) -> Path[Byte]:
                return self.nbt.persistence_required
            @persistence_required.setter
            def persistence_required(self, value: bool):
                self.nbt.persistence_required = Byte(value)
    
            @property
            def sleeping_x(self) -> Path[Int]:
                return self.nbt.sleeping_x
            @property
            def sleeping_y(self) -> Path[Int]:
                return self.nbt.sleeping_y
            @property
            def sleeping_z(self) -> Path[Int]:
                return self.nbt.sleeping_z
            def set_sleeping(self, *,
                             x: int | None = None,
                             y: int | None = None,
                             z: int | None = None):
                if x is not None: self.nbt.sleeping_x = Int(x)
                if y is not None: self.nbt.sleeping_y = Int(y)
                if z is not None: self.nbt.sleeping_z = Int(z)
    
            @property
            def team(self) -> Path[String]:
                return self.nbt.team
            @team.setter
            def team(self, value: str):
                self.nbt.team = String(value)


class JavaBreedableMob(JavaMob):
    class NBT(JavaMob.NBT):
        age: Int
        forced_age: Int
        in_love: Int
        love_cause: IntArray

        class Proxy(JavaMob.NBT.Proxy):
            @property
            def age(self) -> Path[Int]:
                return self.nbt.age
            @age.setter
            def age(self, value: int):
                self.nbt.age = Int(value)

            @property
            def forced_age(self) -> Path[Int]:
                return self.nbt.forced_age
            @forced_age.setter
            def forced_age(self, value: int):
                self.nbt.forced_age = Int(value)

            @property
            def in_love(self) -> Path[Int]:
                return self.nbt.in_love
            @in_love.setter
            def in_love(self, value: int):
                self.nbt.in_love = Int(value)

            @property
            def love_cause(self) -> Path[IntArray]:
                return self.nbt.love_cause
            @love_cause.setter
            def love_cause(self, value: UUID):
                self.nbt.love_cause = IntArray(value) # TODO same

class JavaAngerableMob(JavaMob):
    class NBT(JavaMob.NBT):
        anger_time: Int
        angry_at: IntArray

        class Proxy(JavaMob.NBT.Proxy):
            @property
            def anger_time(self) -> Path[Int]:
                return self.nbt.anger_time
            @anger_time.setter
            def anger_time(self, value: int):
                self.nbt.anger_time = Int(value)

            @property
            def angry_at(self) -> Path[IntArray]:
                return self.nbt.angry_at
            @angry_at.setter
            def angry_at(self, value: UUID):
                self.nbt.angry_at = IntArray(value) # TODO same

class JavaTameableMob(JavaMob):
    class NBT(JavaMob.NBT):
        owner: IntArray
        sitting: Byte

        class Proxy(JavaMob.NBT.Proxy):
            @property
            def owner(self) -> Path[IntArray]:
                return self.nbt.owner
            @owner.setter
            def owner(self, value: UUID):
                self.nbt.owner = IntArray(value) # TODO same

            @property
            def sitting(self) -> Path[Byte]:
                return self.nbt.sitting
            @sitting.setter
            def sitting(self, value: bool):
                self.nbt.sitting = Byte(value)

class JavaZombieMob(JavaMob):
    class NBT(JavaMob.NBT):
        can_break_doors: Byte
        drowned_conversion_time: Int
        in_water_time: Int
        is_baby: Byte | None

        class Proxy(JavaMob.NBT.Proxy):
            @property
            def can_break_doors(self) -> Path[Byte]:
                return self.nbt.can_break_doors
            @can_break_doors.setter
            def can_break_doors(self, value: bool):
                self.nbt.can_break_doors = Byte(value)

            @property
            def drowned_conversion_time(self) -> Path[Int]:
                return self.nbt.drowned_conversion_time
            @drowned_conversion_time.setter
            def drowned_conversion_time(self, value: int):
                self.nbt.drowned_conversion_time = Int(value)

            @property
            def in_water_time(self) -> Path[Int]:
                return self.nbt.in_water_time
            @in_water_time.setter
            def in_water_time(self, value: int):
                self.nbt.in_water_time = Int(value)

            @property
            def is_baby(self) -> Path[Byte | None]:
                return self.nbt.is_baby
            @is_baby.setter
            def is_baby(self, value: bool):
                self.nbt.is_baby = Byte(value)
            @is_baby.deleter
            def is_baby(self):
                del self.nbt.is_baby

class JavaHorseGroup(JavaBreedableMob):
    class NBT(JavaBreedableMob.NBT):
        armor_item: ItemNBT
        eating_haystack: Byte
        owner: IntArray
        saddle_item: ItemNBT
        tame: Byte
        temper: Int

        class Proxy(JavaBreedableMob.Proxy):
            @property
            def armor_item(self) -> Path[ItemNBT]:
                return self.nbt.armor_item
            @armor_item.setter
            def armor_item(self, value: ItemNBT):
                self.nbt.armor_item = value

            @property
            def eating_haystack(self) -> Path[Byte]:
                return self.nbt.eating_haystack
            @eating_haystack.setter
            def eating_haystack(self, value: bool):
                self.nbt.eating_haystack = Byte(value)

            @property
            def owner(self) -> Path[IntArray]:
                return self.nbt.owner
            @owner.setter
            def owner(self, value: UUID):
                self.nbt.owner = IntArray(value) # TODO same

            @property
            def saddle_item(self) -> Path[ItemNBT]:
                return self.nbt.saddle_item
            @saddle_item.setter
            def saddle_item(self, value: ItemNBT):
                self.nbt.saddle_item = value

            @property
            def tame(self) -> Path[Byte]:
                return self.nbt.tame
            @tame.setter
            def tame(self, value: bool):
                self.nbt.tame = Byte(value)

            @property
            def temper(self) -> Path[Int]:
                return self.nbt.temper
            @temper.setter
            def temper(self, value: int):
                self.nbt.temper = Int(value)

class JavaRaidMob(JavaMob):
    class NBT(JavaMob.NBT):
        can_join_raid: Byte
        patrol_leader: Byte
        patrolling: Byte
        patrol_target: CoordNBT
        raid_id: Int
        wave: Int

        class CoordNBT(NBTFormat):
            x: Int
            y: Int
            z: Int

        class Proxy(JavaMob.NBT.Proxy):
            @property
            def can_join_raid(self) -> Path[Byte]:
                return self.nbt.can_join_raid
            @can_join_raid.setter
            def can_join_raid(self, value: bool):
                self.nbt.can_join_raid = Byte(value)

            @property
            def patrol_leader(self) -> Path[Byte]:
                return self.nbt.patrol_leader
            @patrol_leader.setter
            def patrol_leader(self, value: bool):
                self.nbt.patrol_leader = Byte(value)

            @property
            def patrolling(self) -> Path[Byte]:
                return self.nbt.patrolling
            @patrolling.setter
            def patrolling(self, value: bool):
                self.nbt.patrolling = Byte(value)

            @property
            def patrol_target(self) -> Path[JavaRaidMob.NBT.CoordNBT]:
                return self.nbt.patrol_target
            @property
            def patrol_target_x(self) -> Path[Int]:
                return self.nbt.patrol_target.x
            @property
            def patrol_target_y(self) -> Path[Int]:
                return self.nbt.patrol_target.y
            @property
            def patrol_target_z(self) -> Path[Int]:
                return self.nbt.patrol_target.z
            def set_patrol_target(self, *,
                                  coords: Coord | None = None,
                                  x: int | None = None,
                                  y: int | None = None,
                                  z: int | None = None):
                if coords is not None:
                    self.nbt.patrol_target.x = Int(coords.x)
                    self.nbt.patrol_target.y = Int(coords.y)
                    self.nbt.patrol_target.z = Int(coords.z)
                else:
                    if x is not None: self.nbt.patrol_target.x = x
                    if y is not None: self.nbt.patrol_target.y = y
                    if z is not None: self.nbt.patrol_target.z = z

            @property
            def raid_id(self) -> Path[Int]:
                return self.nbt.raid_id
            @raid_id.setter
            def raid_id(self, value: int):
                self.nbt.raid_id = Int(value)

            @property
            def wave(self) -> Path[Int]:
                return self.nbt.wave
            @wave.setter
            def wave(self, value: int):
                self.nbt.wave = Int(value)

class JavaProjectile(JavaEntity):
    class NBT(JavaEntity.NBT):
        has_been_shot: Byte
        left_owner: Byte
        owner: IntArray

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def has_been_shot(self) -> Path[Byte]:
                return self.nbt.has_been_shot
            @has_been_shot.setter
            def has_been_shot(self, value: bool):
                self.nbt.has_been_shot = Byte(value)

            @property
            def left_owner(self) -> Path[Byte]:
                return self.nbt.left_owner
            @left_owner.setter
            def left_owner(self, value: bool):
                self.nbt.left_owner = Byte(value)

            @property
            def owner(self) -> Path[IntArray]:
                return self.nbt.owner
            @owner.setter
            def owner(self, value: UUID):
                self.nbt.owner = IntArray(value)


class JavaPotionEffects(JavaEntity):
    class NBT(JavaEntity.NBT):
        custom_potion_effects: List[PotionEffectNBT]
        potion: String
        custom_potion_color: Int

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def custom_potion_effects(self) -> Path[List[PotionEffectNBT]]:
                return self.nbt.custom_potion_effects
            @custom_potion_effects.setter
            def custom_potion_effects(self, value: List[PotionEffectNBT]):
                self.nbt.custom_potion_effects = List[PotionEffectNBT](value)

            @property
            def potion(self) -> Path[String]:
                return self.nbt.potion
            @potion.setter
            def potion(self, value: str):
                self.nbt.potion = String(value)

            @property
            def custom_potion_color(self) -> Path[Int]:
                return self.nbt.custom_potion_color
            @custom_potion_color.setter
            def custom_potion_color(self, value: int):
                self.nbt.custom_potion_color = Int(value)


class JavaMinecart(JavaEntity):
    class NBT(JavaEntity.NBT):
        custom_display_tile: Byte
        display_offset: Int
        display_state: StateNBT

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def custom_display_tile(self) -> Path[Byte]:
                return self.nbt.custom_display_tile
            @custom_display_tile.setter
            def custom_display_tile(self, value: bool):
                self.nbt.custom_display_tile = Byte(value)

            @property
            def display_offset(self) -> Path[Int]:
                return self.nbt.display_offset
            @display_offset.setter
            def display_offset(self, value: int):
                self.nbt.display_offset = Int(value)

            @property
            def display_state(self) -> Path[StateNBT]:
                return self.nbt.display_state
            @display_state.setter
            def display_state(self, value: StateNBT):
                self.nbt.display_state = value

class JavaContainer(JavaEntity):
    class NBT(JavaEntity.NBT):
        items: List[ItemNBT]
        loot_table: String
        loot_table_seed: Long

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def items(self) -> Path[List[ItemNBT]]:
                return self.nbt.items
            @items.setter
            def items(self, value: List[ItemNBT]):
                self.nbt.items = List[ItemNBT](value)

            @property
            def loot_table(self) -> Path[String]:
                return self.nbt.loot_table
            @loot_table.setter
            def loot_table(self, value: str | LootTable):
                self.nbt.loot_table = String(value)

            @property
            def loot_table_seed(self) -> Path[Long]:
                return self.nbt.loot_table_seed
            @loot_table_seed.setter
            def loot_table_seed(self, value: int):
                self.nbt.loot_table_seed = Long(value)

class JavaHangable(JavaEntity):
    class NBT(JavaEntity.NBT):
        facing: Byte
        tile_x: Float
        tile_y: Float
        tile_z: Float

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def facing(self) -> Path[Byte]:
                return self.nbt.facing
            @facing.setter
            def facing(self, value: int):
                self.nbt.facing = Byte(value)

            @property
            def tile_x(self) -> Path[Float]:
                return self.nbt.tile_x
            @property
            def tile_y(self) -> Path[Float]:
                return self.nbt.tile_y
            @property
            def tile_z(self) -> Path[Float]:
                return self.nbt.tile_z
            def set_tile(self, *,
                         coord: Coord | None = None,
                         x: int = None,
                         y: int = None,
                         z: int = None):
                if coord is not None:
                    self.nbt.tile_x = Float(coord.x)
                    self.nbt.tile_y = Float(coord.y)
                    self.nbt.tile_z = Float(coord.z)
                if x is not None: self.nbt.tile_x = Float(x)
                if y is not None: self.nbt.tile_y = Float(y)
                if z is not None: self.nbt.tile_z = Float(z)

class JavaFireball(JavaEntity):
    class NBT(JavaEntity.NBT):
        power: List[Double]

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def power(self) -> Path[List[Double]]:
                return self.nbt.power
            @property
            def power_x(self) -> Path[Double]:
                return self.nbt.power[0]
            @property
            def power_y(self) -> Path[Double]:
                return self.nbt.power[1]
            @property
            def power_z(self) -> Path[Double]:
                return self.nbt.power[2]
            def set_power(self, *,
                          x: float = None,
                          y: float = None,
                          z: float = None):
                if x is not None: self.nbt.power[0] = Double(x)
                if y is not None: self.nbt.power[1] = Double(y)
                if z is not None: self.nbt.power[2] = Double(z)

class JavaArrowGroup(JavaEntity): # TODO fix case
    class NBT(JavaEntity.NBT):
        crit: Byte
        damage: Double
        in_block_state: StateNBT | None
        in_ground: Byte
        life: Short
        pickup: Byte
        pierce_level: Byte
        shake: Byte
        shot_from_crossbow: Byte
        sound_event: String

        class Proxy(JavaEntity.NBT.Proxy):
            @property
            def crit(self) -> Path[Byte]:
                return self.nbt.crit
            @crit.setter
            def crit(self, value: int):
                self.nbt.crit = Byte(value)

            @property
            def damage(self) -> Path[Double]:
                return self.nbt.damage
            @damage.setter
            def damage(self, value: float):
                self.nbt.damage = Double(value)

            @property
            def in_block_state(self) -> Path[StateNBT]:
                return self.nbt.in_block_state
            @in_block_state.setter
            def in_block_state(self, value: StateNBT):
                self.nbt.in_block_state = value
            @in_block_state.deleter
            def in_block_state(self):
                del self.nbt.in_block_state

            @property
            def in_ground(self) -> Path[Byte]:
                return self.nbt.in_ground
            @in_ground.setter
            def in_ground(self, value: int):
                self.nbt.in_ground = Byte(value)

            @property
            def life(self) -> Path[Short]:
                return self.nbt.life
            @life.setter
            def life(self, value: int):
                self.nbt.life = Short(value)

            @property
            def pickup(self) -> Path[Byte]:
                return self.nbt.pickup
            @pickup.setter
            def pickup(self, value: int):
                self.nbt.pickup = Byte(value)

            @property
            def pierce_level(self) -> Path[Byte]:
                return self.nbt.pierce_level
            @pierce_level.setter
            def pierce_level(self, value: int):
                self.nbt.pierce_level = Byte(value)

            @property
            def shake(self) -> Path[Byte]:
                return self.nbt.shake
            @shake.setter
            def shake(self, value: int):
                self.nbt.shake = Byte(value)

            @property
            def shot_from_crossbow(self) -> Path[Byte]:
                return self.nbt.shot_from_crossbow
            @shot_from_crossbow.setter
            def shot_from_crossbow(self, value: int):
                self.nbt.shot_from_crossbow = Byte(value)

            @property
            def sound_event(self) -> Path[String]:
                return self.nbt.sound_event
            @sound_event.setter
            def sound_event(self, value: str):
                self.nbt.sound_event = String(value)


class JavaPlayer(JavaMob):
    def __init__(self, var: Literal['p', 'r', 'a', 'e', 's'],
                 fh: JavaFunctionHandler | None = None,
                 **arguments: Any):
        super().__init__(var, fh, **arguments)
        if not self.playeronly:
            raise ValueError(f'Non-player entities might be selected with {self}')

    class NBT(JavaMob.NBT):
        abilities: AbilitiesNBT
        data_version: Int
        dimension: String
        ender_items: List[SlottedItemNBT]
        entered_nether_position: CoordNBT
        food_exhaustion_level: Float
        food_level: Int
        food_saturation_level: Float
        food_tick_timer: Int
        inventory: List[SlottedItemNBT]
        last_death_location: LocationNBT
        player_game_type: Int
        previous_player_game_type: Int
        recipe_book: RecipeBookNBT
        root_vehicle: RootVehicleNBT | None
        score: Int
        seen_credits: Byte # TODO case
        selected_item: ItemNBT
        shoulder_entity_left: JavaEntity.NBT
        shoulder_entity_right: JavaEntity.NBT
        sleep_timer: Short
        spawn_dimension: String | None
        spawn_forced: Byte
        spawn_x: Int
        spawn_y: Int | None
        spawn_z: Int
        warden_spawn_tracker: WardenSpawnTrackerNBT
        xp_level: Int
        xp_p: Float
        xp_seed: Int
        xp_total: Int

        class AbilitiesNBT(NBTFormat):
            flying: Byte
            fly_speed: Float
            instabuild: Byte
            invulnerable: Byte
            may_build: Byte
            may_fly: Byte
            walk_speed: Float

            class Proxy(NBTFormat.Proxy):
                @property
                def flying(self) -> Path[Byte]:
                    return self.nbt.flying
                @flying.setter
                def flying(self, value: bool):
                    self.nbt.flying = Byte(value)

                @property
                def fly_speed(self) -> Path[Float]:
                    return self.nbt.fly_speed
                @fly_speed.setter
                def fly_speed(self, value: float):
                    self.nbt.fly_speed = Float(value)

                @property
                def instabuild(self) -> Path[Byte]:
                    return self.nbt.instabuild
                @instabuild.setter
                def instabuild(self, value: bool):
                    self.nbt.instabuild = Byte(value)

                @property
                def invulnerable(self) -> Path[Byte]:
                    return self.nbt.invulnerable
                @invulnerable.setter
                def invulnerable(self, value: bool):
                    self.nbt.invulnerable = Byte(value)

                @property
                def may_build(self) -> Path[Byte]:
                    return self.nbt.may_build
                @may_build.setter
                def may_build(self, value: bool):
                    self.nbt.may_build = Byte(value)

                @property
                def may_fly(self) -> Path[Byte]:
                    return self.nbt.may_fly
                @may_fly.setter
                def may_fly(self, value: bool):
                    self.nbt.may_fly = Byte(value)

                @property
                def walk_speed(self) -> Path[Float]:
                    return self.nbt.walk_speed
                @walk_speed.setter
                def walk_speed(self, value: float):
                    self.nbt.walk_speed = Float(value)

        class CoordNBT(NBTFormat):
            x: Double
            y: Double
            z: Double

        class RecipeBookNBT(NBTFormat):
            recipes: List[String]
            to_be_displayed: List[String]
            is_filtering_craftable: Byte
            is_gui_open: Byte
            is_furnace_filtering_craftable: Byte
            is_furnace_gui_open: Byte
            is_blasting_furnace_filtering_craftable: Byte
            is_blasting_furnace_gui_open: Byte
            is_smoker_filtering_craftable: Byte
            is_smoker_gui_open: Byte

            class Proxy(NBTFormat.Proxy):
                @property
                def recipes(self) -> Path[List[String]]:
                    return self.nbt.recipes
                @recipes.setter
                def recipes(self, value: List[str]):
                    self.nbt.recipes = List[String](value)

                @property
                def to_be_displayed(self) -> Path[List[String]]:
                    return self.nbt.to_be_displayed
                @to_be_displayed.setter
                def to_be_displayed(self, value: List[str]):
                    self.nbt.to_be_displayed = List[String](value)

                @property
                def is_filtering_craftable(self) -> Path[Byte]:
                    return self.nbt.is_filtering_craftable
                @is_filtering_craftable.setter
                def is_filtering_craftable(self, value: bool):
                    self.nbt.is_filtering_craftable = Byte(value)

                @property
                def is_gui_open(self) -> Path[Byte]:
                    return self.nbt.is_gui_open
                @is_gui_open.setter
                def is_gui_open(self, value: bool):
                    self.nbt.is_gui_open = Byte(value)

                @property
                def is_furnace_filtering_craftable(self) -> Path[Byte]:
                    return self.nbt.is_furnace_filtering_craftable
                @is_furnace_filtering_craftable.setter
                def is_furnace_filtering_craftable(self, value: bool):
                    self.nbt.is_furnace_filtering_craftable = Byte(value)

                @property
                def is_furnace_gui_open(self) -> Path[Byte]:
                    return self.nbt.is_furnace_gui_open
                @is_furnace_gui_open.setter
                def is_furnace_gui_open(self, value: bool):
                    self.nbt.is_furnace_gui_open = Byte(value)

                @property
                def is_blasting_furnace_filtering_craftable(self) -> Path[Byte]:
                    return self.nbt.is_blasting_furnace_filtering_craftable
                @is_blasting_furnace_filtering_craftable.setter
                def is_blasting_furnace_filtering_craftable(self, value: bool):
                    self.nbt.is_blasting_furnace_filtering_craftable = Byte(value)

                @property
                def is_blasting_furnace_gui_open(self) -> Path[Byte]:
                    return self.nbt.is_blasting_furnace_gui_open
                @is_blasting_furnace_gui_open.setter
                def is_blasting_furnace_gui_open(self, value: bool):
                    self.nbt.is_blasting_furnace_gui_open = Byte(value)

                @property
                def is_smoker_filtering_craftable(self) -> Path[Byte]:
                    return self.nbt.is_smoker_filtering_craftable
                @is_smoker_filtering_craftable.setter
                def is_smoker_filtering_craftable(self, value: bool):
                    self.nbt.is_smoker_filtering_craftable = Byte(value)

                @property
                def is_smoker_gui_open(self) -> Path[Byte]:
                    return self.nbt.is_smoker_gui_open
                @is_smoker_gui_open.setter
                def is_smoker_gui_open(self, value: bool):
                    self.nbt.is_smoker_gui_open = Byte(value)

        class RootVehicleNBT(NBTFormat):
            attach: IntArray
            entity: JavaEntity.NBT

            class Proxy(NBTFormat.Proxy):
                @property
                def attach(self) -> Path[IntArray]:
                    return self.nbt.attach
                @attach.setter
                def attach(self, value: UUID):
                    self.nbt.attach = IntArray(value)

                @property
                def entity(self) -> Path[JavaEntity.NBT]:
                    return self.nbt.entity
                @entity.setter
                def entity(self, value: JavaEntity.NBT):
                    self.nbt.entity = value

        class WardenSpawnTrackerNBT(NBTFormat):
            cooldown_ticks: Int
            ticks_since_last_warning: Int
            warning_level: Int

            class Proxy(NBTFormat.Proxy):
                @property
                def cooldown_ticks(self) -> Path[Int]:
                    return self.nbt.cooldown_ticks
                @cooldown_ticks.setter
                def cooldown_ticks(self, value: int):
                    self.nbt.cooldown_ticks = Int(value)

                @property
                def ticks_since_last_warning(self) -> Path[Int]:
                    return self.nbt.ticks_since_last_warning
                @ticks_since_last_warning.setter
                def ticks_since_last_warning(self, value: int):
                    self.nbt.ticks_since_last_warning = Int(value)

                @property
                def warning_level(self) -> Path[Int]:
                    return self.nbt.warning_level
                @warning_level.setter
                def warning_level(self, value: int):
                    self.nbt.warning_level = Int(value)

        class Proxy(JavaMob.NBT.Proxy):
            @property
            def abilities(self) -> Path[JavaPlayer.NBT.AbilitiesNBT]:
                return self.nbt.abilities
            @abilities.setter
            def abilities(self, value: JavaPlayer.NBT.AbilitiesNBT):
                self.nbt.abilities = value

            @property
            def data_version(self) -> Path[Int]:
                return self.nbt.data_version
            @data_version.setter
            def data_version(self, value: int):
                self.nbt.data_version = Int(value)

            @property
            def dimension(self) -> Path[String]:
                return self.nbt.dimension
            @dimension.setter
            def dimension(self, value: str):
                self.nbt.dimension = String(value)

            @property
            def ender_items(self) -> Path[List[SlottedItemNBT]]:
                return self.nbt.ender_items
            @ender_items.setter
            def ender_items(self, value: List[SlottedItemNBT]):
                self.nbt.ender_items = value

            @property
            def entered_nether_position(self) -> Path[JavaPlayer.NBT.CoordNBT]:
                return self.nbt.entered_nether_position
            @property
            def entered_nether_position_x(self) -> Path[Double]:
                return self.nbt.entered_nether_position.x
            @property
            def entered_nether_position_y(self) -> Path[Double]:
                return self.nbt.entered_nether_position.y
            @property
            def entered_nether_position_z(self) -> Path[Double]:
                return self.nbt.enteredNetherPosition.z
            def set_entered_nether_position(self, *,
                                            coord: Coord | None = None,
                                            x: Double | None = None,
                                            y: Double | None = None,
                                            z: Double | None = None):
                if coord is not None:
                    self.nbt.entered_nether_position[0] = coord.x
                    self.nbt.entered_nether_position[1] = coord.y
                    self.nbt.entered_nether_position[2] = coord.z
                else:
                    if x is not None: self.nbt.entered_nether_position.x = x
                    if y is not None: self.nbt.entered_nether_position.y = y
                    if z is not None: self.nbt.entered_nether_position.z = z

            @property
            def food_exhaustion_level(self) -> Path[Float]:
                return self.nbt.food_exhaustion_level
            @food_exhaustion_level.setter
            def food_exhaustion_level(self, value: float):
                self.nbt.food_exhaustion_level = Float(value)

            @property
            def food_level(self) -> Path[Int]:
                return self.nbt.food_level
            @food_level.setter
            def food_level(self, value: int):
                self.nbt.food_level = Int(value)

            @property
            def food_saturation_level(self) -> Path[Float]:
                return self.nbt.food_saturation_level
            @food_saturation_level.setter
            def food_saturation_level(self, value: float):
                self.nbt.food_saturation_level = Float(value)

            @property
            def food_tick_timer(self) -> Path[Int]:
                return self.nbt.food_tick_timer
            @food_tick_timer.setter
            def food_tick_timer(self, value: int):
                self.nbt.food_tick_timer = Int(value)

            @property
            def inventory(self) -> Path[List[ItemNBT]]:
                return self.nbt.inventory
            @inventory.setter
            def inventory(self, value: List[ItemNBT]):
                self.nbt.inventory = value

            @property
            def last_death_location(self) -> Path[JavaPlayer.NBT.CoordNBT]:
                return self.nbt.last_death_location
            @property
            def last_death_location_x(self) -> Path[Double]:
                return self.nbt.last_death_location.x
            @property
            def last_death_location_y(self) -> Path[Double]:
                return self.nbt.last_death_location.y
            @property
            def last_death_location_z(self) -> Path[Double]:
                return self.nbt.last_death_location.z
            def set_last_death_location(self, *,
                                        coord: Coord | None = None,
                                        x: Double | None = None,
                                        y: Double | None = None,
                                        z: Double | None = None):
                if coord is not None:
                    self.nbt.last_death_location.x = coord.x
                    self.nbt.last_death_location.y = coord.y
                    self.nbt.last_death_location.z = coord.z
                else:
                    if x is not None: self.nbt.last_death_location.x = x
                    if y is not None: self.nbt.last_death_location.y = y
                    if z is not None: self.nbt.last_death_location.z = z

            @property
            def player_game_type(self) -> Path[Int]:
                return self.nbt.player_game_type

            @property
            def previous_player_game_type(self) -> Path[Int]:
                return self.nbt.previous_player_game_type

            @property
            def recipe_book(self) -> Path[JavaPlayer.NBT.RecipeBookNBT]:
                return self.nbt.recipe_book
            @recipe_book.setter
            def recipe_book(self, value: JavaPlayer.NBT.RecipeBookNBT):
                self.nbt.recipe_book = value

            @property
            def root_vehicle(self) -> Path[JavaPlayer.NBT.RootVehicleNBT]:
                return self.nbt.root_vehicle
            @root_vehicle.setter
            def root_vehicle(self, value: JavaPlayer.NBT.RootVehicleNBT):
                self.nbt.root_vehicle = value
            @root_vehicle.deleter
            def root_vehicle(self):
                del self.nbt.root_vehicle

            @property
            def score(self) -> Path[Int]:
                return self.nbt.score
            @score.setter
            def score(self, value: int):
                self.nbt.score = Int(value)

            @property
            def seen_credits(self) -> Path[Int]:
                return self.nbt.seen_credits
            @seen_credits.setter
            def seen_credits(self, value: int):
                self.nbt.seen_credits = Int(value)

            @property
            def selected_item(self) -> Path[ItemNBT]:
                return self.nbt.selected_item
            @selected_item.setter
            def selected_item(self, value: ItemNBT):
                self.nbt.selected_item = value

            @property
            def selected_item_slot(self) -> Path[Int]:
                return self.nbt.selected_item_slot
            @selected_item_slot.setter
            def selected_item_slot(self, value: int):
                self.nbt.selected_item_slot = Int(value)

            @property
            def shoulder_entity_left(self) -> Path[JavaEntity.NBT]:
                return self.nbt.shoulder_entity_left
            @shoulder_entity_left.setter
            def shoulder_entity_left(self, value: JavaEntity.NBT):
                self.nbt.shoulder_entity_left = value

            @property
            def shoulder_entity_right(self) -> Path[JavaEntity.NBT]:
                return self.nbt.shoulder_entity_right
            @shoulder_entity_right.setter
            def shoulder_entity_right(self, value: JavaEntity.NBT):
                self.nbt.shoulder_entity_right = value

            @property
            def sleep_timer(self) -> Path[Short]:
                return self.nbt.sleep_timer
            @sleep_timer.setter
            def sleep_timer(self, value: int):
                self.nbt.sleep_timer = Short(value)

            @property
            def spawn_dimension(self) -> Path[String]:
                return self.nbt.spawn_dimension
            @spawn_dimension.setter
            def spawn_dimension(self, value: str):
                self.nbt.spawn_dimension = String(value)

            @property
            def spawn_forced(self) -> Path[Byte]:
                return self.nbt.spawn_forced
            @spawn_forced.setter
            def spawn_forced(self, value: int):
                self.nbt.spawn_forced = Byte(value)

            @property
            def spawn_x(self) -> Path[Int]:
                return self.nbt.spawn_x
            @property
            def spawn_y(self) -> Path[Int]:
                return self.nbt.spawn_y
            @property
            def spawn_z(self) -> Path[Int]:
                return self.nbt.spawn_z
            def set_spawn(self, *,
                          coord: Coord | None = None,
                          x: int | None = None,
                          y: int | None = None,
                          z: int | None = None):
                if coord is not None:
                    self.nbt.spawn_x = Int(coord.x)
                    self.nbt.spawn_y = Int(coord.y)
                    self.nbt.spawn_z = Int(coord.z)
                else:
                    if x is not None: self.nbt.spawn_x = Int(x)
                    if y is not None: self.nbt.spawn_y = Int(y)
                    if z is not None: self.nbt.spawn_z = Int(z)

            @property
            def warden_spawn_tracker(self) -> Path[JavaPlayer.NBT.WardenSpawnTrackerNBT]:
                return self.nbt.warden_spawn_tracker
            @warden_spawn_tracker.setter
            def warden_spawn_tracker(self, value: JavaPlayer.NBT.WardenSpawnTrackerNBT):
                self.nbt.warden_spawn_tracker = value

            @property
            def xp_level(self) -> Path[Int]:
                return self.nbt.xp_level
            @xp_level.setter
            def xp_level(self, value: int):
                self.nbt.xp_level = Int(value)

            @property
            def xp_p(self) -> Path[Float]:
                return self.nbt.xp_p
            @xp_p.setter
            def xp_p(self, value: float):
                self.nbt.xp_p = Float(value)

            @property
            def xp_seed(self) -> Path[Int]:
                return self.nbt.xp_s
            @xp_seed.setter
            def xp_seed(self, value: int):
                self.nbt.xp_s = Int(value)

            @property
            def xp_total(self) -> Path[Int]:
                return self.nbt.xp_total
            @xp_total.setter
            def xp_total(self, value: int):
                self.nbt.xp_total = Int(value)

# TODO logic for all mobs
from __future__ import annotations

from typing import Literal, Any

from pymcfunc import JavaFunctionHandler
from pymcfunc.data_formats.base_formats import NBTFormatPath, NBTFormat
from pymcfunc.data_formats.coord import Rotation
from pymcfunc.data_formats.nbt import String, Short, Byte, IntArray, Int, List, Double, Float, Long
from pymcfunc.data_formats.nbt_formats import PotionEffectNBT, ItemNBT, BrainNBT, AttributeNBT, LeashNBT
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

    def __init__(self, var: Literal['p', 'r', 'a', 'e', 's'],
                 fh: JavaFunctionHandler | None = None,
                 **arguments: Any):
        super().__init__(var, fh, **arguments)
        self.nbt = self.NBT.runtime(fh=fh)

    @property
    def display_name(self) -> NBTFormatPath[String]:
        return self.nbt.custom_name
    @display_name.setter
    def display_name(self, value: str | None):
        if value is None:
            self.nbt.custom_name = String("")
            self.nbt.custom_name_visible = 0
        else:
            self.nbt.custom_name = String(value)
            self.nbt.custom_name_visible = 1

    @property
    def pitch(self) -> NBTFormatPath[Float]:
        return self.nbt.rotation[0]
    @pitch.setter
    def pitch(self, value: float):
        self.nbt.rotation[0] = Float(value)

    @property
    def yaw(self) -> NBTFormatPath[Float]:
        return self.nbt.rotation[1]
    @yaw.setter
    def yaw(self, value: float):
        self.nbt.rotation[1] = Float(value)

    def set_rotation(self, rotation: Rotation):
        self.pitch = rotation.pitch
        self.yaw = rotation.yaw

    def force(self, *,
              x: float | None = None,
              y: float | None = None,
              z: float | None = None):
        if x is not None:
            self.nbt.motion[0] = Double(x)
        if y is not None:
            self.nbt.motion[1] = Double(y)
        if z is not None:
            self.nbt.motion[2] = Double(z)


class JavaMob(JavaEntity):
    class NBT(JavaEntity.NBT):
        absorption_amount: Float
        active_effects: List[PotionEffectNBT] | None
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
        Leash: LeashNBT
        left_handed: Byte
        no_ai: Byte
        persistence_required: Byte
        sleeping_x: Int
        sleeping_y: Int
        sleeping_z: Int
        team: String

class JavaBreedableMob(JavaMob):
    class NBT(JavaMob.NBT):
        age: Int
        forced_age: Int
        in_love: Int
        love_cause: IntArray

class JavaAngerableMob(JavaMob):
    class NBT(JavaMob.NBT):
        anger_time: Int
        angry_at: IntArray

class JavaTameableMob(JavaMob):
    class NBT(JavaMob.NBT):
        owner: IntArray
        sitting: Byte

class JavaZombieMob(JavaMob):
    class NBT(JavaMob.NBT):
        can_break_doors: Byte
        drowned_conversion_time: Int
        in_water_time: Int
        is_baby: Byte | None

class JavaRaidMob(JavaMob):
    class NBT(JavaMob.NBT):
        can_join_raid: Byte
        patrol_leader: Byte
        patrolling: Byte
        PatrolTarget: CoordNBT
        raid_id: Int
        wave: Int

        class CoordNBT(NBTFormat):
            x: Int
            y: Int
            z: Int

class JavaProjectile(JavaEntity):
    pass

class JavaPotionEffects(JavaEntity):
    pass

class JavaMinecart(JavaEntity):
    pass

class JavaContainer(JavaEntity):
    pass

class JavaHangable(JavaEntity):
    pass

class JavaFireball(JavaEntity):
    pass

class JavaPlayer(JavaMob):
    pass
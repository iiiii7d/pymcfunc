from __future__ import annotations

from typing import Literal, Any

from pymcfunc import JavaFunctionHandler
from pymcfunc.data_formats.base_formats import NBTFormat
from pymcfunc.data_formats.coord import Rotation
from pymcfunc.data_formats.nbt_path import Path
from pymcfunc.data_formats.nbt_tags import String, Short, Byte, IntArray, Int, List, Double, Float, Long, Compound
from pymcfunc.data_formats.nbt_formats import HideablePotionEffectNBT, ItemNBT, BrainNBT, AttributeNBT, LeashNBT, \
    PotionEffectNBT, SlottedItemNBT, LocationNBT
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
        self.nbt = self.NBT.as_path(fh=fh)

    @property
    def display_name(self) -> Path[String]:
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
    def pitch(self) -> Path[Float]:
        return self.nbt.rotation[0]
    @pitch.setter
    def pitch(self, value: float):
        self.nbt.rotation[0] = Float(value)

    @property
    def yaw(self) -> Path[Float]:
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
    class NBT(JavaEntity.NBT):
        has_been_shot: Byte
        left_owner: Byte
        owner: IntArray


class JavaPotionEffects(JavaEntity):
    class NBT(JavaEntity.NBT):
        custom_potion_effects: List[PotionEffectNBT]
        potion: String
        custom_potion_color: Int

class JavaMinecart(JavaEntity):
    class NBT(JavaEntity.NBT):
        custom_display_tile: Byte
        display_offset: Int
        display_state: DisplayStateNBT

        class DisplayStateNBT(NBTFormat):
            name: String
            properties: Compound

class JavaContainer(JavaEntity):
    class NBT(JavaEntity.NBT):
        items: List[ItemNBT]
        loot_table: String
        loot_table_seed: Long

class JavaHangable(JavaEntity):
    class NBT(JavaEntity.NBT):
        facing: Byte
        tile_x: Float
        tile_y: Float
        tile_z: Float

class JavaFireball(JavaEntity):
    class NBT(JavaEntity.NBT):
        power: List[Double]

class JavaArrowGroup(JavaEntity): # TODO fix case
    class NBT(JavaEntity.NBT):
        crit: Byte
        damage: Double
        in_block_state: BlockStateNBT
        in_ground: Byte
        life: Short
        pickup: Byte
        pierce_level: Byte
        shake: Byte
        shot_from_crossbow: Byte
        sound_event: String

        class BlockStateNBT(NBTFormat):
            name: String
            properties: Compound

class JavaPlayer(JavaMob):
    class NBT(JavaMob.NBT):
        abilities: AbilitiesNBT
        data_version: Int
        dimension: String
        ender_items: List[SlottedItemNBT]
        enteredNetherPosition: CoordNBT
        food_exhaustion_level: Float
        food_level: Int
        food_saturation_level: Float
        food_tick_timer: Int
        inventory: List[SlottedItemNBT]
        last_death_location: LocationNBT
        player_game_type: Int
        previous_player_game_type: Int
        recipe_book: RecipeBookNBT
        root_vehicle: RootVehicleNBT
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
        xp_p: float
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

        class RootVehicleNBT(NBTFormat):
            attach: IntArray
            entity: JavaEntity.NBT

        class WardenSpawnTrackerNBT(NBTFormat):
            cooldown_ticks: Int
            ticks_since_last_warning: Int
            warning_level: Int
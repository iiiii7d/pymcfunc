from __future__ import annotations

from typing import Literal, Any
from uuid import UUID

from pymcfunc import JavaFunctionHandler
from pymcfunc.data_formats.coord import Rotation, Coord
from pymcfunc.data_formats.nbt_path import Path, NamedTag
from pymcfunc.data_formats.nbt_tags import String, Short, Byte, IntArray, Int, List, Double, Float
from pymcfunc.proxies.selectors import JavaSelector


class JavaEntity(JavaSelector):
    def __init_subclass__(cls, type_: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if type_ is not None:
            def __init__(self, var: Literal['p', 'r', 'a', 'e', 's'],
                         fh: JavaFunctionHandler | None = None,
                         **arguments: Any):
                if ('type_' in arguments and 'type_' not in arguments['type_']) or 'type_' not in arguments:
                    JavaEntity.__init__(self, var, fh, **arguments, type_=type_)
                else:
                    JavaEntity.__init__(self, var, fh, **arguments)
            cls.__init__ = __init__

    @property
    def air(self) -> Path[Short]:
        return NamedTag[Short]("Air")

    @air.setter
    def air(self, value: int):
        self.modify_nbt(self.air, "set", value=Short(value))

    @property
    def custom_name(self) -> Path[String]:
        return NamedTag[String]("CustomName")

    @custom_name.setter
    def custom_name(self, value: str | None):
        self.modify_nbt(self.custom_name, "set", value=String(value or ""))

    @property
    def custom_name_visible(self) -> Path[Byte]:
        return NamedTag[Byte]("custom_name_visible")

    @custom_name_visible.setter
    def custom_name_visible(self, value: bool):
        self.modify_nbt(self.custom_name_visible, "set", value=Byte(int(value)))

    @custom_name_visible.deleter
    def custom_name_visible(self):
        del self.nbt.custom_name_visible

    @property
    def fall_distance(self) -> Path[Float]:
        return NamedTag[Float]("fall_distance")

    @fall_distance.setter
    def fall_distance(self, value: float):
        self.modify_nbt(self.fall_distance, "set", value=Float(value))

    @property
    def fire(self) -> Path[Short]:
        return NamedTag[Short]("fire")

    @fire.setter
    def fire(self, value: int):
        self.modify_nbt(self.fire, "set", value=Short(value))

    @property
    def glowing(self) -> Path[Byte]:
        return NamedTag[Byte]("glowing")

    @glowing.setter
    def glowing(self, value: bool):
        self.modify_nbt(self.glowing, "set", value=Byte(int(value)))

    @property
    def has_visual_fire(self) -> Path[Byte]:
        return NamedTag[Byte]("has_visual_fire")

    @has_visual_fire.setter
    def has_visual_fire(self, value: bool):
        self.modify_nbt(self.has_visual_fire, "set", value=Byte(int(value)))

    @property
    def id(self) -> Path[String]:
        return NamedTag[String]("id")

    @id.setter
    def id(self, value: str):
        self.modify_nbt(self.id, "set", value=String(value))

    @property
    def invulnerable(self) -> Path[Byte]:
        return NamedTag[Byte]("invulnerable")

    @invulnerable.setter
    def invulnerable(self, value: bool):
        self.modify_nbt(self.invulnerable, "set", value=Byte(int(value)))

    @property
    def motion(self) -> Path[List[Double]]:
        return NamedTag[List[Double]]("motion")

    @property
    def motion_x(self) -> Path[Double]:
        return NamedTag[Double]("motion_x")

    @property
    def motion_y(self) -> Path[Double]:
        return NamedTag[Double]("motion_y")

    @property
    def motion_z(self) -> Path[Double]:
        return NamedTag[Double]("motion_z")

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
        return NamedTag[Byte]("no_gravity")

    @no_gravity.setter
    def no_gravity(self, value: bool):
        self.modify_nbt(self.no_gravity, "set", value=Byte(int(value)))

    @property
    def passengers(self) -> Path[List[JavaEntity.NBT]]:
        return NamedTag[List[JavaEntity.NBT]]("passengers")

    @passengers.setter
    def passengers(self, value: list[JavaEntity.NBT]):
        self.modify_nbt(self.passengers, "set", value=List[JavaEntity.NBT](value))

    @property
    def portal_cooldown(self) -> Path[Int]:
        return NamedTag[Int]("portal_cooldown")

    @portal_cooldown.setter
    def portal_cooldown(self, value: float):
        self.modify_nbt(self.portal_cooldown, "set", value=Int(value))

    @property
    def pos(self) -> Path[List[Double]]:
        return NamedTag[List[Double]]("pos")

    @property
    def pos_x(self) -> Path[Double]:
        return NamedTag[Double]("pos_x")

    @property
    def pos_y(self) -> Path[Double]:
        return NamedTag[Double]("pos_y")

    @property
    def pos_z(self) -> Path[Double]:
        return NamedTag[Double]("pos_z")

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
        return NamedTag[List[Float]]("rotation")

    @property
    def pitch(self) -> Path[Float]:
        return NamedTag[Float]("pitch")

    @property
    def yaw(self) -> Path[Float]:
        return NamedTag[Float]("yaw")

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
        return NamedTag[Byte]("silent")

    @silent.setter
    def silent(self, value: bool):
        self.modify_nbt(self.silent, "set", value=Byte(int(value)))

    @silent.deleter
    def silent(self):
        del self.nbt.silent

    @property
    def tags(self) -> Path[List[String]]:
        return NamedTag[List[String]]("tags")

    @tags.setter
    def tags(self, value: list[str]):
        self.modify_nbt(self.tags, "set", value=List[String](value))

    @property
    def ticks_frozen(self) -> Path[Int]:
        return NamedTag[Int]("ticks_frozen")

    @ticks_frozen.setter
    def ticks_frozen(self, value: float):
        self.modify_nbt(self.ticks_frozen, "set", value=Int(value))

    @property
    def uuid(self) -> Path[IntArray]:
        return NamedTag[IntArray]("uuid")

    @uuid.setter
    def uuid(self, value: UUID):
        self.modify_nbt(self.uuid, "set", value=IntArray(value))  # TODO see if this works
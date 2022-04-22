from __future__ import annotations

from typing import Literal, Any

from pymcfunc import JavaFunctionHandler
from pymcfunc.data_formats.base_formats import NBTFormatPath, RuntimeNBTFormat
from pymcfunc.data_formats.coord import Rotation
from pymcfunc.data_formats.nbt import String, Short, Byte, IntArray, Int, List, Double, Float
from pymcfunc.proxies.selectors import JavaSelector


class JavaEntity(JavaSelector):
    class NBT(RuntimeNBTFormat):
        NBT_FORMAT = property(lambda self: {
            "air": Short,
            "custom_name": String,
            "custom_name_visible": Byte,
            "fall_distance": Float,
            "fire": Short,
            "glowing": Byte,
            "has_visual_fire": Byte,
            "id": String,
            "invulnerable": Byte,
            "motion": List[Double],
            "no_gravity": Byte,
            "on_ground": Byte,
            "passengers": List[JavaEntity.NBT],
            "portal_cooldown": Int,
            "pos": List[Double],
            "rotation": List[Float],
            "silent": Byte,
            "tags": List[String],
            "ticks_frozen": Int,
            "uuid": IntArray,
        }) # TODO stub file

    def __init__(self, var: Literal['p', 'r', 'a', 'e', 's'],
                 fh: JavaFunctionHandler | None = None,
                 **arguments: Any):
        super().__init__(var, fh, **arguments)
        self.nbt = self.NBT(fh=fh)

    @property
    def display_name(self) -> NBTFormatPath[String]:
        return self.nbt.custom_name
    @display_name.setter
    def display_name(self, value: str | None):
        if value is None:
            self.nbt.custom_name = ""
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
    pass

class JavaBreedableMob(JavaMob):
    pass

class JavaAngerableMob(JavaMob):
    pass

class JavaTameableMob(JavaMob):
    pass

class JavaProjectile(JavaEntity):
    pass

class JavaPotionEffect(JavaEntity):
    pass

class JavaMinecart(JavaEntity):
    pass
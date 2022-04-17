import pymcfunc.internal as internal
from random import randint
from typing import Any, Optional

class Entity:
    """An entity object. This will reference and control entities that match a selector.
    More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity"""

    def __init__(self, fh, target: str):
        """Initialises the entity.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.__init__"""
        self.fh = fh
        self.target = target

    def display_name(self, name: str):
        """Sets the display name of the entities.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.display_name"""
        if name is None:
            self.fh.r.data_modify('set', 'value', 'CustomName',
                                  entity=self.target, value='')
            self.fh.r.data_modify('set', 'value', 'CustomNameVisible',
                                  entity=self.target, value=0)
        else:
            self.fh.r.data_modify('set', 'value', 'CustomName',
                                  entity=self.target, value=name)
            self.fh.r.data_modify('set', 'value', 'CustomNameVisible',
                                  entity=self.target, value=1)

    def data_set_value(self, attr: str, val: Any):
        """Sets an NBTTag data value.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.data_set_value"""
        self.fh.r.data_modify('set', 'value', attr,
                              entity=self.target, value=val)

    def pitch(self, val: float):
        """Rotates the entity, such that it is rotating vertically.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.pitch"""
        self.fh.r.data_modify('insert', 'value', 'Rotation', index=1,
                              entity=self.target, value=val)

    def yaw(self, val: float):
        """Rotates the entity, such that it is rotating horizontally.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.yaw"""
        self.fh.r.data_modify('insert', 'value', 'Rotation', index=0,
                              entity=self.target, value=val)

    def move(self, destxyz: Optional[str]=None, destentity: Optional[str]=None, **kwargs):
        """Moves the entity.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.move"""
        self.fh.r.tp(destxyz=destxyz, destentity=destentity, target=self.target, **kwargs)
    
    def force(self, axis: str, velocity: float):
        """Apply force to the entity.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.force"""
        index = ['x', 'y', 'z']
        internal.options(axis, index)
        self.fh.r.data_modify('insert', 'value', 'Motion', index=index.index(axis),
                              entity=self.target, value=velocity)
    
    def remove(self):
        """Removes the entity.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Entity.remove"""
        self.fh.r.kill(self.target)


class Mob(Entity):
    """A special type of entity, for mobs.
    More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Mob"""

    def set_armour_slot(self, slot: str, item_id: str, count: int=1, tag: Optional[dict]=None):
        """Sets the armour slot of the mob.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Mob.set_armour_slot"""
        index = ['feet', 'legs', 'chest', 'head']
        internal.options(slot, index)
        data = {
            'id': item_id,
            'Count': count,
        }
        if tag is not None:
            data['tag'] = tag
        self.fh.r.data_modify('insert', 'value', f'ArmorItems', index=index.index(slot),
                              entity=self.target, value=data)
    
    def remove_armour_slot(self, slot: str):
        """Removes armour from an armour slot.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.Mob.remove_armour_slot"""
        index = ['feet', 'legs', 'chest', 'head']
        internal.options(slot, index)
        self.fh.r.data_remove(f'ArmorItems[{index.index(slot)}]', entity=self.target)


class ArmourStand(Mob):
    """A special type of entity, for armour stands.
    More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.ArmourStand"""

    def move_limb(self, limb: str, axis: str, val: float):
        """Moves a limb or part of the armour stand.
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.ArmourStand.move_limb"""
        limb_index = ['Body', 'Head', 'LeftArm', 'LeftLeg', 'RightArm', 'RightLeg']
        internal.options(limb, limb_index)
        axis_index = ['x', 'y', 'z']
        internal.options(axis, axis_index)
        self.fh.r.data_modify('insert', 'value', f'Pose.{limb}', index=axis_index.index(axis),
                              entity=self.target, value=val)

    def mess(self):
        """Sets each value of rotation of each limb to a random value, because why not :))
        More info: https://pymcfunc.readthedocs.io/en/latest/reference.html#pymcfunc.ent.ArmourStand.mess"""
        for limb in ['Body', 'Head', 'LeftArm', 'LeftLeg', 'RightArm', 'RightLeg']:
            for axis in ['x', 'y', 'z']:
                self.move_limb(limb, axis, randint(-180, 180))
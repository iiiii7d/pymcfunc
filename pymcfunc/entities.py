from typing import Sequence, Union
from pymcfunc.func_handlers import JavaFuncHandler
import pymcfunc.internal as internal
from random import randint

class Entity:
    def __init__(self, fh: JavaFuncHandler, target: str, tag: str):
        self.fh = fh
        self.tag = tag
        fh.r.tag(target, 'add', name=tag)

    def display_name(self, name: str):
        if name is None:
            self.fh.r.data_modify('set', 'value', 'CustomName',
                                  entity=self.fh.sel.e(tag=self.tag), value='')
            self.fh.r.data_modify('set', 'value', 'CustomNameVisible',
                                  entity=self.fh.sel.e(tag=self.tag), value=0)
        else:
            self.fh.r.data_modify('set', 'value', 'CustomName',
                                  entity=self.fh.sel.e(tag=self.tag), value=name)
            self.fh.r.data_modify('set', 'value', 'CustomNameVisible',
                                  entity=self.fh.sel.e(tag=self.tag), value=1)

    def data_set_value(self, attr: str, val):
        self.fh.r.data_modify('set', 'value', attr,
                              entity=self.fh.sel.e(tag=self.tag), value=val)

    def pitch(self, val: float):
        self.fh.r.data_modify('insert', 'value', 'Rotation', index=1,
                              entity=self.fh.sel.e(tag=self.tag), value=val)

    def yaw(self, val: float):
        self.fh.r.data_modify('insert', 'value', 'Rotation', index=0,
                              entity=self.fh.sel.e(tag=self.tag), value=val)

    def move(self, destxyz: str=None, destentity: str=None, **kwargs):
        self.fh.r.tp(destxyz=destxyz, destentity=destentity, target=self.fh.sel.e(tag=self.tag), **kwargs)
    
    def force(self, axis: str, velocity: float):
        index = ['x', 'y', 'z']
        internal.options('axis', index)
        self.fh.r.data_modify('insert', 'value', 'Motion', index=index.index(axis),
                              entity=self.fh.sel.e(tag=self.tag), value=velocity)
    
    def remove(self):
        self.fh.r.kill(self.fh.sel.e(tag=self.tag))


class Mob(Entity):
    def set_armour_slot(self, slot: str, itemId: str, count: int=1, tag: dict=None):
        index = ['feet', 'legs', 'chest', 'head']
        internal.options('slot', index)
        data = {
            'id': itemId,
            'Count': count,
        }
        if tag is not None:
            data['tag'] = tag
        self.fh.r.data_modify('insert', 'value', f'ArmorItems', index=index.index(slot),
                              entity=self.fh.sel.e(tag=self.tag), value=data)
    
    def remove_armour_slot(self, slot: str):
        index = ['feet', 'legs', 'chest', 'head']
        internal.options('slot', index)
        self.fh.r.data_remove(f'ArmorItems[{index.index(slot)}]')


class ArmourStand(Mob):
    def move_limb(self, limb: str, axis: str, val: float):
        limb_index = ['Body', 'Head', 'LeftArm', 'LeftLeg', 'RightArm', 'RightLeg']
        internal.options('slot', limb_index)
        axis_index = ['x', 'y', 'z']
        internal.options('axis', axis_index)
        self.fh.r.data_modify('insert', 'value', f'Pose.{limb}', index=axis_index.index(axis),
                              entity=self.fh.sel.e(tag=self.tag), value=val)

    def mess(self):
        for limb in ['Body', 'Head', 'LeftArm', 'LeftLeg', 'RightArm', 'RightLeg']:
            for axis in ['x', 'y', 'z']:
                self.move_limb(limb, axis, randint(-180, 180))


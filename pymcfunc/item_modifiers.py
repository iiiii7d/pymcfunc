from typing import Literal

from attr import define, field

from pymcfunc.internal import base_class
from pymcfunc.nbt import NBTFormat, List, String

Predicate = str
@define(init=True)
@base_class
class ItemModifier(NBTFormat):
    function: str = field(init=False)
    conditions: list[Predicate]

    NBT_FORMAT = {
        'function': String,
        'conditions': List[Predicate]
    }

@define(init=True)
class ApplyBonusItemModifier(ItemModifier):
    enchantment: str
    formula: Literal['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops']
    # TODO more
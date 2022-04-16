from __future__ import annotations

from typing import Union, Literal, Optional

from attr import define, field

from pymcfunc.internal import base_class
from pymcfunc.nbt import NBTFormat, String, Int, Float


@define(init=True, frozen=True)
class NumberProvider(NBTFormat):
    type: str = field(init=False)

    NBT_FORMAT = {
        'type': String,
    }

@define(init=True, frozen=True)
class ConstantNumberProvider(NumberProvider):
    value: int | float

    NBT_FORMAT = {
        **NumberProvider.NBT_FORMAT,
        'value': Union[Int, Float],
    }

@define(init=True, frozen=True)
class UniformNumberProvider(NumberProvider):
    min: int | float | NumberProvider
    max: int | float | NumberProvider

    NBT_FORMAT = {
        **NumberProvider.NBT_FORMAT,
        'min': Union[Int, Float, NumberProvider],
        'max': Union[Int, Float, NumberProvider],
    }

@define(init=True, frozen=True)
class BinomialNumberProvider(NumberProvider):
    n: int | NumberProvider
    p: float | NumberProvider

    NBT_FORMAT = {
        **NumberProvider.NBT_FORMAT,
        'n': Union[Int, NumberProvider],
        'p': Union[Float, NumberProvider],
    }

@define(init=True, frozen=True)
class ScoreNumberProvider(NumberProvider):
    target: Target
    score: str
    scale: float | None = None

    @define(init=True, frozen=True)
    @base_class
    class Target(NBTFormat):
        type: Literal['fixed', 'context']

        NBT_FORMAT = {
            'type': String,
        }
    @define(init=True, frozen=True)
    class FixedTarget(Target):
        name: str

        NBT_FORMAT = {
            'type': String,
            'name': String,
        }

    @define(init=True, frozen=True)
    class ContextTarget(Target):
        target: Literal['this', 'killer', 'direct_killer', 'player_killer']

        NBT_FORMAT = {
            'type': String,
            'target': String,
        }

    NBT_FORMAT = {
        **NumberProvider.NBT_FORMAT,
        'target': Target,
        'score': String,
        'scale': Optional[Float],
    }
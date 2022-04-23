from __future__ import annotations

from typing import Union, Literal, Optional

from attr import field, define

from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.internal import base_class


@define(kw_only=True, init=True, frozen=True)
@base_class
class NumberProvider(JsonFormat):
    type: str = field(init=False)

    JSON_FORMAT = {
        'type': str,
    }

@define(kw_only=True, init=True, frozen=True)
class ConstantNumberProvider(NumberProvider):
    value: int | float

    JSON_FORMAT = {
        **NumberProvider.JSON_FORMAT,
        'value': Union[int, float],
    }

@define(kw_only=True, init=True, frozen=True)
class UniformNumberProvider(NumberProvider):
    min: int | float | NumberProvider
    max: int | float | NumberProvider

    JSON_FORMAT = {
        **NumberProvider.JSON_FORMAT,
        'min': Union[int, float, NumberProvider],
        'max': Union[int, float, NumberProvider],
    }

@define(kw_only=True, init=True, frozen=True)
class BinomialNumberProvider(NumberProvider):
    n: int | NumberProvider
    p: float | NumberProvider

    JSON_FORMAT = {
        **NumberProvider.JSON_FORMAT,
        'n': Union[int, NumberProvider],
        'p': Union[float, NumberProvider],
    }

@define(kw_only=True, init=True, frozen=True)
class ScoreNumberProvider(NumberProvider):
    target: Target
    score: str
    scale: float | None = None

    @define(kw_only=True, init=True, frozen=True)
    @base_class
    class Target(JsonFormat):
        type: Literal['fixed', 'context']

        JSON_FORMAT = {
            'type': str,
        }
    @define(kw_only=True, init=True, frozen=True)
    class FixedTarget(Target):
        name: str

        JSON_FORMAT = {
            'type': str,
            'name': str,
        }

    @define(kw_only=True, init=True, frozen=True)
    class ContextTarget(Target):
        target: Literal['this', 'killer', 'direct_killer', 'player_killer']

        JSON_FORMAT = {
            'type': str,
            'target': str,
        }

    JSON_FORMAT = {
        **NumberProvider.JSON_FORMAT,
        'target': Target,
        'score': str,
        'scale': Optional[float],
    }
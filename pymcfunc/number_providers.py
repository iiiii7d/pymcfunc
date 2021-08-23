from typing import Union, Optional
import pymcfunc.internal as internal
NumberProvider = dict

def constant(value: Union[int, float]) -> NumberProvider:
    """A number provider that returns a constant.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.np.constant"""
    return {
        "type": "constant",
        "value": value
    }

def uniform(min_: Union[Union[int, float], NumberProvider], max_: Union[Union[int, float], NumberProvider]) -> NumberProvider:
    """A number provider that returns a random number between two numbers.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.np.uniform"""
    return {
        "type": "uniform",
        "min": min_,
        "max": max_
    }

def binomial(n: Union[int, NumberProvider], p: Union[float, NumberProvider]):
    """A number provider that returns a constant.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.np.constant"""
    return {
        "type": "binomial",
        "n": n,
        "p": p
    }

def score(score_: str, target: Optional[str]=None, type_: Optional[str]=None, name: Optional[str]=None, scale: Optional[float]=None) -> NumberProvider:
    """A number provider that returns a value from the scoreboard.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.np.constant"""
    np = {"type": "score", "score": score_}
    internal.check_invalid_params('fixed', 'type', type_,
        ('name', name, None),
        dep_mandatory=True)
    internal.pick_one_arg(
        (name, None, 'name'),
        (target, None, 'target'),
        optional=False
    )
    if target is not None: internal.options(target, ['this', 'killer', 'direct_killer', 'player_killer'])
    if type_ is None: np['target'] = target
    else:
        internal.options(type_, ['fixed', 'context'])
        np['target'] = {}
        np['target']['type'] = type_
        if target is not None: np['target']['target'] = target
        else: np['target']['name'] = name
    if scale is not None: np['scale'] = scale
    return np

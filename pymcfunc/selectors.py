from math import inf
import json
from typing import Sequence, Dict
import re

import pymcfunc.internal as internal
import pymcfunc.errors as errors

class UniversalSelector:
    """The universal selector class.
       Every function has a **kwargs, which is used for selector arguments. The list of selector arguemnts are in the respective specialised classes.
       If an argument is repeatable, you can express multiple values of the same argument in lists, sets, or tuples.
       More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalSelectors"""

    @classmethod
    def select(cls, var: str, **kwargs):
        """Returns a selector, given the selector variable and optional arguments.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalSelectors.select"""
        internal.options(var, ['p', 'r', 'a', 'e', 's'])
        return "@"+var+cls._sel_args(cls, **kwargs)

    @classmethod
    def nearest_player(cls, **kwargs):
        """Alias of select('p', **kwargs)."""
        return cls.select('p', **kwargs)
    p = nearest_player

    @classmethod
    def random_player(cls, **kwargs):
        """Alias of select('r', **kwargs)."""
        return cls.select('p', **kwargs)
    r = random_player

    @classmethod
    def all_players(cls, **kwargs):
        """Alias of select('a', **kwargs)."""
        return cls.select('a', **kwargs)
    a = all_players

    @classmethod
    def all_entities(cls, **kwargs):
        """Alias of select('e', **kwargs)."""
        return cls.select('e', **kwargs)
    e = all_entities

    @classmethod
    def executor(cls, **kwargs):
        """Alias of select('s', **kwargs)."""
        return cls.select('s', **kwargs)
    s = executor

    @staticmethod
    def _sel_args(cls, **kwargs) -> str:
        args = []
        BEDROCK = ["x", "y", "z", "rmax", "rmin", "dx", "dy", "dz", "scores", "tag",
                   "c", "lmax", "lmin", "m", "name", "rxmax", "rxmin", "rymax", "rymin", "type", "family",
                   "l", "r", "rx", "ry"]
        JAVA = ["x", "y", "z", "distance", "dx", "dy", "dz", "scores", "tag",
                "team", "limit", "sort", "level", "gamemode", "name", "x_rotation", "y_rotation",
                "type", "nbt", "advancements", "predicate"]
        CAN_REPEAT = ["type", "family", "tag", "nbt", "advancements", "predicate"]
        OPTIONS_JAVA = {
            "sort": ["nearest", "furthest", "random", "arbitrary"],
            "gamemode": ["spectator", "adventure", "creative", "survival"]
        }
        OPTIONS_BEDROCK = {
            "gamemode": ["0", "1", "2", "3"]
        }
        ALIASES = {
            "lmax": "l",
            "lmin": "lm",
            "rmax": "r",
            "rmin": "rm",
            "rxmax": "rx",
            "rxmin": "rxm",
            "rymax": "ry",
            "rymin": "rym"
        }
        EXPAND = {
            "l": ("l", "lm"),
            "r": ("r", "rm"),
            "rx": ("rx", "rxm"),
            "ry": ("ry", "rym")
        }

        for k, v in kwargs.items():
            keylist = BEDROCK if type(cls) == BedrockSelector else JAVA
            optionslist = OPTIONS_BEDROCK if type(cls) == BedrockSelector else OPTIONS_JAVA
            if k not in keylist:
                raise KeyError(f"Invalid target selector argument '{k}'")
            if k in optionslist.keys():
                if not str(v) in optionslist[k]:
                    raise errors.OptionError(optionslist[k], v)
            if k in ALIASES and type(cls) == BedrockSelector:
                args.append(f"{ALIASES[k]}={v}")
            elif k in EXPAND and type(cls) == BedrockSelector:
                for i in EXPAND[k]:
                    v = json.dumps(v) if isinstance(v, dict) else v
                    args.append(f"{i}={v}")
            elif k in CAN_REPEAT and isinstance(v, (tuple, list, set)):
                for i in v:
                    i = json.dumps(i) if isinstance(i, dict) else i
                    args.append(f"{k}={i}")
            else:
                v = json.dumps(v) if isinstance(v, dict) else v
                args.append(f"{k}={v}")
        result = "["+", ".join(args)+"]"
        if result == "[]": result = ""
        return result


class BedrockSelector(UniversalSelector):
    """The Bedrock Edition selector class.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockSelectors"""
    def __init__(self):
        pass


class JavaSelector(UniversalSelector):
    """The Java Edition selector class.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaSelectors"""
    def __init__(self):
        pass

    @staticmethod
    def range(minv: int=0, maxv: int=inf) -> str:
        """Returns a range of values, as it is represented in Minecraft commands.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaSelectors.range"""
        if minv > maxv:
            raise ValueError(f"{maxv} is greater than {minv}")
        if minv == 0:
            minv = ""
        if maxv == inf:
            maxv = ""
        result = str(minv)+".."+str(maxv)
        if result == "..":
            raise ValueError(f"Invalid range")
        return result

def cuboid(pos1: Sequence[int], pos2: Sequence[int], dims: str='xyz') -> Dict[str, int]:
    """Finds the northwest-bottommost corner and the volume/area/length of a cuboid, area or line, given two corners.
    This function is mainly for selector arguments, namely x, y, z, dx, dy and dz.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.sel.cuboid"""
    if len(pos1) != len(pos2):
        raise ValueError("Uneven no. of dimensions")
    elif len(pos1) != len(dims) or len(pos2) != len(dims):
        raise ValueError(f"Expected {len(dims)} dimensions, got {len(pos1)} and {len(pos2)}")
    elif not re.search(r"^(?!.*(.).*\1)[xyz]+$", dims):
        raise ValueError(f"Axes are invalid (Got '{dims}')")
    out = {}
    for dim, v1, v2 in zip(dims, pos1, pos2):
        minv = min(v1, v2)
        d = max(v1, v2) - minv
        out[dim] = minv
        out['d'+dim] = d
    return out

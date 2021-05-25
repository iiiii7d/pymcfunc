from math import inf
import json

import pymcfunc.internal as internal
import pymcfunc.errors as errors

class UniversalSelectors:
    """The universal selector class.
       Every function has a **kwargs, which is used for selector arguments. The list of selector arguemnts are in the respective specialised classes.
       If an argument is repeatable, you can express multiple values of the same argument in lists, sets, or tuples.
       More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalSelectors"""
    def select(self, var: str, **kwargs):
        """Returns a selector, given the selector variable and optional arguments.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalSelectors.select"""
        internal.options(var, ['p','r','a','e','s'])
        return "@"+var+self._sel_args(**kwargs)

    def nearest_player(self, **kwargs):
        """Alias of select('p', **kwargs)."""
        return self.select('p', **kwargs)
    p = nearest_player
    
    def random_player(self, **kwargs):
        """Alias of select('r', **kwargs)."""
        return self.select('p', **kwargs)
    r = random_player

    def all_players(self, **kwargs):
        """Alias of select('a', **kwargs)."""
        return self.select('a', **kwargs)
    a = all_players

    def all_entities(self, **kwargs):
        """Alias of select('e', **kwargs)."""
        return self.select('e', **kwargs)
    e = all_entities

    def executor(self, **kwargs):
        """Alias of select('s', **kwargs)."""
        return self.select('s', **kwargs)
    s = executor

    def _sel_args(self, **kwargs):
        args = []
        BEDROCK = ["x","y","z","rmax","rmin","dx","dy","dz","scores","tag",
                   "c","lmax","lmin","m","name","rxmax","rxmin","rymax","rymin","type","family",
                   "l", "r", "rx", "ry"]
        JAVA = ["x","y","z","distance","dx","dy","dz","scores","tag",
                "team","limit","sort","level","gamemode","name","x_rotation","y_rotation",
                "type","nbt","advancements","predicate"]
        CAN_REPEAT = ["type","family","tag","nbt","advancements","predicate"]
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
            keylist = BEDROCK if type(self) == BedrockSelectors else JAVA
            optionslist = OPTIONS_BEDROCK if type(self) == BedrockSelectors else OPTIONS_JAVA
            if not k in keylist:
                raise KeyError(f"Invalid target selector argument '{k}'")
            if k in optionslist.keys():
                if not str(v) in optionslist[k]:
                    raise errors.OptionError(optionslist[k], v)
            if k in ALIASES and type(self) == BedrockSelectors:
                args.append(f"{ALIASES[k]}={v}")
            elif k in EXPAND and type(self) == BedrockSelectors:
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
        result = "["+",".join(args)+"]"
        if result == "[]": result = ""
        return result


class BedrockSelectors(UniversalSelectors):
    """The Bedrock Edition selector class.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockSelectors"""
    def __init__(self):
        pass


class JavaSelectors(UniversalSelectors):
    """The Java Edition selector class.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaSelectors"""
    def __init__(self):
        pass

    def range(self, minv: int=0, maxv: int=inf):
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
        

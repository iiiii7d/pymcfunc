import pymcfunc.internal as internal
import pymcfunc.errors as errors
from math import inf

class UniversalSelectors:
    def select(self, var: str, **kwargs):
        internal.options(var, ['p','r','a','e','s'])
        return "@"+var+self._sel_args(**kwargs)

    def nearest_player(self, **kwargs):
        return self.select('p', **kwargs)
    p = nearest_player
    
    def random_player(self, **kwargs):
        return self.select('p', **kwargs)
    r = random_player

    def all_players(self, **kwargs):
        return self.select('a', **kwargs)
    a = all_players

    def all_entities(self, **kwargs):
        return self.select('e', **kwargs)
    e = all_entities

    def executor(self, **kwargs):
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
                    args.append(f"{i}={v}")
            elif k in CAN_REPEAT and isinstance(v, (tuple, list, set)):
                for i in v:
                    args.append(f"{k}={i}")
            else:
                args.append(f"{k}={v}")
        result = "["+",".join(args)+"]"
        if result == "[]": result = ""
        return result


class BedrockSelectors(UniversalSelectors):
    def __init__(self):
        pass


class JavaSelectors(UniversalSelectors):
    def __init__(self):
        pass

    def range(self, minv: int=0, maxv: int=inf):
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
        

from typing import Union
import itertools
import json

import pymcfunc.errors as errors
import pymcfunc.internal as internal

class UniversalFuncHandler:
    """The function handler which includes commands that are the same for both Java and Bedrock edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler"""
    def __init__(self):
        self.r = UniversalRawCommands(self)

    def __str__(self):
        return "\n".join(self.commands)

    def __iter__(self):
        for i in self.commands:
            yield i

class UniversalRawCommands:
    def __init__(self, fh):
        self.fh = fh

    def say(self, message: str):
        """Adds a /say command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.say"""
        cmd = f"say {message}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tell(self, target: str, message: str):
        """Adds a /tell command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.tell"""
        internal.check_spaces('target', target)
        cmd = f"tell {target} {message}".strip()
        self.fh.commands.append(cmd)
        return cmd
    w = tell
    msg = tell

    def tellraw(self, target: str, message: dict):
        internal.check_spaces('target', target)
        cmd = f"tell {target} {json.dumps(message)}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def title(self, target: str, mode: str, text: Union[str, dict]=None, fadeIn: str=None, stay: str=None, fadeOut: str=None):
        internal.options(mode, ['clear', 'reset', 'times', 'title', 'subtitle', 'actionbar'])
        internal.multi_check_invalid_params(['title', 'subtitle', 'actionbar'], 'mode', mode, ('text', text, None), dep_mandatory=True)
        internal.check_invalid_params('times', 'mode', mode, 
            ('fadeIn', fadeIn, None),
            ('stay', stay, None),
            ('fadeOut', fadeOut, None),
            dep_mandatory=True)

        from pymcfunc.func_handler_java import JavaFuncHandler
        from pymcfunc.func_handler_bedrock import BedrockFuncHandler
        raw = ""
        if issubclass(type(self.fh), JavaFuncHandler) and isinstance(text, str):
            text = {"text": text}
        elif issubclass(type(self.fh), BedrockFuncHandler) and isinstance(text, dict):
            raw = "raw"
        if isinstance(text, dict):
            text = json.dumps(text)
        if mode in ['title', 'subtitle', 'actionbar']:
            cmd = f"title{raw} {mode} {text}"
        elif mode == "times":
            cmd = f"title{raw} {mode} {fadeIn} {stay} {fadeOut}"
        elif mode in ['clear', 'reset']:
            cmd = f"title{raw} {mode}"
        self.fh.commands.append(cmd)
        return cmd

    def help(self):
        """Adds a /help command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.help"""
        self.fh.commands.append("help")
        return "help"

    def kill(self, target: str):
        """Adds a /kill command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.kill"""
        internal.check_spaces('target', target)
        cmd = f"kill {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gamemode(self, mode: Union[int, str], target: str="@s"):
        JAVA = ['survival', 'creative', 'adventure', 'spectator']
        BEDROCK = ['survival', 'creative', 'adventure', 's', 'c', 'a', 0, 1, 2]
        from pymcfunc.func_handler_bedrock import BedrockFuncHandler

        options = BEDROCK if isinstance(self.fh, BedrockFuncHandler) else JAVA
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"))
        internal.options(mode, options)

        cmd = f"gamemode {mode} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gamerule(self, rule: str, value: Union[bool, int]=None):
        BEDROCK = {
            bool: ['commandBlocksEnabled', 'commandBlockOutput', 'doDaylightCycle', 'doEntityDrops', 'doFireTick', 'doInsomnia',
                   'doImmediateRespawn', 'doMobLoot', 'doMobSpawning', 'doTileDrops', 'doWeatherCycle', 'drowningDamage',
                   'fallDamage', 'fireDamage', 'freezeDamage', 'keepInventory', 'mobGriefing', 'naturalRegeneration', 'pvp'
                   'sendCommandFeedback', 'showCoordinates', 'showDeathMessages', 'tntExplodes', 'showTags'],
            int: ['functionCommandLimit', 'maxCommandChainLength', 'randomTickSpeed', 'spawnRadius']
        }
        JAVA = {
            bool: ['announceAdvancements', 'commandBlockOutput', 'disableElytraMovementCheck', 'disableRaids', 'doDaylightCycle',
                   'doEntityDrops', 'doFireTick', 'doInsomnia', 'doImmediateRespawn', 'doLimitedCrafting', 'doMobLoot', 'doMobSpawning',
                   'doPatrolSpawning', 'doTileDrops', 'doTraderSpawning', 'doWeatherCycle', 'drowningDamage', 'fallDamage', 'fireDamage',
                   'forgiveDeadPlayers', 'freezeDamage', 'keepInventory', 'logAdminCommands', 'mobGriefing', 'naturalRegeneration'
                   'randomTickSpeed', 'reducedDebugInfo', 'sendCommandFeedback', 'showDeathMessages', 'spectatorsGenerateChunks',
                   'universalAnger'],
            int: ['maxCommandChainLength', 'maxEntityCramming', 'playersSleepingPercentage', 'spawnRadius']
        }
        from pymcfunc.func_handler_bedrock import BedrockFuncHandler

        rules = BEDROCK if isinstance(self.fh, BedrockFuncHandler) else JAVA
        rulelist = itertools.chain.from_iterable(rules.values())
        internal.options(rule, rulelist)

        if value != None:
            other = int if isinstance(value, bool) else bool
            if rule in rules[other]:
                raise ValueError(f"{rule} is of type {other.__name__} and not {type(value).__name__}")

            if isinstance(value, bool):
                value = "true" if value else "false"
            cmd = f"gamerule {rule} {value}".strip()
        else:
            cmd = f"gamerule {rule}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def seed(self):
        self.fh.commands.append("seed")
        return "seed"

    def enchant(self, target: str, enchantment: str, level: int=1):
        internal.check_spaces('target', target)
        optionals = internal.defaults((level, 1))

        cmd = f"enchant {target} {enchantment} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def function(self, name: str):
        cmd = f"function {name}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def locate(self, name: str):
        cmd = f"locate {name}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def time_add(self, amount: int):
        cmd = f"time add {amount}"
        self.fh.commands.append(cmd)
        return cmd
    
    def time_query(self, query: str):
        internal.options(query, ['daytime', 'gametime', 'day'])
        cmd = f"time query {query}"
        self.fh.commands.append(cmd)
        return cmd
    
    def time_set(self, amount: Union[int, str]):
        BEDROCK = ['day', 'night', 'noon', 'midnight', 'sunrise', 'sunset']
        JAVA = ['day', 'night', 'noon', 'midnight']
        from pymcfunc.func_handler_bedrock import BedrockFuncHandler

        options = BEDROCK if isinstance(self.fh, BedrockFuncHandler) else JAVA
        if isinstance(amount, str):
            internal.options(amount, options)
        cmd = f"time set {amount}"
        self.fh.commands.append(cmd)
        return cmd

    def kick(self, target: str, reason: str=None):
        internal.check_spaces('target', target)
        optionals = internal.defaults((reason, None))
        cmd = f"kick {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def op(self, target: str):
        internal.check_spaces('target', target)
        cmd = f"op {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def deop(self, target: str):
        internal.check_spaces('target', target)
        cmd = f"deop {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def reload(self):
        self.fh.commands.append("reload")
        return "reload"

    def me(self, text: str):
        cmd = f"me {text}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tag(self, target: str, mode: str, name: str=None):
        internal.check_spaces('target', target)
        internal.options(mode, ['add', 'list', 'remove'])
        internal.multi_check_invalid_params(['add', 'remove'], 'mode', mode,
            ('name', name, None),
            dep_mandatory=True)
        if mode == 'list':
            cmd = f"tag {target} list"
        else:
            cmd = f"tag {target} {mode} {name}".strip()
        self.fh.commands.append(cmd)
        return cmd
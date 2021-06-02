from typing import Union
import itertools
import json

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.selectors import UniversalSelectors

class UniversalFuncHandler:
    """The function handler which includes commands that are the same for both Java and Bedrock edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler"""
    sel = UniversalSelectors()
    def __init__(self):
        self.r = UniversalRawCommands(self)

    def __str__(self):
        return "\n".join(self.commands)

    def __iter__(self):
        for i in self.commands:
            yield i

class UniversalRawCommands:
    """A container for raw Minecraft commands that are the same for both Java and Bedrock.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands"""
    def __init__(self, fh):
        self.fh = fh

    def say(self, message: str):
        """**Syntax:** *say <message>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.say"""
        cmd = f"say {message}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tell(self, target: str, message: str):
        """**Syntax:** *tell <target> <message>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.tell"""
        internal.check_spaces('target', target)
        cmd = f"tell {target} {message}".strip()
        self.fh.commands.append(cmd)
        return cmd
    w = tell
    msg = tell

    def tellraw(self, target: str, message: dict):
        """**Syntax:** *tellraw <target> <message>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.tellraw"""
        internal.check_spaces('target', target)
        cmd = f"tell {target} {json.dumps(message)}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def title(self, target: str, mode: str, text: Union[str, dict]=None, fadeIn: int=None, stay: int=None, fadeOut: int=None):
        """**Syntax:** *title <target> ...*\n
        * *... <mode\:clear|reset>*
        * *... <mode\:title|subtitle|actionbar> <text>*
        * *... <mode\:times> <fadeIn> <stay> <fadeOut>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.title"""
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
        """**Syntax:** *help*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.help"""
        self.fh.commands.append("help")
        return "help"

    def kill(self, target: str):
        """**Syntax:** *kill <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.kill"""
        internal.check_spaces('target', target)
        cmd = f"kill {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gamemode(self, mode: Union[int, str], target: str="@s"):
        """**Syntax:** *gamemode <mode> [target]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.gamemode"""
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
        """**Syntax:** *gamerule <rule> [value]*\n
        A complete list of game rules are available at https://minecraft.fandom.com/wiki/Game_rule#List_of_game_rules\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.gamerule"""
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

        if value is not None:
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

    def enchant(self, target: str, enchantment: str, level: int=1):
        """**Syntax:** *enchant <target> <enchantment> [level]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.enchant"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((level, 1))

        cmd = f"enchant {target} {enchantment} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def function(self, name: str):
        """**Syntax:** *function <name>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.function"""
        cmd = f"function {name}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def locate(self, name: str):
        """**Syntax:** *locate <name>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.locate"""
        cmd = f"locate {name}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def time_add(self, amount: int):
        """**Syntax:** *time add <amount>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.time_add"""
        cmd = f"time add {amount}"
        self.fh.commands.append(cmd)
        return cmd
    
    def time_query(self, query: str):
        """**Syntax:** *time query <query\:daytime|gametime|day>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.time_query"""
        internal.options(query, ['daytime', 'gametime', 'day'])
        cmd = f"time query {query}"
        self.fh.commands.append(cmd)
        return cmd
    
    def time_set(self, amount: Union[int, str]):
        """**Syntax:** *time set <amount>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.time_set"""
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
        """**Syntax:** *kick <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.kick"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((reason, None))
        cmd = f"kick {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def op(self, target: str):
        """**Syntax:** *op <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.op"""
        internal.check_spaces('target', target)
        cmd = f"op {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def deop(self, target: str):
        """**Syntax:** *deop <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.deop"""
        internal.check_spaces('target', target)
        cmd = f"deop {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def reload(self):
        """**Syntax:** *reload*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.reload"""
        self.fh.commands.append("reload")
        return "reload"

    def me(self, text: str):
        """**Syntax:** *me <text>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.me"""
        cmd = f"me {text}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tag(self, target: str, mode: str, name: str=None):
        """**Syntax:** *tag <target> <mode\:add|list|remove> <mode=add|remove:name>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.tag"""
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

    def whitelist(self, mode: str, target: str=None):
        """**Syntax:** *whitelist <mode\:add|list|on|off|reload|remove> <mode=add|remove:target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.whitelist"""
        internal.options(mode, ['add', 'list', 'on', 'off', 'reload', 'remove'])
        internal.multi_check_invalid_params(['add', 'remove'], 'mode', mode,
            ('target', target, None),
            dep_mandatory=True)
        target = "" if target is None else target

        cmd = f"whitelist {mode} {target}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def stop(self):
        """**Syntax:** *stop*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.stop"""
        self.fh.commands.append("stop")
        return "stop"

    
from typing import Union
import itertools

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
        cmd = f"tell {target} {str(message)}".strip()
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
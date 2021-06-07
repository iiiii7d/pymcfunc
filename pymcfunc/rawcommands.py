from typing import Union, Callable
import itertools
import re
import json

import pymcfunc.internal as internal
import pymcfunc.errors as errors
from pymcfunc.func_handlers import JavaFuncHandler, BedrockFuncHandler
_b = lambda x: 'true' if x == True else 'false' if x == False else x

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

    def tellraw(self, target: str, message: Union[dict, list]):
        """**Syntax:** *tellraw <target> <message>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalRawCommands.tellraw"""
        internal.check_spaces('target', target)
        cmd = f"tell {target} {json.dumps(message)}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def title(self, target: str, mode: str, text: Union[str, Union[dict, list]]=None, fadeIn: int=None, stay: int=None, fadeOut: int=None):
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


class BedrockRawCommands(UniversalRawCommands):
    """A container for raw Minecraft commands that are specially for Bedrock Edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands"""
    def setblock(self, pos: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace"):
        """**Syntax:** *setblock <pos> <tileName> [tileData/blockStates] [mode:destroy|keep|replace]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates"))
        optionals = internal.defaults((tileData_blockStates, None), (mode, "replace"))

        cmd = f"setblock {pos} {tileName} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace", replaceTileName: str=None, replaceDataValue: int=None):
        """**Syntax:** *fill <pos1> <pos2> <tileName> [tileData/blockStates] [mode:destroy|hollow|keep|outline|replace] [mode=replace:replaceTileName] [mode=replace:replaceDataValue]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.fill"""
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace':
            internal.check_invalid_params('replace', mode, 'mode', ('replaceTileName', replaceTileName, None), ('replaceDataValue', replaceDataValue, None))
        internal.reliant('replaceTileName', replaceTileName, None, 'replaceDataValue', replaceDataValue, None)
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates"))
        optionals = internal.defaults((tileData_blockStates, None), (mode, "replace"), (replaceTileName, None), (replaceDataValue, None))

        cmd = f"fill {pos1} {pos2} {tileName} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", cloneMode: str="normal", tileName: str=None, tileData: int=0, blockStates: list=None):
        """**Syntax:** *clone <pos1> <pos2> <dest> [maskMode:replace|masked] [cloneMode:force|move|normal] <maskMode=filtered:tileName> <maskMode=filtered:tileData/blockStates>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.clone"""
        internal.options(maskMode, ['masked', 'filtered', 'replace'])
        internal.options(cloneMode, ['forced', 'move', 'normal'])
        if maskMode == 'filtered':
            internal.check_invalid_params('filtered', maskMode, 'maskMode', ('tileName', tileName, None), ('tileData', tileData, 0), ('blockStates', blockStates, None))
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates")) if maskMode == 'filtered' else None
        internal.reliant('tileName', tileName, None, 'tileData_blockStates', tileData_blockStates, None)
        optionals = internal.defaults((maskMode, "replace"), (cloneMode, "normal"), (tileName, None), (tileData_blockStates, None))
        
        cmd = f"clone {pos1} {pos2} {dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def give(self, target: str, item: str, amount: int=1, data: int=0, components: dict=None):
        """**Syntax:** *give <target> <item> [amount] [data] [components]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.give"""
        internal.check_spaces('target', target)
        components = json.dumps(components) if isinstance(components, dict) else components
        optionals = internal.defaults((amount, 1), (data, 0), (components, None))

        cmd = f"give {target} {item} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def summon(self, entity: str, pos: str="~ ~ ~", event: str=None, nameTag: str=None):
        """**Syntax:** *summon <entity> ...*
        * *[pos] [event] [nameTag]*
        * *<nameTag> [pos]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.summon"""
        if nameTag is not None:
            optionals = internal.defaults((pos, "~ ~ ~"))
            nameTag = internal.unspace(nameTag)
            cmd = f"summon {entity} {nameTag} {optionals}".strip()
        else:
            optionals = internal.defaults((pos, "~ ~ ~"), (event, None), (nameTag, None))
            if event is not None: event = internal.unspace(event)
            if nameTag is not None: nameTag = internal.unspace(nameTag)
            cmd = f"summon {entity} {optionals}".strip()
        
        self.fh.commands.append(cmd)
        return cmd

    def clear(self, target: str="@s", item: str=None, data: int=-1, maxCount: int=-1):
        """**Syntax:** *clear [target] [item] [data] [maxCount]*
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.clear"""
        internal.reliant('item', item, None, 'data', data, -1)
        internal.reliant('item', maxCount, None, 'data', maxCount, -1)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (data, -1), (maxCount, -1))

        cmd = f"clear {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def teleport(self, destxyz: str=None, destentity: str=None, target: str="@s", facing: str=None, rotation: str=None, checkForBlocks: bool=False):
        """**Syntax:**
        * *teleport <destxyz> ...* / *teleport <target> <destxyz>...*
          * *[checkForBlocks]*
          * *[rotation] [checkForBlocks]*
          * *facing [facing] [checkForBlocks]*
        * *teleport <destentity> ...* / *teleport <target> <destentity>...*
          * *[checkForBlocks]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.teleport"""
        internal.check_spaces('target', target)
        dest = internal.pick_one_arg((destxyz, None, 'destxyz'), (destentity, None, 'destentity'), optional=False)
        target = "" if target == "@s" else target+" "
        if destentity is None:
            rotation_facing = internal.pick_one_arg((rotation, None, 'rotation'), (facing, None, 'facing'))
            if rotation_facing is not None:
                if facing is not None: rotation_facing = "facing "+rotation_facing
                optionals = f"{rotation_facing} {internal.defaults((_b(checkForBlocks), 'false'))}"
            else:
                optionals = internal.defaults((_b(checkForBlocks), 'false'))
        else:
            optionals = internal.defaults((_b(checkForBlocks), 'false'))

        cmd = f"teleport {target}{dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    tp = teleport

    def xp(self, amount: int, level: bool=False, target: str="@s"):
        """**Syntax:**
        * *xp <amount> [target]* if level=False
        * *xp <amount>L [target]* if level=True\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.xp"""
        internal.check_spaces('target', target)
        level = "L" if level else ""
        optionals = internal.defaults((target, "@s"))

        cmd = f"xp {amount}{level} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def effect_give(self, target: str, effect: str, seconds: int=30, amplifier: int=0, hideParticles: bool=False):
        """**Syntax:** *<target> <effect> [seconds] [amplifier] [hideParticles]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.effect_give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((seconds, 30), (amplifier, 0), (_b(hideParticles), 'false'))

        cmd = f"effect {target} {effect} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def effect_clear(self, target: str):
        """**Syntax:** *effect <target> clear*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.effect_clear"""
        internal.check_spaces('target', target)

        cmd = f"effect {target} clear".strip()
        self.fh.commands.append(cmd)
        return cmd

    def setworldspawn(self, pos: str="~ ~ ~"):
        """**Syntax:** *setworldspawn [pos]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.setworldspawn"""
        optionals = internal.defaults((pos, "~ ~ ~"))

        cmd = f"setworldspawn {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spawnpoint(self, target: str="@s", pos: str="~ ~ ~"):
        """**Syntax:** *spawnpoint [target] [pos]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.spawnpoint"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (pos, "~ ~ ~"))

        cmd = f"spawnpoint {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def particle(self, name: str, pos: str):
        """**Syntax:** *particle <name> <pos>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.particle"""
        cmd = f"particle {name} {pos}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def schedule(self, path: str, mode: str, pos1: str=None, pos2: str=None, center: str=None, radius: int=None, tickingAreaName: str=None):
        """**Syntax:** *schedule on_area_loaded add ...*
        * *<pos1> <pos2> <path>* when mode=cuboid
        * *<mode\:circle> <center> <radius> <path>*
        * *<mode\:tickingarea> <tickingAreaName> <path>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.schedule"""
        internal.options(mode, ['cuboid', 'circle', 'tickingarea'])
        internal.check_invalid_params("cuboid", "mode", mode,
            ('pos1', pos1, None),
            ('pos2', pos2, None),
            dep_mandatory=True)
        internal.check_invalid_params("circle", "mode", mode,
            ('center', center, None),
            ('radius', radius, None),
            dep_mandatory=True)
        internal.check_invalid_params("tickingarea", "mode", mode,
            ('tickingAreaName', tickingAreaName, None),
            dep_mandatory=True)
        if mode == "cuboid":
            suffix = f"{pos1} {pos2} {path}"
        elif mode == "circle":
            suffix = f"{center} {radius} {path}"
        else:
            suffix = f"{tickingAreaName} {path}"
        cmd = f"schedule on_area_loaded add {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def playsound(self, sound: str, target: str="@p", pos: str="~ ~ ~", volume: float=1.0, pitch: float=1.0, minVolume: float=None):
        """**Syntax:** *<sound> [target] [pos] [volume] [pitch] [minVolume]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.playsound"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@p"), (pos, "~ ~ ~"), (volume, 1.0), (pitch, 1.0), (minVolume, None))
        cmd = f"playsound {sound} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def stopsound(self, target: str, sound: str=None):
        """**Syntax:** *stopsound <target> [sound]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.stopsound"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((sound, None))

        cmd = f"stopsound {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def weather(self, mode: str, duration: str=5):
        """**Syntax:** *weather <mode\:clear|rain|thunder|query> <mode=clear|rain|thunder:duration>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.weather"""
        internal.options(mode, ['clear', 'rain', 'thunder', 'query'])
        if mode == "query":
            cmd = "weather query"
        else:
            cmd = f"weather {mode} {duration}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def difficulty(self, difficulty: Union[str, int]):
        """**Syntax:** *difficulty <difficulty>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.difficulty"""
        internal.options(difficulty, ['easy', 'hard', 'normal', 'peaceful', 'e', 'h', 'n', 'p', 0, 1, 2, 3])
        cmd = f"difficulty {difficulty}"
        self.fh.commands.append(cmd)
        return cmd

    def list_(self):
        """**Syntax:** *list*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.list_"""
        self.fh.commands.append("list")
        return "list"

    def spreadplayers(self, center: str, dist: float, maxRange: float, target: str):
        """**Syntax:** *spreadplayers <center> <dist> <maxRange> <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.spreadplayers"""
        cmd = f"spreadplayers {center} {dist} {maxRange} {target}"
        self.fh.commands.append(cmd)
        return cmd

    def replaceitem(self, mode: str, slotId: int, itemName: str, pos: str=None, target: str=None, slotType: str=None, itemHandling: str=None, amount: int=1, data: int=0, components: dict=None):
        """**Syntax:** *replaceitem <mode\:block|entity> <pos/target> ...*
        * *slot.container <slotId> <itemName> [amount] [data] [components]* or
        * *slot.container <slotId> <replaceMode\:destroy|keep> <itemName> [amount] [data] [components]* when mode=block
        * *<slotType> <slotId> <itemName> [amount] [data] [components]* or
        * *<slotType> <slotId> <itemHandling\:destroy|keep> <itemName> [amount] [data] [components]* when mode=entity\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.replaceitem"""
        internal.check_invalid_params('block', 'mode', mode,
            ('pos', pos, None),
            dep_mandatory=True)
        internal.check_invalid_params('entity', 'mode', mode,
            ('target', target, None),
            ('slotType', slotType, None),
            dep_mandatory=True)
        if slotType is None and mode == "block":
            slotType = "slot.container"
        if itemHandling is None:
            itemHandling = ""
        else:
            internal.options(itemHandling, ['destroy', 'keep'])
            itemHandling += " "
        if components is not None: components = json.dumps(components)
        pos_target = target if target is not None else pos
        optionals = internal.defaults((amount, 1), (data, 0), (components, None))

        cmd = f"replaceitem {mode} {pos_target} {slotType} {slotId} {itemHandling}{itemName} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    allowlist = UniversalRawCommands.whitelist

    def scoreboard_objectives(self, mode: str, objective: str=None, displayName: str=None, slot: str=None, sortOrder: str=None):
        """**Syntax:** *scoreboard objectives ...*
        * *<mode\:add> <objective> dummy [displayName]*
        * *<mode\:list>*
        * *<mode\:remove> <objective>*
        * *<mode\:setdisplay> <slot\:list|sidebar|belowname> [objective] [slot=list|sidebar:sortOrder:ascending|descending]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.scoreboard_objectives"""
        internal.options(mode, ['add', 'list', 'remove', 'setdisplay'])
        internal.multi_check_invalid_params(['add', 'remove', 'setdisplay'], 'mode', mode, ('objective', objective, None))
        if mode in ['add', 'remove'] and objective is None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode, ('displayName', displayName, None))
        internal.check_invalid_params('setdisplay', 'mode', mode, ('slot', slot, None), dep_mandatory=True)
        if slot is not None:
            internal.options(slot, ['list', 'sidebar', 'belowname'])
            internal.multi_check_invalid_params(['list', 'sidebar'], 'mode', mode, ('sortOrder', sortOrder, None))
            if sortOrder is not None:
                internal.options(sortOrder, ['ascending', 'descending'])
        
        if mode == "add":
            suffix = f"{objective} dummy {displayName}"
        elif mode == "list":
            suffix = ""
        elif mode == "remove":
            suffix = objective
        elif mode == "setdisplay":
            optionals = internal.defaults((objective, None), (sortOrder, None))
            suffix = f"{slot} {optionals}"
        
        cmd = f"scoreboard objectives {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def scoreboard_players(self, mode: str, target: str=None, objective: str=None, minv: Union[int, str]=None, maxv: Union[int, str]=None, count: int=None, operation: str=None, selector: str=None, selectorObjective: str=None):
        """**Syntax:** *scoreboard players ...*

        * *<mod\:list> [target]*
        * *<mod\:reset> <target> [objective]*
        * *<mod\:test|random> <target> <objective> <minv> [maxv]*
        * *<mod\:set|add|remove> <target> <objective> <count>*
        * *<mod\:operation> <target> <objective> <operation:+=|-=|*=|/=|%=|<|>|><> <selector> <selectorObjective>\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.scoreboard_players"""
        internal.options(mode, ['list', 'reset', 'test', 'random', 'set', 'add', 'remove', 'operation'])
        if mode in ['reset', 'test', 'random', 'set', 'add', 'remove', 'operation'] and target is None:
            raise errors.MissingError('target', 'mode', mode)
        internal.multi_check_invalid_params(['reset', 'test', 'random', 'set', 'add', 'remove', 'operation'], 'mode', mode, ('objective', objective, None))
        if mode in ['test', 'random', 'set', 'add', 'remove', 'operation'] and objective is None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.multi_check_invalid_params(['test', 'random'], 'mode', mode,
            ('minv', minv, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['test', 'params'], 'mode', mode,
            ('maxv', maxv, None))
        internal.multi_check_invalid_params(['add', 'set', 'remove'], 'mode', mode,
            ('count', count, None),
            dep_mandatory=True)
        internal.check_invalid_params('operation', 'mode', mode, 
            ('operation', operation, None),
            ('selector', selector, None),
            ('selectorObjective', selectorObjective, None),
            dep_mandatory=True)
        if operation is not None:
            internal.options(operation, ['+=', '-=', '*=', '/=', '%=', '<', '>', '><'])

        if mode == "list":
            optionals = internal.defaults((target, None))
            suffix = optionals
        elif mode == "reset":
            optionals = internal.defaults((objective, None))
            suffix = f"{target} {optionals}"
        elif mode in ['test', 'random']:
            optionals = internal.default((maxv, None))
            suffix = f"{target} {objective} {minv} {optionals}"
        elif mode in ['add', 'set', 'remove']:
            suffix = f"{target} {objective} {count}"
        elif mode == "operation":
            suffix = f"{target} {objective} {operation} {selector} {selectorObjective}"

        cmd = f"scoreboard players {mode} {suffix}"
        self.fh.commands.append(cmd)
        return cmd

    def execute(self, target: str, pos: str, run: Callable[[BedrockFuncHandler], Union[Union[list, tuple], None]], detectPos: str=None, block: str=None, data: int=None):
        """**Syntax** *execute <target> <pos> ...*
        * *<run>*
        * *detect <detectPos> <block> <data> <run>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.execute"""
        internal.check_spaces('target', target)
        cmd = f"execute {target} {pos} "
        internal.reliant('detectPos', detectPos, None, 'block', block, None)
        internal.reliant('block', block, None, 'data', data, None)
        if detectPos is not None:
            cmd += f"detect {detectPos} {block} {data} "

        sf = BedrockFuncHandler()
        result = run(sf)
        if isinstance(result, (list, tuple)):
            result = map(lambda j: (cmd+j).strip(), result)
            self.fh.commands.extend(result)
            return result
        elif isinstance(result, str):
            self.fh.commands.append((cmd+result).strip())
            return result
        else:
            result = sf.commands
            result = map(lambda j: (cmd+j).strip(), result)
            self.fh.commands.extend(result)
            return result

    def ability(self, target: str, ability: str=None, value: bool=None):
        """**Syntax:** *ability <target> [ability] [value]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.ability"""
        internal.reliant('ability', ability, None, 'value', value, None)
        optionals = internal.defaults((ability, None), (_b(value), None))
        cmd = f"ability {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def agent(self, mode: str, direction: str=None, slotNum: str=None, destSlotNum: str=None, pos: str=None, item: str=None, quantity: int=None, turnDirection: str=None):
        """**Syntax:** *agent ...*
        * *<mode\:move|attack|destroy|dropall|inspect|inspectdata|detect|detectredstone|till> <direction\:forward|back|left|right|up|down>*
        * *<mode\:turn> <turnDirection\:left|right>*
        * *<mode\:drop> <slotNum> <quantity> <directon\:forward|back|left|right|up|down>*
        * *<mode\:transfer> <slotNum> <quantity> <destSlotNum>*
        * *<mode\:create>*
        * *<mode\:tp> <pos>*
        * *<mode\:collect> <item>*
        * *<mode\:place> <slotNum> <direction\:forward|back|left|right|up|down>*
        * *<mode\:getitemcount|getitemspace|getitemdetail> <slotNum>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.agent"""
        internal.options(mode, ['move', 'turn', 'attack', 'destroy', 'drop', 'dropall', 'inspect', 'inspectdata', 'detect', 'detectredstone', 'transfer',
                                'create', 'tp', 'collect', 'till', 'place', 'getitemcount', 'getitemspace', 'getitemdetail'])
        internal.multi_check_invalid_params(['move', 'attack', 'destroy', 'drop', 'dropall', 'inspect', 'inspectdata', 'detect', 'detectredstone', 'till', 'place'], 'mode', mode,
            ('direction', direction, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['drop', 'transfer', 'place', 'getitemcount', 'getitemspace', 'getitemdetail'], 'mode', mode,
            ('slotNum', slotNum, None),
            dep_mandatory=True)
        internal.check_invalid_params('transfer', 'mode', mode,
            ('destSlotNum', destSlotNum, None),
            dep_mandatory=True)
        internal.check_invalid_params('tp', 'mode', mode,
            ('pos', pos, None),
            dep_mandatory=True)
        internal.check_invalid_params('collect', 'mode', mode,
            ('item', item, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['drop', 'transfer'], 'mode', mode,
            ('quantity', quantity, None),
            dep_mandatory=True)
        internal.check_invalid_params('turn', 'mode', mode,
            ('turnDirection', turnDirection, None),
            dep_mandatory=True)
        if direction is not None:
            internal.options(direction, ['forward', 'back', 'left', 'right', 'up', 'down'])
        elif turnDirection is not None:
            internal.options(direction, ['left', 'right'])
        
        if mode == 'turn':
            suffix = turnDirection
        elif mode == 'drop':
            suffix = f"{slotNum} {quantity} {direction}"
        elif mode == 'transfer':
            suffix = f"{slotNum} {quantity} {destSlotNum}"
        elif mode == 'create':
            suffix = ""
        elif mode == 'tp':
            suffix = pos
        elif mode == 'collect':
            suffix = item
        elif mode == 'place':
            suffix = f"{slotNum} {direction}"
        elif mode.startswith('getitem'):
            suffix = slotNum
        else:
            suffix = direction
        cmd = f"agent {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd
    
    def alwaysday(self, lock: bool=None):
        """**Syntax:** *alwaysday [lock]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.alwaysday"""
        optionals = internal.defaults((_b(lock), None))
        cmd = f"alwaysday {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    daylock = alwaysday

    def camerashake_add(self, target: str, intensity: float=1, seconds: float=1, shakeType: str=None):
        """**Syntax:** *camerashake add <target> [intensity] [seconds] [shakeType:positional|rotational]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.camerashake_add"""
        if shakeType is not None:
            internal.options(shakeType, ['positional', 'rotational'])
        internal.check_spaces('target', target)
        optionals = internal.defaults((intensity, 1), (seconds, 1), (shakeType, None))
        cmd = f"camerashake add {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def camerashake_stop(self, target: str):
        """**Syntax:** *camerashake stop <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.camerashake_stop"""
        internal.check_spaces('target', target)
        cmd = f"camerashake stop {target}"
        self.fh.commands.append(cmd)
        return cmd

    def changesetting(self, allow_cheats: bool=None, difficulty: Union[str, int]=None):
        """**Syntax:** *changesetting ...*
        * *allow-cheats <allow_cheats>*
        * *difficulty <difficulty>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.changesetting"""
        if difficulty is not None:
            internal.options(difficulty, ['peaceful', 'easy', 'normal', 'hard', 'p', 'e', 'n', 'h', 0, 1, 2, 3])
        value = internal.pick_one_arg(
            (_b(allow_cheats), None, 'allow_cheats'),
            (difficulty, None, 'difficulty'),
            optional=False
        )
        middle = 'allow-cheats' if allow_cheats is not None else difficulty
        cmd = f"changesetting {middle} {value}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clearspawnpoint(self, target: str):
        """**Syntax:** *clearspawnpoint <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.clearspawnpoint"""
        internal.check_spaces('target', target)
        cmd = f"clearspawnpoint {target}"
        self.fh.commands.append(cmd)
        return cmd

    def closewebsocket(self):
        """**Syntax:** *closewebsocket*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.closewebsocket"""
        self.fh.commands.append("closewebsocket")
        return "closewebsocket"

    def connect(self, serverUri: str):
        """**Syntax:** *connect <serverUri>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.connect"""
        cmd = f"connect {serverUri}"
        self.fh.commands.append(cmd)
        return cmd
    wsserver = connect

    # dedicatedwssever

    # enableencryption

    def event(self, target: str, event: str):
        """**Syntax:** *event <target> <event>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.event"""
        internal.check_spaces('target', target)
        cmd = f"event entity {target} {event}"
        self.fh.commands.append(cmd)
        return cmd

    def fog(self, target: str, mode: str, userProvidedId: str, fogId: str=None):
        """**Syntax:** *fog <target> <mode\:push|pop|remove> <mode=push:fogId> <userProvidedId>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.fog"""
        internal.check_spaces('target', target)
        internal.options(mode, ['push', 'pop', 'remove'])
        internal.check_invalid_params('push', 'mode', mode,
            ('fogId', fogId, None),
            dep_mandatory=True
        )

        if mode == 'push':
            mode = f"push {fogId}"
        cmd = f"{target} {mode} {userProvidedId}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gametest_runthis(self):
        """**Syntax:** *gametest runthis*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_runthis"""
        self.fh.commands.append('gametest runthis')
        return 'gametest runthis'

    def gametest_run(self, name: str, rotationSteps: int=None):
        """**Syntax:** *gametest run <name> [rotationSteps]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_run"""
        optionals = internal.defaults((rotationSteps, None))
        cmd = f"gametest run {name} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gametest_runall(self, tag: str, rotationSteps: int=None):
        """**Syntax:** *gametest runall <tag> [rotationSteps]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_runall"""
        optionals = internal.defaults((rotationSteps, None))
        cmd = f"gametest runall {tag} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    gametest_runset = gametest_runall

    def gametest_clearall(self, radius: int=None):
        """**Syntax:** *gametest [radius]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_clearall"""
        optionals = internal.defaults((radius, None))
        cmd = f"gametest clearall {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gametest_pos(self):
        """**Syntax:** *gametest pos*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_pos"""
        self.fh.commands.append('gametest pos')
        return 'gametest pos'

    def gametest_create(self, name: str, width: int=None, height: int=None, depth: int=None):
        """**Syntax:**  *gametest create <name> [width] [height] [depth]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_create"""
        internal.reliant('width', width, None, 'height', height, None)
        internal.reliant('height', height, None, 'depth', depth, None)
        optionals = internal.defaults((width, None), (height, None), (depth, None))
        cmd = f"gametest create {name} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def gametest_runthese(self):
        """**Syntax:** *gametest runthese*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.gametest_runthese"""
        self.fh.commands.append('gametest runthese')
        return 'gametest runthese'

    def getchunkdata(self, dimension: str, chunkPos: str, height: int):
        """**Syntax:** *getchunkdata <dimension> <chunkPos> <height>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.getchunkdata"""
        cmd = f"getchunkdata {dimension} {chunkPos} {height}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def getchunks(self, dimension: str):
        """**Syntax:** *getchunks <dimension>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.getchunks"""
        cmd = f"getchunks {dimension}".strip()
        self.fh.commands.append(cmd)
        return cmd

    # getlocalplayername

    def getspawnpoint(self, target: str):
        """**Syntax:** *getspawnpoint <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.getspawnpoint"""
        cmd = f"getspawnpoint {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    #gettopsolidblock

    def globalpause(self, pause: bool):
        """**Syntax:** *globalpause <pause>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.getspawnpoint"""
        cmd = f"globalpause {_b(pause)}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def immutableworld(self, immutable: bool=None):
        """**Syntax:** *immutableworld [immutable]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.immutableworld"""
        optionals = internal.defaults((_b(immutable), None))
        cmd = f"immutableworld {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def listd(self):
        """**Syntax:** *listd*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.listd"""
        self.fh.commands.append("listd")
        return "listd"

    def mobevent(self, event: str, value: bool=None):
        """**Syntax:** *mobevent <event> [value]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.mobevent"""
        optionals = internal.defaults((_b(value), None))
        cmd = f"mobevent {event} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def music_add(self, name: str, volume: float=None, fadeSeconds: float=None, repeatMode: str=None):
        """**Syntax:** *music add <name> [volume] [fadeSeconds] [repeatMode:loop|play_once]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.music_add"""
        internal.reliant('volume', volume, None, 'fadeSeconds', fadeSeconds, None)
        internal.reliant('fadeSeconds', fadeSeconds, None, 'repeatMode', repeatMode, None)
        if repeatMode is not None:
            internal.options(repeatMode, ['loop', 'play_once'])
        optionals = internal.defaults((volume, None), (fadeSeconds, None), (repeatMode, None))
        cmd = f"music add {name} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    
    def music_queue(self, name: str, volume: float=None, fadeSeconds: float=None, repeatMode: str=None):
        """**Syntax:** *music queue <name> [volume] [fadeSeconds] [repeatMode:loop|play_once]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.music_queue"""
        internal.reliant('volume', volume, None, 'fadeSeconds', fadeSeconds, None)
        internal.reliant('fadeSeconds', fadeSeconds, None, 'repeatMode', repeatMode, None)
        if repeatMode is not None:
            internal.options(repeatMode, ['loop', 'play_once'])
        cmd = f"music queue {name} {volume} {fadeSeconds} {repeatMode}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def music_stop(self, fadeSeconds: float=None):
        """**Syntax:** *music stop [fadeSeconds]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.music_stop"""
        optionals = internal.defaults((fadeSeconds, None))
        cmd = f"music stop {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def music_volume(self, volume: float):
        """**Syntax:** *music float <volume>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.music_volume"""
        cmd = f"music volume {volume}"
        self.fh.commands.append(cmd)
        return cmd

    def permissions(self, mode: str):
        """**Syntax:** *permissions <mode\:list|reload>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.permissions"""
        internal.options(mode, ['list', 'reload'])
        cmd = f"permissions {mode}"
        self.fh.commands.append(cmd)
        return cmd
    ops = permissions

    def playanimation(self, target: str, animation: str, next_state: str=None, blend_out_time: float=None, stop_expression: str=None, controller: str=None):
        """**Syntax:** *playanimation <target> <animation> [next_state] [blend_out_time] [stop_expression] [controller]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.playanimation"""
        internal.reliant('next_state', next_state, None, 'blend_out_time', blend_out_time, None)
        internal.reliant('blend_out_time', blend_out_time, None, 'stop_expression', stop_expression, None)
        internal.reliant('stop_expression', stop_expression, None, 'controller', controller, None)
        optionals = internal.defaults((next_state, None), (blend_out_time, None), (stop_expression, None), (controller, None))
        cmd = f"playanimation {target} {animation} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def querytarget(self, target: str):
        """**Syntax:** *querytarget <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.querytarget"""
        cmd = f"querytaret {target}"
        self.fh.commands.append(cmd)
        return cmd

    def ride_start_riding(self, rider: str, ride: str, teleportWhich: str="teleport_rider", fillMode: str="until_full"):
        """**Syntax:** *ride <rider> start_riding <ride> [teleportWhich:teleport_ride|teleport_rider] [fillMode:if_group_fits|until_full]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.ride_start_riding"""
        internal.options(teleportWhich, ['teleport_ride', 'teleport_rider'])
        internal.options(fillMode, ['if_group_fits', 'until_full'])
        optionals = internal.defaults((teleportWhich, "teleport_rider"), (fillMode, "until_full"))
        cmd = f"ride {rider} start_riding {ride} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ride_stop_riding(self, rider: str):
        """**Syntax:** *ride <rider> stop_riding*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.ride_stop_riding"""
        cmd = f"ride {rider} stop_riding".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ride_evict_riders(self, ride: str):
        """**Syntax:** *ride <ride> evict_riders*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.ride_evict_riders"""
        cmd = f"ride {ride} evict_riders".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ride_summon_rider(self, ride: str, entity: str, event: str=None, nameTag: str=None):
        """**Syntax:** *ride <ride> summon_rider <entity> [event] [nameTag]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.ride_summon_rider"""
        internal.reliant('event', event, None, 'nameTag', nameTag, None)
        optionals = internal.defaults((event, None), (nameTag, None))
        cmd = f"ride {ride} summon_rider {entity} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ride_summon_ride(self, rider: str, entity: str, rideMode: str='reassign_rides', event: str=None, nameTag: str=None):
        """**Syntax:** *ride <rider> summon_ride <entity> [rideMode:skip_riders|no_ride_change|reassign_rides] [event] [nameTag]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.ride_summon_ride"""
        internal.reliant('event', event, None, 'nameTag', nameTag, None)
        internal.options(rideMode, ['skip_riders', 'no_ride_change', 'reassign_rides'])
        optionals = internal.defaults((rideMode, 'reassign_rides'), (event, None), (nameTag, None))
        cmd = f"ride {rider} summon_ride {entity} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def save(self, mode: str):
        """**Syntax:** *save <mode\:hold|query|resume>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.save"""
        internal.options(mode, ['hold', 'query', 'resume'])
        cmd = f"save {mode}"
        self.fh.commands.append(cmd)
        return cmd

    def setmaxplayers(self, maxPlayers: int):
        """**Syntax:** *setmaxplayers <maxPlayers>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.setmaxplayers"""
        cmd = f"setmaxplayers {maxPlayers}"
        self.fh.commands.append(cmd)
        return cmd

    def structure_save(self, name: str, pos1: str, pos2: str, includesEntities: bool=True, saveMode: str='disk', includesBlocks: bool=True):
        """**Syntax:** *structure save <name> <pos1> <pos2> [includesEntities] [saveMode:disk|memory] [includesBlocks]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.structure_save"""
        internal.options(saveMode, ['disk', 'memory'])
        optionals = internal.defaults((_b(includesEntities), 'true'), (saveMode, 'disk'), (_b(includesBlocks), 'true'))
        cmd = f"structue save {name} {pos1} {pos2} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def structure_load(self, name: str, pos: str, rotation: str='0_degrees', mirror: str='none', animationMode: str=None, \
                       animationSeconds: float=1, includesEntities: bool=True, includesBlocks: bool=True, integrity: float=100, seed: str=None):
        """**Syntax:** *structure load <name> <pos> [rotation:0_degrees|90_degrees|180_degrees|270_degrees] [mirror:x|z|xz|none] ...*
        * *...*
        * *[animationMode:block_by_block|layer_by_layer] [animationSeconds] ...*\n
        *[includesEntities] [includesBlocks] [integrity] [seed]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.structure_load"""
        internal.options(rotation, ['0_degrees', '90_degrees', '180_degrees', '270_degrees'])
        internal.options(mirror, ['x', 'z', 'xz', 'none'])
        if animationMode is not None:
            internal.options(animationMode, ['block_by_block', 'layer_by_layer'])
            optional_list = [(rotation, '0_degrees'), (mirror, 'none'), (animationMode, None), (animationSeconds, 1), (_b(includesEntities), 'true'), (_b(includesBlocks), 'true'), (integrity, 100), (seed, None)]
        else:
            optional_list = [(rotation, '0_degrees'), (mirror, 'none'), (_b(includesEntities), 'true'), (_b(includesBlocks), 'true'), (integrity, 100), (seed, None)]

        optionals = internal.defaults(*optional_list)
        cmd = f"structure load {name} {pos} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def structure_delete(self, name: str):
        """**Syntax:** *structure delete <name>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.structure_delete"""
        cmd = f"structure delete {name}"
        self.fh.commands.append(cmd)
        return cmd

    #takepicture

    def testfor(self, target: str):
        """**Syntax:** *testfor <target>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.testfor"""
        cmd = f"testfor {target}"
        self.fh.commands.append(cmd)
        return cmd

    def testforblock(self, pos: str, name: str, dataValue: int=None):
        """**Syntax:** *testforblock <pos> <name> [dataValue]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.testforblock"""
        optionals = internal.defaults((dataValue, None))
        cmd = f"testforblock {pos} {name} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def testforblocks(self, pos1: str, pos2: str, dest: str, mode: str='all'):
        """**Syntax:** *testforblocks <pos1> <pos2> <dest> <mode\:all|masked>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.testforblocks"""
        internal.options(mode, ['all', 'masked'])
        optionals = internal.defaults((mode, 'all'))
        cmd = f"testforblocks {pos1} {pos2} {dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tickingarea_add_cuboid(self, pos1: str, pos2: str, name: str=None):
        """**Syntax:** *tickingarea add <pos1> <pos2> [name]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.tickingarea_add_cuboid"""
        optionals = internal.defaults((name, None))
        cmd = f"tickingarea add {pos1} {pos2} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tickingarea_add_circle(self, pos: str, radius: int, name: str=None):
        """**Syntax:** *tickingarea add circle <pos> <radius> [name]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.tickingarea_add_circle"""
        optionals = internal.defaults((name, None))
        cmd = f"tickingarea add circle {pos} {radius} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def tickingarea_remove(self, name: str=None, pos: str=None, all_: bool=False):
        """**Syntax:** *tickingarea ...*
        * *remove_all* if all_=True
        * *<name/pos>* if all_=False\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.tickingarea_remove"""
        if not all_:
            name_pos = internal.pick_one_arg(
                (name, None, 'name'),
                (pos, None, 'pos'),
                optional = False
            )
            cmd = f"tickingarea remove {name_pos}".strip()
        else:
            cmd = "tickingarea remove_all"
        self.fh.commands.append(cmd)
        return cmd

    def tickingarea_list(self, all_dimensions: bool=False):
        """**Syntax:** *tickingarea ...*
        * *list all-dimensions* if all_dimensions=True
        * *list* if all_dimensions=False\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.tickingarea_list"""
        if all_dimensions:
            cmd = "tickingarea list all-dimensions"
        else:
            cmd = "tickingarea list"
        self.fh.commands.append(cmd)
        return cmd

    def toggledownfall(self):
        """**Syntax:** *toggledownfall*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.toggledownfall"""
        self.fh.commands.append('toggledownfall')
        return 'toggledownfall'

    def worldbuilder(self):
        """**Syntax:** *worldbuilder*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.worldbuilder"""
        self.fh.commands.append('worldbuilder')
        return 'worldbuilder'
    wb = worldbuilder


class JavaRawCommands(UniversalRawCommands):
    def setblock(self, pos: str, block: str, mode="replace"):
        """**Syntax:** *setblock <pos> <block> [mode:destroy|keep|replace]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        optionals = internal.defaults((mode, "replace"))

        cmd = f"setblock {pos} {block} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, block: str, mode="replace", filterPredicate: str=None):
        """**Syntax:** *fill <pos1> <pos2> <block> [mode:destroy|hollow|keep|outline|replace] [mode=replace:filterPredicate]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.fill"""
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace' and filterPredicate is not None:
            raise errors.InvalidParameterError(mode, 'mode', filterPredicate, 'filterPredicate')
        optionals = internal.defaults((mode, "replace"), (filterPredicate, None))

        cmd = f"fill {pos1} {pos2} {block} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", filterPredicate: str=None, cloneMode: str="normal"):
        """**Syntax:** *clone <pos1> <pos2> <dest> [maskMode:replace|masked] <maskMode=masked:filterPredicate> [cloneMode:force|move|normal]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.clone"""
        internal.options(maskMode, ['masked', 'filtered', 'replace'])
        internal.options(cloneMode, ['forced', 'move', 'normal'])
        if maskMode != 'filtered' and filterPredicate is not None:
            raise errors.InvalidParameterError(maskMode, 'maskMode', filterPredicate, 'filterPredicate')
        if maskMode == 'filtered' and filterPredicate is not None:
            optionals = f"filtered {filterPredicate} " + internal.defaults((cloneMode, "normal"))
        else:
            optionals = internal.defaults((maskMode, "replace"), (cloneMode, "normal"))
        
        cmd = f"clone {pos1} {pos2} {dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def give(self, target: str, item: str, count: int=1):
        """**Syntax:** *give <target> <item> [count]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((count, 1))

        cmd = f"give {target} {item} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def summon(self, entity: str, pos: str="~ ~ ~", nbt: dict=None):
        """**Syntax:** *summon <entity> [pos] [nbt]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.summon"""
        nbt = json.dumps(nbt) if isinstance(nbt, dict) else nbt
        optionals = internal.defaults((pos, "~ ~ ~"), (nbt, None))

        cmd = f"summon {entity} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clear(self, target: str="@s", item: str=None, maxCount: int=None):
        """**Syntax:** *clear [target] [item] [maxCount]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.clear"""
        internal.reliant('item', maxCount, None, 'data', maxCount, None)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (maxCount, None))

        cmd = f"clear {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def teleport(self, destentity: str=None, destxyz: str=None, target: str="@s", rotation: str=None, faceMode: str=None, facing: str=None, anchor: str="eyes"):
        """**Syntax:** *teleport <target> ...* / *teleport ...*
        * *<destentity>*
        * *<destxyz> [rotation]*
        * *<destxyz> facing <facing>* when faceMode=entity
        * *<destxyz> facing entity <facing> [anchor:eyes|feet]* when faceMode=location\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.teleport"""
        internal.check_spaces('target', target)
        dest = internal.pick_one_arg((destentity, None, 'destentity'), (destxyz, None, 'destxyz'), optional=False)
        target = "" if target == "@s" else target+" "
        internal.check_invalid_params('entity', 'faceMode', faceMode, ('anchor', anchor, "eyes"))
        internal.reliant('destxyz', destxyz, None, 'rotation', rotation, None)
        internal.reliant('destxyz', destxyz, None, 'faceMode', faceMode, None)
        if destentity is None:
            if faceMode is not None:
                internal.options(faceMode, ['location', 'entity'])
                if facing is None:
                    raise ValueError("facing must not be None if faceMode is specified")
                internal.options(anchor, ['eyes', 'feet'])
                faceMode = "facing" if faceMode == "location" else "facing entity"
                optionals = f"{faceMode} {facing} {internal.defaults((anchor, 'eyes'))}"
            else:
                optionals = ""
        else:
            optionals = ""

        cmd = f"teleport {target}{dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    tp = teleport

    def experience(self, mode: str, target: str="@s", amount: int=None, measurement="points"):
        """**Syntax:** *experience ...*
        * *<mode\:add|set> <target> <amount> [measurement:levels|points]*
        * *<mode\:query> <target> <measurement\:levels|points>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.experience"""
        internal.options(measurement, ['points', 'levels'])
        internal.options(mode, ['add', 'set', 'query'])
        internal.multi_check_invalid_params(['add', 'set'], "mode", mode, ("amount", amount, None))
        if mode != "query" and amount is None:
            raise ValueError("amount must not be None if mode is add or set")
        amount = "" if amount is None else str(amount)+" "
        if mode != "query": measurement = internal.defaults((measurement, 'points'))
        cmd = f"experience {mode} {target} {amount}{measurement}".strip()
        self.fh.commands.append(cmd)
        return cmd
    xp = experience
        
    def effect_give(self, target: str, effect: str, seconds: int=30, amplifier: int=0, hideParticles: bool=False):
        """**Syntax:** *effect give <target> <effect> [seconds] [amplifier] [hideParticles]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.effect_give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((seconds, 30), (amplifier, 0), (_b(hideParticles), 'false'))

        cmd = f"effect give {target} {effect} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def effect_clear(self, target: str="@s", effect: str=None):
        """**Syntax:** *effect clear [target] [effect]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.effect_clear"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((effect, None))

        cmd = f"effect clear {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def setworldspawn(self, pos: str="~ ~ ~", angle: str=None):
        """**Syntax:** *setworldspawn [pos] [angle]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spawnpoint"""
        optionals = internal.defaults((pos, "~ ~ ~"), (angle, None))

        cmd = f"setworldspawn {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spawnpoint(self, target: str="@s", pos: str="~ ~ ~", angle: str=None):
        """**Syntax:** *spawnpoint [target] [pos] [angle]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spawnpoint"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((pos, "~ ~ ~"), (angle, None))

        cmd = f"spawnpoint {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    
    def particle(self, name: str, speed: float, count: int, params: str=None, pos: str="~ ~ ~", delta: str="~ ~ ~", mode: str="normal", viewers: str=None):
        """**Syntax:** *particle <name> [params] [pos] [delta] <speed> <count> [mode:force|normal] [viewers]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.particle"""
        optionals = internal.defaults((mode, "normal"), (viewers, None))
        if params is not None:
            name = f"{name} {params}"
        cmd = f"particle {name} {pos} {delta} {speed} {count} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def schedule(self, name: str, clear: bool=False, duration: int=None, mode: str="replace"):
        """**Syntax:** *schedule ...*
        * *function <name> <duration> [mode:append|replace]*
        * *clear <name>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.schedule"""
        internal.check_invalid_params('false', 'clear', _b(clear), ('duration', duration, None), dep_mandatory=True)
        if clear:
            cmd = f"schedule clear {name}".strip()
        else:
            optionals = internal.defaults((mode, 'replace'))
            cmd = f"schedule function {name} {duration} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def playsound(self, sound: str, source: str, target: str, pos: str="~ ~ ~", volume: float=1.0, pitch: float=1.0, minVolume: float=None):
        """**Syntax:** *playsound <sound> <source\:master|music|record|weather|block|hostile|neutral|player|ambient|voice> <targets> <pos> <volume> <pitch> <minVolume>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.playsound"""
        internal.check_spaces('target', target)
        internal.options(source, ['master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice'])
        optionals = internal.defaults((pos, "~ ~ ~"), (volume, 1.0), (pitch, 1.0), (minVolume, None))
        
        cmd = f"playsound {sound} {source} {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def stopsound(self, target: str, source: str="*", sound: str=None):
        """**Syntax:** *stopsound <target> [source:master|music|record|weather|block|hostile|neutral|player|ambient|voice] [sound]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.stopsound"""
        internal.check_spaces('target', target)
        internal.options(source, ['master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice', '*'])
        optionals = internal.defaults((source, "*"), (sound, None))

        cmd = f"stopsound {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def weather(self, mode: str, duration: str=5):
        """**Syntax:** *weather <mode\:clear|rain|thunder> [duration]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.weather"""
        internal.options(mode, ['clear', 'rain', 'thunder'])
        cmd = f"weather {mode} {duration}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def difficulty(self, difficulty: str=None):
        """**Syntax:** *difficulty <difficulty>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.difficulty"""
        if difficulty is None:
            cmd = "difficulty"
        else:
            internal.options(difficulty, ['easy', 'hard', 'normal', 'peaceful', 'e', 'h', 'n', 'p'])
        cmd = f"difficulty {difficulty}"
        self.fh.commands.append(cmd)
        return cmd

    def list_(self, uuid: bool=False):
        """**Syntax** *list* if uuid=False; *list uuid* if uuid=True\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.list_"""
        cmd = "list" if not uuid else "list uuid"
        self.fh.commands.append(cmd)
        return cmd

    def spreadplayers(self, center: str, dist: float, maxRange: float, respectTeams: bool, target: str, maxHeight: float=None):
        """**Syntax**: *spreadplayers <center> <dist> <maxRange> ...*
        * *<respectTeams> <targets>*
        * *under <maxHeight> <respectTeams>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spreadplayers"""
        if maxHeight is not None:
            maxHeight = "under "+maxHeight+" "
        else:
            maxHeight = ""
        cmd = f"spreadplayers {center} {dist} {maxRange} {maxHeight}{_b(respectTeams)} {target}"
        self.fh.commands.append(cmd)
        return cmd

    def replaceitem(self, mode: str, slot: str, item: str, pos: str=None, target: str=None, count: int=1):
        """**Syntax**: *replaceitem <mode\:block|entity> <pos/target> <slot> <item> [count]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.replaceitem"""
        internal.options(mode, ['block', 'entity'])
        internal.check_invalid_params('block', 'mode', mode,
            ('pos', pos, None),
            dep_mandatory=True)
        internal.check_invalid_params('entity', 'mode', mode,
            ('target', target, None),
            dep_mandatory=True)

        pos_target = target if target is not None else pos
        optionals = internal.defaults((count, 1))
        cmd = f"replaceitem {mode} {pos_target} {slot} {item} {optionals}"
        self.fh.commands.append(cmd)
        return cmd

    def scoreboard_objectives(self, mode: str, objective: str=None, criterion: str=None, displayName: str=None, renderType: str=None, slot: str=None):
        """**Syntax**: *scoreboard objectives ...*
        * *<mode\:add> <objective> <criterion> [displayName]*
        * *<mode\:list>*
        * *<mode\:modify(_displayname)|modify(_rendertype)> <objective> ...*
          * *displayName <displayName>* when mode=modify_displayname*
          * *renderType <renderType\:hearts|integer>* when mode=modify_rendertype*
        * *<mode\:remove> <objective>*
        * *<mode\:setdisplay> <slot> [objective]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.scoreboard_objectives"""
        internal.options(mode, ['add', 'list', 'modify_displayname', 'modify_rendertype', 'remove', 'setdisplay'])
        internal.multi_check_invalid_params(['add', 'modify_displayname', 'modify_rendertype', 'remove', 'setdisplay'], 'mode', mode, ('objective', objective, None))
        if mode != 'setdisplay' and objective is None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode, ('criterion', criterion, None), dep_mandatory=True)
        internal.multi_check_invalid_params(['add', 'modify_displayname'], 'mode', mode, ('displayName', displayName, None))
        if mode == 'modify_displayname' and displayName is None:
            raise errors.MissingError('displayName', 'mode', mode)
        internal.check_invalid_params('modify_rendertype', 'mode', mode, ('renderType', renderType, None), dep_mandatory=True)
        if renderType is not None:
            internal.options(renderType, ['hearts', 'integer'])
        internal.check_invalid_params('setdisplay', 'mode', mode, ('slot', slot, None), dep_mandatory=True)

        if mode == "list":
            suffix = ""
        elif mode == "add":
            optionals = internal.defaults((displayName, None))
            suffix = f"{objective} {criterion} {optionals}"
        elif mode == "modify_displayname":
            suffix = f"{objective} displayName {displayName}"
        elif mode == "modify_rendertype":
            suffix = f"{objective} renderType {renderType}"
        elif mode == "remove":
            suffix = objective
        elif mode == "setdisplay":
            optionals = internal.defaults((objective, None))
            suffix = f"{slot} {objective}"

        cmd = f"scoreboard objectives {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def scoreboard_players(self, mode: str, target: str=None, objective: str=None, score: int=None, operation: str=None, source: str=None, sourceObjective: str=None):
        """**Syntax**: *scoreboard players ...*
        * *<mode\:add|set|remove> <target> <objective> <score>*
        * *<mode\:enable|get> <target> <objective>*
        * *<mode\:reset> <target> [objective]*
        * *<mode\:list> [target]*
        * *<mode\:operation> <target> <objective> <operation:+=|-=|*=|/=|%=|<|>|><> <source> <sourceObjective>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.scoreboard_players"""
        internal.options(mode, ['add', 'enable', 'get', 'list', 'operation', 'remove', 'reset', 'set'])
        if mode in ['add', 'enable', 'get', 'operation', 'remove', 'reset', 'set'] and target is None:
            raise errors.MissingError('target', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'enable', 'get', 'operation', 'remove', 'reset', 'set'], 'mode', mode, ('objective', objective, None))
        if mode in ['add', 'enable', 'get', 'operation', 'remove', 'set'] and objective is None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'remove', 'set'], 'mode', mode, ('score', score, None), dep_mandatory=True)
        internal.check_invalid_params('operation', 'mode', mode, 
            ('operation', operation, None),
            ('source', source, None),
            ('sourceObjective', sourceObjective, None),
            dep_mandatory=True)
        if operation is not None:
            internal.options(operation, ['+=', '-=', '*=', '/=', '%=', '<', '>', '><'])

        if mode == "add":
            suffix = f"{target} {objective} {score}"
        elif mode == "enable" or mode == "get":
            suffix = f"{target} {objective}"
        elif mode == "list":
            optionals = internal.defaults((target, None))
            suffix = optionals
        elif mode == "operation":
            suffix = f"{target} {objective} {operation} {source} {sourceObjective}"
        elif mode == "remove" or mode == "set":
            suffix = f"{target} {objective} {score}"
        elif mode == "reset":
            optionals = internal.defaults((objective, None))
            suffix = f"{target} {optionals}"

        cmd = f"scoreboard objectives {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def execute(self, **subcommands):
        """
        **Syntax:** *execute ...*
        * Key is *mode*, value is *value-NAME*, subvalue is *value.SUBVAL*, next subcommand is *-> sc*
        * *<mode\:align> <value-axes> -> sc*
        * *<mode\:anchored> <value-anchor\:eyes|feet> -> sc*
        * *<mode\:as(_)|at|positionedentity|rotatedentity> <value-target> -> sc*
        * *<mode\:facing(xyz)|positionedxyz|rotatedxyz> <value-pos> -> sc*
        * *<mode\:facing(entity)> entity <value.target> <value.anchor\:eyes|feet> -> sc*
        * *<mode\:in(_)> <value-dimension> -> sc*
        * *<mode\:store> <value.store\:result|success> ...*
          * *<value.mode\:block> <value.pos> <value.path> <value.type\:byte|short|int|long|float|double> <value.scale> -> sc*
          * *<value.mode\:bossbar> <value.id> <value.value\:value|max> -> sc*
          * *<value.mode\:score> <value.target> <value.objective> -> sc*
          * *<value.mode\:entity|storage> <value.target> <value.path> <value.type\:byte|short|int|long|float|double> <value.scale> -> sc*
        * *<mode\:if(_)|unless> ...*
          * *<value.mode\:block> <value.pos> <value.block> -> sc*
          * *<value.mode\:blocks> <value.pos1> <value.pos2> <value.destination> <value.scanMode\:all|masked> -> sc*
          * *<value.mode\:data> <value.check\:block> <value.sourcexyz> <value.path> -> sc*
          * *<value.mode\:data> <value.check\:entity|storage> <value.path> -> sc*
          * *<value.mode\:entity> <value.entity> -> sc*
          * *<value.mode\:predicate> <value.predicate> -> sc*
          * *<value.mode\:score> <value.target> <value.targetObjective> <value.comparer:<|<=|=|>|>=> <value.source> <value.sourceObjective> -> sc*
          * *<value.mode\:score> <value.target> <value.targetObjective> <value.comparer\:matches> <value.range> -> sc*
        * *<mode\:run> <value-function> -> sc*

        **subcommands kwargs format:
        ```
        align = axes: str,
        anchored = anchor: str (eyes|feet),
        as_/at = target: str,
        facingxyz = pos: str,
        facingentity = {
            "target": str,
            "anchor": str
        },
        in_ = dimension: str,
        positionedxyz/rotatedxyz = pos: str,
        positionedentity/rotatedxyz = target: str,
        store = {
            "store": str (result|success),
            "mode": str (block|bossbar|entity|score|storage),
            "pos": str (when mode=block),
            "target": str (when mode=entity,score,storage),
            "id": str (when mode=bossbar),
            "value": str (value|max when mode=bossbar),
            "objective": str (when mode=score),
            "path": str (when mode=block,entity,storage),
            "type": str (byte|short|int|long|float|double when mode=block,entity,storage),
            "scale": str (when mode=block,entity,storage)
        },
        if_/unless = {
            "mode": str (block|blocks|data|entity|predicate|score),
            "pos": str (when mode=block),
            "block": str (when mode=block),
            "pos1": str (when mode=blocks),
            "pos2": str (when mode=blocks),
            "destination": str (when mode=blocks),
            "scanMode": str (all|masked when mode=blocks),
            "check": str (block|entity|storage when mode=data),
            "sourcexyz": str (when check=block),
            "sourceentity": str (when check=entity/storage),
            "path": str (when mode=data),
            "entity": str (when mode=entity),
            "predicate": str (when mode=predicate),
            "target": str (when mode=score),
            "objective": str (when mode=score),
            "comparer": str (<|<=|=|>|>=|matches when mode=score),
            "source": str (when comparer!=matches),
            "sourceObjective": str (when comparer!=matches),
            "range": Union[int, str] (when comparer=matches)
        },
        run = function(sf): ...```\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.execute
        """
        if "run" in subcommands.keys() and list(subcommands.keys()).index('run') != len(subcommands.keys())-1:
            raise ValueError("'run' subcommand must be last subcommand")
        
        class subcommandhandler:
            @staticmethod
            def s_align(v):
                if not re.search(r"^(?!.*(.).*\1)[xyz]+$", v):
                    raise ValueError(f"Axes are invalid (Got '{v}')")
                return v+" "
            
            @staticmethod
            def s_anchor(v):
                internal.options(v, ['eyes', 'feet'])
                return v+" "

            @staticmethod
            def s_as_(v):
                internal.check_spaces('as', v)
                return v+" "
            @staticmethod
            def s_at(v):
                internal.check_spaces('at', v)
                return v+" "

            @staticmethod
            def s_facingxyz(v):
                return v+" "
            @staticmethod
            def s_facingentity(v):
                internal.options(v['anchor'], ['eyes', 'feet'])
                return f"entity {v['target']} {v['anchor']} "

            s_in_ = s_facingxyz
            s_positionedxyz = s_facingxyz
            s_rotatedxyz = s_facingxyz

            @staticmethod
            def s_positionedentity(v):
                internal.check_spaces('positionedentity', v)
                return f"as {v} "
            s_rotatedentity = s_positionedentity

            @staticmethod
            def s_store(v):
                internal.options(v['store'], ['result', 'success'])
                internal.options(v['mode'], ['block', 'bossbar', 'entity', 'score', 'storage'])
                prefix = f"{v['store']} {v['mode']}"
                if 'type' in v.keys():
                    internal.options(v['type'], ['byte', 'short', 'int', 'long', 'float', 'double'])
                if v['mode'] == 'block':
                    return f"{prefix} {v['pos']} {v['path']} {v['type']} {v['scale']} "
                elif v['mode'] == 'bossbar':
                    internal.options(v['value'], ['max', 'value'])
                    return f"{prefix} {v['id']} {v['value']} "
                elif v['mode'] in ['entity', 'storage']:
                    return f"{prefix} {v['target']} {v['path']} {v['type']} {v['scale']} "
                elif v['mode'] == 'score':
                    return f"{prefix} {v['target']} {v['objective']} "

            @staticmethod
            def s_if_(v):
                internal.options(v['mode'], ['block', 'blocks', 'data', 'entity', 'predicate', 'score'])
                prefix = v['mode']
                if v['mode'] == "block":
                    return f"{prefix} {v['pos']} {v['block']} "
                elif v['mode'] == "blocks":
                    return f"{prefix} {v['pos1']} {v['pos2']} {v['dest']} {v['scanMode']} "
                elif v['mode'] == "entity":
                    return f"{prefix} {v['entity']} "
                elif v['mode'] == "predicate":
                    return f"{prefix} {v['predicate']} "
                elif v['mode'] == "data":
                    internal.options(v['check'], ['block', 'entity', 'storage'])
                    source_sourcePos = v['sourcePos'] if v['check'] == 'block' else v['source']
                    return f"{prefix} {v['check']} {source_sourcePos} {v['path']} "
                elif v['mode'] == "score":
                    internal.options(v['comparer'], ['<', '<=', '=', '>', '>=', 'matches'])
                    internal.check_spaces('target', v['target'])
                    if v['comparer'] == "matches":
                        return f"{prefix} {v['target']} {v['objective']} matches {v['range']} "
                    else:
                        return f"{prefix} {v['target']} {v['objective']} {v['comparer']} {v['source']} {v['sourceObjective']} "
            s_unless = s_if_

            @staticmethod
            def s_run(v):
                return ""


        cmd = "execute "
        for k, v in subcommands.items():
            scn = k if not k.endswith("_") else k[:-1]
            if scn.endswith("xyz") or scn.endswith("entity"):
                scn = scn.replace("xyz", "").replace("entity", "")
            cmd += scn + " " + getattr(subcommandhandler, 's_'+k)(v)

        if 'run' in subcommands.keys():
            sf = JavaFuncHandler()
            result = subcommands['run'](sf)
            if isinstance(result, (list, tuple)):
                result = map(lambda j: (cmd+j).strip(), result)
                self.fh.commands.extend(result)
                return result
            elif isinstance(result, str):
                self.fh.commands.append((cmd+result).strip())
                return result
            else:
                result = sf.commands
                result = map(lambda j: (cmd+j).strip(), result)
                self.fh.commands.extend(result)
                return result
            

        else:
            self.fh.commands.append(cmd.strip())
            return cmd.strip()

    def item(self, mode: str, slot: str, pos: str=None, target: str=None, replaceMode: str=None, item: str=None, count: int=None, sourcexyz: str=None, sourceentity: str=None, sourceSlot: str=None, modifier: str=None):
        """**Syntax:** *item <mode\:modify|replace> {block <pos>|entity <target>} <slot> ...*
        * *<modifier>* if mode=modify
        * *<replaceMode\:with> <item> [count]* if mode=replace
        * *<replaceMode\:from> {block <sourcexyz>|entity <sourceentity>} <sourceSlot> [modifier]* if mode=replace\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.item"""
        internal.options(mode, ['modify', 'replace'])
        if mode == "modify" and modifier is None:
            raise errors.MissingError('modifier', 'mode', mode)
        
        internal.check_invalid_params('replace', 'mode', mode,
            ('replaceMode', replaceMode, None))
        if replaceMode is not None:
            internal.options(replaceMode, ['from', 'with'])
        internal.check_invalid_params('with', 'replaceMode', replaceMode,
            ('item', item, None),
            dep_mandatory=True)
        internal.check_invalid_params('with', 'replaceMode', replaceMode,
            ('count', count, None))
        internal.check_invalid_params('from', 'replaceMode', replaceMode,
            ('sourceSlot', sourceSlot, None),
            dep_mandatory=True)
        internal.check_invalid_params('from', 'replaceMode', replaceMode,
            ('sourceSlot', sourceSlot, None))

        target_pos = internal.pick_one_arg((target, None, 'target'), (pos, None, 'pos'), optional=False)
        
        target_pos = ("block " if pos is not None else "entity ") + target_pos
        

        if mode == "modify":
            suffix = modifier
        elif replaceMode == "with":
            optionals = internal.defaults((count, None))
            suffix = f"with {item} {optionals}"
        else:
            source = internal.pick_one_arg((sourcexyz, None, 'sourcexyz'), (sourceentity, None, 'sourceentity'), optional=True)
            source = ("block " if sourcexyz is not None else "entity ") + source
            optionals = internal.defaults((modifier, None))
            suffix = f"from {source} {sourceSlot} {optionals}"

        cmd = f"item {mode} {target_pos} {slot} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def advancement(self, task: str, target: str, mode: str, advancement: str=None, criterion: str=None):
        """**Syntax:** *advancement <task\:grant|revoke> <target> ...*
        * *<mode\:everything>*
        * *<mode\:only> <advancement> [criterion]*
        * *<mode\:from|through|until> <advancement>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.advancement"""
        internal.options(task, ['grant', 'revoke'])
        internal.options(mode, ['everything', 'only', 'from', 'through', 'until'])
        internal.multi_check_invalid_params(['only', 'from', 'through', 'until'], 'mode', mode, 
            ('advancement', advancement, None),
            dep_mandatory=True)
        internal.check_invalid_params('only', 'mode', mode, ('criterion', criterion, None))
        
        if mode == "everything":
            suffix = ""
        else:
            optionals = internal.defaults((criterion, None))
            suffix = f"{advancement} {optionals}"
        cmd = f"advancement {task} {target} {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def attribute(self, target: str, attribute: str, mode: str, scale: int=None, uuid: str=None, name: str=None, value: str=None, addMode: str=None):
        """**Syntax:** *attribute <target> <attribute> ...*
        * *<mode\:get|base(_)get> [scale]*
        * *<mode\:base(_)set> <value>*
        * *<mode\:modifier(_)add> <uuid> <name> <value> <addMode\:add|multiply|multiply_base>
        * *<mode\:modifier(_)remove> <uuid>
        * *<mode\:modifier(_)value(_)get> <uuid> [scale]\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.attribute"""
        internal.options(mode, ['get', 'base_get', 'base_set', 'modifier_add', 'modifier_remove', 'modifier_value_get'])
        internal.multi_check_invalid_params(['get', 'base_get', 'modifier_value_get'], 'mode', mode,
            ('scale', scale, None))
        internal.multi_check_invalid_params(['modifier_add', 'modifier_remove', 'modifier_value_get'], 'mode', mode,
            ('uuid', uuid, None),
            dep_mandatory=True)
        internal.check_invalid_params('modifier_add', 'mode', mode,
            ('name', name, None),
            ('addMode', addMode, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['base_set', 'modifier_add'], 'mode', mode,
            ('value', value, None),
            dep_mandatory=True)
        if addMode is not None:
            internal.options(addMode, ['add', 'multiply', 'multiply_base'])
        
        if mode == "modifier_add":
            suffix = f"{uuid} {name} {value} {addMode}"
        elif mode in ['modifier_remove', 'modifier_value_get']:
            optionals = internal.defaults((scale, None))
            suffix = f"{uuid} {optionals}"
        elif mode in ['get', 'base_get']:
            suffix = internal.defaults((scale, None))
        elif mode == "base_set":
            suffix = value
        mode = mode.replace('_', ' ')
        cmd = f"attribute {target} {attribute} {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ban(self, target: str, reason: str=None):
        """**Syntax:** *ban <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.ban"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((reason, None))
        cmd = f"ban {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ban_ip(self, target: str, reason: str=None):
        """**Syntax:** *ban-ip <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.ban_ip"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((reason, None))
        cmd = f"ban-ip {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def banlist(self, get="players"):
        """**Syntax:** *banlist <get\:players|ips>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.banlist"""
        internal.options(get, ['ips', 'players'])
        optionals = internal.defaults((get, "players"))
        cmd = f"banlist {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_add(self, barId: str, name: str):
        """**Syntax:** *bossbar add <barId> <name>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_add"""
        cmd = f"bossbar add {barId} {name}"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_get(self, barId: str, get: str):
        """**Syntax:** *bossbar get <barId> <get\:max|players|value|visible>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_get"""
        internal.options(get, ['max', 'players', 'value', 'visible'])
        cmd = f"bossbar get {barId} {get}"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_list(self):
        """**Syntax:** *bossbar list*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_list"""
        cmd = "bossbar list"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_remove(self, barId: str):
        """**Syntax:** *bossbar remove <barId>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_remove"""
        cmd = f"bossbar remove {barId}"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_set(self, barId: str, mode: str, color: str=None, maxv: int=None, name: str=None, target: str=None, style: str=None, value: int=None, visible: bool=None):
        """**Syntax:** *bossbar set <barId>*
        * *<mode\:color> <color\:blue|green|pink|purple|red|white|yellow>*
        * *<mode\:max> <maxv>*
        * *<mode\:name> <name>*
        * *<mode\:players> [target]*
        * *<mode\:style> <style\:notched_6|notched_10|notched_12|notched_20|progress>*
        * *<mode\:value> <value>*
        * *<mode\:visible> <visible>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_set"""
        internal.options(mode, ['color', 'max', 'name', 'players', 'style', 'value', 'visible'])
        internal.check_invalid_params('color', 'mode', mode,
            ('color', color, None),
            dep_mandatory=True)
        if color is not None:
            internal.options(color, ['blue', 'green', 'pink', 'purple', 'red', 'white', 'yellow'])
        internal.check_invalid_params('max', 'mode', mode,
            ('maxv', maxv, None),
            dep_mandatory=True)
        internal.check_invalid_params('name', 'mode', mode,
            ('name', name, None),
            dep_mandatory=True)
        internal.check_invalid_params('players', 'mode', mode,
            ('target', target, None))
        internal.check_invalid_params('style', 'mode', mode,
            ('style', style, None),
            dep_mandatory=True)
        if style is not None:
            internal.options(style, ['notched_6', 'notched_10', 'notched_12', 'notched_20', 'progress'])
        internal.check_invalid_params('value', 'mode', mode,
            ('value', value, None),
            dep_mandatory=True)
        internal.check_invalid_params('visible', 'mode', mode,
            ('visible', visible, None),
            dep_mandatory=True)

        v = internal.pick_one_arg(
            (color, None, 'color'),
            (maxv, None, 'maxv'),
            (name, None, 'name'),
            (target, None, 'target'),
            (style, None, 'style'),
            (value, None, 'value'),
            (_b(visible), None, 'visible')
        )
        cmd = f"bossbar set {barId} {mode} {v}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_get(self, block: str=None, entity: str=None, storage: str=None, path: str=None, scale: float=None):
        """**Syntax:** *data get {block <pos>|entity <target>|storage <storage>} [path] [scale]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_get"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        internal.reliant('path', path, None, 'scale', scale, None)
        optionals = internal.defaults((path, None), (scale, None))

        cmd = f"data get {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_remove(self, path: str, block: str=None, entity: str=None, storage: str=None):
        """**Syntax:** *data remove {block <pos>|entity <target>|storage <storage>} <path>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_remove"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        cmd = f"data get {target} {path}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_merge(self, nbt: dict, block: str=None, entity: str=None, storage: str=None):
        """**Syntax:** *data merge {block <pos>|entity <target>|storage <storage>} <nbt>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_merge"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        cmd = f"data merge {target} {json.dumps(nbt)}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_modify(self, mode: str, sourceMode: str, path: str, block: str=None, entity: str=None, storage: str=None, index: str=None, sourceBlock: str=None, sourceEntity: str=None, sourceStorage: str=None, sourcePath: str=None, value: str=None):
        """**Syntax:** *data modify {block <pos>|entity <target>|storage <storage>} <path> <mode\:append|insert|merge|prepend|set> <mode=insert:index> ...*
        * *<sourceMode\:from> {block <sourcePos>|entity <sourceTarget>|storage <sourceStorage>} [sourcePath]*
        * *<sourceMode\:value> <value>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_modify"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        source = internal.pick_one_arg(
            (sourceBlock, None, 'block'),
            (sourceEntity, None, 'entity'),
            (sourceStorage, None, 'storage')
        )
        internal.options(mode, ['append', 'insert', 'merge', 'prepend', 'set'])
        internal.check_invalid_params('insert', 'mode', mode,
            ('index', index, None),
            dep_mandatory=True)
        internal.options(sourceMode, ['from', 'value'])
        internal.check_invalid_params('from', 'sourceMode', sourceMode,
            ('source', source, None),
            dep_mandatory=True)
        internal.check_invalid_params('from', 'sourceMode', sourceMode,
            ('sourcePath', sourcePath, None))
        internal.check_invalid_params('value', 'sourceMode', sourceMode,
            ('value', value, None))
        
        if source is not None:
            source = ('block ' if sourceBlock is not None else 'entity ' if sourceEntity is not None else 'storage') + source

        if sourceMode == "from":
            optionals = internal.defaults((sourcePath, None))
            suffix = f"{source} {optionals}"
        else:
            suffix = json.dumps(value)
        if mode == "index":
            mode = f"{mode} {index}"
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        cmd = f"data modify {target} {path} {mode} {sourceMode} {suffix}"
        self.fh.commands.append(cmd)
        return cmd

    def datapack(self, mode: str, name: str=None, priority: str=None, existing: str=None, listMode: str=None):
        """**Syntax:** *datapack ...*
        * *<mode\:disable> <name>*
        * *<mode\:enable> <name> [priority:first|last|before|after] [priority=before|after:existing]*
        * *<mode\:list> [listMode:available|enabled]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.datapack"""
        internal.options(mode, ['disable', 'enable', 'list'])
        internal.multi_check_invalid_params(['disable', 'enable'], 'mode', mode,
            ('name', name, None),
            dep_mandatory=True)
        internal.check_invalid_params('enable', 'mode', mode,
            ('priority', priority, None),
            dep_mandatory=None)
        if priority is not None:
            internal.options(priority, ['first', 'last', 'before', 'after'])
        internal.multi_check_invalid_params(['before', 'after'], 'priority', priority,
            ('existing', existing, None),
            dep_mandatory=True)
        internal.check_invalid_params('list', 'mode', listMode,
            ('listMode', listMode, None),
            dep_mandatory=True)
        if listMode is not None:
            internal.options(listMode, ['available', 'ended'])

        if mode == "list":
            suffix = listMode
        elif mode == "disable":
            suffix = name
        else:
            optionals = internal.defaults((priority, None), (existing, None))
            suffix = f"{name} {optionals}"
        cmd = f"datapack {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def debug(self, mode: str):
        """**Syntax:** *debug <mode\:start|stop|report|function>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.debug"""
        internal.options(mode, ['start', 'stop', 'report', 'function'])
        cmd = f"debug {mode}"
        self.fh.commands.append(cmd)
        return cmd

    def defaultgamemode(self, mode: str):
        """**Syntax:** *defaultgamemode <mode\:survival|creative|adventure|spectator>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.defaultgamemode"""
        internal.options(mode, ['survival', 'creative', 'adventure', 'spectator'])
        cmd = f"defaultgamemode {mode}"
        self.fh.commands.append(cmd)
        return cmd

    def forceload(self, mode: str, chunk: str=None, chunk2: str=None):
        """**Syntax:** *forceload ...*
        * *<mode\:add|remove> <chunk> [chunk2]*
        * *<mode\:remove(_)all>*
        * *<mode\:query> [chunk]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.forceload"""
        internal.options(mode, ['add', 'remove', 'remove_all', 'query'])
        internal.multi_check_invalid_params(['add', 'remove', 'query'], 'mode', mode,
            ('chunk', chunk, None))
        if mode in ['add', 'remove'] and chunk is None:
            raise errors.MissingError('chunk', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'remove'], 'mode', mode,
            ('chunk2', chunk2, None))

        if mode == "remove_all":
            suffix = ""
        elif mode == "query":
            suffix = internal.defaults((chunk, None))
        else:
            optionals = internal.defaults((chunk2, None))
            suffix = f"{chunk} {optionals}"

        mode = mode.replace('_', ' ')
        cmd = f"forceload {mode} {suffix}"
        self.fh.commands.append(cmd)
        return cmd

    def locatebiome(self, biomeId: str):
        """**Syntax:** *locatebiome <biomeId>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.locatebiome"""
        cmd = f"locatebiome {biomeId}"
        self.fh.commands.append(cmd)
        return cmd
    
    def loot(self, targetMode: str, sourceMode: str, targetPos: str=None, targetEntity: str=None, targetSlot: str=None, \
             targetCount: int=None, sourceLootTable: str=None, sourcePos: str=None, sourceEntity: str=None, sourceTool: str=None):
        """ **Syntax:** *loot ...*

        * *<targetMode\:spawn> <targetPos>...*
        * *<targetMode\:replace> {entity <targetEntity>|block <targetPos>}...*
        * *<targetMode\:give> <targetEntity>...*
        * *<targetMode\:insert> <targetPos>...*\n
        *...*
        * *<sourceMode\:fish> <sourceLootTable> <sourcePos> [sourceTool]*
        * *<sourceMode\:loot> <sourceLootTable>*
        * *<sourceMode\:kill> <sourceEntity>*
        * *<sourceMode\:mine> <sourcePos> [sourceTool]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.loot"""
        internal.options(targetMode, ['spawn', 'replace', 'give', 'insert'])
        internal.multi_check_invalid_params(['spawn', 'replace', 'insert'], 'targetMode', targetMode,
            ('targetPos', targetPos, None))
        if targetMode in ['spawn', 'insert'] and targetPos is None:
            raise errors.MissingError('targetPos', 'targetMode', targetMode)
        internal.multi_check_invalid_params(['give', 'replace'], 'targetMode', targetMode,
            ('targetEntity', targetEntity, None))
        if targetMode == 'give' and targetEntity is None:
            raise errors.MissingError('targetEntity', 'targetMode', targetMode)
        internal.check_invalid_params('replace', 'targetMode', targetMode,
            ('targetSlot', targetSlot, None),
            dep_mandatory=True)
        internal.check_invalid_params('replace', 'targetMode', targetMode,
            ('targetCount', targetCount, None))
        targetPosEntity = internal.pick_one_arg(
            (targetPos, None, 'targetPos'),
            (targetEntity, None, 'targetEntity')
        )
        targetPosEntity = ('block ' if targetPos is not None else 'entity ') + targetPosEntity

        if targetMode in ['spawn', 'insert']:
            target = f"{targetMode}, {targetPos}".strip()
        elif targetMode == "give":
            target = f"{targetMode} {targetEntity}".strip()
        else:
            optionals = internal.defaults((targetCount, None))
            target = f"{targetMode} {targetPosEntity} {targetSlot} {optionals}".strip()

        internal.multi_check_invalid_params(['fish', 'loot'], 'sourceMode', sourceMode,
            ('sourceLootTable', sourceLootTable, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['fish', 'mine'], 'sourceMode', sourceMode,
            ('sourcePos', sourcePos, None),
            dep_mandatory=True)
        internal.check_invalid_params('kill', 'sourceMode', sourceMode,
            ('sourceEntity', sourceEntity, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['fish', 'mine'], 'sourceMode', sourceMode,
            ('sourceTool', sourceTool, None))

        if sourceMode == 'fish':
            optionals = internal.defaults((sourceTool, None))
            source = f"{sourceMode} {sourceLootTable} {sourcePos} {optionals}".strip()
        elif sourceMode == 'loot':
            source = f"{sourceMode} {sourceLootTable}".strip()
        elif sourceMode == 'kill':
            source = f"{sourceMode} {sourceEntity}".strip()
        else:
            optionals = internal.defaults((sourceTool, None))
            source = f"{sourceMode} {optionals}".strip()

        cmd = f"loot {target} {source}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def pardon(self, target: str, reason: str=None):
        """**Syntax:** *pardon <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.pardon"""
        internal.check_spaces('target', target)
        cmd = f"pardon {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def pardon_ip(self, target: str, reason: str=None):
        """**Syntax:** *pardon-ip <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.pardon_ip"""
        internal.check_spaces('target', target)
        cmd = f"pardon-ip {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def publish(self, port: int):
        """**Syntax:** *publish <port>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.publish"""
        cmd = f"publish {port}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def recipe(self, mode: str, target: str, recipe: str):
        """**Syntax:** *recipe <mode\:give|take> <target> <recipe>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.recipe"""
        internal.options(mode, ['give', 'take'])
        internal.check_spaces('target', target)
        cmd = f"recipe {mode} {target} {recipe}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def save_all(self, flush: bool=False):
        """**Syntax:**
        * *save-all flush* if flush=True
        * *save-all* if flush=False\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.save_all"""
        if flush: cmd = "save-all flush"
        else: cmd = "save-all"
        self.fh.commands.append(cmd)
        return cmd

    def save_on(self):
        """**Syntax:** *save-on*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.save_on"""
        self.fh.commands.append("save-on")
        return "save-on"

    def save_off(self):
        """**Syntax:** *save-off*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.save_off"""
        self.fh.commands.append("save-off")
        return "save-off"

    def seed(self):
        """**Syntax:** *seed*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.seed"""
        self.fh.commands.append("seed")
        return "seed"

    def setidletimeout(self, mins: int):
        """**Syntax:** *setidletimeout <mins>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.setidletimeout"""
        cmd = f"setidletimeout {mins}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spectate(self, target: str=None, spectator: str=None):
        """**Syntax:** *spectate [target] [spectator]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spectate"""
        internal.reliant('target', target, None, 'spectator', spectator, None)
        optionals = internal.defaults((target, None), (spectator, None))
        cmd = f"spectate {optionals}".strip()
        return cmd

    def team(self, mode: str, team: str=None, members: str=None, displayName: str=None, option: str=None, value=None):
        """**Syntax:** *team ...*
        * *<mode\:add> [displayName]*
        * *<mode\:empty|remove> <team>*
        * *<mode\:join> <team> [members]*
        * *<mode\:list> [team]*
        * *<mode\:modify> [team] ...*
          * *<option\:collisionRule> <value\:always|never|pushOtherTeams|pushOwnTeam>*
          * *<option\:color> <value\:aqua|black|blue|gold|gray|green|light_purple|red|reset|yellow|white|dark_aqua|dark_blue|dark_gray|dark_green|dark_purle|dark_red>*
          * *<option\:deathMessageVisibility|nametagVisibility> <value\:always|never|hideForOtherTeams|hideForOwnTeam>*
          * *<option\:friendlyFire|seeFriendlyInvisibles> <value\:True|False>*
          * *<option\:displayName|prefix|suffix> <value>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.team"""
        internal.options(mode, ['add', 'empty', 'join', 'leave', 'list', 'modify', 'remove'])
        internal.multi_check_invalid_params(['add', 'empty', 'join', 'list', 'modify', 'remove'], 'mode', mode,
            ('team', team, None))
        if mode in ['add', 'empty', 'join', 'modify', 'remove'] and team is None:
            raise errors.MissingError('team', 'mode', mode)
        internal.multi_check_invalid_params(['join', 'leave'], 'mode', mode,
            ('members', members, None))
        if mode == 'leave' and members is None:
            raise errors.MissingError('members', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode,
            ('displayName', displayName, None))
        internal.check_invalid_params('modify', 'mode', mode,
            ('option', option, None),
            ('value', value, None),
            dep_mandatory=True)
        if option is not None:
            internal.options(option, ['collisionRule', 'color', 'deathMessageVisibility', 'displayName', 'friendlyFire', 'nametagVisibility', 'prefix', 'seeFriendlyInvisibles', 'suffix'])
            VALS = {
                "collisionRule": ['always', 'never', 'pushOtherTeams', 'pushOwnTeam'],
                "color": ['aqua', 'black', 'blue', 'gold', 'gray', 'green', 'light_purple', 'red', 'reset', 'yellow', 'white', 'dark_aqua', 'dark_blue', 'dark_gray', 'dark_green', 'dark_purle', 'dark_red'],
                "deathMessageVisibility": ['always', 'never', 'hideForOtherTeams', 'hideForOwnTeam'],
                "nameTagVisibility": ['always', 'never', 'hideForOtherTeams', 'hideForOwnTeam'],
            }
            if option in VALS.keys():
                internal.options(value, VALS[option])
        
        if mode == "add":
            optionals = internal.defaults((displayName, None))
            suffix = f"{team} {optionals}"
        elif mode in ['empty', 'remove']:
            suffix = team
        elif mode == "join":
            optionals = internal.defaults((members, None))
            suffix = f"{team} {optionals}"
        elif mode == "leave":
            suffix = members
        elif mode == "list":
            suffix = internal.defaults((team, None))
        else:
            suffix = f"{team} {option} {value}"

        cmd = f"team {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def teammsg(self, message: str):
        """**Syntax:** *teammsg <message>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.teammsg"""
        cmd = f"teammsg {message}".strip()
        self.fh.commands.append(cmd)
        return cmd
    tm = teammsg

    def trigger(self, objective: str, mode: str=None, value: int=None):
        """**Syntax:** *trigger <objective> ...*
        * *<mode\:(None)>*
        * *<mode\:add|set> <value>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.trigger"""
        internal.reliant('mode', mode, None, 'value', value, None)
        internal.unstated('mode', mode, ['add', 'set'], 'value', value, None)
        if mode is not None:
            internal.options(mode, ['add', 'set'])
        optionals = internal.defaults((mode, None), (value, None))
        cmd = f"trigger {objective} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_add(self, distance: float, duration: int=0):
        """**Syntax:** *worldborder add <distance> [duration]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_add"""
        optionals = internal.defaults((duration, 0))
        cmd = f"worldborder add {distance} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_center(self, pos: str):
        """**Syntax:** *worldborder center <pos>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_center"""
        cmd = f"worldborder center {pos}"
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_damage(self, damagePerBlock: float=None, distance: float=None):
        """**Syntax:** *worldborder damage {amount <damagePerBlock>|buffer <distance>}*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_damage"""
        value = internal.pick_one_arg(
            (damagePerBlock, None, 'damagePerBlock'),
            (distance, None, 'distance'),
            optional=False
        )

        middle = "amount" if damagePerBlock is not None else "buffer"
        cmd = f"worldborder damage {middle} {value}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_get(self):
        """**Syntax:** *worldborder get*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_get"""
        cmd = "worldborder get"
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_set(self, distance: float=None, duration: int=0):
        """**Syntax:** *worldborder set <distance> [duration]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_set"""
        optionals = internal.defaults((duration, 0))
        cmd = f"worldborder add {distance} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_warning(self, distance: float=None, duration: int=None):
        """**Syntax:** *worldborder warning {distance <distance>|time <duration>}*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_warning"""
        value = internal.pick_one_arg(
            (distance, None, 'distance'),
            (duration, None, 'duration'),
            optional=False
        )

        middle = "distance" if distance is not None else "time"
        cmd = f"worldborder warning {middle} {value}".strip()
        cmd = "worldborder get"
        self.fh.commands.append(cmd)
        return cmd
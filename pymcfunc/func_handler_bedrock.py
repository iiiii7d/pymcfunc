from typing import Union, Callable
import json

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_universal import UniversalFuncHandler, UniversalRawCommands
from pymcfunc.selectors import BedrockSelectors

class BedrockFuncHandler(UniversalFuncHandler):
    """The Beckrock Edition function handler.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler"""
    sel = BedrockSelectors()

    def __init__(self):
        self.commands = []
        self.r = BedrockRawCommands(self)

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
        """**Syntax:** *summon <entity> ...*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.summon"""
        if event == None:
            optionals = internal.defaults((pos, "~ ~ ~"))
            nameTag = internal.unspace(nameTag)
            cmd = f"summon {entity} {nameTag} {optionals}".strip()
        else:
            optionals = internal.defaults((pos, "~ ~ ~"), (event, None), (nameTag, None))
            if event != None: event = internal.unspace(event)
            if nameTag != None: nameTag = internal.unspace(nameTag)
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
        if destentity == None:
            rotation_facing = internal.pick_one_arg((rotation, None, 'rotation'), (facing, None, 'facing'))
            if rotation_facing != None:
                if facing != None: rotation_facing = "facing "+rotation_facing
                optionals = f"{rotation_facing} {internal.defaults((checkForBlocks, False))}"
            else:
                optionals = internal.defaults((checkForBlocks, False))
        else:
            optionals = internal.defaults((checkForBlocks, False))

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
        optionals = internal.defaults((seconds, 30), (amplifier, 0), (hideParticles, False))

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
        if slotType == None and mode == "block":
            slotType = "slot.container"
        if itemHandling == None:
            itemHandling = ""
        else:
            internal.options(itemHandling, ['destroy', 'keep'])
            itemHandling += " "
        if components != None: components = json.dumps(components)
        pos_target = target if target != None else pos
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
        if mode in ['add', 'remove'] and objective == None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode, ('displayName', displayName, None), dep_mandatory=True)
        internal.check_invalid_params('setdisplay', 'mode', mode, ('slot', slot, None), dep_mandatory=True)
        if slot != None:
            internal.options(slot, ['list', 'sidebar', 'belowname'])
            internal.multi_check_invalid_params(['list', 'sidebar'], 'mode', mode, ('sortOrder', sortOrder, None))
            if sortOrder != None:
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
        if mode in ['reset', 'test', 'random', 'set', 'add', 'remove', 'operation'] and target == None:
            raise errors.MissingError('target', 'mode', mode)
        internal.multi_check_invalid_params(['reset', 'test', 'random', 'set', 'add', 'remove', 'operation'], 'mode', mode, ('objective', objective, None))
        if mode in ['test', 'random', 'set', 'add', 'remove', 'operation'] and objective == None:
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
        if operation != None:
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
        if detectPos != None:
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
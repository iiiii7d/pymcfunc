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
        internal.check_invalid_params('add', 'mode', mode, ('displayName', displayName, None), dep_mandatory=True)
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
        optionals = internal.defaults((ability, None), (value, None))
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
        internal.defaults((lock, None))
        cmd = f"alwaysday {lock}".strip()
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
            (allow_cheats, None, 'allow_cheats'),
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
        cmd = f"globalpause {pause}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def immutableworld(self, immutable: bool=None):
        """**Syntax:** *immutableworld [immutable]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockRawCommands.immutableworld"""
        optionals = internal.defaults((immutable, None))
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
        optionals = internal.defaults((value, None))
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
        optionals = internal.defaults((includesEntities, True), (saveMode, 'disk'), (includesBlocks, True))
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
            optional_list = [(rotation, '0_degrees'), (mirror, 'none'), (animationMode, None), (animationSeconds, 1), (includesEntities, True), (includesBlocks, True), (integrity, 100), (seed, None)]
        else:
            optional_list = [(rotation, '0_degrees'), (mirror, 'none'), (includesEntities, True), (includesBlocks, True), (integrity, 100), (seed, None)]

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
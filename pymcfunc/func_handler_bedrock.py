from typing import Union

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
    def setblock(self, pos: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace"):
        """Adds a /setblock command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates"))
        optionals = internal.defaults((tileData_blockStates, None), (mode, "replace"))

        cmd = f"setblock {pos} {tileName} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace", replaceTileName: str=None, replaceDataValue: int=None):
        """Adds a /fill command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.fill"""
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
        """Adds a /clone command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.clone"""
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
        """Adds a /give command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((amount, 1), (data, 0), (components, None))

        cmd = f"give {target} {item} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def summon(self, entity: str, pos: str="~ ~ ~", event: str=None, nameTag: str=None):
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
        internal.reliant('item', item, None, 'data', data, -1)
        internal.reliant('item', maxCount, None, 'data', maxCount, -1)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (data, -1), (maxCount, -1))

        cmd = f"clear {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def teleport(self, destxyz: str=None, destentity: str=None, target: str="@s", facing: str=None, rotation: str=None, checkForBlocks: bool=False):
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

    def experience(self, amount: int, level: bool=False, target: str="@s"):
        internal.check_spaces('target', target)
        level = "L" if level else ""
        optionals = internal.defaults((target, "@s"))

        cmd = f"experience {amount}{level} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    xp = experience

    def effect_give(self, target: str, effect: str, seconds: int=30, amplifier: int=0, hideParticles: bool=False):
        internal.check_spaces('target', target)
        optionals = internal.defaults((seconds, 30), (amplifier, 0), (hideParticles, False))

        cmd = f"effect {target} {effect} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def effect_clear(self, target: str):
        internal.check_spaces('target', target)

        cmd = f"effect {target} clear".strip()
        self.fh.commands.append(cmd)
        return cmd

    def setworldspawn(self, pos: str="~ ~ ~"):
        optionals = internal.defaults((pos, "~ ~ ~"))

        cmd = f"setworldspawn {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spawnpoint(self, target: str="@s", pos: str="~ ~ ~"):
        internal.check_spaces('target', target)
        optionals = internal.defaults((pos, "~ ~ ~"))

        cmd = f"spawnpoint {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def particle(self, name: str, pos: str):
        cmd = f"particle {name} {pos}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def schedule(self, path: str, mode: str, pos1: str=None, pos2: str=None, center: str=None, radius: int=None, tickingAreaName: str=None):
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
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@p"), (pos, "~ ~ ~"), (volume, 1.0), (pitch, 1.0), (minVolume, None))
        cmd = f"playsound {sound} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def stopsound(self, target: str, sound: str=None):
        internal.check_spaces('target', target)
        optionals = internal.defaults((sound, None))

        cmd = f"stopsound {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def weather(self, mode: str, duration: str=5):
        internal.options(mode, ['clear', 'rain', 'thunder', 'query'])
        if mode == "query":
            cmd = "weather query"
        else:
            cmd = f"weather {mode} {duration}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def difficulty(self, difficulty: Union[str, int]):
        internal.options(difficulty, ['easy', 'hard', 'normal', 'peaceful', 'e', 'h', 'n', 'p', 0, 1, 2, 3])
        cmd = f"difficulty {difficulty}"
        self.fh.commands.append(cmd)
        return cmd
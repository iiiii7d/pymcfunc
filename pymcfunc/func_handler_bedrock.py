from typing import Union

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_universal import UniversalFuncHandler
from pymcfunc.selectors import BedrockSelectors

class BedrockFuncHandler(UniversalFuncHandler):
    """The Beckrock Edition function handler.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler"""
    sel = BedrockSelectors()

    def __init__(self):
        self.commands = []

    def setblock(self, pos: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace"):
        """Adds a /setblock command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates"))
        optionals = internal.defaults((tileData_blockStates, None), (mode, "replace"))

        cmd = f"setblock {pos} {tileName} {optionals}".strip()
        self.commands.append(cmd)
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
        self.commands.append(cmd)
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
        self.commands.append(cmd)
        return cmd

    def give(self, target: str, item: str, amount: int=1, data: int=0, components: dict=None):
        """Adds a /give command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((amount, 1), (data, 0), (components, None))

        cmd = f"give {target} {item} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def gamemode(self, mode: Union[int, str], target: str="@s"):
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"))
        internal.options(mode, ['survival', 'creative', 'adventure', 's', 'c', 'a', 0, 1, 2])

        cmd = f"gamemode {mode} {optionals}".strip()
        self.commands.append(cmd)
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
        
        self.commands.append(cmd)
        return cmd

    def clear(self, target: str="@s", item: str=None, data: int=-1, maxCount: int=-1):
        internal.reliant('item', item, None, 'data', data, -1)
        internal.reliant('item', maxCount, None, 'data', maxCount, -1)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (data, -1), (maxCount, -1))

        cmd = f"clear {optionals}"
        self.commands.append(cmd)
        return cmd
        
        
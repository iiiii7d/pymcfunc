import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_universal import UniversalFuncHandler

class BedrockFuncHandler(UniversalFuncHandler):
    def __init__(self):
        self.commands = []

    def setblock(self, pos: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace"):
        internal.options(mode, ['destroy', 'keep', 'replace'])
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates"))
        optionals = internal.defaults((tileData_blockStates, None), (mode, "replace"))

        cmd = f"setblock {pos} {tileName} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, block: str, tileData: int=0, blockStates: list=None, mode="replace", replaceTileName: str=None, replaceDataValue: int=None):
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace' and replaceTileName != None:
            raise errors.InvalidParameterError('replace', 'mode', mode, 'replaceTileName')
        elif mode != 'replace' and replaceDataValue != None:
            raise errors.InvalidParameterError('replace', 'mode', mode, 'replaceDataValue')
        internal.reliant('replaceTileName', replaceTileName, None, 'replaceDataValue', replaceDataValue, None)
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates"))
        optionals = internal.defaults((tileData_blockStates, None), (mode, "replace"), (replaceTileName, None), (replaceDataValue, None))

        cmd = f"fill {pos1} {pos2} {block} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", cloneMode: str="normal", tileName: str=None, tileData: int=0, blockStates: list=None):
        internal.options(maskMode, ['masked', 'filtered', 'replace'])
        internal.options(cloneMode, ['forced', 'move', 'normal'])
        if maskMode != 'filtered' and tileName != None:
            raise errors.InvalidParameterError('filtered', 'maskMode', maskMode, 'tileName')
        elif maskMode != 'filtered' and tileData != 0:
            raise errors.InvalidParameterError('filtered', 'maskMode', tileData, 'tileData')
        elif maskMode != 'filtered' and blockStates != None:
            raise errors.InvalidParameterError('filtered', 'maskMode', blockStates, 'blockStates')
        tileData_blockStates = internal.pick_one_arg((tileData, 0, "tileData"), (blockStates, None, "blockStates")) if maskMode == 'filtered' else None
        internal.reliant('tileName', tileName, None, 'tileData_blockStates', tileData_blockStates, None)
        optionals = internal.defaults((maskMode, "replace"), (cloneMode, "normal"), (tileName, None), (tileData_blockStates, None))
        
        cmd = f"clone {pos1} {pos2} {dest} {optionals}".strip()
        self.commands.append(cmd)
        return cmd
        
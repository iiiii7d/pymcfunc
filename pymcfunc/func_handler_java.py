import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_universal import UniversalFuncHandler

class JavaFuncHandler(UniversalFuncHandler):
    def __init__(self):
        self.commands = []

    def setblock(self, pos: str, block: str, mode="replace"):
        internal.options(mode, ['destroy', 'keep', 'replace'])
        optionals = internal.defaults((mode, "replace"))

        cmd = f"setblock {pos} {block} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, block: str, mode="replace", filterPredicate: str=None):
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace' and filterPredicate != None:
            raise errors.InvalidParameterError(mode, 'mode', filterPredicate, 'filterPredicate')
        optionals = internal.defaults((mode, "replace"), (filterPredicate, None))

        cmd = f"fill {pos1} {pos2} {block} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", filterPredicate: str=None, cloneMode: str="normal"):
        internal.options(maskMode, ['masked', 'filtered', 'replace'])
        internal.options(cloneMode, ['forced', 'move', 'normal'])
        if maskMode != 'filtered' and filterPredicate != None:
            raise errors.InvalidParameterError(maskMode, 'maskMode', filterPredicate, 'filterPredicate')
        if maskMode == 'filtered' and filterPredicate != None:
            optionals = f"filtered {filterPredicate} " + internal.defaults((cloneMode, "normal"))
        else:
            optionals = internal.defaults((maskMode, "replace"), (cloneMode, "normal"))
        
        cmd = f"clone {pos1} {pos2} {dest} {optionals}".strip()
        self.commands.append(cmd)
        return cmd
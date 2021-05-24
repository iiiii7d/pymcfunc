import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_universal import UniversalFuncHandler
from pymcfunc.selectors import JavaSelectors

class JavaFuncHandler(UniversalFuncHandler):
    """The Java Edition function handler.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler"""
    sel = JavaSelectors()

    def __init__(self):
        self.commands = []

    def setblock(self, pos: str, block: str, mode="replace"):
        """Adds a /setblock command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        optionals = internal.defaults((mode, "replace"))

        cmd = f"setblock {pos} {block} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, block: str, mode="replace", filterPredicate: str=None):
        """Adds a /fill command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.fill"""
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace' and filterPredicate != None:
            raise errors.InvalidParameterError(mode, 'mode', filterPredicate, 'filterPredicate')
        optionals = internal.defaults((mode, "replace"), (filterPredicate, None))

        cmd = f"fill {pos1} {pos2} {block} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", filterPredicate: str=None, cloneMode: str="normal"):
        """Adds a /clone command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.clone"""
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

    def give(self, target: str, item: str, count: int=1):
        """Adds a /give command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((count, 1))

        cmd = f"give {target} {item} {optionals}".strip()
        self.commands.append(cmd)
        return cmd
        
    def gamemode(self, mode: str, target: int="@s"):
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"))
        internal.options(mode, ['survival', 'creative', 'adventure', 'spectator'])

        cmd = f"gamemode {mode} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def summon(self, entity: str, pos: str="~ ~ ~", nbt: dict=None):
        optionals = internal.defaults((pos, "~ ~ ~"), (nbt, None))

        cmd = f"summon {entity} {optionals}".strip()
        self.commands.append(cmd)
        return cmd

    def clear(self, target: str="@s", item: str=None, maxCount: int=None):
        internal.reliant('item', maxCount, None, 'data', maxCount, None)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (maxCount, None))

        cmd = f"clear {optionals}"
        self.commands.append(cmd)
        return cmd

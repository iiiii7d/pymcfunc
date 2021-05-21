import pymcfunc.errors as errors
import pymcfunc.internal as internal

class UniversalFuncHandler:
    commands = []

    def __init__(self):
        pass

    def __str__(self):
        return "\n".join(self.commands)

    def say(self, message: str):
        self.commands.append(f"say {message}")

    def tell(self, target: str, message: str):
        if " " in target:
            raise errors.SpaceError('target', target)
        self.commands.append(f"tell {target} {message}")
    w = tell
    msg = tell

    def setblock(self, pos: str, block: str, mode="replace"):
        internal.options(mode, ['destroy', 'keep', 'replace'])
        optionals = internal.defaults((mode, "replace"))
        self.commands.append(f"setblock {pos} {block} {optionals}")
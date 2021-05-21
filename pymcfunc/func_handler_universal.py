import pymcfunc.errors as errors
import pymcfunc.internal as internal

class UniversalFuncHandler:
    def __init__(self):
        self.commands = []

    def __str__(self):
        return "\n".join(self.commands)

    def say(self, message: str):
        self.commands.append(f"say {message}".strip())

    def tell(self, target: str, message: str):
        if " " in target:
            raise errors.SpaceError('target', target)
        self.commands.append(f"tell {target} {message}".strip())
    w = tell
    msg = tell

    def help(self):
        self.commands.append("help")
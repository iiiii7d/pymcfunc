import pymcfunc.errors as errors
import pymcfunc.internal as internal

class UniversalFuncHandler:
    def __init__(self):
        self.commands = []

    def __str__(self):
        return "\n".join(self.commands)

    def __iter__(self):
        for i in self.commands:
            yield i

    def say(self, message: str):
        cmd = f"say {message}".strip()
        self.commands.append(cmd)
        return cmd

    def tell(self, target: str, message: str):
        internal.check_spaces('target', target)
        cmd = f"tell {target} {message}".strip()
        self.commands.append(cmd)
        return cmd
    w = tell
    msg = tell

    def help(self):
        self.commands.append("help")
        return "help"

    def kill(self, target: str):
        internal.check_spaces('target', target)
        cmd = f"kill {target}".strip()
        self.commands.append(cmd)
        return cmd
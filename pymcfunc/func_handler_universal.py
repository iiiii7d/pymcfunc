import pymcfunc.errors as errors
import pymcfunc.internal as internal

class UniversalFuncHandler:
    """The function handler which includes commands that are the same for both Java and Bedrock edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler"""
    def __init__(self):
        self.commands = []

    def __str__(self):
        return "\n".join(self.commands)

    def __iter__(self):
        for i in self.commands:
            yield i

    def say(self, message: str):
        """Adds a /say command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.say"""
        cmd = f"say {message}".strip()
        self.commands.append(cmd)
        return cmd

    def tell(self, target: str, message: str):
        """Adds a /tell command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.tell"""
        internal.check_spaces('target', target)
        cmd = f"tell {target} {message}".strip()
        self.commands.append(cmd)
        return cmd
    w = tell
    msg = tell

    def help(self):
        """Adds a /help command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.help"""
        self.commands.append("help")
        return "help"

    def kill(self, target: str):
        """Adds a /kill command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.kill"""
        internal.check_spaces('target', target)
        cmd = f"kill {target}".strip()
        self.commands.append(cmd)
        return cmd
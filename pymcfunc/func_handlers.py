from pymcfunc.selectors import UniversalSelectors, JavaSelectors, BedrockSelectors
from pymcfunc.variables import JavaVariable, BedrockVariable
import pymcfunc.entities as entities
from pymcfunc.entities import Entity
#from pymcfunc.rawcommands import UniversalRawCommands, JavaRawCommands, BedrockRawCommands

class UniversalFuncHandler:
    """The function handler which includes commands that are the same for both Java and Bedrock edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler"""
    sel = UniversalSelectors()

    def __init__(self):
        from pymcfunc.rawcommands import UniversalRawCommands
        self.r = UniversalRawCommands(self)

    def __str__(self):
        return "\n".join(self.commands)

    def __iter__(self):
        for i in self.commands:
            yield i

    def clear(self):
        """Clears the command list.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.clear"""
        self.commands = []

    def comment(self, comment: str):
        """Adds a comment.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.UniversalFuncHandler.comment"""
        self.commands.append('# '+comment.strip())

class BedrockFuncHandler(UniversalFuncHandler):
    """The Beckrock Edition function handler.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler"""
    sel = BedrockSelectors()

    def __init__(self):
        self.commands = []
        from pymcfunc.rawcommands import BedrockRawCommands
        self.r = BedrockRawCommands(self)

    def v(self, name: str, target: str) -> BedrockVariable:
        """Creates a variable.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockFuncHandler.v"""
        return BedrockVariable(self, name, target)

class JavaFuncHandler(UniversalFuncHandler):
    """The Java Edition function handler.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler"""
    sel = JavaSelectors()

    def __init__(self):
        self.commands = []
        from pymcfunc.rawcommands import JavaRawCommands
        self.r = JavaRawCommands(self)

    def v(self, name: str, target: str, trigger: bool=False) -> JavaVariable:
        """Creates a variable.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.v"""
        return JavaVariable(self, name, target, trigger=trigger)

    def entity(self, entity_name: str, target: str) -> Entity:
        """Creates an entity object.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.entity"""
        return getattr(entities, entity_name)(self, target)

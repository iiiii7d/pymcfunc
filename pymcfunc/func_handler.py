from __future__ import annotations
from typing import TYPE_CHECKING
from pymcfunc.selectors import UniversalSelector, JavaSelector, BedrockSelector
from pymcfunc.variables import JavaVariable, BedrockVariable
import pymcfunc.entities as entities
from pymcfunc.entities import Entity
from pymcfunc.raw_commands import UniversalRawCommands, JavaRawCommands, BedrockRawCommands
if TYPE_CHECKING:
    from pymcfunc.pack import JavaPack

class UniversalFuncHandler:
    """
    The function handler that is inherited by both :py:class:`JavaFuncHandler` and :py:class:`BedrockFuncHandler`.

    This includes commands and features that are the same for both Java and Bedrock edition.

    .. warning::
       Use either :py:class:`BedrockFuncHandler` or :py:class:`JavaFuncHandler` for extended support of commands for your edition.
    """
    sel = UniversalSelector()

    def __init__(self, p):
        self.commands = []
        self.r = UniversalRawCommands(self)
        self.p = p

    def __str__(self):
        return "\n".join(self.commands)

    def __iter__(self):
        for i in self.commands:
            yield i

    def clear(self):
        """Clears the command list."""
        self.commands = []

    def comment(self, comment: str):
        """
        Adds a comment.

        :param str comment: The comment to add
        """
        self.commands.append('# '+comment.strip())

class BedrockFuncHandler(UniversalFuncHandler):
    """The Beckrock Edition function handler."""
    sel = BedrockSelector()

    def __init__(self, p):
        super().__init__(p)
        self.r = BedrockRawCommands(self)

    def v(self, name: str, target: str) -> BedrockVariable:
        """
        Creates and registers a variable.

        :param str name: The name of the variable
        :param str target: The target of the variable, or whom it applies to
        :return: The variable
        :rtype: BedrockVariable
        """
        return BedrockVariable(self, name, target)

class JavaFuncHandler(UniversalFuncHandler):
    """The Java Edition function handler."""
    sel = JavaSelector()

    def __init__(self, p: JavaPack):
        super().__init__(p)
        self.commands = []
        self.r = JavaRawCommands(self)
        self.p = p

    def v(self, name: str, target: str, trigger: bool=False) -> JavaVariable:
        """
        Creates and registers a variable.

        :param trigger:
        :param str name: The name of the variable
        :param str target: The target of the variable, or whom it applies to
        :return: The variable
        :rtype: BedrockVariable
        """
        return JavaVariable(self, name, target, trigger=trigger)

    def entity(self, entity_name: str, target: str) -> Entity:
        """Creates an entity selector object.

        :param str entity_name: Can be one of ``Entity``, ``Mob``, ``ArmourStand``
        :param str target: The target for the object
        :returns: The entity selector object
        :rtype: Entity"""
        return getattr(entities, entity_name)(self, target)

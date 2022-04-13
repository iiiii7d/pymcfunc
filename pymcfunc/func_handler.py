from __future__ import annotations
from typing import TYPE_CHECKING, List

from pymcfunc.internal import base_class
from pymcfunc.selectors import BaseSelector, JavaSelector, BedrockSelector
from pymcfunc.variables import JavaVariable, BedrockVariable
import pymcfunc.entities as entities
from pymcfunc.entities import Entity
from pymcfunc.raw_commands import BaseRawCommands, JavaRawCommands, BedrockRawCommands, ExecutedCommand

if TYPE_CHECKING:
    from pymcfunc.pack import JavaPack

@base_class
class BaseFunctionHandler:
    """
    The function handler that is inherited by both :py:class:`JavaFunctionHandler` and :py:class:`BedrockFunctionHandler`.

    This includes commands and features that are the same for both Java and Bedrock edition.

    .. warning::
       Use either :py:class:`BedrockFunctionHandler` or :py:class:`JavaFunctionHandler` for extended support of commands for your edition.
    """
    sel = BaseSelector()

    def __init__(self, p):
        self.commands: List[ExecutedCommand] = []
        self.r = BaseRawCommands(self)
        self.p = p

    def __str__(self):
        return "\n".join(c.command_string for c in self.commands)

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

class BedrockFunctionHandler(BaseFunctionHandler):
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

class JavaFunctionHandler(BaseFunctionHandler):
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

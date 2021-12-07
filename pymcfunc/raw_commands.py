import inspect
import warnings
from functools import wraps
from typing import Optional, Any, Callable

from pymcfunc.command_builder import CommandBuilder
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning
from pymcfunc.func_handler import UniversalFuncHandler
from pymcfunc.minecraft_version import MinecraftVersion
from pymcfunc.selectors import BedrockSelectors


def _get_default(func: Callable[[Any, ...], Any], param: str) -> Any:
    return inspect.signature(func).parameters[param].default
_gd = _get_default

class UniversalRawCommands:
    """
    A container for raw Minecraft commands that are the same for both Java and Bedrock.

    .. warning::
       Do not instantiate UniversalRawCommands directly; use a FuncHandler and access the commands via the ‘r’ attribute.
    """

    def __init__(self, fh: UniversalFuncHandler):
        self.fh = fh

    def version(self, version_introduced: Optional[MinecraftVersion]=None, version_deprecated: Optional[MinecraftVersion]=None):
        def decorator(func: Callable[[Any, ...], Any]):
            @wraps(func)
            def wrapper(*args, **kwargs):
                pack_version = self.fh.p.version
                if version_introduced is not None and pack_version < version_introduced:
                    warnings.warn(f"The command `{func.__name__}` was introduced in {version_introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
                elif version_deprecated is not None and pack_version >= version_deprecated:
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {version_deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
                return func(*args, **kwargs)
            return wrapper
        return decorator


class BedrockRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Bedrock Edition.

    .. warning::
       Do not instantiate BedrockRawCommands directly; use a :py:class:`BedrockFuncHandler` and access the commands via the ‘r’ attribute.
    """
    version = super().version

    def help_(self, command: Optional[str]=None, page: int=1) -> str:
        cb = CommandBuilder("help")
        cba: CommandBuilder; cbb: CommandBuilder
        cba, cbb = cb.add_branch()
        cba.add_param("page", int, default=_gd(self.help_, 'page'))
        cbb.add_param("command", str)
        cmd = cb.build(command=command, page=page)
        self.fh.commands.append(cmd)
        return cmd

    def ability(self, player: BedrockSelectors):
        cb = CommandBuilder("ability")
        cb.add_param("player", BedrockSelectors)
        cba: CommandBuilder; cbb: CommandBuilder

class JavaRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFuncHandler` and access the commands via the ‘r’ attribute.
    """
    version = super().version

    @version(version_introduced=MinecraftVersion("12w17a"))
    def help_(self, command: Optional[str]=None) -> str:
        cb = CommandBuilder("help")
        cb.add_param("command", str)
        cmd = cb.build(command=command)
        self.fh.commands.append(cmd)
        return cmd
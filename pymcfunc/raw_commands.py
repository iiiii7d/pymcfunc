import inspect
import warnings
from functools import wraps
from typing import Optional, Any, Callable, Literal, get_args

from pymcfunc.command_builder import CommandBuilder
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.func_handler import UniversalFuncHandler
from pymcfunc.selectors import JavaSelector, BedrockSelector
from pymcfunc.version import JavaVersion, BedrockVersion


def _get_default(func: Callable[..., Any], param: str) -> Any:
    return inspect.signature(func).parameters[param].default
_gd = _get_default

def _get_options(func: Callable[..., Any], param: str) -> Any:
    # noinspection PyUnresolvedReferences
    options = get_args(get_args(func.__annotations__[param])[0])
    if len(options) == 0:
        # noinspection PyUnresolvedReferences
        options = get_args(func.__annotations__[param])
    return options
_go = _get_options

class ExecutedCommand:
    def __init__(self, fh: UniversalFuncHandler, name: str, command_string: str):
        self.fh = fh
        self.name = name
        self.command_string = command_string

    def store_success(self):
        pass

    def store_result(self):
        pass

class UniversalRawCommands:
    """
    A container for raw Minecraft commands that are the same for both Java and Bedrock.

    .. warning::
       Do not instantiate UniversalRawCommands directly; use a FuncHandler and access the commands via the ‘r’ attribute.
    """

    def __init__(self, fh: UniversalFuncHandler):
        self.fh = fh


class BedrockRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Bedrock Edition.

    .. warning::
       Do not instantiate BedrockRawCommands directly; use a :py:class:`BedrockFuncHandler` and access the commands via the ‘r’ attribute.
    """
    @staticmethod
    def education_edition(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.fh.p.education:
                warnings.warn(f"The command `{func.__name__}` is an Education Edition feature. Your pack is not for Education Edition.", category=EducationEditionWarning)
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def version(version_introduced: Optional[str]=None, version_deprecated: Optional[str]=None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                pack_version = self.fh.p.version
                if version_introduced is not None and pack_version < BedrockVersion(version_introduced):
                    warnings.warn(f"The command `{func.__name__}` was introduced in {version_introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
                elif version_deprecated is not None and pack_version >= BedrockVersion(version_deprecated):
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {version_deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    @version(version_introduced="0.16.0b1")
    def help_(self,
              command: Optional[str]=None,
              page: int=1) -> ExecutedCommand:
        cb = self.help_cb()
        cmd = ExecutedCommand(self.fh, "help", cb.build(command=command, page=page))
        self.fh.commands.append(cmd)
        return cmd
    def help_cb(self) -> CommandBuilder:
        cb = CommandBuilder("help")
        cba: CommandBuilder; cbb: CommandBuilder
        cba, cbb = cb.add_branch()
        cba.add_param("page", int, optional=True, default=_gd(self.help_, 'page'))
        cbb.add_param("command", str)
        return cb

    @education_edition
    @version(version_introduced="v0.16.0")
    def ability(self,
                player: BedrockSelector,
                ability: Optional[Literal["worldborder", "mayfly", "mute"]]=None,
                value: Optional[bool]=None) -> ExecutedCommand:
        cb = self.ability_cb()
        cmd = ExecutedCommand(self.fh, "ability", cb.build(player=player, ability=ability, value=value))
        self.fh.commands.append(cmd)
        return cmd
    def ability_cb(self):
        cb = CommandBuilder("ability")
        cb.add_param("player", BedrockSelector, playeronly=True, qty="single")
        cb.add_param("ability", str, optional=True, options=_go(self.ability, "ability"))
        cb.add_param("value", bool, optional=True)
        return cb

    @version(version_introduced="1.2.0")
    def daylock(self, lock: Optional[bool]=None):
        cb = self.daylock_cb()
        cmd = ExecutedCommand(self.fh, "daylock", cb.build(lock=lock))
        self.fh.commands.append(cmd)
        return cmd
    alwaysday = daylock
    def daylock_cb(self):
        cb = CommandBuilder("daylock")
        cb.add_param("lock", bool, optional=True)
        return cb
    alwaysday_cb = daylock_cb

class JavaRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFuncHandler` and access the commands via the ‘r’ attribute.
    """
    @staticmethod
    def version(version_introduced: Optional[str]=None, version_deprecated: Optional[str]=None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                pack_version = self.fh.p.version
                if version_introduced is not None and pack_version < JavaVersion(version_introduced):
                    warnings.warn(f"The command `{func.__name__}` was introduced in {version_introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
                elif version_deprecated is not None and pack_version >= JavaVersion(version_deprecated):
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {version_deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    @version(version_introduced="12w17a")
    def help_(self, command: Optional[str]=None) -> ExecutedCommand:
        cb = self.help_cb()
        cmd = ExecutedCommand(self.fh, "help", cb.build(command=command))
        self.fh.commands.append(cmd)
        return cmd
    @staticmethod
    def help_cb():
        cb = CommandBuilder("help")
        cb.add_param("command", str)
        return cb

    @version(version_introduced="17w13a")
    def advancement(self, targets: JavaSelector, *,
                    mode: Literal["grant", "revoke"],
                    action: Literal["everything", "only", "from", "through", "until"],
                    advancement: Optional[str]=None,
                    criterion: Optional[str]=None) -> ExecutedCommand:
        cb = self.advancement_cb()
        cmd = ExecutedCommand(self.fh, "advancement", cb.build(targets=targets, mode=mode, action=action, advancement=advancement, criterion=criterion))
        self.fh.commands.append(cmd)
        return cmd
        
    def advancement_cb(self):
        cb = CommandBuilder("advancement")
        cb.add_switch("mode", _go(self.advancement, "mode"))
        cb.add_param("targets", JavaSelector, playeronly=True)
        branches = cb.add_branch(3)
        branches[0].add_switch("action", ["everything"])
        branches[1].add_switch("action", ["only"])
        branches[1].add_param("advancement", str) # TODO add Advancement class when it is written
        branches[1].add_param("criterion", str, optional=True) # TODO add Criterion class when it is written
        branches[2].add_switch("action", ["from", "through", "until"])
        branches[2].add_param("advancement", str) # TODO add Advancement class when it is written
        return cb
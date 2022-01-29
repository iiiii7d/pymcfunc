from __future__ import annotations

import inspect
import warnings
from functools import wraps
from typing import Optional, Any, Callable, Tuple, get_args, TYPE_CHECKING, Union, TypeAlias, Annotated, Literal
from uuid import UUID

from pymcfunc.advancements import Advancement
from pymcfunc.command import ExecutedCommand, Command, SE, AE, Range, NoSpace, Element, Player, Single, Regex, \
    PlayerName
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.nbt import Int
from pymcfunc.selectors import BedrockSelector, JavaSelector
from pymcfunc.version import JavaVersion, BedrockVersion

if TYPE_CHECKING:
    from pymcfunc.func_handler import UniversalFuncHandler

RawJson: TypeAlias = Union[dict, list]
ResourceLocation: TypeAlias = str
_JavaPNUTS: TypeAlias = Union[Annotated[str, PlayerName], UUID, Annotated[JavaSelector, Player]]

class _MissingType: pass
Missing = _MissingType()

def _get_default(func: Callable[..., Any], param: str) -> Any:
    return inspect.signature(func).parameters[param].default
_gd = _get_default

def _get_type(func: Callable[..., Any], param: str) -> type:
    # noinspection PyUnresolvedReferences
    type_ = func.__annotations__[param]
    if get_args(type_) != () and len(get_args(type_)) >= 2 and isinstance(get_args(type_)[1], type(None)): type_ = get_args(type_)[0]
    return type_
_gt = _get_type

def _get_options(func: Callable[..., Any], param: str) -> Any:
    # noinspection PyUnresolvedReferences
    options = get_args(get_args(func.__annotations__[param])[0])
    if len(options) == 0:
        # noinspection PyUnresolvedReferences
        options = get_args(func.__annotations__[param])
    return options
_go = _get_options

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
    def command(order: list[Element], cmd_name: str | None = None, segment_name: str | None = None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                return Command.command(self.fh, order, cmd_name, segment_name)(func)(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def education_edition(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.fh.p.education:
                warnings.warn(f"The command `{func.__name__}` is an Education Edition feature. Your pack is not for Education Edition.", category=EducationEditionWarning)
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def version(introduced: Optional[str]=None, deprecated: Optional[str]=None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                pack_version = self.fh.p.version
                if introduced is not None and pack_version < BedrockVersion(introduced):
                    warnings.warn(f"The command `{func.__name__}` was introduced in {introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
                elif deprecated is not None and pack_version >= BedrockVersion(deprecated):
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def param_version_introduced(self, param_name: str, param_value: Any, version_introduced: str, default: Any=None):
        if param_value != default and self.fh.p.version < BedrockVersion(version_introduced):
            warnings.warn(f"The `{param_name}` parameter was introduced in {version_introduced}, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)

    def option_version_introduced(self, param_name: str, param_value: Any, version_introduced: str, option: Any):
        if param_value == option and self.fh.p.version < BedrockVersion(version_introduced):
            warnings.warn(f"The `{option}` option of the `{param_name}` parameter was introduced in {version_introduced}, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)

    @version(introduced="0.16.0b1")
    @command([
        SE([AE("command")],
           [AE("page", True)])
    ])
    def help_(self,
              command: Annotated[str, NoSpace] | None = None,
              page: Annotated[int, Range(Int.min, Int.max)] | None = None) -> ExecutedCommand: pass

    @education_edition
    @version(introduced="0.16.0b1")
    @command([
        AE("target"),
        AE("ability", True),
        AE("value", True)
    ])
    def ability(self, target: Annotated[BedrockSelector, Player, Single],
                ability: Literal["worldbuilder", "mayfly", "mute"] | None = None,
                value: bool | None = None) -> ExecutedCommand: pass


class JavaRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFuncHandler` and access the commands via the ‘r’ attribute.
    """

    @staticmethod
    def command(order: list[Element], cmd_name: str | None = None, segment_name: str | None = None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                return Command.command(self.fh, order, cmd_name, segment_name)(func)(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def version(introduced: Optional[str]=None, deprecated: Optional[str]=None, temp_removed: Optional[Tuple[str, str]]=None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                pack_version = self.fh.p.version
                if introduced is not None and pack_version < JavaVersion(introduced):
                    warnings.warn(f"The command `{func.__name__}` was introduced in {introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
                elif deprecated is not None and pack_version >= JavaVersion(deprecated):
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
                elif temp_removed is not None and JavaVersion(temp_removed[0]) <= pack_version < JavaVersion(temp_removed[1]):
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {temp_removed[0]} and reintroduced in {temp_removed[1]}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def param_version_introduced(self, param_name: str, param_value: Any, version_introduced: str, default: Any=None):
        if param_value != default and self.fh.p.version < JavaVersion(version_introduced):
            warnings.warn(f"The `{param_name}` parameter was introduced in {version_introduced}, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)

    def option_version_introduced(self, param_name: str, param_value: Any, version_introduced: str, option: Any):
        if param_value == option and self.fh.p.version < JavaVersion(version_introduced):
            warnings.warn(f"The `{option}` option of the `{param_name}` parameter was introduced in {version_introduced}, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)

    def option_version_deprecated(self, param_name: str, param_value: Any, version_deprecated: str, option: Any):
        if param_value == option and self.fh.p.version >= JavaVersion(version_deprecated):
            warnings.warn(
                f"The `{option}` option of the `{param_name}` parameter was deprecated in {version_deprecated}, but your pack is for {self.fh.p.version}",
                category=FutureCommandWarning)

    @version(introduced="12w17a")
    @command([AE("command", True)])
    def help_(self, command: str) -> ExecutedCommand: pass

    @version(introduced="17w13a")
    @command([
        AE("targets"),
        SE([AE("mode", options=["everything"])],
           [AE("mode", options=["only"]),
            AE("advancement"),
            AE("criterion", True)],
           [AE("mode", options=["from", "through", "until"]),
            AE("advancement")])
    ], cmd_name="advancement")
    def advancement_grant(self, targets: _JavaPNUTS,
                          mode: Literal["everything", "only", "from", "through", "until"],
                          advancement: Advancement | None = None,
                          criterion: str | None = None) -> ExecutedCommand: pass

    @version(introduced="17w13a")
    @command([
        AE("targets"),
        SE([AE("mode", options=["everything"])],
           [AE("mode", options=["only"]),
            AE("advancement"),
            AE("criterion", True)],
           [AE("mode", options=["from", "through", "until"]),
            AE("advancement")])
    ], cmd_name="advancement")
    def advancement_revoke(self, targets: _JavaPNUTS,
                           mode: Literal["everything", "only", "from", "through", "until"],
                           advancement: Advancement | None = None,
                           criterion: str | None = None) -> ExecutedCommand: pass
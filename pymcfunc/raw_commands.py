from __future__ import annotations

import inspect
import json
import warnings
from functools import wraps
from typing import Optional, Any, Callable, Literal, get_args, TYPE_CHECKING, Union, TypeAlias
from uuid import UUID

from pymcfunc.command_builder import CommandBuilder
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.selectors import JavaSelector, BedrockSelector
from pymcfunc.version import JavaVersion, BedrockVersion

if TYPE_CHECKING:
    from pymcfunc.func_handler import UniversalFuncHandler

RawJson: TypeAlias = Union[dict, list]

def _get_default(func: Callable[..., Any], param: str) -> Any:
    return inspect.signature(func).parameters[param].default
_gd = _get_default

def _get_type(func: Callable[..., Any], param: str) -> type:
    # noinspection PyUnresolvedReferences
    type_ = func.__annotations__[param]
    if get_args(type_) != () and get_args(type_)[1] == type(None): type_ = get_args(type_)[0]
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
    def help_(self, command: Optional[str]=None,
              page: int=1) -> ExecutedCommand:
        cb = self.help_cb()
        cmd = ExecutedCommand(self.fh, "help", cb.build(command=command, page=page))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def help_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("help")
        nt = lambda param: (param, _gt(cls.help_, param))
        node = cb.add_branch_node()
        node.add_branch().add_param(*nt("page"), optional=True, default=_gd(cls.help_, 'page'), range=lambda x: x > 0)
        node.add_branch().add_param(*nt("command"))
        return cb

    @education_edition
    @version(version_introduced="v0.16.0")
    def ability(self, player: BedrockSelector,
                ability: Optional[Literal["worldborder", "mayfly", "mute"]]=None,
                value: Optional[bool]=None) -> ExecutedCommand:
        cb = self.ability_cb()
        cmd = ExecutedCommand(self.fh, "ability", cb.build(player=player, ability=ability, value=value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ability_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ability")
        nt = lambda param: (param, _gt(cls.ability, param))
        cb.add_param(*nt("player"), playeronly=True, singleonly=True)
        cb.add_param(*nt("ability"), optional=True, options=_go(cls.ability, "ability"))
        cb.add_param(*nt("value"), optional=True)
        return cb

    @version(version_introduced="1.2.0")
    def daylock(self, lock: Optional[bool]=None):
        cb = self.daylock_cb()
        cmd = ExecutedCommand(self.fh, "daylock", cb.build(lock=lock))
        self.fh.commands.append(cmd)
        return cmd
    alwaysday = daylock
    @classmethod
    def daylock_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("daylock")
        nt = lambda param: (param, _gt(cls.daylock, param))
        cb.add_param(*nt("lock"), optional=True)
        return cb
    alwaysday_cb = daylock_cb

    @version(version_introduced="1.16.100.57")
    def camerashake_add(self, target: BedrockSelector,
                        intensity: Optional[float]=None,
                        seconds: Optional[float]=None,
                        shake_type: Optional[Literal["positional", "rotational"]]=None):
        cb = self.camerashake_add_cb()
        if shake_type is not None and self.fh.p.version < BedrockVersion('1.16.100.59'):
            warnings.warn(f"The `shake_type` parameter was introduced in 1.16.100.59, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)
        cmd = ExecutedCommand(self.fh, "camerashake", cb.build(target=target, intensity=intensity, seconds=seconds, shake_type=shake_type))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def camerashake_add_cb(cls):
        cb = CommandBuilder("camerashake")
        nt = lambda param: (param, _gt(cls.camerashake_add, param))
        cb.add_literal("add")
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("intensity"), range=lambda x: 0 <= x <= 4, optional=True)
        cb.add_param(*nt("seconds"), range=lambda x: x >= 0, optional=True)
        cb.add_switch("shake_type", _go(cls.camerashake_add, "shake_type"), optional=True)
        return cb

    @version(version_introduced="1.16.210.54")
    def camerashake_stop(self, target: BedrockSelector):
        cb = self.camerashake_stop_cb()
        cmd = ExecutedCommand(self.fh, "camerashake", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def camerashake_stop_cb(cls):
        cb = CommandBuilder("camerashake")
        nt = lambda param: (param, _gt(cls.camerashake_stop, param))
        cb.add_literal("stop")
        cb.add_param(*nt("target"), playeronly=True)
        return cb

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
    @classmethod
    def help_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("help")
        nt = lambda param: (param, _gt(cls.help_, param))
        cb.add_param(*nt("command"), optional=True)
        return cb

    @version(version_introduced="17w13a")
    def advancement(self, targets: Union[JavaSelector, UUID], *,
                    mode: Literal["grant", "revoke"],
                    action: Literal["everything", "only", "from", "through", "until"],
                    advancement: Optional[str]=None,
                    criterion: Optional[str]=None) -> ExecutedCommand:
        cb = self.advancement_cb()
        cmd = ExecutedCommand(self.fh, "advancement", cb.build(targets=targets, mode=mode, action=action, advancement=advancement, criterion=criterion))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def advancement_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("advancement")
        nt = lambda param: (param, _gt(cls.advancement, param))
        cb.add_switch("mode", _go(cls.advancement, "mode"))
        cb.add_param(*nt("targets"), playeronly=True)
        node = cb.add_branch_node()
        node.add_branch("action", ["everything"])
        cb_only = node.add_branch("action", ["only"])
        cb_only.add_param(*nt("advancement"))  # TODO add Advancement & ResourceLocation class when it is written
        cb_only.add_param(*nt("criterion"), optional=True)  # TODO add Criterion class when it is written
        cb_others = node.add_branch("action", ["from", "through", "until"])
        cb_others.add_param(*nt("advancement")) # TODO add Advancement class when it is written
        return cb

    @version(version_introduced="20w17a")
    def attribute_get_total(self, target: Union[JavaSelector, UUID], *,
                            attribute: str,
                            scale: Optional[float]=None) -> ExecutedCommand:
        cb = self.attribute_get_total_cb()
        cmd = ExecutedCommand(self.fh, "attribute", cb.build(target=target, attribute=attribute, scale=scale))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def attribute_get_total_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("attribute")
        nt = lambda param: (param, _gt(cls.attribute_get_total, param))
        cb.add_param(*nt("target"), singleonly=True)
        cb.add_param(*nt("attribute")) # TODO add ResourceLocation class when it is written
        cb.add_literal("get")
        cb.add_param(*nt("scale"), optional=True)
        return cb

    @version(version_introduced="20w17a")
    def attribute_base(self, target: Union[JavaSelector, UUID], *,
                       attribute: str,
                       mode: Literal["get", "set"],
                       scale: Optional[float]=None,
                       value: Optional[float]=None) -> ExecutedCommand:
        cb = self.attribute_base_cb()
        cmd = ExecutedCommand(self.fh, "attribute", cb.build(target=target, attribute=attribute, mode=mode, scale=scale, value=value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def attribute_base_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("attribute")
        nt = lambda param: (param, _gt(cls.attribute_base, param))
        cb.add_param(*nt("target"), singleonly=True)
        cb.add_param(*nt("attribute"))  # TODO add ResourceLocation class when it is written
        cb.add_literal("base")
        node = cb.add_branch_node()
        node.add_branch("mode", ["get"]).add_param(*nt("scale"), optional=True)
        node.add_branch("mode", ["set"]).add_param(*nt("value"))
        return cb

    @version(version_introduced="20w17a")
    def attribute_modifier(self, target: Union[JavaSelector, UUID], *,
                           attribute: str,
                           mode: Literal["add", "remove", "value get"],
                           uuid: UUID,
                           name: Optional[str]=None,
                           value: Optional[float]=None,
                           add_mode: Optional[Literal["add", "multiply", "multiply_base"]],
                           scale: Optional[float]=None) -> ExecutedCommand:
        cb = self.attribute_modifier_cb()
        cmd = ExecutedCommand(self.fh, "attribute", cb.build(target=target, attribute=attribute, mode=mode, uuid=uuid,
                                                             name=name, value=value, add_mode=add_mode, scale=scale))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def attribute_modifier_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("attribute")
        nt = lambda param: (param, _gt(cls.attribute_modifier, param))
        cb.add_param(*nt("target"), singleonly=True)
        cb.add_param(*nt("attribute"))  # TODO add ResourceLocation class when it is written
        cb.add_literal("modifier")
        node = cb.add_branch_node()
        cb_add = node.add_branch("mode", ["add"])
        cb_add.add_param(*nt("uuid"))
        cb_add.add_param(*nt("name"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb_add.add_param(*nt("value"))
        cb_add.add_switch("add_mode", _go(cls.attribute_modifier, "add_mode"))
        node.add_branch("mode", ["remove"]).add_param(*nt("uuid"))
        cb_value_get = node.add_branch("mode", ["value get"])
        cb_value_get.add_param(*nt("uuid"))
        cb_value_get.add_param(*nt("scale"), optional=True)
        return cb

    @version(version_introduced="a1.0.16")
    def ban(self, target: JavaSelector, reason: Optional[str]="Banned by an operator."):
        cb = self.ban_cb()
        cmd = ExecutedCommand(self.fh, "ban", cb.build(target=target, reason=reason))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ban_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ban")
        nt = lambda param: (param, _gt(cls.ban, param))
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("reason"), default=_gd(cls.ban, "reason"), spaces=True)
        return cb

    @version(version_introduced="a1.0.16")
    def ban_ip(self, target: Union[str, JavaSelector], reason: Optional[str]="Banned by an operator."):
        cb = self.ban_ip_cb()
        cmd = ExecutedCommand(self.fh, "ban-ip", cb.build(target=target, reason=reason))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ban_ip_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ban-ip")
        nt = lambda param: (param, _gt(cls.ban_ip, param))
        cb.add_param(*nt("target"), playeronly=True, regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_param(*nt("reason"), default=_gd(cls.ban, "reason"), spaces=True)
        return cb

    @version(version_introduced="a1.0.16")
    def banlist(self, view: Optional[Literal["ips", "players"]]=None):
        cb = self.banlist_cb()
        cmd = ExecutedCommand(self.fh, "banlist", cb.build(view=view))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def banlist_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("banlist")
        cb.add_switch("view", _go(cls.banlist, "view"), optional=True)
        return cb

    @version(version_introduced="18w05a")
    def bossbar_add(self, id_: str, name: Union[str, RawJson]) -> ExecutedCommand:
        cb = self.bossbar_add_cb()
        cmd = ExecutedCommand(self.fh, "bossbar", cb.build(id=id_, name=json.dumps(name) if isinstance(name, str) else name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def bossbar_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("bossbar add")
        nt = lambda param: (param, _gt(cls.bossbar_add, param))
        cb.add_param(*nt("id")) # TODO add ResourceLocation class when it is written
        cb.add_param(*nt("name"), spaces=True)
        return cb

    @version(version_introduced="18w05a")
    def bossbar_get(self, id_: str, setting: Literal["max", "players", "value", "visible"]) -> ExecutedCommand:
        cb = self.bossbar_get_cb()
        cmd = ExecutedCommand(self.fh, "bossbar", cb.build(id=id_, setting=setting))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def bossbar_get_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("bossbar get")
        nt = lambda param: (param, _gt(cls.bossbar_get, param))
        cb.add_param(*nt("id"))  # TODO add ResourceLocation class when it is written
        cb.add_switch("setting", _go(cls.bossbar_get, "setting"))
        return cb

    @version(version_introduced="18w05a")
    def bossbar_list(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "bossbar", "bossbar list")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def bossbar_list_cb(cls) -> CommandBuilder:
        return CommandBuilder("bossbar list")

    @version(version_introduced="18w05a")
    def bossbar_remove(self, id_: str) -> ExecutedCommand:
        cb = self.bossbar_add_cb()
        cmd = ExecutedCommand(self.fh, "bossbar", cb.build(id=id_))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def bossbar_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("bossbar remove")
        nt = lambda param: (param, _gt(cls.bossbar_remove, param))
        cb.add_param(*nt("id"))  # TODO add ResourceLocation class when it is written
        return cb

    @version(version_introduced="18w05a")
    def bossbar_set(self, id_: str, *,
                    color: Optional[Literal["blue", "green", "pink", "purple", "red", "white", "yellow"]]=None,
                    max_: Optional[int]=None,
                    name: Optional[Union[str, RawJson]]=None,
                    players: Optional[Union[JavaSelector, UUID]]=None,
                    style: Optional[Literal["notched_6", "notched_10", "notched_12", "notched_20", "progress"]]=None,
                    value: Optional[int]=None,
                    visible: Optional[bool]=None) -> ExecutedCommand:
        cb = self.bossbar_set_cb()
        cmd = ExecutedCommand(self.fh, "bossbar", cb.build(id=id_, color=color, max_=max_, name=json.dumps(name) if isinstance(name, str) else name,
                                                           players=players, style=style, value=value, visible=visible))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def bossbar_set_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("bossbar set")
        nt = lambda param: (param, _gt(cls.bossbar_set, param))
        node = cb.add_branch_node()
        cb_color = node.add_branch()
        cb_color.add_literal("color")
        cb_color.add_param(*nt("color"), options=_go(cls.bossbar_set, "color"))
        cb_max = node.add_branch()
        cb_max.add_literal("max")
        cb_max.add_param(*nt("max"), range=lambda x: 1 <= x <= 2147483647)
        cb_name = node.add_branch()
        cb_name.add_literal("name")
        cb_name.add_param(*nt("name"))
        cb_players = node.add_branch()
        cb_players.add_literal("players")
        cb_players.add_param(*nt("players"), playeronly=True, optional=True)
        cb_style = node.add_branch()
        cb_style.add_literal("style")
        cb_style.add_param(*nt("style"), options=_go(cls.bossbar_set, "style"))
        cb_value = node.add_branch()
        cb_value.add_literal("value")
        cb_value.add_param(*nt("value"), range=lambda x: 0 <= x <= 2147483647)
        cb_visible = node.add_branch()
        cb_visible.add_literal("visible")
        cb_visible.add_param(*nt("visible"))
        return cb


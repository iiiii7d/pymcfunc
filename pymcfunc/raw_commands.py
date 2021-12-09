from __future__ import annotations

import inspect
import json
import warnings
from functools import wraps
from typing import Optional, Any, Callable, Literal, get_args, TYPE_CHECKING, Union, TypeAlias, List
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
    if get_args(type_) != () and isinstance(get_args(type_)[1], type(None)): type_ = get_args(type_)[0]
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
    @version(introduced="v0.16.0")
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
        cb.add_switch("ability", _go(cls.ability, "ability"), optional=True)
        cb.add_param(*nt("value"), optional=True)
        return cb

    @version(introduced="1.2.0")
    def daylock(self, lock: Optional[bool]=None) -> ExecutedCommand:
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

    @version(introduced="1.16.100.57")
    def camerashake_add(self, target: BedrockSelector=BedrockSelector.s,
                        intensity: Optional[float]=None,
                        seconds: Optional[float]=None,
                        shake_type: Optional[Literal["positional", "rotational"]]=None) -> ExecutedCommand:
        cb = self.camerashake_add_cb()
        self.param_version_introduced("shake_type", shake_type, "1.16.100.59")
        cmd = ExecutedCommand(self.fh, "camerashake", cb.build(target=target, intensity=intensity, seconds=seconds, shake_type=shake_type))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def camerashake_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("camerashake")
        nt = lambda param: (param, _gt(cls.camerashake_add, param))
        cb.add_literal("add")
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("intensity"), range=lambda x: 0 <= x <= 4, optional=True)
        cb.add_param(*nt("seconds"), range=lambda x: x >= 0, optional=True)
        cb.add_switch("shake_type", _go(cls.camerashake_add, "shake_type"), optional=True)
        return cb

    @version(introduced="1.16.210.54")
    def camerashake_stop(self, target: BedrockSelector=BedrockSelector.s) -> ExecutedCommand:
        cb = self.camerashake_stop_cb()
        cmd = ExecutedCommand(self.fh, "camerashake", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def camerashake_stop_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("camerashake")
        nt = lambda param: (param, _gt(cls.camerashake_stop, param))
        cb.add_literal("stop")
        cb.add_param(*nt("target"), playeronly=True)
        return cb

    # version introduced unknown
    def changesetting(self, allow_cheats: Optional[bool]=None,
                      difficulty: Optional[Union[int, Literal["peaceful", "easy", "normal", "hard", "p", "e", "n", "h"]]]=None) -> ExecutedCommand:
        cb = self.changesetting_cb()
        cmd = ExecutedCommand(self.fh, "changesetting", cb.build(allow_cheats=allow_cheats, difficulty=difficulty))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def changesetting_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("changesetting")
        nt = lambda param: (param, _gt(cls.changesetting, param))
        node = cb.add_branch_node()
        node.add_branch(literal="allow-cheats").add_param(*nt("allow_cheats"))
        node.add_branch(literal="difficulty").add_param(*nt("difficulty"), range=lambda x: 0 <= x <= 3)
        return cb

    @version(introduced="1.0.5.0")
    def clear(self, player: BedrockSelector=BedrockSelector.s,
              item: Union[str, int]=None, # TODO add block predicate thingy when it is written
              data: int=-1,
              max_count: int=-1) -> ExecutedCommand:
        cb = self.clear_cb()
        cmd = ExecutedCommand(self.fh, "clear", cb.build(player=player, item=item, data=data, max_count=max_count))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def clear_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("clear")
        nt = lambda param: (param, _gt(cls.clear, param))
        cb.add_param(*nt("player"), default=_gd(cls.clear, "player"), optional=True, playeronly=True)
        cb.add_param(*nt("item"), optional=True)
        cb.add_param(*nt("data"), optional=True, range=lambda x: -1 <= x <= 2147483647)
        cb.add_param(*nt("max_count"), optional=True, range=lambda x: -1 <= x <= 2147483647)
        return cb

    @version(introduced="1.16.100.57")
    def clearspawnpoint(self, player: BedrockSelector=BedrockSelector.s) -> ExecutedCommand:
        cb = self.clearspawnpoint_cb()
        cmd = ExecutedCommand(self.fh, "clearspawnpoint", cb.build(player=player))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def clearspawnpoint_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("clearspawnpoint")
        nt = lambda param: (param, _gt(cls.clearspawnpoint, param))
        cb.add_param(*nt("player"), default=_gd(cls.clearspawnpoint, "player"), optional=True, playeronly=True)
        return cb

    @version(introduced="0.16.0b1")
    def clone(self, *,
              begin: str, # TODO add Coordinates class when it is written
              end: str,
              destination: str,
              mask_mode: Literal["replace", "masked", "filtered"]="replace",
              clone_mode: Literal["force", "move", "normal"]="normal",
              tile_name: Optional[Union[str, int]]=None,
              tile_data: int=-1,
              block_states: Optional[List[str, Any]]=None) -> ExecutedCommand: # TODO add block predicate thingy when it is written
        cb = self.clone_cb()
        self.param_version_introduced("block_states", block_states, "1.16.210.53")
        cmd = ExecutedCommand(self.fh, "clone", cb.build(begin=begin, end=end, destination=destination, mask_mode=mask_mode,
                                                         clone_mode=clone_mode, tile_name=tile_name, tile_data=tile_data, block_states=block_states))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def clone_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("clone")
        nt = lambda param: (param, _gt(cls.clone, param))
        cb.add_param(*nt("begin"))
        cb.add_param(*nt("end"))
        cb.add_param(*nt("destination"))
        node = cb.add_branch_node()
        cb_filtered = node.add_branch("mask_mode", ["filtered"])
        cb_filtered.add_switch("clone_mode", _go(cls.clone, "clone_mode"))
        cb_filtered.add_param(*nt("tile_name"))
        node2 = cb_filtered.add_branch_node()
        node2.add_branch().add_param(*nt("tile_data"), default=_gd(cls.clone, "tile_data"))
        node2.add_branch().add_param(*nt("block_states"))
        cb_others = node.add_branch("mask_mode", ["replace", "masked"])
        cb_others.add_switch("clone_mode", _go(cls.clone, "clone_mode"))
        return cb

    @version(introduced="0.16.0b1")
    def wsserver(self, server_uri: str) -> ExecutedCommand:
        cb = self.wsserver_cb()
        cmd = ExecutedCommand(self.fh, "wsserver", cb.build(server_uri=server_uri))
        self.fh.commands.append(cmd)
        return cmd
    connect = wsserver
    @classmethod
    def wsserver_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("wsserver")
        nt = lambda param: (param, _gt(cls.wsserver, param))
        cb.add_param(*nt("server_uri"))
        return cb
    connect_cb = wsserver_cb

    #/dedicatedwsserver

    @version(introduced="a1.0.16")
    def deop(self, target: BedrockSelector) -> ExecutedCommand:
        cb = self.deop_cb()
        cmd = ExecutedCommand(self.fh, "deop", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def deop_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("deop")
        nt = lambda param: (param, _gt(cls.deop, param))
        cb.add_param(*nt("target"), playeronly=True, singleonly=True)
        return cb

class JavaRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFuncHandler` and access the commands via the ‘r’ attribute.
    """
    @staticmethod
    def version(introduced: Optional[str]=None, deprecated: Optional[str]=None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                pack_version = self.fh.p.version
                if introduced is not None and pack_version < JavaVersion(introduced):
                    warnings.warn(f"The command `{func.__name__}` was introduced in {introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
                elif deprecated is not None and pack_version >= JavaVersion(deprecated):
                    warnings.warn(f"The command `{func.__name__}` was deprecated in {deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
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

    @version(introduced="17w13a")
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

    @version(introduced="20w17a")
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

    @version(introduced="20w17a")
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

    @version(introduced="20w17a")
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

    @version(introduced="a1.0.16")
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

    @version(introduced="a1.0.16")
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

    @version(introduced="a1.0.16")
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

    @version(introduced="18w05a")
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

    @version(introduced="18w05a")
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

    @version(introduced="18w05a")
    def bossbar_list(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "bossbar", "bossbar list")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def bossbar_list_cb(cls) -> CommandBuilder:
        return CommandBuilder("bossbar list")

    @version(introduced="18w05a")
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

    @version(introduced="18w05a")
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
        node.add_branch(literal="color").add_switch("color", _go(cls.bossbar_set, "color"))
        node.add_branch(literal="max").add_param(*nt("max"), range=lambda x: 1 <= x <= 2147483647)
        node.add_branch(literal="name").add_param(*nt("name"))
        node.add_branch(literal="players").add_param(*nt("players"), playeronly=True, optional=True)
        node.add_branch(literal="style").add_switch("style", _go(cls.bossbar_set, "style"))
        node.add_branch(literal="value").add_param(*nt("value"), range=lambda x: 0 <= x <= 2147483647)
        node.add_branch(literal="visible").add_param(*nt("visible"))
        return cb

    @version(introduced="17w45a")
    def clear(self, target: JavaSelector=JavaSelector.s,
              item: Optional[str]=None, # TODO item predicate thingy
              count: Optional[int]=None) -> ExecutedCommand:
        if self.fh.p.version < JavaVersion("17w45a"):
            return self.clear_pre17w45a(target=target, item=item, count=count)
        cb = self.clear_cb()
        cmd = ExecutedCommand(self.fh, "clear", cb.build(target=target, item=item, count=count))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def clear_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("clear")
        nt = lambda param: (param, _gt(cls.clear, param))
        cb.add_param(*nt("target"), default=_gd(cls.clear, "target"), optional=True, playeronly=True)
        cb.add_param(*nt("item"), optional=True)
        cb.add_param(*nt("count"), optional=True, range=lambda x: 0 <= x <= 2147483647)
        return cb
    @version(introduced="12w37a", deprecated="17w45a")
    def clear_pre17w45a(self, target: JavaSelector=JavaSelector.p,
                        item: Optional[str]=None, # TODO add block predicate when it is written
                        data: Optional[int]=None,
                        count: Optional[int]=None,
                        nbt: Optional[dict]=None) -> ExecutedCommand: # TODO NBT class when it is written
        cb = self.clear_pre17w45a_cb()
        self.param_version_introduced("item", item, "12w38a")
        self.param_version_introduced("data", data, "14w02a")
        cmd = ExecutedCommand(self.fh, "clear", cb.build(target=target, item=item, data=data, count=count, nbt=nbt))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def clear_pre17w45a_cb(cls, version: JavaVersion=JavaVersion("17w45a")) -> CommandBuilder:
        cb = CommandBuilder("clear")
        nt = lambda param: (param, _gt(cls.clear_pre17w45a, param))
        cb.add_param(*nt("target"), default=_gd(cls.clear_pre17w45a, "target"), optional=True, playeronly=True)
        if version >= JavaVersion("12w38a"): cb.add_param(*nt("item"), optional=True)
        if version >= JavaVersion("14w02a"): cb.add_param(*nt("data"), optional=True)
        cb.add_param(*nt("count"), optional=True)
        cb.add_param(*nt("nbt"), optional=True)
        return cb

    @version(introduced="14w03a")
    def clone(self, *,
              begin: str, # TODO add Coordinates class when it is written
              end: str,
              destination: str,
              mask_mode: Literal["replace", "masked", "filtered"]="replace",
              clone_mode: Literal["force", "move", "normal"]="normal",
              filter_: Optional[str]=None) -> ExecutedCommand: # TODO add block predicate when it is written
        cb = self.clone_cb()
        self.option_version_introduced("clone_mode", clone_mode, "14w10a", "force")
        self.option_version_introduced("clone_mode", clone_mode, "14w20a", "move")
        cmd = ExecutedCommand(self.fh, "clean", cb.build(begin=begin, end=end, destination=destination,
                                                         mask_mode=mask_mode, clone_mode=clone_mode, filter=filter_))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def clone_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("clone")
        nt = lambda param: (param, _gt(cls.clone, param))
        cb.add_param(*nt("begin"))
        cb.add_param(*nt("end"))
        cb.add_param(*nt("destination"))
        node = cb.add_branch_node()
        node.add_branch("mask_mode", ["filtered"]).add_param(*nt("filter"))
        node.add_branch("mask_mode", ["replace", "masked"])
        cb.add_switch("clone_mode", _go(cls.clone, "clone_mode"))
        return cb

    @version(introduced="17w45b")
    def data_get(self,
                 block: Optional[str]=None,
                 entity: Optional[JavaSelector]=None,  # TODO add Coordinates class when it is written
                 storage: Optional[str]=None, # TODO add ResourceLocation class when it is written
                 path: Optional[str]=None, # TODO add NBTPath class when it is written
                 scale: Optional[float]=None) -> ExecutedCommand:
        cb = self.data_get_cb()
        self.param_version_introduced("storage", storage, "19w38a")
        cmd = ExecutedCommand(self.fh, "data", cb.build(block=block, entity=entity, storage=storage, path=path, scale=scale))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def data_get_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("data get")
        nt = lambda param: (param, _gt(cls.data_get, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        node.add_branch(literal="storage").add_param(*nt("storage"))
        cb.add_param(*nt("path"), optional=True)
        cb.add_param(*nt("scale"), optional=True)
        return cb

    @version(introduced="17w45b")
    def data_merge(self, *,
                   block: Optional[str]=None,
                   entity: Optional[JavaSelector]=None,  # TODO add Coordinates class when it is written
                   storage: Optional[str]=None,
                   nbt: dict) -> ExecutedCommand: # TODO add NBT class when it is written
        cb = self.data_merge_cb()
        self.param_version_introduced("storage", storage, "19w38a")
        cmd = ExecutedCommand(self.fh, "data",
                              cb.build(block=block, entity=entity, storage=storage, nbt=nbt))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def data_merge_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("data merge")
        nt = lambda param: (param, _gt(cls.data_merge, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        node.add_branch(literal="storage").add_param(*nt("storage"))
        cb.add_param(*nt("nbt"))
        return cb

    @version(introduced="18w43a")
    def data_modify(self, *,
                    block: Optional[str]=None,
                    entity: Optional[JavaSelector]=None,  # TODO add Coordinates class when it is written
                    storage: Optional[str]=None,
                    target_path: str, # TODO add NBTPath when it is written
                    mode: Literal["add", "index", "merge", "prepend", "set"],
                    index: Optional[int]=None,
                    from_block: Optional[str]=None,
                    from_entity: Optional[JavaSelector]=None,  # TODO add Coordinates class when it is written
                    from_storage: Optional[str]=None,
                    source_path: Optional[str]=None, # TODO add NBTPath when it is written
                    value: Optional[Any]=None) -> ExecutedCommand:
        cb = self.data_modify_cb()
        self.param_version_introduced("storage", storage, "19w38a")
        cmd = ExecutedCommand(self.fh, "data", cb.build(block=block, entity=entity, storage=storage, target_path=target_path,
                                                        mode=mode, index=index, from_block=from_block, from_entity=from_entity,
                                                        from_storage=from_storage, source_path=source_path, value=json.dumps(value)))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def data_modify_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("data modify")
        nt = lambda param: (param, _gt(cls.data_merge, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        node.add_branch(literal="storage").add_param(*nt("storage"))
        cb.add_param(*nt("target_path"))
        node2 = cb.add_branch_node()
        node2.add_branch("mode", ["index"]).add_param(*nt("index"), range=lambda x: -2147483648 <= x <= 2147483647)
        node2.add_branch("mode", ["add", "merge", "prepend", "set"])
        node3 = cb.add_branch_node()
        cb_from = node3.add_branch(literal="from")
        node4 = cb_from.add_branch_node()
        node4.add_branch(literal="block").add_param(*nt("block"))
        node4.add_branch(literal="entity").add_param(*nt("entity"))
        node4.add_branch(literal="storage").add_param(*nt("storage"))
        cb_from.add_param(*nt("source_path"), optional=True)
        node3.add_branch(literal="value").add_param(*nt("value"))
        return cb

    @version(introduced="17w45b")
    def data_remove(self, *,
                    block: Optional[str]=None,
                    entity: Optional[JavaSelector]=None,  # TODO add Coordinates class when it is written
                    storage: Optional[str]=None,
                    path: str) -> ExecutedCommand: # TODO add NBTPath class when it is written
        cb = self.data_remove_cb()
        self.param_version_introduced("storage", storage, "19w38a")
        cmd = ExecutedCommand(self.fh, "data",
                              cb.build(block=block, entity=entity, storage=storage, path=path))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def data_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("data remove")
        nt = lambda param: (param, _gt(cls.data_remove, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        node.add_branch(literal="storage").add_param(*nt("storage"))
        cb.add_param(*nt("path"))
        return cb

    @version(introduced="17w46a")
    def datapack_enable(self,
                        name: str,
                        priority: Optional[Literal["first", "last", "before", "after"]]=None,
                        existing_pack: Optional[str]=None) -> ExecutedCommand:
        cb = self.datapack_enable_cb()
        cmd = ExecutedCommand(self.fh, "datapack", cb.build(name=name, priority=priority, existing_pack=existing_pack))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def datapack_enable_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("datapack enable")
        nt = lambda param: (param, _gt(cls.datapack_enable, param))
        cb.add_param(*nt("name"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        node = cb.add_branch_node(optional=True)
        node.add_branch(switch_name="priority", switch_options=["first", "last"])
        node.add_branch(switch_name="priority", switch_options=["before", "after"]).add_param(*nt("existing_pack"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        return cb

    @version(introduced="17w46a")
    def datapack_disable(self, name: str) -> ExecutedCommand:
        cb = self.datapack_disable_cb()
        cmd = ExecutedCommand(self.fh, "datapack", cb.build(name=name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def datapack_disable_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("datapack enable")
        nt = lambda param: (param, _gt(cls.datapack_disable, param))
        cb.add_param(*nt("name"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        return cb

    @version(introduced="17w46a")
    def datapack_list(self, view: Optional[Literal["available", "enabled"]]) -> ExecutedCommand:
        cb = self.datapack_list_cb()
        cmd = ExecutedCommand(self.fh, "datapack", cb.build(view=view))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def datapack_list_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("datapack list")
        nt = lambda param: (param, _gt(cls.datapack_list, param))
        cb.add_param(*nt("datapack"), optional=True)
        return cb

    @version(introduced="18w03a")
    def debug(self,
              action: Literal["start", "stop", "function", "report"],
              function_name: Optional[str]=None) -> ExecutedCommand: # TODO function name thingy when it is written
        cb = self.debug_cb()
        self.option_version_introduced("action", action, "1.14.4pre1", "report")
        self.option_version_deprecated("action", action, "1.17pre1", "report")
        self.option_version_introduced("action", action, "21w15a", "function")
        cmd = ExecutedCommand(self.fh, "debug", cb.build(action=action, function_name=function_name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def debug_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("debug")
        nt = lambda param: (param, _gt(cls.debug, param))
        node = cb.add_branch_node()
        node.add_branch(switch_name="action", switch_options=["start", "stop", "report"])
        node.add_branch(switch_name="action", switch_options=["function"]).add_param(*nt("name"))
        return cb

    @version(introduced="12w22a")
    def defaultgamemode(self, mode: Literal["survival", "creative", "adventure", "spectator"]) -> ExecutedCommand:
        cb = self.defaultgamemode_cb()
        self.option_version_introduced("mode", mode, "14w05a", "spectator")
        cmd = ExecutedCommand(self.fh, "defaultgamemode", cb.build(mode=mode))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def defaultgamemode_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("defaultgamemode")
        nt = lambda param: (param, _gt(cls.defaultgamemode, param))
        cb.add_param(*nt("mode"))
        return cb

    @version(introduced="a1.0.16")
    def deop(self, targets: JavaSelector) -> ExecutedCommand:
        cb = self.deop_cb()
        cmd = ExecutedCommand(self.fh, "deop", cb.build(target=targets))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def deop_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("deop")
        nt = lambda param: (param, _gt(cls.deop, param))
        cb.add_param(*nt("targets"), playeronly=True)
        return cb

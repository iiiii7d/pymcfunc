from __future__ import annotations

import inspect
import json
import warnings
from functools import wraps
from typing import Dict, Optional, Any, Callable, Literal, Tuple, get_args, TYPE_CHECKING, Union, TypeAlias, List
from uuid import UUID

from typing_extensions import Self

from pymcfunc.command_builder import CommandBuilder
from pymcfunc.coord import Coord, BlockCoord
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.nbt import Int, Path
from pymcfunc.selectors import JavaSelector, BedrockSelector
from pymcfunc.version import JavaVersion, BedrockVersion

if TYPE_CHECKING:
    from pymcfunc.func_handler import UniversalFuncHandler

RawJson: TypeAlias = Union[dict, list]
ResourceLocation: TypeAlias = str

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
    def camerashake_add(self, target: BedrockSelector=BedrockSelector.s(),
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
    def camerashake_stop(self, target: BedrockSelector=BedrockSelector.s()) -> ExecutedCommand:
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
    def clear(self, player: BedrockSelector=BedrockSelector.s(),
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
        cb.add_param(*nt("data"), optional=True, range=lambda x: -1 <= x <= Int.max)
        cb.add_param(*nt("max_count"), optional=True, range=lambda x: -1 <= x <= Int.max)
        return cb

    @version(introduced="1.16.100.57")
    def clearspawnpoint(self, player: BedrockSelector=BedrockSelector.s()) -> ExecutedCommand:
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
              begin: BlockCoord,
              end: BlockCoord,
              destination: BlockCoord,
              mask_mode: Literal["replace", "masked", "filtered"]="replace",
              clone_mode: Literal["force", "move", "normal"]="normal",
              tile_name: Optional[Union[str, int]]=None,
              tile_data: int=-1,
              block_states: Optional[Dict[str, Any]]=None) -> ExecutedCommand: # TODO add block state thingy when it is written
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
        node2.add_branch().add_param(*nt("tile_data"), default=_gd(cls.clone, "tile_data"), range=lambda x: -1 <= x <= 65536)
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
    def deop(self, target: Union[str, BedrockSelector]) -> ExecutedCommand:
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

    @version(introduced="1.17.10.22")
    def dialogue(self, *,
                 mode: Literal["open", "change"],
                 npc: BedrockSelector,
                 player: Optional[BedrockSelector]=None,
                 scene_name: Optional[str]=None) -> ExecutedCommand:
        cb = self.dialogue_cb()
        cmd = ExecutedCommand(self.fh, "dialogue", cb.build(mode=mode, npc=npc, player=player, scene_name=scene_name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def dialogue_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("dialogue")
        nt = lambda param: (param, _gt(cls.dialogue, param))
        node = cb.add_branch_node()
        cb_open = node.add_branch(literal="open")
        cb_open.add_param(*nt("npc"))
        cb_open.add_param(*nt("player"), playeronly=True)
        cb_open.add_param(*nt("scene_name"), optional=True, spaces="q")
        cb_change = node.add_branch(literal="change")
        cb_change.add_param(*nt("npc"))
        cb_change.add_param(*nt("scene_name"), spaces="q")
        cb_change.add_param(*nt("player"), playeronly=True, optional=True)
        return cb

    @version(introduced="1.0.5.0")
    def difficulty(self, difficulty: Union[int, Literal["peaceful", "easy", "normal", "hard", "p", "e", "n", "h"]]) -> ExecutedCommand:
        cb = self.difficulty_cb()
        cmd = ExecutedCommand(self.fh, "difficulty", cb.build(difficulty=difficulty))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def difficulty_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("difficulty")
        nt = lambda param: (param, _gt(cls.difficulty, param))
        cb.add_param(*nt("difficulty"), range=lambda x: 0 <= x <= 3)
        return cb

    @version(introduced="1.0.5.0")
    def effect_give(self,
                    targets: BedrockSelector,
                    effect: str,
                    seconds: int=30,
                    amplifier: int=1,
                    hide_particles: bool=False) -> ExecutedCommand:
        cb = self.effect_give_cb()
        self.param_version_introduced("hide_particles", hide_particles, "14w06a", default=False)
        cmd = ExecutedCommand(self.fh, "effect", cb.build(targets=targets, effect=effect, seconds=seconds, amplifier=amplifier))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def effect_give_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("effect")
        nt = lambda param: (param, _gt(cls.effect_give, param))
        cb.add_param(*nt("targets"))
        cb.add_param(*nt("effect"))
        cb.add_param(*nt("seconds"), default=_gd(cls.effect_give, "seconds"), range=lambda x: 0 <= x <= Int.max)
        cb.add_param(*nt("amplifier"), default=_gd(cls.effect_give, "amplifier"), range=lambda x: 0 <= x <= 255)
        cb.add_param(*nt("hide_particles"), default=False)
        return cb
    
    @version(introduced="1.0.5.0")
    def effect_clear(self, targets: BedrockSelector) -> ExecutedCommand:
        cb = self.effect_clear_cb()
        cmd = ExecutedCommand(self.fh, "effect", cb.build(targets=targets))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def effect_clear_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("effect")
        nt = lambda param: (param, _gt(cls.effect_clear, param))
        cb.add_param(*nt("targets"))
        cb.add_literal("clear")
        return cb

    @version(introduced="0.16.0b5")
    def enchant(self, target: BedrockSelector, enchantment: Union[str, int], level: int=1) -> ExecutedCommand:
        cb = self.enchant_cb()
        cmd = ExecutedCommand(self.fh, "enchant", cb.build(target=target, enchantment=enchantment, level=level))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def enchant_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("enchant")
        nt = lambda param: (param, _gt(cls.enchant, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("enchantment"))
        cb.add_param(*nt("level"), range=lambda x: 1 <= x <= Int.max, default=_gd(cls.enchant, "level"))
        return cb

    @version(introduced="1.16.100.57")
    def event(self, target: BedrockSelector, event_name: str) -> ExecutedCommand:
        cb = self.event_cb()
        cmd = ExecutedCommand(self.fh, "event", cb.build(target=target, event_name=event_name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def event_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("event entity")
        nt = lambda param: (param, _gt(cls.event, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("event_name"), spaces="q")
        return cb

    @version(introduced="0.16.0b1")
    def execute(self, origin: BedrockSelector, *,
                position: Coord,
                detect_pos: Optional[Coord]=None,
                detect_block: Optional[str]=None,
                detect_data: int=-1,
                commands: Union[ExecutedCommand, List[ExecutedCommand]]) -> Union[ExecutedCommand, List[ExecutedCommand]]:
        cb = self.execute_cb()
        cmds = []
        commands = [commands] if not isinstance(commands, list) else commands # TODO flatten list
        commands = [item for sublist in commands for item in sublist]
        for command in commands:
            cmd = ExecutedCommand(self.fh, "execute", cb.build(origin=origin, position=position, detect_pos=detect_pos,
                                                               detect_block=detect_block, detect_data=detect_data,
                                                               command=command.command_string))
            self.fh.commands[self.fh.commands.index(command)] = cmd
            cmds.append(cmd)
        return cmds[0] if len(cmds) == 1 else cmds
    @classmethod
    def execute_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("execute")
        nt = lambda param: (param, _gt(cls.execute, param))
        cb.add_param(*nt("origin"))
        cb.add_param(*nt("position"))
        cb_detect = cb.add_branch_node(optional=True).add_branch(literal="detect")
        cb_detect.add_param(*nt("detect_pos"))
        cb_detect.add_param(*nt("detect_block"))
        cb_detect.add_param(*nt("detect_data"), default=_gd(cls.execute, "detect_data"))
        cb.add_param("command", str, spaces=True)
        return cb

    @version(introduced="0.16.0b1")
    def xp(self, *,
           amount: int,
           levels: bool=False,
           player: BedrockSelector=BedrockSelector.s()) -> ExecutedCommand:
        cb = self.xp_cb()
        cmd = ExecutedCommand(self.fh, "xp", cb.build(amount=str(amount)+"L" if levels else amount, player=player))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def xp_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("xp")
        nt = lambda param: (param, _gt(cls.xp, "player"))
        cb.add_param("amount", Union[str, int], range=lambda x: 0 <= x <= Int.max)
        cb.add_param(*nt("player"), optional=True, default=_gd(cls.xp, "player"))
        return cb

    @version(introduced="0.16.0b1")
    def fill(self, *,
             from_: BlockCoord,
             to: BlockCoord,
             block: str,
             tile_data: int=0,
             block_states: Optional[str]=None,
             fill_mode: Literal["destroy", "hollow", "keep", "outline", "replace"]="replace",
             replace_block: Optional[str]=None,
             replace_data_value: Optional[int]=None) -> ExecutedCommand:
        cb = self.fill_cb()
        self.param_version_introduced("block_states", block_states, "1.16.210.53")
        cmd = ExecutedCommand(self.fh, "fill", cb.build(from_=from_, to=to, block=block, tile_data=tile_data,
                                                        block_states=block_states, fill_mode=fill_mode,
                                                        replace_block=replace_block, replace_data_value=replace_data_value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def fill_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("fill")
        nt = lambda param: (param, _gt(cls.fill, "fill"))
        cb.add_param(*nt("from_"))
        cb.add_param(*nt("to"))
        cb.add_param(*nt("block"))
        node = cb.add_branch_node()
        node.add_branch().add_param(*nt("tile_data"), default=_gd(cls.fill, "tile_data"))
        node.add_branch().add_param(*nt("block_states"))
        node2 = cb.add_branch_node()
        cb_replace = node2.add_branch(switch_name="mode", switch_options=["replace"])
        cb_replace.add_param(*nt("replace_block"), optional=True)
        cb_replace.add_param(*nt("replace_data_value"), optional=True)
        node2.add_branch(switch_name="mode", switch_options=["destroy", "hollow", "keep", "outline"])
        return cb

    @version(introduced="1.16.100.54")
    def fog(self, mode: Literal["push", "pop", "remove"], *,
            player: BedrockSelector=BedrockSelector.s(),
            fog_id: Optional[str]=None,
            user_provided_id: str) -> ExecutedCommand:
        cb = self.fog_cb()
        cmd = ExecutedCommand(self.fh, "fog", cb.build(player=player, mode=mode, fog_id=fog_id, user_provided_id=user_provided_id))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def fog_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("fog")
        nt = lambda param: (param, _gt(cls.fog, "fog"))
        cb.add_param(*nt("player"))
        node = cb.add_branch_node()
        node.add_branch(switch_name="mode", switch_options=["push"]).add_param(*nt("fog_id"), spaces="q")
        node.add_branch(switch_name="mode", switch_options=["pop", "remove"])
        cb.add_param(*nt("user_provided_id"), spaces="q")
        return cb

    @version(introduced="1.8.0.8")
    def function(self, name: str) -> ExecutedCommand:  # TODO add ResourceLocation when it is written
        cb = self.function_cb()
        cmd = ExecutedCommand(self.fh, "function", cb.build(name=name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def function_cb(cls):
        cb = CommandBuilder("function")
        nt = lambda param: (param, _gt(cls.function, param))
        cb.add_param(*nt("name"))
        return cb

    @version(introduced="0.16.0b1")
    def gamemode(self, mode: Literal["survival", "creative", "adventure", "s", "c", "a", 0, 1, 2],
                 target: Union[BedrockSelector, str] = BedrockSelector.s()) -> ExecutedCommand:
        cb = self.gamemode_cb()
        self.option_version_introduced("mode", mode, "1.1.0.0", "adventure")
        self.option_version_introduced("mode", mode, "1.1.0.0", "a")
        self.option_version_introduced("mode", mode, "1.1.0.0", 2)
        cmd = ExecutedCommand(self.fh, "gamemode", cb.build(mode=mode, target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gamemode_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("gamemode")
        nt = lambda param: (param, _gt(cls.gamemode, param))
        cb.add_param(*nt("mode"))
        cb.add_param(*nt("target"), default=_gd(cls.gamemode, "target"), playeronly=True)
        return cb

    @version(introduced="1.0.5.0")
    def gamerule(self, rule_name: str, value: Union[bool, int]) -> ExecutedCommand:
        cb = self.gamerule_cb()
        cmd = ExecutedCommand(self.fh, "gamerule", cb.build(rule_name=rule_name, value=value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gamerule_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("gamerule")
        nt = lambda param: (param, _gt(cls.gamerule, param))
        cb.add_param(*nt("rule_name"))
        cb.add_param(*nt("value"), optional=True)
        return cb

    @version(introduced="1.16.210.60")
    def gametest_runthis(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "gametest", "gametest runthis")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_runthis_cb(cls) -> CommandBuilder:
        return CommandBuilder("gametest runthis")

    @version(introduced="1.16.210.60")
    def gametest_run(self, test_name: str, rotation_steps: Optional[int]=None) -> ExecutedCommand:
        cb = self.gametest_run_cb()
        cmd = ExecutedCommand(self.fh, "gametest", cb.build(test_name=test_name, rotation_steps=rotation_steps))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_run_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("gametest run")
        nt = lambda param: (param, _gt(cls.gametest_run, param))
        cb.add_param(*nt("test_name"))
        cb.add_param(*nt("rotation_steps"), optional=True)
        return cb

    @version(introduced="1.16.210.60")
    def gametest_runset(self, tag: Optional[str]=None, rotation_steps: Optional[int]=None) -> ExecutedCommand:
        cb = self.gametest_run_cb()
        cmd = ExecutedCommand(self.fh, "gametest", cb.build(tag=tag, rotation_steps=rotation_steps))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_runset_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("gametest runset")
        nt = lambda param: (param, _gt(cls.gametest_runset, param))
        cb.add_param(*nt("tag"), optional=True)
        cb.add_param(*nt("rotation_steps"), optional=True)
        return cb

    @version(introduced="1.16.210.60")
    def gametest_clearall(self, radius: Optional[int]=None) -> ExecutedCommand:
        cb = self.gametest_clearall_cb()
        cmd = ExecutedCommand(self.fh, "gametest", cb.build(radius=radius))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_clearall_cb(cls):
        cb = CommandBuilder("gametest clearall")
        nt = lambda param: (param, _gt(cls.gametest_clearall, param))
        cb.add_param(*nt("radius"), optional=True)
        return cb

    @version(introduced="1.16.210.60")
    def gametest_pos(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "gametest", "gametest pos")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_pos_cb(cls) -> CommandBuilder:
        return CommandBuilder("gametest pos")

    @version(introduced="1.16.210.60")
    def gametest_create(self, test_name: str, width: Optional[int]=None, height: Optional[int]=None, depth: Optional[int]=None) -> ExecutedCommand:
        cb = self.gametest_clearall_cb()
        cmd = ExecutedCommand(self.fh, "gametest", cb.build(test_name=test_name, width=width, height=height, depth=depth))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_create_cb(cls):
        cb = CommandBuilder("gametest create")
        nt = lambda param: (param, _gt(cls.gametest_create, param))
        cb.add_param(*nt("test_name"))
        cb.add_param(*nt("width"), optional=True, range=lambda x: 0 <= x <= Int.max)
        cb.add_param(*nt("height"), optional=True, range=lambda x: 0 <= x <= Int.max)
        cb.add_param(*nt("depth"), optional=True, range=lambda x: 0 <= x <= Int.max)
        return cb

    @version(introduced="1.16.210.60")
    def gametest_runthese(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "gametest", "gametest runthese")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gametest_runthese_cb(cls) -> CommandBuilder:
        return CommandBuilder("gametest runthese")

    @version(introduced="0.16.0b1")
    def give(self, player: Union[str, BedrockSelector],
             item_name: str,
             amount: int=1,
             data: int=0,
             components: Optional[dict]=None) -> ExecutedCommand: # add ItemComponents class when it is written
        cb = self.give_cb()
        cmd = ExecutedCommand(self.fh, "give", cb.build(player=player, item_name=item_name, amount=amount, data=data, components=components))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def give_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("give")
        nt = lambda param: (param, _gt(cls.give, param))
        cb.add_param(*nt("player"), playeronly=True)
        cb.add_param(*nt("item_name"))
        cb.add_param(*nt("amount"), default=_gd(cls.give, "amount"))
        cb.add_param(*nt("data"), default=_gd(cls.give, "data"))
        cb.add_param(*nt("components"), optional=True)
        return cb

    @version(introduced="1.2.0.1")
    @education_edition
    def immutable(self, value: Optional[bool]=False) -> ExecutedCommand:
        cb = self.immutable_cb()
        cmd = ExecutedCommand(self.fh, "immutable", cb.build(value=value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def immutable_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("immutable")
        nt = lambda param: (param, _gt(cls.immutable, param))
        cb.add_param(*nt("value"), optional=True)
        return cb

    @version(introduced="1.16.0.57")
    def kick(self, target: Union[BedrockSelector, str],
             reason: str = "Kicked by an operator") -> ExecutedCommand:
        cb = self.kick_cb()
        cmd = ExecutedCommand(self.fh, "kick", cb.build(target=target, reason=reason))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def kick_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("kick")
        nt = lambda param: (param, _gt(cls.kick, param))
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("reason"), default=_gd(cls.kick, "reason"))
        return cb

    @version(introduced="1.16.0b1")
    def kill(self, target: Union[Union[BedrockSelector, UUID], str]=BedrockSelector.s()) -> ExecutedCommand:
        cb = self.kick_cb()
        cmd = ExecutedCommand(self.fh, "kick", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def kill_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("kick")
        nt = lambda param: (param, _gt(cls.kick, param))
        cb.add_param(*nt("target"))
        return cb

    @version(introduced="1.16.0b1")
    def list(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "list", "list")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def list_cb(cls) -> CommandBuilder:
        return CommandBuilder("list")

    @version(introduced="0.17.0.1")
    def locate(self, structure: str) -> ExecutedCommand:
        cb = self.locate_cb()
        cmd = ExecutedCommand(self.fh, "locate", cb.build(structure=structure))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def locate_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("locate")
        nt = lambda param: (param, _gt(cls.locate, param))
        cb.add_param(*nt("structure"))
        return cb

    @version(introduced="1.18.0.21")
    def loot(self, *,
             position: BlockCoord,
             loot_table: str, # TODO LootTable class
             tool: Union[str, Literal["mainhand", "offland"]]) -> ExecutedCommand: # TODO Item class?
        cb = self.loot_cb()
        cmd = ExecutedCommand(self.fh, "loot", cb.build(position=position, loot_table=loot_table, tool=tool))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def loot_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("loot spawn")
        nt = lambda param: (param, _gt(cls.loot, param))
        cb.add_param(*nt("position"))
        cb.add_literal("loot")
        cb.add_param(*nt("loot_table"))
        cb.add_param(*nt("tool"))
        return cb

    @version(introduced="1.0.5.0")
    def me(self, msg: str) -> ExecutedCommand:
        cb = self.me_cb()
        cmd = ExecutedCommand(self.fh, "me", cb.build(msg=msg))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def me_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("me")
        nt = lambda param: (param, _gt(cls.me, param))
        cb.add_param(*nt("msg"))
        return cb

    @version(introduced="1.11.0.3")
    def mobevent(self, event: Literal["minecraft:pillager_patrols_event",
                                      "minecraft:wandering_trader_event",
                                      "events_enabled"],
                 value: Optional[bool]=None) -> ExecutedCommand:
        cb = self.mobevent_cb()
        cmd = ExecutedCommand(self.fh, "mobevent", cb.build(event=event, value=value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def mobevent_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("mobevent")
        nt = lambda param: (param, _gt(cls.mobevent, param))
        cb.add_switch(*_go(cls.mobevent, "event"))
        cb.add_param(*nt("value"), optional=True)
        return cb

    @version(introduced="0.16.0b1")
    def msg(self, targets: Union[BedrockSelector, str], message: str) -> ExecutedCommand:
        cb = self.msg_cb()
        cmd = ExecutedCommand(self.fh, "msg", cb.build(targets=targets, message=message))
        self.fh.commands.append(cmd)
        return cmd
    tell = w = msg
    @classmethod
    def msg_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("msg")
        nt = lambda param: (param, _gt(cls.msg, param))
        cb.add_param(*nt("targets"), playeronly=True)
        cb.add_param(*nt("message"), spaces=True)
        return cb
    tell_cb = w_cb = msg_cb

    @version(introduced="1.16.100.58")
    def music_play(self, *,
                   track_name: str,
                   volume: Optional[float]=None,
                   fade_seconds: Optional[float]=None,
                   repeat_mode: Literal["loop", "play_once"]="play_once"):
        cb = self.music_play_cb()
        cmd = ExecutedCommand(self.fh, "music", cb.build(track_name=track_name, volume=volume,
                                                         fade_seconds=fade_seconds, repeat_mode=repeat_mode))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def music_play_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("music play")
        nt = lambda param: (param, _gt(cls.music_play, param))
        cb.add_param(*nt("track_name"), spaces="q"),
        cb.add_param(*nt("volume"), range=lambda x: 0 <= x <= 1)
        cb.add_param(*nt("fade_seconds"), range=lambda x: 0 <= x <= 10)
        cb.add_switch(*_go(cls.music_play, "repeat_mode"), default=_gd(cls.music_play, "repeat_mode"))
        return cb

    @version(introduced="1.16.100.58")
    def music_queue(self, *,
                    track_name: str,
                    volume: Optional[float] = None,
                    fade_seconds: Optional[float] = None,
                    repeat_mode: Literal["loop", "play_once"] = "play_once"):
        cb = self.music_queue_cb()
        cmd = ExecutedCommand(self.fh, "music", cb.build(track_name=track_name, volume=volume,
                                                         fade_seconds=fade_seconds, repeat_mode=repeat_mode))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def music_queue_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("music queue")
        nt = lambda param: (param, _gt(cls.music_queue, param))
        cb.add_param(*nt("track_name"), spaces="q"),
        cb.add_param(*nt("volume"), range=lambda x: 0 <= x <= 1)
        cb.add_param(*nt("fade_seconds"), range=lambda x: 0 <= x <= 10)
        cb.add_switch(*_go(cls.music_queue, "repeat_mode"), default=_gd(cls.music_queue, "repeat_mode"))
        return cb

    @version(introduced="1.16.100.58")
    def music_stop(self, fade_seconds: Optional[float] = None,):
        cb = self.music_stop_cb()
        cmd = ExecutedCommand(self.fh, "music", cb.build(fade_seconds=fade_seconds))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def music_stop_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("music stop")
        nt = lambda param: (param, _gt(cls.music_play, param))
        cb.add_param(*nt("fade_seconds"), range=lambda x: 0 <= x <= 10)
        return cb

    @version(introduced="1.16.100.58")
    def music_volume(self, volume: Optional[float]):
        cb = self.music_volume_cb()
        cmd = ExecutedCommand(self.fh, "music", cb.build(volume=volume))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def music_volume_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("music volume")
        nt = lambda param: (param, _gt(cls.music_volume, param))
        cb.add_param(*nt("volume"), range=lambda x: 0 <= x <= 1)
        return cb

    @version(introduced="a1.0.16")
    def op(self, target: Union[str, BedrockSelector]) -> ExecutedCommand:
        cb = self.op_cb()
        cmd = ExecutedCommand(self.fh, "op", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def op_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("op")
        nt = lambda param: (param, _gt(cls.op, param))
        cb.add_param(*nt("target"), playeronly=True, singleonly=True)
        return cb

    # version unknown
    def ops(self, view: Literal["list", "reload"]) -> ExecutedCommand:
        cb = self.ops_cb()
        cmd = ExecutedCommand(self.fh, "ops", cb.build(view=view))
        self.fh.commands.append(cmd)
        return cmd
    permissions = ops
    @classmethod
    def ops_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ops")
        cb.add_switch(*_go(cls.ops, "view"))
        return cb
    permissions_cb = ops_cb

    @version(introduced="1.0.5.0")
    def particle(self, effect: str, position: Coord) -> ExecutedCommand:
        cb = self.particle_cb()
        cmd = ExecutedCommand(self.fh, "particle", cb.build(effect=effect, position=position))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def particle_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("particle")
        nt = lambda param: (param, _gt(cls.particle, param))
        cb.add_param(*nt("effect"))
        cb.add_param(*nt("position"))
        return cb

    @version(introduced="1.16.100.52")
    def playanimation(self, target: Union[str, BedrockSelector], *,
                      animation: str,
                      next_state: Optional[str]=None,
                      blend_out_time: float,
                      stop_expression: str, # TODO MoLang
                      controller: str) -> ExecutedCommand:
        cb = self.playanimation_cb()
        cmd = ExecutedCommand(self.fh, "playanimation", cb.build(target=target, animation=animation, next_state=next_state,
                                                                 blend_out_time=blend_out_time, stop_expression=stop_expression,
                                                                 controller=controller))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def playanimation_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("playanimation")
        nt = lambda param: (param, _gt(cls.playanimation, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("animation"), spaces="q", regex=r"^.*(?<!\.v1\.0)$")
        cb.add_param(*nt("next_states"), spaces="q")
        cb.add_param(*nt("blend_out_time"))
        cb.add_param(*nt("stop_expression"), spaces="q")
        cb.add_param(*nt("controller"), spaces="q")
        return cb

    @version(introduced="1.0.5.0")
    def playsound(self, sound: str,
                  player: Union[str, BedrockSelector],
                  position: Optional[Coord]=None,
                  volume: float=1.0,
                  pitch: float=1.0,
                  minimum_volume: float=0.0) -> ExecutedCommand:
        cb = self.playsound_cb()
        cmd = ExecutedCommand(self.fh, "playsound", cb.build(sound=sound, player=player, position=position, volume=volume,
                                                             pitch=pitch, minimum_volume=minimum_volume))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def playsound_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("playsound")
        nt = lambda param: (param, _gt(cls.playsound, param))
        cb.add_param(*nt("sound"), spaces="q")
        cb.add_param(*nt("player"), playeronly=True)
        cb.add_param(*nt("position"), optional=True)
        cb.add_param(*nt("volume"), default=_gd(cls.playsound, "volume"))
        cb.add_param(*nt("pitch"), default=_gd(cls.playsound, "pitch"))
        cb.add_param(*nt("minimum_volume"), default=_gd(cls.playsound, "minimum_volume"))
        return cb

    @version(introduced="1.8.0.8")
    def reload(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "reload", "reload")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def reload_cb(cls) -> CommandBuilder:
        return CommandBuilder("reload")

    @education_edition
    def remove(self, targets: Optional[BedrockSelector]=None) -> ExecutedCommand:
        cb = self.remove_cb()
        cmd = ExecutedCommand(self.fh, "remove", cb.build(targets=targets))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("remove")
        nt = lambda param: (param, _gt(cls.remove, param))
        cb.add_param(*nt("targets"))
        return cb
    
    @version(introduced="1.0.5.0")
    def replaceitem(self, *,
                    block: Optional[BlockCoord]=None,
                    entity: Optional[Union[str, BedrockSelector]]=None,
                    slot_type: str, # TODO Slot class
                    slot_id: int,
                    old_item_handling: Optional[Literal["destroy", "keep"]]=None,
                    item_name: str,
                    amount: int=1,
                    data: int=0,
                    components: Optional[dict]=None) -> ExecutedCommand: # TODO ItemComponents class
        cb = self.replaceitem_cb()
        cmd = ExecutedCommand(self.fh, "replaceitem", cb.build(block=block, entity=entity, slot_type=slot_type, slot_id=slot_id,
                                                               old_item_handling=old_item_handling, item_name=item_name,
                                                               amount=amount, data=data, components=components))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def replaceitem_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("replaceitem")
        nt = lambda param: (param, _gt(cls.replaceitem, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        cb.add_param(*nt("slot_type"))
        cb.add_param(*nt("slot_id"), range=lambda x: Int.min <= x <= Int.max)
        cb.add_branch_node(optional=True).add_branch().add_switch(*_go(cls.replaceitem, "old_item_handling"))
        cb.add_param(*nt("item_name"))
        cb.add_param(*nt("amount"), default=_gd(cls.replaceitem, "amount"), range=lambda x: 1 <= x <= 64)
        cb.add_param(*nt("data"), default=_gd(cls.replaceitem, "data"), range=lambda x: Int.min <= x <= Int.max)
        cb.add_param(*nt("components"), optional=True)
        return cb

    @version(introduced="1.16.100.52")
    def ride_start_riding(self, *,
                          riders: Union[str, BedrockSelector],
                          ride: Union[str, BedrockSelector],
                          teleport_rules: Literal["teleport_ride", "teleport_rider"]="teleport_rider",
                          fill_type: Optional[Literal["if_group_fits", "until_full"]]=None) -> ExecutedCommand:
        cb = self.ride_start_riding.cb()
        cmd = ExecutedCommand(self.fh, "ride", cb.build(riders=riders, ride=ride, teleport_rules=teleport_rules, fill_type=fill_type))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ride_start_riding_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ride")
        nt = lambda param: (param, _gt(cls.ride_start_riding, param))
        cb.add_param(*nt("riders"))
        cb.add_literal("start_riding")
        cb.add_param(*nt("ride"), singleonly=True)
        cb.add_switch(*_go(cls.ride_start_riding, "teleport_rules"))
        cb.add_switch(*_go(cls.ride_start_riding, "fill_type"))
        return cb

    @version(introduced="1.16.100.52")
    def ride_stop_riding(self, *, riders: Union[str, BedrockSelector]) -> ExecutedCommand:
        cb = self.ride_stop_riding_cb()
        cmd = ExecutedCommand(self.fh, "ride", cb.build(riders=riders))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ride_stop_riding_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ride")
        nt = lambda param: (param, _gt(cls.ride_stop_riding, param))
        cb.add_param(*nt("riders"))
        cb.add_literal("stop_riding")
        return cb

    @version(introduced="1.16.100.52")
    def ride_evict_riders(self, *, rides: Union[str, BedrockSelector]) -> ExecutedCommand:
        cb = self.ride_evict_riders_cb()
        cmd = ExecutedCommand(self.fh, "ride", cb.build(rides=rides))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ride_evict_riders_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ride")
        nt = lambda param: (param, _gt(cls.ride_evict_riders, param))
        cb.add_param(*nt("rides"))
        cb.add_literal("evict_riders")
        return cb

    @version(introduced="1.16.100.52")
    def ride_summon_rider(self, *,
                          rides: Union[str, BedrockSelector],
                          entity_type: str,
                          spawn_event: Optional[str]=None,
                          name_tag: Optional[str]=None) -> ExecutedCommand:
        cb = self.ride_summon_rider_cb()
        cmd = ExecutedCommand(self.fh, "ride", cb.build(rides=rides, entity_type=entity_type,
                                                        spawn_event=spawn_event, name_tag=name_tag))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ride_summon_rider_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ride")
        nt = lambda param: (param, _gt(cls.ride_summon_rider, param))
        cb.add_param(*nt("rides"))
        cb.add_literal("summon_rider")
        cb.add_param(*nt("entity_type"))
        cb.add_param(*nt("spawn_event"), spaces="q", optional=True)
        cb.add_param(*nt("name_tag"), spaces="q", optional=True)
        return cb

    @version(introduced="1.16.100.52")
    def ride_summon_ride(self, *,
                         riders: Union[str, BedrockSelector],
                         entity_type: str,
                         ride_rules: Literal["no_ride_change", "reassign_rides", "skip_riders"]="reassign_rides",
                         spawn_event: Optional[str] = None,
                         name_tag: Optional[str] = None) -> ExecutedCommand:
        cb = self.ride_summon_rider_cb()
        cmd = ExecutedCommand(self.fh, "ride", cb.build(riders=riders, entity_type=entity_type, ride_rules=ride_rules,
                                                        spawn_event=spawn_event, name_tag=name_tag))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def ride_summon_ride_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("ride")
        nt = lambda param: (param, _gt(cls.ride_summon_ride, param))
        cb.add_param(*nt("riders"))
        cb.add_literal("summon_ride")
        cb.add_param(*nt("entity_type"))
        cb.add_switch(*_go(cls.ride_summon_ride, "ride_rules"), default=_gd(cls.ride_summon_ride, "ride_rules"))
        cb.add_param(*nt("spawn_event"), spaces="q")
        cb.add_param(*nt("name_tag"), spaces="q")
        return cb

    @version(introduced="1.6.1")
    def save(self, action: Literal["hold", "query", "resume"]) -> ExecutedCommand:
        cb = self.save_cb()
        cmd = ExecutedCommand(self.fh, "save", cb.build(action=action))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def save_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("save")
        cb.add_switch(*_go(cls.save, "action"))
        return cb

    @version(introduced="0.16.0b1")
    def say(self, msg: str) -> ExecutedCommand:
        cb = self.say_cb()
        cmd = ExecutedCommand(self.fh, "say", cb.build(msg=msg))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def say_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("say")
        nt = lambda param: (param, _gt(cls.say, param))
        cb.add_param(*nt("msg"), spaces=True)
        return cb

    @version(introduced="1.16.100.59")
    def schedule_on_area_loaded_add(self, *,
                                    cuboid_from: BlockCoord,
                                    cuboid_to: BlockCoord,
                                    circle_center: BlockCoord,
                                    circle_radius: int,
                                    tickingarea_name: str,
                                    function: str) -> ExecutedCommand: # TODO Function class
        cb = self.schedule_on_area_loaded_add_cb()
        cmd = ExecutedCommand(self.fh, "schedule", cb.build(cuboid_from=cuboid_from, cuboid_to=cuboid_to, circle_center=circle_center,
                                                            circle_radius=circle_radius, tickingarea_name=tickingarea_name, function=function))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def schedule_on_area_loaded_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("schedule on_area_loaded add")
        nt = lambda param: (param, _gt(cls.schedule_on_area_loaded_add, param))
        node = cb.add_branch_node()
        cb_cuboid = node.add_branch()
        cb_cuboid.add_param(*nt("cuboid_from"))
        cb_cuboid.add_param(*nt("cuboid_to"))
        cb_circle = node.add_branch(literal="circle")
        cb_circle.add_param(*nt("circle_center"))
        cb_circle.add_param(*nt("circle_radius"), range=lambda x: 0 <= x <= Int.max)
        node.add_branch(literal="tickingarea").add_param(*nt("tickingarea_name"))
        cb.add_param(*nt("function"))
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_objectives_list(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "scoreboard", "scoreboard objectives list")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_list_cb(cls) -> CommandBuilder:
        return CommandBuilder("scoreboard objectives list")

    @version(introduced="1.7.0.2")
    def scoreboard_objectives_add(self, objective: str,
                                  displayname: Optional[Union[str, RawJson]]=None) -> ExecutedCommand:
        cb = self.scoreboard_objectives_add_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(objective=objective,
                                                              displayname=json.dumps(displayname) if isinstance(displayname, str) else displayname))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives add")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_add, param))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_literal("dummy")
        cb.add_param(*nt("displayname"), regex=r"^[ A-Za-z0-9\-+\._]*$", optional=True)
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_objectives_remove(self, objective: str) -> ExecutedCommand:
        cb = self.scoreboard_objectives_remove_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives remove")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_remove, param))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_objectives_setdisplay(self,
                                         slot: Literal["list", "sidebar", "belowname"],
                                         objective: str,
                                         sort_order: Optional[Literal["ascending", "descending"]]=None) -> ExecutedCommand:
        cb = self.scoreboard_objectives_setdisplay_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(slot=slot, objective=objective, sort_order=sort_order))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_setdisplay_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives setdisplay")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_setdisplay, param))
        node = cb.add_branch_node()
        cb_belowname = node.add_branch(switch_name="slot", switch_options=["belowname"])
        cb_belowname.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb_other = node.add_branch(switch_name="slot", switch_options=["list, sidebar"])
        cb_other.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb_other.add_switch(*_go(cls.scoreboard_objectives_setdisplay, "sort_order"), optional=True)
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_list(self, targets: Optional[Union[BedrockSelector, str]]=None) -> ExecutedCommand:
        cb = self.scoreboard_players_list_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(targets=targets))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_list_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players list")
        nt = lambda param: (param, _gt(cls.scoreboard_players_list, param))
        cb.add_param(*nt("targets"))
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_set(self,
                               target: Union[BedrockSelector, str],
                               objective: str,
                               score: int) -> ExecutedCommand:
        cb = self.scoreboard_players_set_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, score=score))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_set_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players set")
        nt = lambda param: (param, _gt(cls.scoreboard_players_set, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_param(*nt("set"))
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_add(self,
                               target: Union[BedrockSelector, str],
                               objective: str,
                               score: int) -> ExecutedCommand:
        cb = self.scoreboard_players_add_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, score=score))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players add")
        nt = lambda param: (param, _gt(cls.scoreboard_players_add, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_param(*nt("set"))
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_remove(self,
                                  target: Union[BedrockSelector, str],
                                  objective: str,
                                  score: int) -> ExecutedCommand:
        cb = self.scoreboard_players_remove_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, score=score))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players remove")
        nt = lambda param: (param, _gt(cls.scoreboard_players_remove, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_param(*nt("set"))
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_random(self,
                                  target: Union[BedrockSelector, str],
                                  objective: str,
                                  min_: int,
                                  max_: int) -> ExecutedCommand:
        cb = self.scoreboard_players_random_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, min=min_, max=max_))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_random_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players random")
        nt = lambda param: (param, _gt(cls.scoreboard_players_random, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_param(*nt("min"))
        cb.add_param(*nt("max"))
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_reset(self,
                                 target: Union[BedrockSelector, str],
                                 objective: Optional[str]=None) -> ExecutedCommand:
        cb = self.scoreboard_players_reset_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_reset_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players reset")
        nt = lambda param: (param, _gt(cls.scoreboard_players_reset, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", optional=True, spaces="q")
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_test(self,
                                target: Union[BedrockSelector, str],
                                objective: str,
                                min_: Union[int, Literal["*"]],
                                max_: Optional[Union[int, Literal["*"]]]=None) -> ExecutedCommand:
        cb = self.scoreboard_players_test_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, min=min_, max=max_))
        self.fh.commands.append(cmd)
        return cmd

    @classmethod
    def scoreboard_players_test_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players test")
        nt = lambda param: (param, _gt(cls.scoreboard_players_test, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_param(*nt("min"))
        cb.add_param(*nt("max"), optional=True)
        return cb

    @version(introduced="1.7.0.2")
    def scoreboard_players_operation(self, *,
                                     target: Union[JavaSelector, str],
                                     target_objective: str,
                                     operation: Literal["+=", "-=", "*=", "/=", "%=", "=", "<", ">", "><"],
                                     source: Union[JavaSelector, str],
                                     source_objective: str) -> ExecutedCommand:
        cb = self.scoreboard_players_operation_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, target_objective=target_objective,
                                                              operation=operation, source=source,
                                                              source_objective=source_objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_operation_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players operation")
        nt = lambda param: (param, _gt(cls.scoreboard_players_operation, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("target_objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        cb.add_switch(*_go(cls.scoreboard_players_operation, "operation"))
        cb.add_param(*nt("source"))
        cb.add_param(*nt("source_objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", spaces="q")
        return cb

    @version(introduced="0.16.0b1")
    def setblock(self, pos: BlockCoord,
                 block: str,
                 tile_data: int=0,
                 block_states: Optional[dict]=None, # TODO BlockStates class
                 mode: Literal["destroy", "keep", "replace"]="replace") -> ExecutedCommand:
        cb = self.setblock_cb()
        cmd = ExecutedCommand(self.fh, "setblock", cb.build(pos=pos, block=block, tile_data=tile_data,
                                                            block_states=block_states, mode=mode))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def setblock_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("setblock")
        nt = lambda param: (param, _gt(cls.setblock, param))
        cb.add_param(*nt("pos"))
        cb.add_param(*nt("block"))
        node = cb.add_branch_node(optional=True)
        node.add_branch().add_param(*nt("tile_data"), _gd(cls.setblock, "tile_data"), range=lambda x: 0 <= x <= 65536)
        node.add_branch().add_param(*nt("block_states"))
        cb.add_param(*nt("mode"), default=_gd(cls.setblock, "mode"))
        return cb

    @version(introduced="a1.1.0.3")
    def setmaxplayers(self, max_players: int) -> ExecutedCommand:
        cb = self.setmaxplayers_cb()
        cmd = ExecutedCommand(self.fh, "setmaxplayers", cb.build(max_players=max_players))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def setmaxplayers_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("setmaxplayers")
        nt = lambda param: (param, _gt(cls.setmaxplayers, param))
        cb.add_param(*nt("max_players"), range=lambda x: 1 <= x <= 30)
        return cb

class JavaRawCommands(UniversalRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFuncHandler` and access the commands via the ‘r’ attribute.
    """
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
    def ban(self, target: Union[str, JavaSelector], reason: Optional[str]="Banned by an operator"):
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
    def ban_ip(self, target: Union[str, JavaSelector], reason: Optional[str]="Banned by an operator"):
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
                    players: Union[Optional[Union[JavaSelector, UUID]], Missing]=Missing,
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
        node.add_branch(literal="max").add_param(*nt("max"), range=lambda x: 1 <= x <= Int.max)
        node.add_branch(literal="name").add_param(*nt("name"))
        node.add_branch(literal="players").add_param(*nt("players"), playeronly=True, optional=True, default=_gd(cls.bossbar_set, "players"))
        node.add_branch(literal="style").add_switch("style", _go(cls.bossbar_set, "style"))
        node.add_branch(literal="value").add_param(*nt("value"), range=lambda x: 0 <= x <= Int.max)
        node.add_branch(literal="visible").add_param(*nt("visible"))
        return cb

    @version(introduced="17w45a")
    def clear(self, target: JavaSelector=JavaSelector.s(),
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
        cb.add_param(*nt("count"), optional=True, range=lambda x: 0 <= x <= Int.max)
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
              begin: BlockCoord,
              end: BlockCoord,
              destination: BlockCoord,
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
                 block: Optional[BlockCoord]=None,
                 entity: Optional[Union[JavaSelector, UUID]]=None,
                 storage: Optional[str]=None, # TODO add ResourceLocation class when it is written
                 path: Optional[Path]=None,
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
                   block: Optional[BlockCoord]=None,
                   entity: Optional[Union[JavaSelector, UUID]]=None,
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
                    block: Optional[BlockCoord]=None,
                    entity: Optional[Union[JavaSelector, UUID]]=None,
                    storage: Optional[str]=None,
                    target_path: Path,
                    mode: Literal["add", "index", "merge", "prepend", "set"],
                    index: Optional[int]=None,
                    from_block: Optional[BlockCoord]=None,
                    from_entity: Optional[Union[JavaSelector, UUID]]=None,
                    from_storage: Optional[str]=None,
                    source_path: Optional[Path]=None,
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
        node2.add_branch("mode", ["index"]).add_param(*nt("index"), range=lambda x: Int.min <= x <= Int.max)
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
                    block: Optional[BlockCoord]=None,
                    entity: Optional[Union[JavaSelector, UUID]]=None,
                    storage: Optional[str]=None,
                    path: Path) -> ExecutedCommand:
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
    def deop(self, targets: Union[str, JavaSelector]) -> ExecutedCommand:
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

    @version(introduced="12w32a")
    def difficulty(self, difficulty: Optional[Literal["peaceful", "easy", "normal", "hard"]]) -> ExecutedCommand:
        cb = self.difficulty_cb()
        cmd = ExecutedCommand(self.fh, "difficulty", cb.build(difficulty=difficulty))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def difficulty_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("difficulty")
        nt = lambda param: (param, _gt(cls.difficulty, param))
        cb.add_param(*nt("difficulty"), optional=True)
        return cb

    @version(introduced="13w09b")
    def effect_give(self,
                    targets: Union[JavaSelector, UUID],
                    effect: str,
                    seconds: int=30,
                    amplifier: int=1,
                    hide_particles: bool=False) -> ExecutedCommand:
        cb = self.effect_give_cb()
        self.param_version_introduced("hide_particles", hide_particles, "14w06a", default=False)
        cmd = ExecutedCommand(self.fh, "effect", cb.build(targets=targets, effect=effect, seconds=seconds, amplifier=amplifier))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def effect_give_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("effect give")
        nt = lambda param: (param, _gt(cls.effect_give, param))
        cb.add_param(*nt("targets"))
        cb.add_param(*nt("effect"))
        cb.add_param(*nt("seconds"), default=_gd(cls.effect_give, "seconds"), range=lambda x: 0 <= x <= 1e6)
        cb.add_param(*nt("amplifier"), default=_gd(cls.effect_give, "amplifier"), range=lambda x: 0 <= x <= 255)
        cb.add_param(*nt("hide_particles"), default=False)
        return cb
    
    @version(introduced="1.6.1p")
    def effect_clear(self,
                     targets: Union[JavaSelector, UUID]=JavaSelector.s(),
                     effect: Optional[str]=None) -> ExecutedCommand:
        cb = self.effect_clear_cb()
        cmd = ExecutedCommand(self.fh, "effect", cb.build(targets=targets, effect=effect))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def effect_clear_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("effect clear")
        nt = lambda param: (param, _gt(cls.effect_clear, param))
        cb.add_param(*nt("targets"), optional=True, default=_gd(cls.effect_clear, "targets"))
        cb.add_param(*nt("effect"), optional=True)
        return cb

    @version(introduced="1.4.4p", temp_removed=("17w45a", "18w06a"))
    def enchant(self, target: Union[JavaVersion, UUID], enchantment: str, level: int=1) -> ExecutedCommand:
        cb = self.enchant_cb()
        cmd = ExecutedCommand(self.fh, "enchant", cb.build(target=target, enchantment=enchantment, level=level))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def enchant_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("enchant")
        nt = lambda param: (param, _gt(cls.enchant, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("enchantment"))
        cb.add_param(*nt("level"), range=lambda x: 0 <= x <= Int.max, default=_gd(cls.enchant, "level"))
        return cb

    class ExecuteCommand:
        """Handler for the (over)complicated /execute command for Java Edition."""
        def __init__(self):
            self.command_strings: List[str] = []
            self.commands: List[ExecutedCommand] = []

        @staticmethod
        def _check_run(func: Callable[..., Self]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if len(self.command_strings) > 0 and self.command_strings[-1].startswith("run"):
                    raise ValueError("The `run` subcommand has already been registered. No additional subcommands can be entered.")
                return func(self, *args, **kwargs)
            return wrapper

        @_check_run
        def align(self, axes: str) -> Self:
            cb = self.align_cb()
            self.command_strings.append(cb.build(axes=axes))
            return self
        @classmethod
        def align_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("align")
            nt = lambda param: (param, _gt(cls.align, param))
            cb.add_param(*nt("align"), regex=r"^(?!.*(.).*\1)[xyz]+$")
            return cb

        @_check_run
        def anchored(self, anchor: Literal["eyes", "feet"]) -> Self:
            cb = self.anchored_cb()
            self.command_strings.append(cb.build(anchor=anchor))
            return self
        @classmethod
        def anchored_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("anchored")
            cb.add_switch("anchor", _go(cls.anchored, "anchor"))
            return cb

        @_check_run
        def as_(self, targets: Union[JavaSelector, UUID]) -> Self:
            cb = self.as_cb()
            self.command_strings.append(cb.build(targets=targets))
            return self
        @classmethod
        def as_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("as")
            nt = lambda param: (param, _gt(cls.as_, param))
            cb.add_param(*nt("targets"))
            return cb

        @_check_run
        def at(self, targets: Union[JavaSelector, UUID]) -> Self:
            cb = self.at_cb()
            self.command_strings.append(cb.build(targets=targets))
            return self
        @classmethod
        def at_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("as")
            nt = lambda param: (param, _gt(cls.at, param))
            cb.add_param(*nt("targets"))
            return cb

        @_check_run
        def facing_position(self, position: Coord) -> Self:
            cb = self.facing_position_cb()
            self.command_strings.append(cb.build(position=position))
            return self
        @classmethod
        def facing_position_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("facing")
            nt = lambda param: (param, _gt(cls.facing_position, param))
            cb.add_param(*nt("position"))
            return cb

        @_check_run
        def facing_entity(self, targets: Union[JavaSelector, UUID], anchor: Literal["eyes", "feet"]) -> Self:
            cb = self.facing_entity_cb()
            self.command_strings.append(cb.build(targets=targets, anchor=anchor))
            return self
        @classmethod
        def facing_entity_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("facing entity")
            nt = lambda param: (param, _gt(cls.facing_entity, param))
            cb.add_param(*nt("targets"))
            cb.add_switch("anchor", _go(cls.anchored, "anchor"))
            return cb

        @_check_run
        def in_(self, dimension: str) -> Self: # TODO add resource location when it is written
            cb = self.in_cb()
            self.command_strings.append(cb.build(dimension=dimension))
            return self
        @classmethod
        def in_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("in")
            nt = lambda param: (param, _gt(cls.in_, param))
            cb.add_param(*nt("targets"))
            return cb

        @_check_run
        def positioned_position(self, position: Coord) -> Self:
            cb = self.positioned_position_cb()
            self.command_strings.append(cb.build(position=position))
            return self
        @classmethod
        def positioned_position_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("positioned")
            nt = lambda param: (param, _gt(cls.positioned_position, param))
            cb.add_param(*nt("position"))
            return cb

        @_check_run
        def positioned_entity(self, targets: Union[JavaSelector, UUID]) -> Self:
            cb = self.positioned_entity_cb()
            self.command_strings.append(cb.build(targets=targets))
            return self
        @classmethod
        def positioned_entity_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("positioned as")
            nt = lambda param: (param, _gt(cls.positioned_entity, param))
            cb.add_param(*nt("targets"))
            return cb

        @_check_run
        def rotated(self, yaw: float, pitch: float) -> Self:
            cb = self.rotated_cb()
            self.command_strings.append(cb.build(yaw=yaw, pitch=pitch))
            return self
        @classmethod
        def rotated_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("rotated")
            nt = lambda param: (param, _gt(cls.rotated, param))
            cb.add_param(*nt("yaw"), range=lambda x: -180 <= x <= 180)
            cb.add_param(*nt("pitch"), range=lambda x: -90 <= x <= 90)
            return cb

        @_check_run
        def rotated_entity(self, targets: Union[JavaSelector, UUID]) -> Self:
            cb = self.rotated_entity_cb()
            self.command_strings.append(cb.build(targets=targets))
            return self
        @classmethod
        def rotated_entity_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("rotated as")
            nt = lambda param: (param, _gt(cls.rotated_entity, param))
            cb.add_param(*nt("targets"))
            return cb

        @_check_run
        def cond_block(self, cond: Literal["if", "unless"], *,
                       position: BlockCoord, # TODO BlockType class
                       block: str) -> Self:
            cb = self.cond_block_cb()
            self.command_strings.append(cb.build(cond=cond, position=position, block=block))
            return self
        @classmethod
        def cond_block_cb(cls) -> CommandBuilder:
            cb = CommandBuilder()
            nt = lambda param: (param, _gt(cls.cond_block, param))
            cb.add_switch("cond", _go(cls.cond_block, "cond"))
            cb.add_literal("block")
            cb.add_param(*nt("position"))
            cb.add_param(*nt("block"))
            return cb

        @_check_run
        def cond_blocks(self, cond: Literal["if", "unless"], *,
                        start: BlockCoord,
                        end: BlockCoord,
                        destination: BlockCoord,
                        scan_mode: Literal["all", "masked"]) -> Self:
            cb = self.cond_blocks_cb()
            self.command_strings.append(cb.build(cond=cond, start=start, end=end, destination=destination, scan_mode=scan_mode))
            return self
        @classmethod
        def cond_blocks_cb(cls) -> CommandBuilder:
            cb = CommandBuilder()
            nt = lambda param: (param, _gt(cls.cond_blocks, param))
            cb.add_switch("cond", _go(cls.cond_blocks, "cond"))
            cb.add_literal("blocks")
            cb.add_param(*nt("start"))
            cb.add_param(*nt("end"))
            cb.add_param(*nt("destination"))
            cb.add_switch("scan_mode", _go(cls.cond_blocks, "scan_mode"))
            return cb

        @_check_run
        def cond_data(self, cond: Literal["if", "unless"], *,
                      block: BlockCoord,# TODO add ResourceLocation
                      entity: Union[JavaSelector, UUID],
                      storage: str,
                      path: Path) -> Self:
            cb = self.cond_data_cb()
            self.command_strings.append(cb.build(cond=cond, block=block, entity=entity, storage=storage, path=path))
            return self
        @classmethod
        def cond_data_cb(cls) -> CommandBuilder:
            cb = CommandBuilder()
            nt = lambda param: (param, _gt(cls.cond_data, param))
            cb.add_switch("cond", _go(cls.cond_data, "cond"))
            cb.add_literal("data")
            node = cb.add_branch_node()
            node.add_branch(literal="block").add_param(*nt("block"))
            node.add_branch(literal="entity").add_param(*nt("entity"))
            node.add_branch(literal="storage").add_param(*nt("storage"))
            cb.add_param(*nt("path"))
            return cb

        @_check_run
        def cond_entity(self, cond: Literal["if", "unless"], *,
                        targets: Union[JavaSelector, UUID]) -> Self:
            cb = self.cond_entity_cb()
            self.command_strings.append(cb.build(cond=cond, targets=targets))
            return self
        @classmethod
        def cond_entity_cb(cls) -> CommandBuilder:
            cb = CommandBuilder()
            nt = lambda param: (param, _gt(cls.cond_entity, param))
            cb.add_switch("cond", _go(cls.cond_entity, "cond"))
            cb.add_literal("entity")
            cb.add_param(*nt("entity"))
            return cb

        @_check_run
        def cond_predicate(self, cond: Literal["if", "unless"], *,
                           predicate: str) -> Self: # TODO add Predicate class when it is written
            cb = self.cond_predicate_cb()
            self.command_strings.append(cb.build(cond=cond, predicate=predicate))
            return self
        @classmethod
        def cond_predicate_cb(cls) -> CommandBuilder:
            cb = CommandBuilder()
            nt = lambda param: (param, _gt(cls.cond_predicate, param))
            cb.add_switch("cond", _go(cls.cond_predicate, "cond"))
            cb.add_literal("predicate")
            cb.add_param(*nt("predicate"))
            return cb

        @_check_run
        def cond_score(self, cond: Literal["if", "unless"], *,
                       target: Union[Union[JavaSelector, UUID], Literal["*"]],
                       target_objective: str,
                       comparator: Literal["<", "<=", "=", ">=", ">", "matches"],
                       source: Optional[Union[Union[JavaSelector, UUID], Literal["*"]]]=None,
                       source_objective: Optional[str]=None,
                       range_: Optional[Union[str, int]]=None) -> Self:
            cb = self.cond_score_cb()
            self.command_strings.append(cb.build(cond=cond, target=target, target_objective=target_objective,
                                                 comparator=comparator, source=source, source_objective=source_objective,
                                                 range=range_))
            return self
        @classmethod
        def cond_score_cb(cls) -> CommandBuilder:
            cb = CommandBuilder()
            nt = lambda param: (param, _gt(cls.cond_score, param))
            cb.add_switch("cond", _go(cls.cond_score, "cond"))
            cb.add_literal("score")
            cb.add_param(*nt("target"))
            cb.add_param(*nt("target_objective"))
            node = cb.add_branch_node()
            node.add_branch(switch_name="comparator", switch_options=["matches"]).add_param(*nt("range"))
            cb_others = node.add_branch(switch_name="comparator", switch_options=["<", "<=", "=", ">=", ">"])
            cb_others.add_param(*nt("source"))
            cb_others.add_param(*nt("source_objective"))
            return cb

        @_check_run
        def store_block(self, what: Literal["result", "success"], *,
                        position: BlockCoord,
                        path: Path,
                        type_: Literal["byte", "short", "int", "long", "float", "double"],
                        scale: float) -> Self:
            cb = self.store_block_cb()
            self.command_strings.append(cb.build(what=what, position=position, path=path, type=type_, scale=scale))
            return self
        @classmethod
        def store_block_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("store")
            nt = lambda param: (param, _gt(cls.store_block, param))
            cb.add_switch("what", _go(cls.store_block, "what"))
            cb.add_literal("block")
            cb.add_param(*nt("position"))
            cb.add_param(*nt("path"))
            cb.add_switch("type", _go(cls.store_block, "type"))
            cb.add_param(*nt("scale"))
            return cb

        @_check_run
        def store_bossbar(self, what: Literal["result", "success"], *,
                          id_: str,  # TODO add ResourceLocation class when it is written
                          value: Literal["value", "max"]) -> Self:
            cb = self.store_bossbar_cb()
            self.command_strings.append(cb.build(what=what, id=id_, value=value))
            return self
        @classmethod
        def store_bossbar_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("store")
            nt = lambda param: (param, _gt(cls.store_block, param))
            cb.add_switch("what", _go(cls.store_bossbar, "what"))
            cb.add_literal("bossbar")
            cb.add_param(*nt("id"))
            cb.add_switch("value", _go(cls.store_bossbar, "value"))
            return cb

        @_check_run
        def store_entity(self, what: Literal["result", "success"], *,
                         target: JavaSelector,
                         path: Path,
                         type_: Literal["byte", "short", "int", "long", "float", "double"],
                         scale: float) -> Self:
            cb = self.store_entity_cb()
            self.command_strings.append(cb.build(what=what, target=target, path=path, type=type_, scale=scale))
            return self
        @classmethod
        def store_entity_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("store")
            nt = lambda param: (param, _gt(cls.store_entity, param))
            cb.add_switch("what", _go(cls.store_entity, "what"))
            cb.add_literal("entity")
            cb.add_param(*nt("target"))
            cb.add_param(*nt("path"))
            cb.add_switch("type", _go(cls.store_entity, "type"))
            cb.add_param(*nt("scale"))
            return cb

        @_check_run
        def store_score(self, what: Literal["result", "success"], *,
                        target: Union[Union[JavaSelector, UUID], Literal["*"]],
                        objective: str) -> Self:
            cb = self.store_score_cb()
            self.command_strings.append(cb.build(what=what, target=target, objective=objective))
            return self
        @classmethod
        def store_score_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("store")
            nt = lambda param: (param, _gt(cls.store_score, param))
            cb.add_switch("what", _go(cls.store_score, "what"))
            cb.add_literal("score")
            cb.add_param(*nt("target"))
            cb.add_param(*nt("objective"))
            return cb

        @_check_run
        def store_storage(self, what: Literal["result", "success"], *,
                          target: str,  # TODO add ResourceLocation class when it is written
                          path: Path,
                          type_: Literal["byte", "short", "int", "long", "float", "double"],
                          scale: float) -> Self:
            cb = self.store_storage_cb()
            self.command_strings.append(cb.build(what=what, target=target, path=path, type=type_, scale=scale))
            return self
        @classmethod
        def store_storage_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("store")
            nt = lambda param: (param, _gt(cls.store_storage, param))
            cb.add_switch("what", _go(cls.store_storage, "what"))
            cb.add_literal("storage")
            cb.add_param(*nt("target"))
            cb.add_param(*nt("path"))
            cb.add_switch("type", _go(cls.store_storage, "type"))
            cb.add_param(*nt("scale"))
            return cb

        @_check_run
        def run(self, commands: Union[List[ExecutedCommand], ExecutedCommand]):
            self.command_strings.append("run")
            self.commands.extend([commands] if not isinstance(commands, list) else [item for sublist in commands for item in sublist])
        @classmethod
        def run_cb(cls) -> CommandBuilder:
            cb = CommandBuilder("run")
            cb.add_param("command", str)
            return cb

    EC = ExecutedCommand

    @version(introduced="14w07a")
    def execute(self, handler: ExecuteCommand) -> Union[ExecutedCommand, List[ExecutedCommand]]:
        cmds = [] # TODO version checking for subcommands
        for command in handler.commands:
            cmd = ExecutedCommand(self.fh, "execute", " ".join(handler.command_strings)+" "+command.command_string)
            self.fh.commands[self.fh.commands.index(command)] = cmd
            cmds.append(cmd)
        return cmds[0] if len(cmds) == 1 else cmds

    @version(introduced="b1.5p5")
    def experience(self, mode: Literal["add", "set", "query"], *,
                   targets: Union[JavaSelector, UUID],
                   amount: Optional[int]=None,
                   unit: Optional[Literal["levels", "points"]]=None) -> ExecutedCommand:
        cb = self.experience_cb()
        cmd = ExecutedCommand(self.fh, "experience", cb.build(mode=mode, targets=targets, amount=amount, unit=unit))
        self.fh.commands.append(cmd)
        return cmd
    xp = experience
    @classmethod
    def experience_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("experience")
        nt = lambda param: (param, _gt(cls.experience, param))
        node = cb.add_branch_node()
        cb_add = node.add_branch("mode", ["add"])
        cb_add.add_param(*nt("targets"), playeronly=True)
        cb_add.add_param(*nt("amount"), range=lambda x: Int.min <= x <= Int.max)
        cb_add.add_switch("unit", _go(cls.experience, "unit"), optional=True)
        cb_set = node.add_branch("mode", ["set"])
        cb_set.add_param(*nt("targets"), playeronly=True)
        cb_set.add_param(*nt("amount"), range=lambda x: 0 <= x <= Int.max)
        cb_set.add_switch("unit", _go(cls.experience, "unit"), optional=True)
        cb_query = node.add_branch("mode", ["query"])
        cb_query.add_param(*nt("targets"), playeronly=True)
        cb_query.add_switch("unit", _go(cls.experience, "unit"))
        return cb
    xp_cb = experience_cb

    @version(introduced="14w03a")
    def fill(self, from_: BlockCoord,
             to: BlockCoord,
             block: str,
             mode: Literal["destroy", "hollow", "keep", "outline", "replace"]="replace",
             filter_: Optional[str]=None) -> ExecutedCommand:
        cb = self.fill_cb()
        cmd = ExecutedCommand(self.fh, "fill", cb.build(from_=from_, to=to, block=block, mode=mode, filter=filter_))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def fill_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("fill")
        nt = lambda param: (param, _gt(cls.fill, param))
        cb.add_param(*nt("from_"))
        cb.add_param(*nt("to"))
        cb.add_param(*nt("block"))
        node = cb.add_branch_node()
        node.add_branch(switch_name="mode", switch_options=["replace"]).add_param(*nt("filter"), optional=True)
        node.add_branch(switch_name="mode", switch_options=["destroy", "hollow", "keep", "outline"])
        return cb

    @version(introduced="18w31a")
    def forceload_add(self, from_: str, to: Optional[str]=None) -> ExecutedCommand: # TODO add Chunk coords when it is written
        cb = self.forceload_add_cb()
        cmd = ExecutedCommand(self.fh, "forceload", cb.build(from_=from_, to=to))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def forceload_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("forceload add")
        nt = lambda param: (param, _gt(cls.forceload_add, param))
        cb.add_param(*nt("from_"))
        cb.add_param(*nt("to"), optional=True)
        return cb

    @version(introduced="18w31a")
    def forceload_remove(self, from_: str,
                         to: Optional[str] = None) -> ExecutedCommand:  # TODO add Chunk coords when it is written
        cb = self.forceload_add_cb()
        cmd = ExecutedCommand(self.fh, "forceload", cb.build(from_=from_, to=to))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def forceload_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("forceload remove")
        nt = lambda param: (param, _gt(cls.forceload_add, param))
        cb.add_param(*nt("from_"))
        cb.add_param(*nt("to"), optional=True)
        return cb

    @version(introduced="18w31a")
    def forceload_remove_all(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "forceload", "forceload remove all")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def forceload_remove_all_cb(cls) -> CommandBuilder:
        return CommandBuilder("forceload remove all")

    @version(introduced="18w31a")
    def forceload_query(self, pos: Optional[str]=None) -> ExecutedCommand:
        cb = self.forceload_query_cb()
        cmd = ExecutedCommand(self.fh, "forceload", cb.build(pos=pos))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def forceload_query_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("forceload")
        nt = lambda param: (param, _gt(cls.forceload_query, param))
        cb.add_param(*nt("pos"), optional=True)
        return cb

    @version(introduced="1.12pre1")
    def function(self, name: str) -> ExecutedCommand: # TODO add ResourceLocation and tag when it is written
        cb = self.function_cb()
        cmd = ExecutedCommand(self.fh, "function", cb.build(name=name))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def function_cb(cls):
        cb = CommandBuilder("function")
        nt = lambda param: (param, _gt(cls.function, param))
        cb.add_param(*nt("name"))
        return cb

    @version(introduced="b1.8pre")
    def gamemode(self, mode: Literal["survival", "creative", "adventure", "spectator"],
                 target: Union[Union[JavaSelector, UUID], str]=JavaSelector.s()) -> ExecutedCommand:
        cb = self.gamemode_cb()
        self.option_version_introduced("mode", mode, "14w05a", "spectator")
        cmd = ExecutedCommand(self.fh, "gamemode", cb.build(mode=mode, target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gamemode_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("gamemode")
        nt = lambda param: (param, _gt(cls.gamemode, param))
        cb.add_param(*nt("mode"))
        cb.add_param(*nt("target"), default=_gd(cls.gamemode, "target"), playeronly=True)
        return cb

    @version(introduced="12w32a")
    def gamerule(self, rule_name: str, value: Union[bool, int]) -> ExecutedCommand:
        cb = self.gamerule_cb()
        cmd = ExecutedCommand(self.fh, "gamerule", cb.build(rule_name=rule_name, value=value))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def gamerule_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("gamerule")
        nt = lambda param: (param, _gt(cls.gamerule, param))
        cb.add_param(*nt("rule_name"))
        cb.add_param(*nt("value"), optional=True)
        return cb

    @version(introduced="a1.0.15")
    def give(self, target: Union[Union[JavaSelector, UUID], str], item: str, count: int=1) -> ExecutedCommand:
        cb = self.give_cb()
        cmd = ExecutedCommand(self.fh, "give", cb.build(target=target, item=item, count=count))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def give_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("give")
        nt = lambda param: (param, _gt(cls.give, param))
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("item"))
        cb.add_param(*nt("count"), default=_gd(cls.give, "count"))
        return cb

    @version(introduced="20w46a")
    def item_modify(self, *,
                    block: Optional[BlockCoord] = None,
                    entity: Optional[Union[str, Union[JavaSelector, UUID]]] = None,
                    slot: str,  # TODO class for slots?
                    modifier: Optional[str]=None) -> ExecutedCommand: # TODO ResourceLocation and ItemModifier class
        cb = self.item_modify_cb()
        cmd = ExecutedCommand(self.fh, "item", cb.build(block=block, entity=entity, slot=slot, modifier=modifier))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def item_modify_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("item modify")
        nt = lambda param: (param, _gt(cls.item_modify, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        cb.add_param(*nt("slot"))
        cb.add_param(*nt("modifier"))
        return cb

    @version(introduced="20w46a")
    def item_replace(self, *,
                     block: Optional[BlockCoord]=None,
                     entity: Optional[Union[str, Union[JavaSelector, UUID]]]=None,
                     slot: str, # TODO class for slots?
                     replace_mode: Literal["with", "from"],
                     item: Optional[str]=None,
                     count: int=1,
                     from_block: Optional[BlockCoord]=None,
                     from_entity: Optional[Union[str, Union[JavaSelector, UUID]]]=None,
                     from_slot: Optional[str]=None,
                     modifier: Optional[str]=None) -> ExecutedCommand: # TODO ResourceLocation and ItemModifier class
        cb = self.item_replace_cb()
        cmd = ExecutedCommand(self.fh, "item", cb.build(block=block, entity=entity, slot=slot, replace_mode=replace_mode,
                                                        modifier=modifier, item=item, count=count, from_block=from_block,
                                                        from_entity=from_entity, from_slot=from_slot))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def item_replace_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("item replace")
        nt = lambda param: (param, _gt(cls.item_replace, param))
        node = cb.add_branch_node()
        node.add_branch(literal="block").add_param(*nt("block"))
        node.add_branch(literal="entity").add_param(*nt("entity"))
        cb.add_param(*nt("slot"))
        node2 = cb.add_branch_node()
        cb_with = node2.add_branch(switch_name="replace_mode", switch_options=["with"])
        cb_with.add_param(*nt("item"))
        cb_with.add_param(*nt("count"), default=_gd(cls.item_replace, "count"))
        cb_from = node2.add_branch(switch_name="replace_mode", switch_options=["from"])
        node3 = cb_from.add_branch_node()
        node3.add_branch(literal="block").add_param(*nt("block"))
        node3.add_branch(literal="entity").add_param(*nt("entity"))
        cb_from.add_param(*nt("from_slot"))
        cb_from.add_param(*nt("modifier"), optional=True)
        return cb

    @version(introduced="21w37a")
    def jfr(self, switch: Literal["start", "stop"]) -> ExecutedCommand:
        cb = self.jfr_cb()
        cmd = ExecutedCommand(self.fh, "jfr", cb.build(switch=switch))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def jfr_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("jfr")
        cb.add_switch(*_go(cls.jfr, "switch"))
        return cb

    @version(introduced="1.0.16")
    def kick(self, target: Union[Union[JavaSelector, UUID], str], reason: str="Kicked by an operator") -> ExecutedCommand:
        cb = self.kick_cb()
        cmd = ExecutedCommand(self.fh, "kick", cb.build(target=target, reason=reason))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def kick_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("kick")
        nt = lambda param: (param, _gt(cls.kick, param))
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("reason"), default=_gd(cls.kick, "reason"))
        return cb

    @version(introduced="a1.2.6")
    def kill(self, target: Union[Union[JavaSelector, UUID], str]=JavaSelector.s()) -> ExecutedCommand:
        cb = self.kick_cb()
        cmd = ExecutedCommand(self.fh, "kick", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def kill_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("kick")
        nt = lambda param: (param, _gt(cls.kick, param))
        cb.add_param(*nt("target"))
        return cb

    @version(introduced="a1.0.16_02")
    def list(self, uuids: bool=False) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "list", "list uuids" if uuids else "list")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def list_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("list")
        cb.add_branch_node(optional=True).add_branch(literal="uuids")
        return cb

    @version(introduced="16w39a")
    def locate(self, structure: str) -> ExecutedCommand:
        cb = self.locate_cb()
        cmd = ExecutedCommand(self.fh, "locate", cb.build(structure=structure))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def locate_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("locate")
        nt = lambda param: (param, _gt(cls.locate, param))
        cb.add_param(*nt("structure"))
        return cb

    @version(introduced="20w06a")
    def locatebiome(self, biome: str) -> ExecutedCommand: # TODO ResourceLocation
        cb = self.locate_cb()
        cmd = ExecutedCommand(self.fh, "locatebiome", cb.build(biome=biome))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def locatebiome_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("locatebiome")
        nt = lambda param: (param, _gt(cls.locatebiome, param))
        cb.add_param(*nt("biome"))
        return cb

    @version(introduced="18w43a")
    def loot(self, *,
             spawn_target_pos: Optional[Coord]=None,
             replace_entities: Optional[Union[Union[JavaSelector, UUID], str]]=None,
             replace_block: Optional[str]=None,
             replace_slot: Optional[str]=None, # TODO Slot class
             replace_count: Optional[int]=None,
             give_players: Optional[Union[Union[JavaSelector, UUID], str]]=None,
             insert_target_pos: Optional[Coord]=None,
             fish_loot_table: Optional[str]=None, # TODO LootTable, ResourceLocation class
             fish_pos: Optional[Coord]=None,
             fish_tool: Optional[Union[str, Literal["mainhand", "offhand"]]]=None, # TODO item class?
             loot_loot_table: Optional[str]=None,
             kill_target: Optional[Union[Union[JavaSelector, UUID], str]]=None,
             mine_pos: Optional[BlockCoord]=None,
             mine_tool: Optional[Union[str, Literal["mainhand", "offhand"]]]=None) -> ExecutedCommand:  # TODO item class?
        cb = self.loot_cb()
        cmd = ExecutedCommand(self.fh, "loot", cb.build(spawn_target_pos=spawn_target_pos, replace_entities=replace_entities,
                                                        replace_block=replace_block, replace_slot=replace_slot,
                                                        replace_count=replace_count, give_players=give_players,
                                                        insert_target_pos=insert_target_pos, fish_loot_table=fish_loot_table,
                                                        fish_pos=fish_pos, fish_tool=fish_tool, loot_loot_table=loot_loot_table,
                                                        kill_target=kill_target, mine_pos=mine_pos, mine_tool=mine_tool))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def loot_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("loot")
        nt = lambda param: (param, _gt(cls.loot, param))
        node = cb.add_branch_node()
        node.add_branch(literal="spawn").add_param(*nt("spawn_target_pos"))
        cb_target_replace = node.add_branch(literal="replace")
        node2 = cb_target_replace.add_branch_node()
        node2.add_branch(literal="entity").add_param(*nt("replace_entities"))
        node2.add_branch(literal="block").add_param(*nt("replace_block"))
        cb_target_replace.add_param(*nt("replace_slot"))
        cb_target_replace.add_param(*nt("replace_count"), optional=True, range=lambda x: 0 <= x <= Int.max)
        node.add_branch(literal="give").add_param(*nt("give_players"), playeronly=True)
        node.add_branch(literal="insert").add_param(*nt("insert_target_pos"))
        node3 = cb.add_branch_node()
        cb_fish = node3.add_branch(literal="fish")
        cb_fish.add_param(*nt("fish_loot_table"))
        cb_fish.add_param(*nt("fish_pos"))
        cb_fish.add_param(*nt("fish_tool"))
        node3.add_branch(literal="loot").add_param(*nt("loot_loot_table"))
        node3.add_branch(literal="kill").add_param(*nt("kill_target"), singleonly=True)
        cb_mine = node3.add_branch(literal="mine")
        cb_mine.add_param(*nt("mine_pos"))
        cb_mine.add_param(*nt("mine_tool"))
        return cb

    # version unknown
    def me(self, msg: str) -> ExecutedCommand:
        cb = self.me_cb()
        cmd = ExecutedCommand(self.fh, "me", cb.build(msg=msg))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def me_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("me")
        nt = lambda param: (param, _gt(cls.me, param))
        cb.add_param(*nt("msg"))
        return cb

    @version(introduced="a1.0.16_02")
    def msg(self, targets: Union[Union[JavaSelector, UUID], str], message: str) -> ExecutedCommand:
        cb = self.msg_cb()
        cmd = ExecutedCommand(self.fh, "msg", cb.build(targets=targets, message=message))
        self.fh.commands.append(cmd)
        return cmd
    tell = w = msg
    @classmethod
    def msg_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("msg")
        nt = lambda param: (param, _gt(cls.msg, param))
        cb.add_param(*nt("targets"), playeronly=True)
        cb.add_param(*nt("message"), spaces=True)
        return cb
    tell_cb = w_cb = msg_cb

    @version(introduced="a1.0.16")
    def op(self, targets: Union[str, JavaSelector]) -> ExecutedCommand:
        cb = self.op_cb()
        cmd = ExecutedCommand(self.fh, "op", cb.build(target=targets))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def op_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("op")
        nt = lambda param: (param, _gt(cls.op, param))
        cb.add_param(*nt("targets"), playeronly=True)
        return cb

    @version(introduced="a1.0.16")
    def pardon(self, target: Union[str, JavaSelector]) -> ExecutedCommand:
        cb = self.pardon_cb()
        cmd = ExecutedCommand(self.fh, "pardon", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def pardon_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("pardon")
        nt = lambda param: (param, _gt(cls.pardon, param))
        cb.add_param(*nt("target"), playeronly=True)
        cb.add_param(*nt("reason"), default=_gd(cls.pardon, "reason"), spaces=True)
        return cb

    @version(introduced="a1.0.16")
    def pardon_ip(self, target: str) -> ExecutedCommand:
        cb = self.pardon_ip_cb()
        cmd = ExecutedCommand(self.fh, "pardon-ip", cb.build(target=target))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def pardon_ip_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("pardon-ip")
        nt = lambda param: (param, _gt(cls.pardon_ip, param))
        cb.add_param(*nt("target"),  regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_param(*nt("reason"), default=_gd(cls.pardon, "reason"), spaces=True)
        return cb

    @version(introduced="14w04a")
    def particle(self, *, particle: str, # TODO Particle class
                 pos: Coord=Coord.at_executor(),
                 delta: Optional[str]=None,
                 speed: Optional[float]=None,
                 count: Optional[int]=None,
                 display_mode: Literal["force", "normal"]="normal",
                 viewers: Optional[Union[Union[JavaSelector, UUID], str]]=None) -> ExecutedCommand:
        cb = self.particle_cb()
        cmd = ExecutedCommand(self.fh, "particle", cb.build(particle=particle, pos=pos, delta=delta, speed=speed, count=count,
                                                            display_mode=display_mode, viewers=viewers))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def particle_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("particle")
        nt = lambda param: (param, _gt(cls.particle, param))
        cb.add_param(*nt("particle")),
        node = cb.add_branch_node()
        node.add_branch().add_param(*nt("pos"), default=_gd(cls.particle, "pos"))
        cb2 = node.add_branch()
        cb2.add_param(*nt("pos"))
        cb2.add_param(*nt("delta"))
        cb2.add_param(*nt("speed"), range=lambda x: 0.0 <= x <= 340282356779733661637539395458142568447.9)
        cb2.add_param(*nt("count"), range=lambda x: 0 <= x <= Int.max)
        cb2.add_switch(*_go(cls.particle, "display_mode"), default=_gd(cls.particle, "display_mode"))
        cb2.add_param(*nt("viewers"), optional=True, playeronly=True)
        return cb

    @version(introduced="1.17pre1")
    def perf(self, switch: Literal["start", "stop"]) -> ExecutedCommand:
        cb = self.perf_cb()
        cmd = ExecutedCommand(self.fh, "perf", cb.build(switch=switch))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def perf_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("perf")
        cb.add_switch(*_go(cls.perf, "switch"))
        return cb

    @version(introduced="1.16.1pre")
    def playsound(self, sound: str, *, # TODO ResourceLocation class
                  source: Literal["master", "music", "record", "weather", "block",
                                  "hostile", "neutral", "player", "ambient", "voice"],
                  targets: Union[Union[JavaSelector, UUID], str],
                  position: Optional[Coord]=None,
                  volume: float=1.0,
                  pitch: float=1.0,
                  minimum_volume: float=0.0) -> ExecutedCommand:
        cb = self.playsound_cb()
        cmd = ExecutedCommand(self.fh, "playsound", cb.build(sound=sound, source=source, targets=targets, position=position,
                                                             volume=volume, pitch=pitch, minimum_volume=minimum_volume))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def playsound_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("playsound")
        nt = lambda param: (param, _gt(cls.playsound, param))
        cb.add_param(*nt("sound"))
        cb.add_switch(*_go(cls.playsound, "source"))
        cb.add_param(*nt("targets"), playeronly=True)
        cb.add_param(*nt("position"), optional=True)
        cb.add_param(*nt("volume"), default=_gd(cls.playsound, "volume"), range=lambda x: x >= 0)
        cb.add_param(*nt("pitch"), default=_gd(cls.playsound, "pitch"), range=lambda x: 0 <= x <= 2)
        cb.add_param(*nt("minimum_volume"), default=_gd(cls.playsound, "minimum_volume"), range=lambda x: 0 <= x <= 1)
        return cb

    @version(introduced="12w24a")
    def publish(self, port: int) -> ExecutedCommand:
        cb = self.publish_cb()
        cmd = ExecutedCommand(self.fh, "publish", cb.build(port=port))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def publish_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("publish")
        nt = lambda param: (param, _gt(cls.publish, param))
        cb.add_param(*nt("port"), range=lambda x: 0 <= x <= 65535)
        return cb

    @version(introduced="17w13a")
    def recipe(self, action: Literal["give", "take"],
               targets: Union[Union[JavaSelector, UUID], str],
               recipe: Union[str, Literal["*"]]) -> ExecutedCommand: # TODO ResourceLocation
        cb = self.recipe_cb()
        cmd = ExecutedCommand(self.fh, "recipe", cb.build(action=action, targets=targets, recipe=recipe))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def recipe_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("recipe")
        nt = lambda param: (param, _gt(cls.recipe, param))
        cb.add_switch(*_go(cls.recipe, "action"))
        cb.add_param(*nt("targets"), playeronly=True)
        cb.add_param(*nt("recipe"))
        return cb

    @version(introduced="17w18a")
    def reload(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "reload", "reload")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def reload_cb(cls) -> CommandBuilder:
        return CommandBuilder("reload")

    # TODO replaceitem for java

    @version(introduced="a1.0.16_01")
    def save_all(self, flush: bool=False) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "save-all", "save-all flush" if flush else "save-all")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def save_all_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("save-all")
        cb.add_branch_node(optional=True).add_branch(literal="flush")
        return cb

    @version(introduced="a1.0.16_01")
    def save_off(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "save-off", "save-off")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def save_off_cb(cls) -> CommandBuilder:
        return CommandBuilder("save-off")

    @version(introduced="a1.0.16_01")
    def save_on(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "save-on", "save-on")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def save_on_cb(cls) -> CommandBuilder:
        return CommandBuilder("save-on")

    @version(introduced="0.0.16a_01")
    def say(self, msg: str) -> ExecutedCommand:
        cb = self.say_cb()
        cmd = ExecutedCommand(self.fh, "say", cb.build(msg=msg))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def say_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("say")
        nt = lambda param: (param, _gt(cls.say, param))
        cb.add_param(*nt("msg"), spaces=True)
        return cb

    @version(introduced="18w43a")
    def schedule_function(self, function: str, # TODO Function class?
                          time: Union[str, int],
                          mode: Literal["append", "replace"]="replace") -> ExecutedCommand:
        cb = self.schedule_function_cb()
        self.option_version_introduced("mode", mode, "19w38a", "append")
        cmd = ExecutedCommand(self.fh, "schedule", cb.build(function=function, time=time, mode=mode))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def schedule_function_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("schedule function")
        nt = lambda param: (param, _gt(cls.schedule_function, param))
        cb.add_param(*nt("function"))
        cb.add_param(*nt("time"))
        cb.add_switch(*_go(cls.schedule_function, "mode"), default=_gd(cls.schedule_function, "mode"))
        return cb

    @version(introduced="18w43a")
    def schedule_clear(self, function: str) -> ExecutedCommand:
        cb = self.schedule_clear_cb()
        cmd = ExecutedCommand(self.fh, "schedule", cb.build(function=function))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def schedule_clear_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("schedule clear")
        nt = lambda param: (param, _gt(cls.schedule_clear, param))
        cb.add_param(*nt("function"), spaces=True)
        return cb

    @version(introduced="13w04a")
    def scoreboard_objectives_list(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "scoreboard", "scoreboard objectives list")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_list_cb(cls) -> CommandBuilder:
        return CommandBuilder("scoreboard objectives list")

    @version(introduced="13w04a")
    def scoreboard_objectives_add(self, objective: str,
                                  criteria: str, # TODO Criteria class
                                  displayname: Optional[Union[str, RawJson]]=None) -> ExecutedCommand:
        cb = self.scoreboard_objectives_add_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(objective=objective, criteria=criteria,
                                                              displayname=json.dumps(displayname) if isinstance(displayname, str) else displayname))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives add")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_add, param))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_param(*nt("criteria"))
        cb.add_param(*nt("displayname"), regex=r"^[ A-Za-z0-9\-+\._]*$", optional=True)
        return cb

    @version(introduced="13w04a")
    def scoreboard_objectives_remove(self, objective: str) -> ExecutedCommand:
        cb = self.scoreboard_objectives_remove_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives remove")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_remove, param))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        return cb

    @version(introduced="13w04a")
    def scoreboard_objectives_setdisplay(self,
                                         slot: Literal["list", "sidebar", "belowname"],
                                         objective: str) -> ExecutedCommand:
        cb = self.scoreboard_objectives_setdisplay_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(slot=slot, objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_setdisplay_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives setdisplay")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_setdisplay, param))
        cb.add_switch(*_go(cls.scoreboard_objectives_setdisplay, "slot"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        return cb

    @version(introduced="1.13pre7")
    def scoreboard_objectives_modify(self, objective: str, *,
                                     displayname: Optional[Union[str, RawJson]]=None,
                                     rendertype: Optional[Literal["hearts", "integer"]]=None):
        cb = self.scoreboard_objectives_modify_cb()
        self.param_version_introduced("rendertype", rendertype, "1.13pre8")
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(objective=objective,
                                                              displayname=json.dumps(displayname) if isinstance(displayname, str) else displayname,
                                                              rendertype=rendertype))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_objectives_modify_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard objectives modify")
        nt = lambda param: (param, _gt(cls.scoreboard_objectives_modify, param))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        node = cb.add_branch_node()
        node.add_branch(literal="displayname").add_param(*nt("displayname"))
        node.add_branch(literal="rendertype").add_switch(*_go(cls.scoreboard_objectives_modify, "rendertype"))
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_list(self, targets: Optional[Union[Union[JavaSelector, UUID], str]]=None) -> ExecutedCommand:
        cb = self.scoreboard_players_list_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(targets=targets))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_list_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players list")
        nt = lambda param: (param, _gt(cls.scoreboard_players_list, param))
        cb.add_param(*nt("targets"), singleonly=True)
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_get(self,
                               target: Union[Union[JavaSelector, UUID], str],
                               objective: str) -> ExecutedCommand:
        cb = self.scoreboard_players_get_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_get_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players get")
        nt = lambda param: (param, _gt(cls.scoreboard_players_get, param))
        cb.add_param(*nt("target"), singleonly=True)
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_set(self,
                               target: Union[Union[JavaSelector, UUID], str],
                               objective: str,
                               score: int) -> ExecutedCommand:
        cb = self.scoreboard_players_set_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, score=score))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_set_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players set")
        nt = lambda param: (param, _gt(cls.scoreboard_players_set, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_param(*nt("set"))
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_add(self,
                               target: Union[Union[JavaSelector, UUID], str],
                               objective: str,
                               score: int) -> ExecutedCommand:
        cb = self.scoreboard_players_add_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, score=score))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_add_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players add")
        nt = lambda param: (param, _gt(cls.scoreboard_players_add, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_param(*nt("set"), range=lambda x: 0 <= x <= Int.max)
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_remove(self,
                                  target: Union[Union[JavaSelector, UUID], str],
                                  objective: str,
                                  score: int) -> ExecutedCommand:
        cb = self.scoreboard_players_remove_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective, score=score))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_remove_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players remove")
        nt = lambda param: (param, _gt(cls.scoreboard_players_remove, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_param(*nt("set"), range=lambda x: 0 <= x <= Int.max)
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_reset(self,
                                 target: Union[Union[JavaSelector, UUID], str],
                                 objective: Optional[str]=None) -> ExecutedCommand:
        cb = self.scoreboard_players_reset_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_reset_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players reset")
        nt = lambda param: (param, _gt(cls.scoreboard_players_reset, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$", optional=True)
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_enable(self,
                                  target: Union[Union[JavaSelector, UUID], str],
                                  objective: str) -> ExecutedCommand:
        cb = self.scoreboard_players_enable_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, objective=objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_enable_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players enable")
        nt = lambda param: (param, _gt(cls.scoreboard_players_enable, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        return cb

    @version(introduced="13w04a")
    def scoreboard_players_operation(self, *,
                                     target: Union[Union[JavaSelector, UUID], str],
                                     target_objective: str,
                                     operation: Literal["+=", "-=", "*=", "/=", "%=", "=", "<", ">", "><"],
                                     source: Union[Union[JavaSelector, UUID], str],
                                     source_objective: str) -> ExecutedCommand:
        cb = self.scoreboard_players_operation_cb()
        cmd = ExecutedCommand(self.fh, "scoreboard", cb.build(target=target, target_objective=target_objective,
                                                              operation=operation, source=source,
                                                              source_objective=source_objective))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def scoreboard_players_operation_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("scoreboard players operation")
        nt = lambda param: (param, _gt(cls.scoreboard_players_operation, param))
        cb.add_param(*nt("target"))
        cb.add_param(*nt("target_objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        cb.add_switch(*_go(cls.scoreboard_players_operation, "operation"))
        cb.add_param(*nt("source"))
        cb.add_param(*nt("source_objective"), regex=r"^[ A-Za-z0-9\-+\._]*$")
        return cb

    @version(introduced="12w21a")
    def seed(self) -> ExecutedCommand:
        cmd = ExecutedCommand(self.fh, "seed", "seed")
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def seed_cb(cls) -> CommandBuilder:
        return CommandBuilder("seed")

    @version(introduced="13w37a")
    def setblock(self, pos: BlockCoord,
                 block: str,
                 mode: Literal["destroy", "keep", "replace"]="replace") -> ExecutedCommand:
        cb = self.setblock_cb()
        cmd = ExecutedCommand(self.fh, "setblock", cb.build(pos=pos, block=block, mode=mode))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def setblock_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("setblock")
        nt = lambda param: (param, _gt(cls.setblock, param))
        cb.add_param(*nt("pos"))
        cb.add_param(*nt("block"))
        cb.add_param(*nt("mode"), default=_gd(cls.setblock, "mode"))
        return cb

    @version(introduced="13w38a")
    def setidletimeout(self, minutes: int) -> ExecutedCommand:
        cb = self.setidletimeout_cb()
        cmd = ExecutedCommand(self.fh, "setidletimeout", cb.build(minutes=minutes))
        self.fh.commands.append(cmd)
        return cmd
    @classmethod
    def setidletimeout_cb(cls) -> CommandBuilder:
        cb = CommandBuilder("setidletimeout")
        nt = lambda param: (param, _gt(cls.setidletimeout, param))
        cb.add_param(*nt("minutes"), range=lambda x: 0 <= x <= Int.max)
        return cb

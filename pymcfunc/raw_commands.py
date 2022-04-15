from __future__ import annotations

import inspect
import warnings
from functools import wraps
from typing import Optional, Any, Callable, Tuple, TYPE_CHECKING, Annotated, Literal, Self, Type
from uuid import UUID

from pymcfunc.advancements import Advancement
from pymcfunc.command import ExecutedCommand, Command, SE, AE, Range, NoSpace, Element, Player, Regex, \
    PlayerName, LE, _JavaPlayerTarget, _JavaSingleTarget, ResourceLocation, RawJson, _BedrockSinglePlayerTarget, \
    _BedrockPlayerTarget, _BedrockTarget, _BedrockSingleTarget, Quoted
from pymcfunc.coord import BlockCoord, Coord, Rotation, ChunkCoord
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.internal import base_class
from pymcfunc.nbt import Int, Path, Compound, NBT
from pymcfunc.range import FloatRange
from pymcfunc.selectors import BedrockSelector, JavaSelector
from pymcfunc.version import JavaVersion, BedrockVersion

if TYPE_CHECKING:
    from pymcfunc.func_handler import BaseFunctionHandler

def _command(order: list[Element], cmd_name: str | None = None, segment_name: str | None = None):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return Command.command(self.fh, order, cmd_name, segment_name)(func)(*args, **kwargs)
        return wrapper
    return decorator

def _base_version(platform: Type[JavaVersion, BedrockVersion], introduced: Optional[str]=None, deprecated: Optional[str]=None, temp_removed: Optional[Tuple[str, str]]=None):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            pack_version = self.fh.p.version
            if introduced is not None and pack_version < platform(introduced):
                warnings.warn(f"The command `{func.__name__}` was introduced in {introduced}, but your pack is for {pack_version}", category=FutureCommandWarning)
            elif deprecated is not None and pack_version >= platform(deprecated):
                warnings.warn(f"The command `{func.__name__}` was deprecated in {deprecated}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
            elif temp_removed is not None and platform(temp_removed[0]) <= pack_version < platform(temp_removed[1]):
                warnings.warn(f"The command `{func.__name__}` was deprecated in {temp_removed[0]} and reintroduced in {temp_removed[1]}, but your pack is for {pack_version}", category=DeprecatedCommandWarning)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def param_version_introduced(self, platform: Type[JavaVersion, BedrockVersion], param_name: str, param_value: Any, version_introduced: str, default: Any=None):
    if param_value != default and self.fh.p.version < platform(version_introduced):
        warnings.warn(f"The `{param_name}` parameter was introduced in {version_introduced}, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)

def option_version_introduced(self, platform: Type[JavaVersion, BedrockVersion], param_name: str, param_value: Any, version_introduced: str, option: Any):
    if param_value == option and self.fh.p.version < platform(version_introduced):
        warnings.warn(f"The `{option}` option of the `{param_name}` parameter was introduced in {version_introduced}, but your pack is for {self.fh.p.version}", category=FutureCommandWarning)

def option_version_deprecated(self, platform: Type[JavaVersion, BedrockVersion], param_name: str, param_value: Any, version_deprecated: str, option: Any):
    if param_value == option and self.fh.p.version >= platform(version_deprecated):
        warnings.warn(
            f"The `{option}` option of the `{param_name}` parameter was deprecated in {version_deprecated}, but your pack is for {self.fh.p.version}",
            category=FutureCommandWarning)

@base_class
class BaseRawCommands:
    """
    A container for raw Minecraft commands that are the same for both Java and Bedrock.

    .. warning::
       Do not instantiate BaseRawCommands directly; use a FuncHandler and access the commands via the ‘r’ attribute.
    """

    def __init__(self, fh: BaseFunctionHandler):
        self.fh = fh


class BedrockRawCommands(BaseRawCommands):
    """
    A container for raw Minecraft commands that are specially for Bedrock Edition.

    .. warning::
       Do not instantiate BedrockRawCommands directly; use a :py:class:`BedrockFunctionHandler` and access the commands via the ‘r’ attribute.
    """

    @staticmethod
    def _education_edition(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.fh.p.education:
                warnings.warn(f"The command `{func.__name__}` is an Education Edition feature. Your pack is not for Education Edition.", category=EducationEditionWarning)
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def _version(introduced: Optional[str]=None, deprecated: Optional[str]=None, temp_removed: Optional[Tuple[str, str]]=None):
        return _base_version(BedrockVersion, introduced, deprecated, temp_removed)
    
    @_command([
        SE([AE("cmd")],
           [AE("page", True)])
    ])
    @_version(introduced="0.16.0b1")
    def help_(self,
              cmd: Annotated[str, NoSpace] | None = None,
              page: Annotated[int, Range(Int.min, Int.max)] | None = None) -> ExecutedCommand: pass

    @_command([
        AE("target"),
        AE("ability", True),
        AE("value", True)
    ])
    @_education_edition
    @_version(introduced="0.16.0b1")
    def ability(self, target: _BedrockSinglePlayerTarget,
                ability: Literal["worldbuilder", "mayfly", "mute"] | None = None,
                value: bool | None = None) -> ExecutedCommand: pass

    @_command([AE("lock", True)])
    @_version(introduced="1.2.0")
    def alwaysday(self, lock: bool) -> ExecutedCommand: pass
    daylock = alwaysday

    @_command([
        AE("target"),
        AE("intensity", True),
        AE("seconds", True),
        AE("shake_type", True)
    ])
    @_version(introduced="1.16.100.57")
    def camerashake_add(self, target: _BedrockPlayerTarget = BedrockSelector.s(), *,
                        intensity: Annotated[float, Range(0, 4)] | None = None,
                        seconds: float | None = None,
                        shake_type: Literal["positional", "rotational"] | None = None) -> ExecutedCommand: pass

    @_command([AE("target")])
    @_version(introduced="1.16.210.54")
    def camerashake_stop(self, target: _BedrockPlayerTarget = BedrockSelector.s()) -> ExecutedCommand:
        pass

    @_command([AE("value")],
              segment_name="changesetting allow-cheats")
    def changesetting_allow_cheats(self, value: bool) -> ExecutedCommand: pass

    @_command([AE("value")])
    def changesetting_difficulty(self, value: Literal['peaceful', 'easy', 'normal', 'hard',
                                                      'p', 'e', 'n', 'h', 0, 1, 2, 3]) -> ExecutedCommand: pass

    @_command([AE("targets", True),
              AE("item", True),
              AE("max_count", True)])
    @_version(introduced="1.0.5.0")
    def clear(self, targets: _BedrockPlayerTarget = BedrockSelector.s(),
              item: str | None = None,
              max_count: Annotated[int, Range(-1, Int.max)] = -1) -> ExecutedCommand: pass

    @_command([AE("player", True)])
    @_version(introduced="1.16.100.57")
    def clearspawnpoint(self, player: _BedrockPlayerTarget = BedrockSelector.s()) -> ExecutedCommand: pass

    @_command([AE("begin"),
              AE("end"),
              AE("destination"),
              SE([AE("mask_mode", True, options=['replace', 'masked']),
                  AE("clone_mode", True, options=['force', 'move', 'normal'])],
                 [AE("mask_mode", options=['filtered']),
                  AE("clone_mode", options=['force', 'move', 'normal']),
                  AE("tile_name"),
                  SE([AE("tile_data")], [AE("block_states")])
                  ])
               ])
    @_version(introduced="0.16.0b1")
    def clone(self, begin: BlockCoord,
              end: BlockCoord,
              destination: BlockCoord, *,
              mask_mode: Literal['replace', 'masked', 'filtered'] = 'replace',
              clone_mode: Literal['force', 'move', 'normal'] = 'normal',
              tile_name: str | None = None,
              tile_data: Annotated[int, Range(-1, 65535)] | None = None,
              block_states: dict | None = None) -> ExecutedCommand: pass # TODO special handling for BlockStates syntax

    @_command([AE("server_uri")])
    @_version(introduced="0.16.0b1")
    def wsserver(self, server_uri: str) -> ExecutedCommand: pass
    connect = wsserver

    @_command([])
    @_version(introduced="0.16.0b1")
    def wsserver_out(self) -> ExecutedCommand: pass
    connect_out = wsserver_out

    @_command([AE("target"),
              AE("amount"),
              AE("cause", True),
              SE([LE("entity"),
                  AE("damager")],
                 optional=True)])
    @_version(introduced="1.18.10.26")
    def damage(self, target: _BedrockTarget,
               amount: Annotated[int, Range(Int.min, Int.max)],
               cause: Literal['all', 'anvil', 'block-explosion', 'charging', 'contact', 'drowning', 'enemy-attack',
                              'enemy-explosion', 'fall', 'falling-block', 'fire', 'fire-tick'],
               damager: _BedrockSingleTarget) -> ExecutedCommand: pass

    #dedicatedwsserver

    @_command([AE("player")])
    @_version(introduced="0.16.0b1")
    def deop(self, player: _BedrockPlayerTarget) -> ExecutedCommand: pass

    @_command([AE("npc"),
              AE("player"),
              AE("scene_name", True)])
    @_version(introduced="1.17.10.22")
    def dialogue_open(self, npc: BedrockSelector,
                      player: _BedrockPlayerTarget,
                      scene_name: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([AE("npc"),
              AE("scene_name"),
              AE("player", True)])
    @_version(introduced="1.17.10.22")
    def dialogue_change(self, npc: BedrockSelector,
                        scene_name: Annotated[str, Quoted],
                        player: _BedrockPlayerTarget | None = None) -> ExecutedCommand: pass

    @_command([AE("value")])
    @_version(introduced="1.0.5.0")
    def difficulty(self, value: Literal['peaceful', 'easy', 'normal', 'hard',
                                        'p', 'e', 'n', 'h', 0, 1, 2, 3]) -> ExecutedCommand: pass

    @_command([AE("player"),
              LE("clear")],
              segment_name="effect")
    @_version(introduced="1.0.5.0")
    def effect_clear(self, player: _BedrockTarget) -> ExecutedCommand: pass

    @_command([AE("player"),
              AE("effect"),
              AE("seconds", True),
              AE("amplifier", True),
              AE("hide_particles", True)],
              segment_name="effect")
    @_version(introduced="1.0.5.0")
    def effect_give(self, player: _BedrockTarget,
                    effect: str,
                    seconds: Annotated[int, Range(0, Int.max)] | None = None,
                    amplifier: Annotated[int, Range(0, 255)] = 0,
                    hide_particles: bool = False) -> ExecutedCommand: pass

    @_command([AE("player"),
              AE("enchantment"),
              AE("level", True)])
    @_version(introduced="0.16.0b5")
    def enchant(self, player: _BedrockTarget,
                enchantment: str | int,
                level: Annotated[int, Range(1, Int.max)] = 1) -> ExecutedCommand: pass

    @_command([LE("entity"), AE("target"), AE("event_name")])
    @_version(introduced="1.16.100.57")
    def event(self, target: _BedrockTarget, event_name: Annotated[str, Quoted]) -> ExecutedCommand: pass

    @_command([AE("origin"),
              AE("position"),
              SE([LE("detect"),
                  AE("detect_pos"),
                  AE("block"),
                  AE("data")],
                 optional=True),
              AE("command")])
    @_version(introduced="0.16.0b1")
    def execute(self, origin: _BedrockTarget,
                position: Coord, *,
                detect_pos: Coord | None = None,
                block: str | None = None,
                data: int | None = None,
                command: ExecutedCommand) -> ExecutedCommand: pass

    @_command([AE("from_"),
               AE("to"),
               AE("tile_name"),
               SE([AE("tile_data")],
                  [AE("block_states")],
                  optional=True),
               SE([AE("fill_mode", options=['destroy', 'hollow', 'keep', 'outline'])],
                  [AE("fill_mode", options=['replace']),
                   AE("replace_tile_name", True),
                   AE("replace_data_value", True)])
               ])
    @_version(introduced="0.16.0b1")
    def fill(self, from_: BlockCoord,
             to: BlockCoord,
             tile_name: str, *,
             tile_data: Annotated[int, Range(0, 65535)] = 0,
             block_states: dict | None = None, # TODO special format for blockstates
             fill_mode: Literal['destroy', 'hollow', 'keep', 'outline', 'replace'] = 'replace',
             replace_tile_name: str,
             replace_data_value: Annotated[int, Range(Int.min, Int.max)] = -1) -> ExecutedCommand: pass

    @_command([AE("victim"),
               SE([AE("mode", options=['push']),
                   AE("fog_id")],
                  [AE("mode", options=['pop', 'remove'])]),
               AE("user_provided_id")])
    @_version(introduced="1.16.100.54")
    def fog(self, victim: _BedrockTarget,
            mode: Literal['push', 'pop', 'remove'], *,
            fog_id: Annotated[str, Quoted] | None = None,
            user_provided_id: Annotated[str, Quoted]) -> ExecutedCommand: pass

    @_command([AE("name")])
    @_version(introduced="1.8.0.8")  # TODO Function class
    def function(self, name: str) -> ExecutedCommand: pass

    @_command([AE("mode"), AE("target", True)])
    @_version(introduced="0.16.0b1")
    def gamemode(self, mode: Literal['survival', 'creative', 'adventure', 'spectator', 'default', 's', 'c', 'a', 'd', 0, 1, 2, 5, 6],
                 target: _BedrockPlayerTarget = BedrockSelector.s()) -> ExecutedCommand: pass

    @_command([AE("rule"), AE("value", True)])
    @_version(introduced="a1.0.5.0")
    def gamerule(self, rule: Annotated[str, NoSpace], value: int | bool | None = None) -> ExecutedCommand: pass

class JavaRawCommands(BaseRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFunctionHandler` and access the commands via the ‘r’ attribute.
    """

    @staticmethod
    def _version(introduced: Optional[str] = None, deprecated: Optional[str] = None,
                 temp_removed: Optional[Tuple[str, str]] = None):
        return _base_version(JavaVersion, introduced, deprecated, temp_removed)

    def __getattribute__(self, item: str):
        res = super().__getattribute__(item)
        if 'cmd_info' in dir(res):
            return Command.command(self.fh, *res.cmd_info)(res)
        return res

    @_command([AE("command", True)])
    #@_version(introduced="12w17a")
    def help_(self, command: str) -> ExecutedCommand: pass

    @_command([
        AE("targets"),
        SE([AE("mode", options=["everything"])],
           [AE("mode", options=["only"]),
            AE("advancement"),
            AE("criterion", True)],
           [AE("mode", options=["from", "through", "until"]),
            AE("advancement")])
    ], cmd_name="advancement")
    @_version(introduced="17w13a")
    def advancement_grant(self, targets: _JavaPlayerTarget,
                          mode: Literal["everything", "only", "from", "through", "until"],
                          advancement: Advancement | None = None,
                          criterion: str | None = None) -> ExecutedCommand: pass

    @_command([
        AE("targets"),
        SE([AE("mode", options=["everything"])],
           [AE("mode", options=["only"]),
            AE("advancement"),
            AE("criterion", True)],
           [AE("mode", options=["from", "through", "until"]),
            AE("advancement")])
    ], cmd_name="advancement")
    @_version(introduced="17w13a")
    def advancement_revoke(self, targets: _JavaPlayerTarget,
                           mode: Literal["everything", "only", "from", "through", "until"],
                           advancement: Advancement | None = None,
                           criterion: str | None = None) -> ExecutedCommand: pass

    @_command([
        AE("target"),
        AE("attribute"),
        LE("get"),
        AE("scale", True)
    ], segment_name="attribute")
    @_version(introduced="20w17a")
    def attribute_get_total(self, target: _JavaSingleTarget,
                            attribute: ResourceLocation,
                            scale: float | None = None) -> ExecutedCommand: pass

    @_command([
        AE("target"),
        AE("attribute"),
        LE("base"),
        SE([AE("mode", options=["get"]),
            AE("scale", True)],
           [AE("mode", options=["set"]),
            AE("value")])
    ], segment_name="attribute")
    @_version(introduced="20w17a")
    def attribute_base(self, target: _JavaSingleTarget,
                       attribute: ResourceLocation,
                       mode: Literal["get", "set"],
                       scale: float | None = None,
                       value: float | None = None) -> ExecutedCommand: pass

    @_command([
        AE("target"),
        AE("attribute"),
        LE("modifier"),
        SE([AE("mode", options=["add"]),
            AE("uuid"),
            AE("name"),
            AE("value"),
            AE("add_mode")],
           [AE("mode", options=["remove"]),
            AE("uuid")],
           [AE("mode", options=["value get"]),
            AE("scale", True)])
    ], segment_name="attribute")
    @_version(introduced="20w17a")
    def attribute_modifier(self, target: _JavaSingleTarget,
                           attribute: ResourceLocation,
                           mode: Literal["add", "remove", "value get"], *,
                           uuid: UUID | None = None,
                           name: Annotated[str, Regex(r"^[\w.+-]*$")] | None = None,
                           value: float | None = None,
                           add_mode: Literal["add", "multiply", "multiply_base"] | None = None,
                           scale: float | None = None) -> ExecutedCommand: pass

    @_command([
        AE("targets"),
        AE("message", True)
    ])
    @_version(introduced="a1.0.16")
    def ban(self, targets: Annotated[str, PlayerName] | Annotated[JavaSelector, Player],
            message: str = "Banned by an operator.") -> ExecutedCommand: pass

    @_command([
        AE("targets"),
        AE("message", True)
    ], cmd_name="ban-ip")
    @_version(introduced="a1.0.16")
    def ban_ip(self, targets: Annotated[str, Regex(r"^[\w.+-]*$")] | Annotated[JavaSelector, Player],
               message: str = "Banned by an operator.") -> ExecutedCommand: pass

    @_command([AE("view", True)])
    @_version(introduced="a1.0.16")
    def banlist(self, view: Literal["ips", "players"] | None = None) -> ExecutedCommand: pass

    @_command([
        AE("id_"),
        AE("name")
    ])
    @_version(introduced="18w05a")
    def bossbar_add(self, id_: ResourceLocation, name: RawJson) -> ExecutedCommand: pass

    @_command([
        AE("id_"),
        AE("view")
    ])
    @_version(introduced="18w05a")
    def bossbar_get(self, id_: ResourceLocation,
                    view: Literal["max", "players", "value", "visible"]) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="18w05a")
    def bossbar_list(self, id_: ResourceLocation) -> ExecutedCommand: pass

    @_command([
        AE("id_")
    ])
    @_version(introduced="18w05a")
    def bossbar_remove(self, id_: ResourceLocation) -> ExecutedCommand: pass

    @_command([
        AE("id_"),
        SE([LE("colour"), AE("colour")],
           [LE("max_"), AE("max_")],
           [LE("name"), AE("name")],
           [LE("players"), AE("players", True)],
           [LE("style"), AE("style")],
           [LE("value"), AE("value")],
           [LE("visible"), AE("visible")])
    ])
    @_version(introduced="18w05a")
    def bossbar_set(self, id_: ResourceLocation, *,
                    colour: Literal["blue", "green", "pink", "purple", "red", "white", "yellow"] | None = None,
                    max_: Annotated[int, Range(1, Int.max)] | None = None,
                    name: str | RawJson | None = None,
                    players: _JavaPlayerTarget | None = None,
                    style: Literal["notched_6", "notched_10", "notched_12", "notched_20", "progress"] | None = None,
                    value: Annotated[int, Range(0, Int.max)] | None = None,
                    visible: bool | None = None) -> ExecutedCommand: pass

    @_command([AE("player", True),
              AE("item_name", True),
              AE("data", True),
              AE("max_count", True)])
    @_version(introduced="17w45a") # TODO old format
    def clear(self, player: _JavaPlayerTarget = JavaSelector.s(),
              item_name: str | None = None,
              data: Annotated[int, Range(-1, Int.max)] = -1,
              max_count: Annotated[int, Range(0, Int.max)] = -1) -> ExecutedCommand: pass

    @_command([AE("begin"),
              AE("end"),
              AE("destination"),
              SE([AE("mask_mode", True, options=["replace", "masked"]),
                  AE("clone_mode", True, options=["force", "move", "normal"])],
                 [AE("mask_mode", options=["filtered"]),
                  AE("filter_"),
                  AE("clone_mode", True, options=["force", "move", "normal"])
                  ])
               ])
    @_version(introduced="14w03a")
    def clone(self, begin: BlockCoord,
              end: BlockCoord,
              destination: BlockCoord, *,
              mask_mode: Literal["replace", "masked", "filtered"] = "replace",
              clone_mode: Literal["force", "move", "normal"] = "normal",
              filter_: str | None = None) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("block")],
                  [LE("entity"), AE("entity")],
                  [LE("storage"), AE("storage")]),
              AE("path", True),
              AE("scale", True)])
    @_version(introduced="17w45b")
    def data_get(self, *,
                 block: BlockCoord | None = None,
                 entity: _JavaSingleTarget | None = None,
                 storage: ResourceLocation | None = None,
                 path: Path | None = None,
                 scale: float | None = None) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("block")],
                  [LE("entity"), AE("entity")],
                  [LE("storage"), AE("storage")]),
              AE("nbt")])
    @_version(introduced="17w45b")
    def data_merge(self, *,
                   block: BlockCoord | None = None,
                   entity: _JavaSingleTarget | None = None,
                   storage: ResourceLocation | None = None,
                   nbt: Compound) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("target_block")],
                  [LE("entity"), AE("target_entity")],
                  [LE("storage"), AE("target_storage")]),
              AE("target_path", True),
              SE([AE("mode", options=['append', 'merge', 'prepend', 'set'])],
                 [AE("mode", options=['insert']),
                  AE("index")
                  ]),
              SE([LE("from"),
                  SE([LE("block"), AE("source_block")],
                     [LE("entity"), AE("source_entity")],
                     [LE("storage"), AE("source_storage")]),
                  AE("source_path", True)],
                 [LE("value"), AE("value")])
               ])
    @_version(introduced="18w43a")
    def data_modify(self, *,
                    target_block: BlockCoord | None = None,
                    target_entity: _JavaSingleTarget | None = None,
                    target_storage: ResourceLocation | None = None,
                    target_path: Path,
                    mode: Literal['append', 'insert', 'merge', 'prepend', 'set'],
                    index: Annotated[int, Range(Int.min, Int.max)] | None = None,
                    source_block: BlockCoord | None = None,
                    source_entity: _JavaSingleTarget | None = None,
                    source_storage: ResourceLocation | None = None,
                    source_path: Path | None = None,
                    value: NBT) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("block")],
                  [LE("entity"), AE("entity")],
                  [LE("storage"), AE("storage")]),
              AE("path")])
    @_version(introduced="17w45b")
    def data_remove(self, *,
                    block: BlockCoord | None = None,
                    entity: _JavaSingleTarget | None = None,
                    storage: ResourceLocation | None = None,
                    path: Path) -> ExecutedCommand: pass

    @_command([AE("name")])
    @_version(introduced="17w46a")
    def datapack_disable(self, name: Annotated[str, Quoted, Regex(r"^[\w.+-]*$")]) -> ExecutedCommand: pass

    @_command([AE("name"),
              SE([AE("priority", options=['first', 'last'])],
                 [AE("priority", options=['before', 'after']),
                  AE("existing")],
                 optional=True)])
    @_version(introduced="17w46a")
    def datapack_enable(self, name: Annotated[str, Quoted, Regex(r"^[\w.+-]*$")],
                        priority: Literal['first', 'last', 'before', 'after'] | None = None,
                        existing: Annotated[str, Quoted, Regex(r"^[\w.+-]*$")] | None = None) -> ExecutedCommand: pass

    @_command([AE("view", True)])
    @_version(introduced="17w46a")
    def datapack_list(self, view: Literal['available', 'enabled'] | None = None) -> ExecutedCommand: pass

    @_command([SE([AE("mode", options=['start', 'stop'])],
                  [AE("mode", options=['function']),
                  AE("name")])])
    @_version(introduced="12w27a") # TODO support for outdated syntax
    def debug(self, mode: Literal['start', 'stop', 'function'],
              name: ResourceLocation | str | None = None) -> ExecutedCommand: pass

    @_command([AE("mode")])
    @_version(introduced="12w22a")
    def defaultgamemode(self, mode: Literal['survival', 'creative', 'adventure', 'spectator']) -> ExecutedCommand: pass

    @_command([AE("targets")])
    @_version(introduced="1.0.16")
    def deop(self, targets: Annotated[str, PlayerName] | Annotated[JavaSelector, Player]) -> ExecutedCommand: pass

    @_command([AE("value", True)])
    @_version(introduced="12w32a")
    def difficulty(self, value: Literal['peaceful', 'easy', 'normal', 'hard'] | None = None) -> ExecutedCommand: pass

    @_command([AE("targets", True),
              AE("effect", True)])
    @_version(introduced="1.6.1pre")
    def effect_clear(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID | None = None,
                     effect: str | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
              AE("effect"),
              AE("seconds", True),
              AE("amplifier", True),
              AE("hide_particles", True)])
    @_version(introduced="13w09b")
    def effect_clear(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID,
                     effect: str,
                     seconds: Annotated[int, Range(0, 1000000)] | None = None,
                     amplifier: Annotated[int, Range(0, 255)] = 0,
                     hide_particles: bool = False) -> ExecutedCommand: pass

    @_command([AE("targets"),
              AE("enchantment"),
              AE("level", True)])
    @_version(introduced="1.4.4pre", temp_removed=("17w45a", "18w06a"))
    def enchant(self, targets: _BedrockTarget,
                enchantment: str | int,
                level: Annotated[int, Range(0, Int.max)] = 1) -> ExecutedCommand: pass

    class ExecuteSubcommandHandler:
        """Handler for the (over)complicated /execute command for Java Edition."""

        def __init__(self):
            self.command_strings = []
            self.prev_obj = None

        def __str__(self):
            return ' '.join(self.command_strings)

        @staticmethod
        def _check_run(func: Callable[..., Self]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if len(self.command_strings) > 0 and self.command_strings[-1].startswith("run"):
                    raise ValueError(
                        "The `run` subcommand has already been registered. No additional subcommands can be entered.")
                return func(self, *args, **kwargs)

            return wrapper

        class Subcommand(Command):
            command_strings: list[str]
            handler: JavaRawCommands.ExecuteSubcommandHandler

            @classmethod
            def subcommand(cls, handler: JavaRawCommands.ExecuteSubcommandHandler,
                           order: list[Element],
                           cmd_name: str | None = None,
                           segment_name: str | None = None):
                def decorator(func: Callable[[BaseRawCommands, ...], ExecutedCommand]):
                    subcmd = cls()
                    subcmd.order = order
                    subcmd.func = func
                    subcmd.name = cmd_name or func.__name__.split("_")[0]
                    subcmd.segment_name = segment_name or func.__name__.replace("_", " ")
                    subcmd.arg_namelist = []
                    subcmd.handler = handler
                    subcmd.subcmd_obj = None
                    for name, arg in inspect.signature(func).parameters.items():
                        if name == "self": pass
                        if arg.POSITIONAL_OR_KEYWORD or arg.POSITIONAL_ONLY:
                            subcmd.arg_namelist.append(name)

                        subcmd.eles = cls._process_order(order, func)
                    return subcmd
                return decorator

            def __call__(self, *args, **kwargs) -> str:
                for i, arg in enumerate(args):
                    kwargs[self.arg_namelist[i]] = arg

                cmd_string, subcmd_obj = self._process_arglist(kwargs)
                self.handler.command_strings.append(cmd_string)
                self.handler.subcmd_obj = subcmd_obj
                return cmd_string

        @staticmethod
        def _subcommand(order: list[Element], cmd_name: str | None = None, segment_name: str | None = None):
            def decorator(func: Callable[..., Any]):
                @wraps(func)
                def wrapper(self, *args, **kwargs):
                    JavaRawCommands.ExecuteSubcommandHandler\
                        .Subcommand.subcommand(self, order, cmd_name, segment_name)(func)(*args, **kwargs)
                    return self
                return wrapper
            return decorator

        @_check_run
        @_subcommand([AE("axes")])
        def align(self, axes: Annotated[str, Regex(r"^(?!.*(.).*\1)[xyz]+$")]) -> Self: pass

        @_check_run
        @_subcommand([AE("anchor")])
        def anchor(self, anchor: Literal["eyes", "feet"]) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")])
        def as_(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")])
        def at(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID) -> Self: pass

        @_check_run
        @_subcommand([AE("pos")], segment_name="facing")
        def facing_position(self, pos: Coord) -> Self: pass

        @_check_run
        @_subcommand([AE("targets"), AE("anchor")])
        def facing_entity(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID,
                          anchor: Literal['eyes', 'feet']) -> Self: pass

        @_check_run
        @_subcommand([AE("dimension")])
        def in_(self, dimension: ResourceLocation) -> Self: pass

        @_check_run
        @_subcommand([AE("position")], segment_name="positioned")
        def positioned_position(self, position: Coord) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")], segment_name="positioned as")
        def positioned_entity(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID) -> Self: pass

        @_check_run
        @_subcommand([AE("rotation")])
        def rotated(self, rotation: Rotation) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")])
        def rotated_as(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID) -> Self: pass

        @_check_run
        @_subcommand([AE("pos"), AE("block")])
        def if_block(self, pos: Coord, block: str) -> Self: pass

        @_check_run
        @_subcommand([AE("pos"), AE("block")])
        def unless_block(self, pos: BlockCoord, block: str) -> Self: pass

        @_check_run
        @_subcommand([AE("start"), AE("end"), AE("destination"), AE("scan_mode")])
        def if_blocks(self, start: BlockCoord,
                      end: BlockCoord,
                      destination: BlockCoord,
                      scan_mode: Literal['all', 'masked']) -> Self: pass

        @_check_run
        @_subcommand([AE("start"), AE("end"), AE("destination"), AE("scan_mode")])
        def unless_blocks(self, start: BlockCoord,
                          end: BlockCoord,
                          destination: BlockCoord,
                          scan_mode: Literal['all', 'masked']) -> Self: pass

        @_check_run
        @_subcommand([SE([LE("block"), AE("block")],
                         [LE("entity"), AE("entity")],
                         [LE("storage"), AE("storage")]),
                      AE("path")])
        def if_data(self, *,
                    block: BlockCoord | None = None,
                    entity: _JavaSingleTarget | None = None,
                    storage: ResourceLocation | None = None,
                    path: Path) -> Self: pass

        @_check_run
        @_subcommand([SE([LE("block"), AE("block")],
                         [LE("entity"), AE("entity")],
                         [LE("storage"), AE("storage")]),
                      AE("path")])
        def unless_data(self, *,
                        block: BlockCoord | None = None,
                        entity: _JavaSingleTarget | None = None,
                        storage: ResourceLocation | None = None,
                        path: Path) -> Self: pass
        @_check_run
        @_subcommand([AE("targets")])
        def if_entity(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID): pass

        @_check_run
        @_subcommand([AE("targets")])
        def unless_entity(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID): pass

        @_check_run
        @_subcommand([AE("predicate")])
        def if_predicate(self, predicate: ResourceLocation) -> Self: pass # TODO Predicate class

        @_check_run
        @_subcommand([AE("predicate")])
        def unless_predicate(self, predicate: ResourceLocation) -> Self: pass  # TODO Predicate class

        @_check_run
        @_subcommand([AE("target"),
                      AE("target_objective"),
                      SE([AE("comparator", options=["<", "<=", "=", ">=", ">"]),
                          AE("source"),
                          AE("source_objective")],
                         [AE("comparator", options=["matches"]),
                          AE("range_")])])
        def if_score(self, *,
                     target: JavaSelector | Annotated[str, PlayerName] | UUID | Literal['*'],
                     target_objective: Annotated[str, Regex(r"^[\w.+-]*$")],
                     comparator: Literal["<", "<=", "=", ">=", ">", "matches"],
                     source: JavaSelector | Annotated[str, PlayerName] | UUID | Literal['*'] = None,
                     source_objective: Annotated[str, Regex(r"^[\w.+-]*$")] | None = None,
                     range_: FloatRange | None = None) -> Self: pass

        @_check_run
        @_subcommand([AE("target"),
                      AE("target_objective"),
                      SE([AE("comparator", options=["<", "<=", "=", ">=", ">"]),
                          AE("source"),
                          AE("source_objective")],
                         [AE("comparator", options=["matches"]),
                          AE("range_")])])
        def unless_score(self, *,
                         target: JavaSelector | Annotated[str, PlayerName] | UUID | Literal['*'],
                         target_objective: Annotated[str, Regex(r"^[\w.+-]*$")],
                         comparator: Literal["<", "<=", "=", ">=", ">", "matches"],
                         source: JavaSelector | Annotated[str, PlayerName] | UUID | Literal['*'] = None,
                         source_objective: Annotated[str, Regex(r"^[\w.+-]*$")] | None = None,
                         range_: FloatRange | None = None) -> Self: pass

        @_check_run
        @_subcommand([AE("target_pos"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_result_block(self, target_pos: BlockCoord,
                               path: Path,
                               type_: Literal["byte", "short", "int", "long", "float", "double"],
                               scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("target_pos"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_success_block(self, target_pos: BlockCoord,
                                path: Path,
                                type_: Literal["byte", "short", "int", "long", "float", "double"],
                                scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("id_"), AE("value")])
        def store_result_bossbar(self, id_: ResourceLocation, value: Literal["value", "max"]) -> Self: pass

        @_check_run
        @_subcommand([AE("id_"), AE("value")])
        def store_success_bossbar(self, id_: ResourceLocation, value: Literal["value", "max"]) -> Self: pass

        @_check_run
        @_subcommand([AE("target"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_result_entity(self, target: JavaSelector | Annotated[str, PlayerName] | UUID,
                                path: Path,
                                type_: Literal["byte", "short", "int", "long", "float", "double"],
                                scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("target"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_success_entity(self, target: JavaSelector | Annotated[str, PlayerName] | UUID,
                                 path: Path,
                                 type_: Literal["byte", "short", "int", "long", "float", "double"],
                                 scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("targets"), AE("objective")])
        def store_result_score(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID | Literal['*'],
                               objective: Annotated[str, Regex(r"^[\w.+-]*$")]) -> Self: pass

        @_check_run
        @_subcommand([AE("targets"), AE("objective")])
        def store_success_score(self, targets: JavaSelector | Annotated[str, PlayerName] | UUID | Literal['*'],
                                objective: Annotated[str, Regex(r"^[\w.+-]*$")]) -> Self: pass

        @_check_run
        @_subcommand([AE("target"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_result_block(self, target_pos: ResourceLocation,
                               path: Path,
                               type_: Literal["byte", "short", "int", "long", "float", "double"],
                               scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("target"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_success_block(self, target_pos: ResourceLocation,
                                path: Path,
                                type_: Literal["byte", "short", "int", "long", "float", "double"],
                                scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("command")])
        def run(self, command: ExecutedCommand) -> Self: pass

    EC = ExecutedCommand

    @_command([AE("subcommands")])
    @_version(introduced="14w07a")
    def execute(self, subcommands: ExecuteSubcommandHandler) -> ExecutedCommand: pass

    @_command([AE("from_"),
               AE("to"),
               AE("block"),
               SE([AE("mode", options=['destroy', 'hollow', 'keep', 'outline'])],
                  [AE("mode", options=['replace']),
                   AE("filter_", True)])
               ])
    @_version(introduced="14w03a")
    def fill(self, from_: BlockCoord,
             to: BlockCoord,
             block: str, *,
             mode: Literal['destroy', 'hollow', 'keep', 'outline', 'replace'] = 'replace',
             filter_: str | None = None) -> ExecutedCommand: pass

    @_command([SE([AE("mode", options=['add', 'remove']),
                   AE("from_"),
                   AE("to", True)],
                  [AE("mode", options=['remove all'])],
                  [AE("mode", options=['query']),
                   AE("pos", True)])])
    @_version(introduced="1.13.1pre1") # TODO /chunk
    def forceload(self, mode: Literal['add', 'remove', 'remove all', 'query'], *,
                  from_: ChunkCoord | None = None,
                  to: ChunkCoord | None = None,
                  pos: ChunkCoord | None = None) -> ExecutedCommand: pass

    @_command([AE("name")])
    @_version(introduced="1.12pre1") # TODO Function class
    def function(self, name: ResourceLocation) -> ExecutedCommand: pass

    @_command([AE("mode"), AE("target", True)])
    @_version(introduced="12w16a") # TODO old syntax
    def gamemode(self, mode: Literal['survival', 'creative', 'adventure', 'spectator', 'default'],
                 target: _JavaPlayerTarget = JavaSelector.s()) -> ExecutedCommand: pass

    @_command([AE("rule"), AE("value", True)])
    @_version(introduced="12w32a")
    def gamerule(self, rule: Annotated[str, NoSpace], value: int | bool | None = None) -> ExecutedCommand: pass
from __future__ import annotations

import inspect
import warnings
from functools import wraps
from typing import Optional, Any, Callable, Tuple, TYPE_CHECKING, Annotated, Literal, Type
from uuid import UUID

from typing_extensions import Self

from pymcfunc.advancements import Advancement
from pymcfunc.command import ExecutedCommand, Command, SE, AE, Range, NoSpace, Element, Player, Regex, \
    PlayerName, LE, _JavaPlayerTarget, _JavaSingleTarget, ResourceLocation, RawJson, _BedrockSinglePlayerTarget, \
    _BedrockPlayerTarget, _BedrockTarget, _BedrockSingleTarget, Quoted, _JavaObjectiveName, _JavaTarget, \
    _BedrockObjectiveName, _JavaSinglePlayerTarget
from pymcfunc.coord import BlockCoord, Coord, Rotation, ChunkCoord, Coord2d
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.internal import base_class
from pymcfunc.nbt import Int, Path, Compound, NBT, Float
from pymcfunc.range import FloatRange
from pymcfunc.selectors import BedrockSelector, JavaSelector
from pymcfunc.version import JavaVersion, BedrockVersion

if TYPE_CHECKING:
    from pymcfunc.func_handler import BaseFunctionHandler

def _command(order: list[Element], cmd_name: str | None = None, segment_name: str | None = None):
    def decorator(func: Callable[..., Any]):
        return Command.command(None, order, cmd_name, segment_name)(func)
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

    def __getattribute__(self, item: str):
        attr = super().__getattribute__(item)
        if isinstance(attr, Command):
            attr.fh = self.fh
        return attr


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

    @_command([SE([AE("mode", options=['runthis', 'pos', 'runthese'])],
                  [AE("mode", options=['run']),
                   AE("test_name"),
                   AE("rotation_steps", True)],
                  [AE("mode", options=['runset']),
                   AE("tag", True),
                   AE("rotation_steps", True)],
                  [AE("mode", options=['create']),
                   AE("test_name"),
                   AE("width"),
                   AE("height"),
                   AE("depth")],
                  [AE("mode", options=['clearall']),
                   AE("radius", True)])
               ])
    @_version(introduced="1.16.210.60")
    def gametest(self, mode: Literal['runthis', 'pos', 'runthese', 'run', 'runset', 'create', 'clearall'], *,
                 test_name: Annotated[str, NoSpace] | None = None,
                 rotation_steps: int | None = None,
                 tag: Annotated[str, NoSpace] | None = None,
                 radius: int | None = None,
                 width: int | None = None,
                 height: int | None = None,
                 depth: int | None = None) -> ExecutedCommand: pass

    @_command([AE("player"),
               AE("item"),
               AE("amount", True),
               AE("data", True),
               AE("components", True)])
    @_version(introduced="0.16.0b1")
    def give(self, player: _BedrockPlayerTarget,
             item: str,
             amount: Annotated[int, Range(1, 32767)] = 1,
             data: Annotated[int, Range(0, 32767)] = 0,
             components: dict | None = None) -> ExecutedCommand: pass

    @_command([AE("value", True)])
    @_education_edition
    @_version(introduced="1.2.0.2")
    def immutableworld(self, value: bool | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("reason")])
    @_version(introduced="1.16.0.57")
    def kick(self, targets: _BedrockPlayerTarget,
             reason: str = "Kicked by an operator") -> ExecutedCommand: pass

    @_command([AE("targets", True)])
    @_version(introduced="0.16.0b1")
    def kill(self, targets: _BedrockTarget = BedrockSelector.s()) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="1.0.16_02")
    def list(self) -> ExecutedCommand: pass

    @_command([AE("structure")])
    @_version(introduced="a0.17.0.1", temp_removed=("a0.17.0.2", "a1.0.0.0"))
    def locate(self, structure: Annotated[str, NoSpace]) -> ExecutedCommand: pass

    @_command([SE([LE("give"), AE("give_player")],
                  [LE("spawn"), AE("spawn_position")]),
               SE([LE("kill"), AE("kill_entity")],
                  [LE("loot"), AE("loot_table")]),
               AE("tool", True)])
    @_version(introduced="1.18.0.21", temp_removed=("1.18.0.22", "1.18.10.21"))
    def loot(self, *,
             give_player: _BedrockSinglePlayerTarget | None = None,
             spawn_position: Coord | None = None,
             kill_entity: _BedrockSingleTarget | None = None,
             loot_table: ResourceLocation | None = None, # TODO LootTable
             tool: str | Literal['mainhand', 'offhand'] | None = None) -> ExecutedCommand: pass

    @_command([AE("message")])
    @_version(introduced="a1.0.5.0")
    def me(self, message: str) -> ExecutedCommand: pass

    @_command([AE("event"), AE("value", True)])
    @_version(introduced="b1.11.0.3")
    def mobevent(self, event: Literal['minecraft:pillager_patrols_event',
                                      'minecraft:wandering_trader_event',
                                      'events_enabled'],
                 value: bool | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("message")])
    @_version(introduced="0.16.0b1")
    def msg(self, targets: _BedrockPlayerTarget, message: str) -> ExecutedCommand: pass
    w = tell = msg

    @_command([SE([AE("action", options=['play', 'queue']),
                   AE("track_name"),
                   AE("volume", True),
                   AE("fade_seconds", True),
                   AE("repeat_mode", True)],
                  [AE("action", options=['stop']),
                   AE("fade_seconds", True)],
                  [AE("action", options=['volume']),
                   AE("volume")])
               ])
    @_version(introduced="1.16.100.58")
    def music(self, action: Literal['play', 'queue', 'stop', 'volume'], *,
              track_name: Annotated[str, Quoted] | None = None,
              volume: Annotated[float, Range(0, 1)] | None = None,
              fade_seconds: Annotated[float, Range(0, 10)] | None = None,
              repeat_mode: Literal['loop', 'play_once'] = 'play_once') -> ExecutedCommand: pass

    @_command([AE("player")])
    @_version(introduced="0.16.0b1")
    def op(self, player: _BedrockPlayerTarget) -> ExecutedCommand: pass

    @_command([AE("action")])
    def ops(self, action: Literal['list', 'reload']) -> ExecutedCommand: pass
    permission = ops

    @_command([AE("effect"), AE("position")])
    @_version(introduced="a1.0.5.0", temp_removed=("a1.0.5.3", "b1.8.0.8"))
    def particle(self, effect: Annotated[str, Quoted], position: Coord) -> ExecutedCommand: pass

    @_command([AE("entity"),
               AE("animation"),
               AE("next_state", True),
               AE("blend_out_time", True),
               AE("stop_expression", True),
               AE("controller", True)])
    @_version(introduced="1.16.100.52")
    def playanimation(self, entity: Annotated[str, PlayerName] | BedrockSelector,
                      animation: Annotated[str, Quoted, Regex(r".*(?<!\.v1\.0)$")],
                      next_state: Annotated[str, Quoted, Regex(r".*(?<!\.v1\.0)$")] | None = None,
                      blend_out_time: float = None,
                      stop_expression: Annotated[str, Quoted] | None = None, # TODO MoLang
                      controller: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([AE("sound"),
               AE("player", True),
               AE("position", True),
               AE("volume", True),
               AE("pitch", True),
               AE("minimum_volume", True)])
    @_version(introduced="a1.0.5.0")
    def playsound(self, sound: Annotated[str, Quoted],
                  player: _BedrockPlayerTarget | None = None,
                  position: Coord | None = None,
                  volume: float = 1.0,
                  pitch: float = 1.0,
                  minimum_volume: float = 0.0) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="b1.8.0.8")
    def reload(self) -> ExecutedCommand: pass

    @_command([AE("target")])
    @_education_edition
    def remove(self, target: BedrockSelector) -> ExecutedCommand: pass

    @_command([SE([LE("block"),
                   AE("block"),
                   LE("slot.container"),
                   AE("slot_id")],
                  [LE("entity"),
                   AE("entity"),
                   AE("slot_type"),
                   AE("slot_id")]),
               AE("replace_mode", True),
               AE("item_name"),
               AE("amount", True),
               AE("data", True),
               AE("components", True)])
    @_version(introduced="a1.0.5.0")
    def replaceitem(self, block: Coord,
                    entity: _BedrockTarget, *,
                    slot_type: Annotated[str, NoSpace] | None = None,
                    slot_id: Annotated[int, Range(Int.min, Int.max)],
                    replace_mode: Literal['destroy', 'keep'] | None = None,
                    item_name: str,
                    amount: Annotated[int, Range(1, 64)] = 1,
                    data: Annotated[int, Range(Int.min, Int.max)] = 0,
                    components: dict) -> ExecutedCommand: pass

    @_command([AE("riders"),
               LE("start_riding"),
               AE("ride"),
               AE("teleport_rules", True),
               AE("fill_type", True)],
              segment_name="ride")
    @_version(introduced="1.16.100.52")
    def ride_start_riding(self, riders: _BedrockTarget,
                          ride: _BedrockSingleTarget,
                          teleport_rules: Literal['teleport_ride', 'teleport_rider'] = 'teleport_rider',
                          fill_type: Literal['if_group_fits', 'until_full'] = 'until_full') -> ExecutedCommand: pass

    @_command([AE("riders"),
               LE("stop_riding")],
              segment_name="ride")
    @_version(introduced="1.16.100.52")
    def ride_stop_riding(self, riders: _BedrockTarget) -> ExecutedCommand: pass

    @_command([AE("rides"),
               LE("evict_riders")],
              segment_name="ride")
    @_version(introduced="1.16.100.52")
    def ride_evict_riders(self, rides: _BedrockTarget) -> ExecutedCommand: pass

    @_command([AE("rides"),
               LE("summon_rider"),
               AE("entity_type"),
               AE("spawn_event", True),
               AE("name_tag", True)],
              segment_name="ride")
    @_version(introduced="1.16.100.52")
    def ride_summon_rider(self, rides: _BedrockTarget,
                          entity_type: str,
                          spawn_event: Annotated[str, Quoted] | None = None, # TODO spawn event
                          name_tag: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([AE("riders"),
               LE("summon_ride"),
               AE("entity_type"),
               AE("ride_rules", True),
               AE("spawn_event", True),
               AE("name_tag", True)
               ])
    @_version(introduced="1.16.100.52")
    def ride_summon_ride(self, riders: _BedrockTarget,
                         entity_type: str,
                         ride_rules: Literal['skip_riders', 'no_ride_change', 'reassign_rides'] = 'reassign_rides',
                         spawn_event: Annotated[str, Quoted] | None = None,  # TODO spawn event
                         name_tag: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([AE("action")])
    @_version(introduced="1.6.1")
    def save(self, action: Literal['hold', 'query', 'resume']) -> ExecutedCommand: pass

    @_command([AE("message")])
    @_version(introduced="0.16.0b1")
    def say(self, message: str) -> ExecutedCommand: pass

    @_command([SE([AE("cuboid_from"), AE("cuboid_to")],
                  [LE("circle"), AE("circle_center"), AE("circle_radius")],
                  [LE("tickingarea"), AE("tickingarea_name")]),
               AE("function")],
              segment_name="schedule on_area_loaded add")
    @_version(introduced="1.16.100.59")
    def schedule_on_area_loaded_add(self, *,
                                    cuboid_from: Coord | None = None,
                                    cuboid_to: Coord | None = None,
                                    circle_center: Coord | None = None,
                                    circle_radius: Annotated[int, Range(0, Int.max)] | None = None,
                                    tickingarea_name: Annotated[str, Quoted] | None = None,
                                    function: str) -> ExecutedCommand: pass # TODO Function class

    @_command([])
    @_version(introduced="1.7.0.2")
    def scoreboard_objectives_list(self) -> ExecutedCommand: pass

    @_command([AE("objective"), LE("dummy"), AE("display_name")])
    @_version(introduced="1.7.0.2")
    def scoreboard_objectives_add(self, objective: _BedrockObjectiveName,
                                  display_name: _BedrockObjectiveName | None = None) -> ExecutedCommand: pass

    @_command([AE("objective")])
    @_version(introduced="1.7.0.2")
    def scoreboard_objectives_remove(self, objective: _BedrockObjectiveName) -> ExecutedCommand: pass

    @_command([SE([AE("slot", options=['list', 'sidebar']),
                   AE("objective", True),
                   AE("sort_order", True)],
                  [AE("slot", options=['belowname']),
                   AE("objective", True)])
               ])
    @_version(introduced="1.7.0.2")
    def scoreboard_objective_setdisplay(self, slot: Literal['list', 'sidebar', 'belowname'],
                                        objective: _BedrockObjectiveName | None = None,
                                        sort_order: Literal['ascending', 'descending'] | None = None) -> ExecutedCommand: pass

    @_command([AE("target", True)])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_list(self, target: _BedrockTarget | Literal['*'] | None = None) -> ExecutedCommand: pass

    @_command([AE("target"), AE("objective"), AE("count")])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_set(self, target: _BedrockTarget | Literal['*'],
                               objective: _BedrockObjectiveName,
                               count: int) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective"), AE("score")])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_add(self, targets: _BedrockTarget | Literal['*'],
                               objective: _BedrockObjectiveName,
                               score: int) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective"), AE("score")])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_remove(self, targets: _BedrockTarget | Literal['*'],
                                  objective: _BedrockObjectiveName,
                                  score: int) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective"), AE("min_"), AE("max_")])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_random(self, targets: _BedrockTarget | Literal['*'],
                                  objective: _BedrockObjectiveName,
                                  min_: int, max_: int) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective", True)])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_reset(self, targets: _BedrockTarget | Literal['*'],
                                 objective: _BedrockObjectiveName | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective"), AE("min_"), AE("max_", True)])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_test(self, targets: _BedrockTarget | Literal['*'],
                                objective: _BedrockObjectiveName,
                                min_: int | Literal['*'],
                                max_: int | Literal['*'] | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("target_objective"), AE("operation"), AE("source"), AE("source_objective")])
    @_version(introduced="1.7.0.2")
    def scoreboard_players_operation(self, targets: _BedrockTarget | Literal['*'],
                                     target_objective: _BedrockObjectiveName,
                                     operation: Literal['=', '+=', '-=', '*=', '/=', '%=', '><', '<', '>'],
                                     source: _BedrockTarget | Literal['*'],
                                     source_objective: _BedrockObjectiveName) -> ExecutedCommand: pass

    @_command([AE("pos"),
               AE("block"),
               SE([AE("tile_data")],
                  [AE("block_states")],
                  optional=True),
               AE("change_mode", True)])
    @_version(introduced="13w37a")
    def setblock(self, pos: BlockCoord,
                 block: str,
                 tile_data: Annotated[int, Range(0, 65536)] = 0,
                 block_states: dict | None = None,
                 change_mode: Literal['destroy', 'keep', 'replace'] = 'replace') -> ExecutedCommand: pass

    @_command([AE("max_players")])
    @_version(introduced="1.1.0.3")
    def setmaxplayers(self, max_players: Annotated[int, Range(1, 30)]) -> ExecutedCommand: pass

    @_command([AE("spawn_point", True)])
    @_version(introduced="0.16.0b1")
    def setworldspawn(self, spawn_point: Coord = Coord.at_executor()) -> ExecutedCommand: pass

    @_command([AE("targets", True), AE("spawn_pos", True)])
    @_version(introduced="0.16.0b1")
    def spawnpoint(self, targets: _BedrockPlayerTarget = BedrockSelector.s(),
                   spawn_pos: Coord = Coord.at_executor()) -> ExecutedCommand: pass

    @_command([AE("center"),
               AE("spread_distance"),
               AE("max_range"),
               AE("victim")])
    @_version(introduced="1.0.5.0")
    def spreadplayers(self, *,
                      center: Coord2d,
                      spread_distance: Annotated[float, Range(0.0, Float.max)],
                      max_range: Annotated[float, Range(1.0, Float.max)],
                      victim: _BedrockTarget) -> ExecutedCommand: pass

    @_command([])
    def stop(self) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("sound", True)])
    @_version(introduced="1.0.5.0")
    def stopsound(self, targets: _JavaPlayerTarget,
                  sound: ResourceLocation | None = None) -> ExecutedCommand: pass

    @_command([AE("name"),
               AE("from_"),
               AE("to"),
               AE("includes_entities", True),
               AE("save_mode", True),
               AE("includes_blocks", True)])
    @_version(introduced="1.16.100.52")
    def structure_save(self, name: Annotated[str, Quoted],
                       from_: Coord,
                       to: Coord,
                       includes_entities: bool = True,
                       save_mode: Literal['disk', 'memory'] | None = None,
                       includes_blocks: bool = True) -> ExecutedCommand: pass

    @_command([AE("name"),
               AE("to"),
               AE("rotation", True),
               AE("mirror", True),
               SE([AE("animation_mode"),
                   AE("animation_seconds")],
                  optional=True),
               AE("includes_entities", True),
               AE("includes_blocks", True),
               AE("integrity", True),
               AE("seed", True)])
    @_version(introduced="1.16.100.52")
    def structure_load(self, name: Annotated[str, Quoted],
                       to: Coord,
                       rotation: Literal['0_degrees', '90_degrees', '180_degrees', '270_degrees'] = '0_degrees',
                       mirror: Literal['x', 'z', 'xz', 'none'] = 'none',
                       animation_mode: Literal['block_by_block', 'layer_by_layer'] | None = None,
                       animation_seconds: float | None = None,
                       includes_entities: bool = True,
                       includes_blocks: bool = True,
                       integrity: Annotated[float, Range(0, 100)] = 100,
                       seed: str | None = None) -> ExecutedCommand: pass

    @_command([AE("name")])
    @_version(introduced="1.16.100.52")
    def structure_delete(self, name: Annotated[str, Quoted]) -> ExecutedCommand: pass

    @_command([AE("entity_type"),
               SE([AE("name_tag"),
                   AE("spawn_pos", True)],
                  [AE("spawn_pos", True),
                   AE("spawn_event", True),
                   AE("name_tag", True)])
               ])
    @_version(introduced="0.16.0b1")
    def summon(self, entity_type: ResourceLocation,
               spawn_pos: Coord = Coord.at_executor(),
               spawn_event: Annotated[str, Quoted] | None = None, # TODO event maybe?
               name_tag: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
               SE([AE("action", options=['add', 'remove']),
                   AE("name")],
                  [AE("action", options=['list'])])])
    @_version(introduced="1.9.0.2")
    def tag(self, targets: _BedrockTarget,
            action: Literal['add', 'remove', 'list'],
            name: Annotated[str, Quoted]) -> ExecutedCommand: pass

    @_command([SE([AE("victim", True),
                   SE([AE("destination_entity")],
                      [AE("destination_pos")]),
                   AE("check_for_blocks", True)],
                  [AE("victim", True),
                   SE([AE("destination_entity")],
                      [AE("destination_pos")]),
                   SE([AE("rotation")],
                      [LE("facing"),
                       SE([AE("look_pos")],
                          [AE("look_entity")]),
                       AE("check_for_blocks", True)
                       ])
                   ])
               ])
    @_version(introduced="0.16.0b1")
    def teleport(self, *,
                 victim: _BedrockTarget = BedrockSelector.s(),
                 destination_entity: _BedrockTarget | None = None,
                 destination_pos: Coord | None = None,
                 rotation: Rotation | None = None,
                 look_pos: Coord | None = None,
                 look_entity: _BedrockTarget | None = None,
                 check_for_blocks: bool = False) -> ExecutedCommand: pass
    tp = teleport

    @_command([AE("targets"), AE("message")])
    @_version(introduced="1.9.0.0")
    def tellraw(self, targets: _BedrockPlayerTarget,
                message: RawJson) -> ExecutedCommand: pass

    @_command([AE("victim")])
    @_version(introduced="1.0.5.0")
    def testfor(self, victim: _BedrockTarget) -> ExecutedCommand: pass

    @_command([AE("position"), AE("tile_name"), AE("data_value")])
    @_version(introduced="0.16.0b1")
    def testforblock(self, position: Coord,
                     tile_name: str,
                     data_value: int) -> ExecutedCommand: pass

    @_command([AE("begin"), AE("end"), AE("destination"), AE("block_match", True)])
    @_version(introduced="0.16.0b1")
    def testforblocks(self, begin: Coord,
                      end: Coord,
                      destination: Coord,
                      block_match: Literal['masked', 'all'] = 'all') -> ExecutedCommand: pass

    @_command([SE([AE("from_"),
                   AE("to")],
                  [LE("circle"),
                   AE("center"),
                   AE("radius")]),
               AE("name", True)])
    @_version(introduced="1.2.0.2")
    def tickingara_add(self, *,
                       from_: Coord | None = None,
                       to: Coord | None = None,
                       center: Coord | None = None,
                       radius: Annotated[int, Range(0, Int.max)] | None = None,
                       name: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([SE([AE("name")], [AE("position")])])
    @_version(introduced="1.2.0.2")
    def tickingarea_remove(self, *,
                           name: Annotated[str, Quoted] | None = None,
                           position: Coord | None = None) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="1.2.0.2")
    def tickingarea_list(self) -> ExecutedCommand: pass

    @_command([], segment_name="tickingarea list all-dimensions")
    @_version(introduced="1.2.0.2")
    def tickingarea_list_all_dimensions(self) -> ExecutedCommand: pass

    @_command([SE([LE("add"),
                   AE("add")],
                  [LE("query"),
                   AE("query")],
                  [LE("set"),
                   AE("set_")])])
    @_version(introduced="0.16.0b1")
    def time(self, *,
             add: int | None = None,
             query: Literal['daytime', 'gametime', 'day'] | None = None,
             set_: Literal['day', 'night', 'noon', 'midnight', 'sunrise', 'sunset']
             | int | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
               SE([AE("action", options=['clear', 'reset'])],
                  [AE("action", options=['title', 'subtitle', 'actionbar']),
                   AE("title")],
                  [AE("action", options=['times']),
                   AE("fade_in"),
                   AE("stay"),
                   AE("fade_out")])
               ])
    @_version(introduced="1.0.5.0")
    def title(self, targets: _BedrockPlayerTarget,
              action: Literal['clear', 'reset', 'title', 'subtitle', 'actionbar', 'times'],
              title: str | None = None,
              fade_in: int | None = None,
              stay: int | None = None,
              fade_out: int | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
               SE([AE("action", options=['clear', 'reset'])],
                  [AE("action", options=['title', 'subtitle', 'actionbar']),
                   AE("title")],
                  [AE("action", options=['times']),
                   AE("fade_in"),
                   AE("stay"),
                   AE("fade_out")])
               ])
    @_version(introduced="1.0.5.0")
    def titleraw(self, targets: _BedrockPlayerTarget,
                 action: Literal['clear', 'reset', 'title', 'subtitle', 'actionbar', 'times'],
                 title: RawJson | None = None,
                 fade_in: int | None = None,
                 stay: int | None = None,
                 fade_out: int | None = None) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="0.16.0b1")
    def toggledownfall(self) -> ExecutedCommand: pass

    @_command([])
    def worldbuilder(self) -> ExecutedCommand: pass
    wb = worldbuilder

    @_command([AE("weather"), AE("duration", True)])
    @_version(introduced="0.16.0b1")
    def weather(self, weather: Literal['clear', 'rain', 'thunder'],
                duration: Annotated[int, Range(0, 1999999999)] = 300) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="0.16.0b1")
    def weather_clear(self) -> ExecutedCommand: pass

    @_command([SE([AE("action", options=['add', 'remove']),
                   AE("targets")],
                  [AE("action", options=['list', 'off', 'on', 'reload'])
                   ])
               ])
    @_version(introduced="b1.3")
    def allowlist(self, action: Literal['add', 'remove', 'list', 'off', 'on', 'reload'],
                  targets: Annotated[str, Quoted] | None = None) -> ExecutedCommand: pass

    @_command([AE("amount"), AE("player")])
    @_version(introduced="0.16.0b1")
    def xp(self, amount: int | Annotated[str, Regex(r"^\d+L?$")],
           player: _BedrockPlayerTarget) -> ExecutedCommand: pass

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
                           name: _JavaObjectiveName | None = None,
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
    def ban_ip(self, targets: _JavaObjectiveName | Annotated[JavaSelector, Player],
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
    def effect_clear(self, targets: _JavaTarget | None = None,
                     effect: str | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
              AE("effect"),
              AE("seconds", True),
              AE("amplifier", True),
              AE("hide_particles", True)])
    @_version(introduced="13w09b")
    def effect_clear(self, targets: _JavaTarget,
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
            self.subcmd_obj = None

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
                    subcmd.name = cmd_name or func.__name__.split("_")[0].strip()
                    subcmd.segment_name = segment_name or func.__name__.replace("_", " ").strip()
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
                        .Subcommand.subcommand(self, order, cmd_name, segment_name)(func)(self, *args, **kwargs)
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
        def as_(self, targets: _JavaTarget) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")])
        def at(self, targets: _JavaTarget) -> Self: pass

        @_check_run
        @_subcommand([AE("pos")], segment_name="facing")
        def facing_position(self, pos: Coord) -> Self: pass

        @_check_run
        @_subcommand([AE("targets"), AE("anchor")])
        def facing_entity(self, targets: _JavaTarget,
                          anchor: Literal['eyes', 'feet']) -> Self: pass

        @_check_run
        @_subcommand([AE("dimension")])
        def in_(self, dimension: ResourceLocation) -> Self: pass

        @_check_run
        @_subcommand([AE("position")], segment_name="positioned")
        def positioned_position(self, position: Coord) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")], segment_name="positioned as")
        def positioned_entity(self, targets: _JavaTarget) -> Self: pass

        @_check_run
        @_subcommand([AE("rotation")])
        def rotated(self, rotation: Rotation) -> Self: pass

        @_check_run
        @_subcommand([AE("targets")])
        def rotated_as(self, targets: _JavaTarget) -> Self: pass

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
        def if_entity(self, targets: _JavaTarget): pass

        @_check_run
        @_subcommand([AE("targets")])
        def unless_entity(self, targets: _JavaTarget): pass

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
                     target: _JavaTarget | Literal['*'],
                     target_objective: _JavaObjectiveName,
                     comparator: Literal["<", "<=", "=", ">=", ">", "matches"],
                     source: _JavaTarget | Literal['*'] = None,
                     source_objective: _JavaObjectiveName | None = None,
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
                         target: _JavaTarget | Literal['*'],
                         target_objective: _JavaObjectiveName,
                         comparator: Literal["<", "<=", "=", ">=", ">", "matches"],
                         source: _JavaTarget | Literal['*'] = None,
                         source_objective: _JavaObjectiveName | None = None,
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
        def store_result_entity(self, target: _JavaTarget,
                                path: Path,
                                type_: Literal["byte", "short", "int", "long", "float", "double"],
                                scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("target"),
                      AE("path"),
                      AE("type_"),
                      AE("scale")])
        def store_success_entity(self, target: _JavaTarget,
                                 path: Path,
                                 type_: Literal["byte", "short", "int", "long", "float", "double"],
                                 scale: float) -> Self: pass

        @_check_run
        @_subcommand([AE("targets"), AE("objective")])
        def store_result_score(self, targets: _JavaTarget | Literal['*'],
                               objective: _JavaObjectiveName) -> Self: pass

        @_check_run
        @_subcommand([AE("targets"), AE("objective")])
        def store_success_score(self, targets: _JavaTarget | Literal['*'],
                                objective: _JavaObjectiveName) -> Self: pass

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

    ESH = ExecuteSubcommandHandler

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

    @_command([AE("target"), AE("item"), AE("count", True)])
    @_version(introduced="a1.0.15")
    def give(self, target: _JavaPlayerTarget,
             item: str,
             count: Annotated[int, Range(1, Int.max)] = 1) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("block")],
                  [LE("entity"), AE("entity")]),
               AE("slot"),
               AE("modifier")])
    @_version(introduced="20w46a")
    def item_modify(self, *,
                    block: BlockCoord | None = None,
                    entity: _JavaTarget | None = None,
                    slot: str,
                    modifier: ResourceLocation) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("block")],
                  [LE("entity"), AE("entity")]),
               AE("slot"),
               LE("with"),
               AE("item"),
               AE("count", True)],
              segment_name="item replace")
    @_version(introduced="20w46a")
    def item_replace_with(self, *,
                          block: BlockCoord | None = None,
                          entity: _JavaTarget | None = None,
                          slot: str,
                          item: int,
                          count: Annotated[int, Range(1, 64)]) -> ExecutedCommand: pass

    @_command([SE([LE("block"), AE("block")],
                  [LE("entity"), AE("entity")]),
               AE("slot"),
               LE("from"),
               SE([LE("block"), AE("source_block")],
                  [LE("entity"), AE("source_entity")]),
               AE("source_slot"),
               AE("modifier", True)],
              segment_name="item replace")
    @_version(introduced="20w46a")
    def item_replace_with(self, *,
                          block: BlockCoord | None = None,
                          entity: _JavaTarget | None = None,
                          slot: str,
                          item: int,
                          count: Annotated[int, Range(1, 64)],
                          source_block: BlockCoord | None = None,
                          source_entity: _JavaTarget | None = None,
                          source_slot: str,
                          modifier: ResourceLocation, ) -> ExecutedCommand: pass

    @_command([AE("action")])
    @_version(introduced="21w37a")
    def jfr(self, action: Literal['start', 'stop']) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("reason")])
    @_version(introduced="a1.0.16")
    def kick(self, targets: _JavaPlayerTarget,
             reason: str = "Kicked by an operator") -> ExecutedCommand: pass

    @_command([AE("targets", True)])
    @_version(introduced="0.16.0b1")
    def kill(self, targets: Annotated[str, PlayerName] | JavaSelector = JavaSelector.s()) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="1.0.16_02")
    def list(self) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="1.8.1pre1")
    def list_uuids(self) -> ExecutedCommand: pass

    @_command([AE("structure")])
    @_version(introduced="16w39a")
    def locate(self, structure: Annotated[str, NoSpace]) -> ExecutedCommand: pass

    @_command([AE("biome")])
    @_version(introduced="20w06a")
    def locatebiome(self, biome: ResourceLocation) -> ExecutedCommand: pass

    @_command([SE([LE("spawn"),
                   AE("spawn_target_pos")],
                  [LE("replace entity"),
                   AE("replace_entities"),
                   AE("replace_slot"),
                   AE("replace_count", True)],
                  [LE("replace block"),
                   AE("replace_block_pos"),
                   AE("replace_slot"),
                   AE("replace_count", True)],
                  [LE("give"),
                   AE("give_players")],
                  [LE("insert"),
                   AE("insert_target_pos")]),
               SE([LE("fish"),
                   AE("fish_loot_table"),
                   AE("fish_pos"),
                   AE("fish_tool", True)],
                  [LE("loot"),
                   AE("loot_loot_table")],
                  [LE("kill"),
                   AE("kill_target")],
                  [LE("mine"),
                   AE("mine_pos"),
                   AE("mine_tool", True)])])
    @_version(introduced="18w45a") # TODO /drop
    def loot(self, *,
             spawn_target_pos: Coord | None = None,
             replace_entities: _JavaTarget | None = None,
             replace_block_pos: BlockCoord | None = None,
             replace_slot: Annotated[str, NoSpace] | None = None,
             replace_count: Annotated[int, Range(0, Int.max)] | None = None,
             give_players: _JavaPlayerTarget | None = None,
             insert_target_pos: BlockCoord | None = None,
             fish_loot_table: ResourceLocation | None = None, # TODO LootTable
             fish_pos: BlockCoord | None = None,
             fish_tool: str | Literal['mainhand', 'offhand'] | None = None,
             loot_loot_table: ResourceLocation | None = None, # TODO LootTable,
             kill_target: _JavaSingleTarget | None = None,
             mine_pos: BlockCoord | None = None,
             mine_tool: str | Literal['mainhand', 'offhand'] | None = None) -> ExecutedCommand: pass

    @_command([AE("message")])
    def me(self, message: str) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("message")])
    @_version(introduced="1.0.16_02")
    def msg(self, targets: _JavaPlayerTarget, message: str) -> ExecutedCommand: pass
    w = tell = msg

    @_command([AE("targets")])
    @_version(introduced="1.0.16")
    def op(self, targets: Annotated[str, PlayerName] | Annotated[JavaSelector, Player]) -> ExecutedCommand: pass

    @_command([AE("targets")])
    @_version(introduced="1.0.16")
    def pardon(self, targets: Annotated[str, PlayerName] | Annotated[JavaSelector, Player]) -> ExecutedCommand: pass

    @_command([AE("target")], cmd_name="pardon-ip")
    @_version(introduced="1.0.16")
    def pardon_ip(self, target: _JavaObjectiveName) -> ExecutedCommand: pass

    @_command([AE("name"),
               AE("pos", True),
               SE([AE("delta"),
                   AE("speed"),
                   AE("count"),
                   AE("display_mode", True),
                   AE("viewers", True)],
                  optional=True)
               ])
    @_version(introduced="14w04a")
    def particle(self, name: str | ResourceLocation, # TODO Particle class
                 pos: Coord | None = None,
                 delta: Coord | None = None,
                 speed: Annotated[float,
                                  Range(0, 340_282_356_779_733_661_637_539_395_458_142_568_447.9)] | None = None,
                 count: Annotated[int, Range(0, Int.max)] | None = None,
                 display_mode: Literal['force', 'normal'] = 'normal',
                 viewers: _JavaPlayerTarget | None = None) -> ExecutedCommand: pass

    @_command([AE("action")])
    @_version(introduced="1.17pre1")
    def perf(self, action: Literal['start', 'stop']) -> ExecutedCommand: pass

    @_command([AE("feature"), AE("pos")])
    @_version(introduced="22w03a")
    def placefeature(self, feature: ResourceLocation, pos: BlockCoord) -> ExecutedCommand: pass

    @_command([AE("sound"),
               AE("source"),
               AE("targets"),
               AE("position", True),
               AE("volume", True),
               AE("pitch", True),
               AE("minimum_volume", True)])
    @_version(introduced="1.6.1pre")
    def playsound(self, sound: ResourceLocation,
                  source: Literal['master', 'music', 'record', 'weather', 'block',
                                  'hostile', 'neutral', 'player', 'ambient', 'voice'],
                  targets: _JavaPlayerTarget | None = None,
                  position: Coord | None = None,
                  volume: float = 1.0,
                  pitch: float = 1.0,
                  minimum_volume: float = 0.0) -> ExecutedCommand: pass

    @_command([AE("port")])
    @_version(introduced="12w24a")
    def publish(self, port: Annotated[int, Range(0, 65536)] | None = None) -> ExecutedCommand: pass

    @_command([AE("action"),
               AE("targets"),
               AE("recipe")])
    @_version(introduced="17w13a")
    def recipe(self, action: Literal['give', 'take'],
               targets: _JavaPlayerTarget,
               recipe: ResourceLocation | Literal['*']) -> ExecutedCommand: pass # TODO Recipe class

    @_command([])
    @_version(introduced="17w18a")
    def reload(self) -> ExecutedCommand: pass

    @_command([], cmd_name="save-all", segment_name="save-all")
    @_version(introduced="a1.0.16_01")
    def save_all(self) -> ExecutedCommand: pass

    @_command([], cmd_name="save-all", segment_name="save-all flush")
    @_version(introduced="a1.0.16_01")
    def save_all_flush(self) -> ExecutedCommand: pass

    @_command([], cmd_name="save-off", segment_name="save-off")
    @_version(introduced="a1.0.16_01")
    def save_off(self) -> ExecutedCommand:
        pass

    @_command([], cmd_name="save-on", segment_name="save-on")
    @_version(introduced="a1.0.16_01")
    def save_on(self) -> ExecutedCommand: pass

    @_command([AE("message")])
    @_version(introduced="0.0.16a_01")
    def say(self, message: str) -> ExecutedCommand: pass

    @_command([AE("function"), AE("time"), AE("action", True)])
    @_version(introduced="18w43a") # TODO old syntax? idk
    def schedule_function(self, function: ResourceLocation, # TODO Function
                          time: int | float | Annotated[str, Regex(r"^\d+(?:\.\d+)?[dst]?$")],
                          action: Literal['append', 'replace'] = 'replace') -> ExecutedCommand: pass

    @_command([AE("function")])
    @_version(introduced="18w43a")
    def schedule_clear(self, function: ResourceLocation) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="13w04a")
    def scoreboard_objectives_list(self) -> ExecutedCommand: pass

    @_command([AE("objective"), AE("criteria"), AE("display_name")])
    @_version(introduced="13w04a")
    def scoreboard_objectives_add(self, objective: _JavaObjectiveName,
                                  criteria: str,
                                  display_name: RawJson | None = None) -> ExecutedCommand: pass

    @_command([AE("objective")])
    @_version(introduced="13w04a")
    def scoreboard_objectives_remove(self, objective: _JavaObjectiveName) -> ExecutedCommand: pass

    @_command([AE("slot"), AE("objective", True)])
    @_version(introduced="13w04a")
    def scoreboard_objective_setdisplay(self, slot: Literal['list', 'sidebar', 'belowname'],
                                        objective: _JavaObjectiveName | None = None) -> ExecutedCommand: pass

    @_command([AE("objective"),
               SE([LE("displayname"), AE("display_name")],
                  [LE("rendertype"), AE("render_type")])
               ])
    @_version(introduced="1.13pre7")
    def scoreboard_objectives_modify(self, objective: _JavaObjectiveName,
                                     display_name: RawJson | None = None,
                                     render_type: Literal['hearts', 'integer'] | None = None) -> ExecutedCommand: pass

    @_command([AE("target", True)])
    @_version(introduced="13w04a")
    def scoreboard_players_list(self, target: _JavaTarget | None = None) -> ExecutedCommand: pass

    @_command([AE("target"), AE("objective")])
    @_version(introduced="13w04a")
    def scoreboard_players_get(self, target: _JavaSingleTarget,
                               objective: _JavaObjectiveName) -> ExecutedCommand: pass

    @_command([AE("target"), AE("objective"), AE("score")])
    @_version(introduced="13w04a")
    def scoreboard_players_set(self, target: _JavaTarget | Literal['*'],
                               objective: _JavaObjectiveName,
                               score: int) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective"), AE("score")])
    @_version(introduced="13w04a")
    def scoreboard_players_add(self, targets: _JavaTarget | Literal['*'],
                               objective: _JavaObjectiveName,
                               score: Annotated[int, Range(0, Int.max)]) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective"), AE("score")])
    @_version(introduced="13w04a")
    def scoreboard_players_remove(self, targets: _JavaTarget | Literal['*'],
                                  objective: _JavaObjectiveName,
                                  score: Annotated[int, Range(0, Int.max)]) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective", True)])
    @_version(introduced="13w04a")
    def scoreboard_players_reset(self, targets: _JavaTarget | Literal['*'],
                                 objective: _JavaObjectiveName | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("objective")])
    @_version(introduced="")
    def scoreboard_players_enable(self, targets: _JavaTarget | Literal['*'],
                                  objective: _JavaObjectiveName) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("target_objective"), AE("operation"), AE("source"), AE("source_objective")])
    @_version(introduced="13w04a")
    def scoreboard_players_operation(self, targets: _JavaTarget | Literal['*'],
                                     target_objective: _JavaObjectiveName,
                                     operation: Literal['=', '+=', '-=', '*=', '/=', '%=', '><', '<', '>'],
                                     source: _JavaTarget | Literal['*'],
                                     source_objective: _JavaObjectiveName) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="12w21a")
    def seed(self) -> ExecutedCommand: pass

    @_command([AE("pos"),
               AE("block"),
               AE("change_mode", True)])
    @_version(introduced="13w37a")
    def setblock(self, pos: BlockCoord,
                 block: str,
                 change_mode: Literal['destroy', 'keep', 'replace'] = 'replace') -> ExecutedCommand: pass

    @_command([AE("minutes")])
    @_version(introduced="13w38a")
    def setidletimeout(self, minutes: Annotated[int, Range(0, Int.max)]) -> ExecutedCommand: pass

    @_command([AE("spawn_point", True), AE("angle", True)])
    @_version(introduced='13w43a')
    def setworldspawn(self, spawn_point: Coord = Coord.at_executor(),
                      angle: Rotation | None = None) -> ExecutedCommand: pass

    @_command([AE("targets", True), AE("pos", True), AE("angle", True)])
    @_version(introduced="12w32a")
    def spawnpoint(self, targets: _JavaPlayerTarget = JavaSelector.s(),
                   pos: Coord = Coord.at_executor(),
                   angle: Rotation | None = None) -> ExecutedCommand: pass

    @_command([AE("target", True), AE("player", True)])
    @_version(introduced="19w41a")
    def spectate(self, target: _JavaSingleTarget | None = None,
                 player: _JavaSinglePlayerTarget = JavaSelector.s()) -> ExecutedCommand: pass

    @_command([AE("center"),
               AE("spread_distance"),
               AE("max_range"),
               SE([LE("under"),
                   AE("max_height")],
                  optional=True),
               AE("respect_teams"),
               AE("targets")])
    @_version(introduced="13w23a")
    def spreadplayers(self, *,
                      center: Coord2d,
                      spread_distance: Annotated[float, Range(0.0, Float.max)],
                      max_range: Annotated[float, Range(1.0, Float.max)],
                      max_height: Annotated[float, Range(1.0, Float.max)] | None = None,
                      respect_teams: bool,
                      targets: _JavaTarget) -> ExecutedCommand: pass

    @_command([])
    @_version(introduced="a1.0.16")
    def stop(self) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("source", True), AE("sound", True)])
    @_version(introduced="1.9.3pre2")
    def stopsound(self, targets: _JavaPlayerTarget,
                  source: Literal['master', 'music', 'record', 'weather', 'block',
                                  'hostile', 'neutral', 'player', 'ambient', 'voice', '*'] | None = None,
                  sound: ResourceLocation | None = None) -> ExecutedCommand: pass

    @_command([AE("entity"), AE("pos", True), AE("nbt", True)])
    @_version(introduced="13w36a")
    def summon(self, entity: str,
               pos: Coord = Coord.at_executor(),
               nbt: Compound | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
               SE([AE("action", options=['add', 'remove']),
                   AE("name")],
                  [AE("action", options=['list'])])])
    @_version(introduced="17w45a")
    def tag(self, targets: _JavaTarget,
            action: Literal['add', 'remove', 'list'],
            name: Annotated[str, Regex(r"^%[-+.\w]+$")]) -> ExecutedCommand: pass

    @_command([SE([AE("action", options=['list']),
                   AE("team", True)],
                  [AE("action", options=['add']),
                   AE("team"),
                   AE("display_name", True)],
                  [AE("action", options=['remove', 'empty'])],
                  [AE("action", options=['join']),
                   AE("team"),
                   AE("members", True)],
                  [AE("action", options=['leave']),
                   AE("members")],
                  [AE("action", options=['modify']),
                   AE("team"),
                   AE("option"),
                   AE("value")])
               ])
    @_version(introduced="17w45a")
    def team(self, action: Literal['list', 'add', 'remove', 'empty', 'join', 'leave', 'modify'],
             team: Annotated[str, Regex(r"^(?=.{1,16}$)[-+.\w]+$")] | None = None,
             display_name: RawJson | None = None,
             members: _JavaTarget | Literal['*'] | None = None,
             option: Literal['displayName', 'color', 'friendlyFire', 'seeFriendlyInvisibles', 'nameTagVisibility',
                             'deathMessageVisibility', 'collisionRule', 'prefix', 'suffix'] | None = None,
             value: RawJson | Literal['never', 'hideForOwnTeam', 'hideForOtherTeams', 'always'] |
             Literal['always', 'never', 'pushOtherTeams', 'pushOwnTeam'] | None = None) -> ExecutedCommand: pass

    @_command([AE("message")])
    @_version(introduced="19w02a")
    def teammsg(self, message: str) -> ExecutedCommand: pass
    tm = teammsg

    @_command([SE([AE("destination")],
                  [AE("location")],
                  [AE("targets"),
                   SE([AE("destination")],
                      [AE("location"),
                       SE([AE("rotation")],
                          [LE("facing"),
                           AE("facing_location")],
                          [LE("facing entity"),
                           AE("facing_entity"),
                           AE("facing_anchor", True)],
                          optional=True)
                       ])
                   ])
               ])
    @_version(introduced="1.10.pre1") # TODO `tp` alias consideration for pre1.13?
    def teleport(self, *,
                 targets: _JavaTarget = JavaSelector.s(),
                 destination: _JavaSingleTarget | None = None,
                 location: Coord | None = None,
                 rotation: Rotation | None = None,
                 facing_location: Coord | None = None,
                 facing_entity: _JavaTarget | None = None,
                 facing_anchor: Literal['eyes', 'feet'] | None = None) -> ExecutedCommand: pass
    tp = teleport

    @_command([AE("targets"), AE("message")])
    @_version(introduced="13w37a")
    def tellraw(self, targets: _JavaPlayerTarget,
                message: RawJson) -> ExecutedCommand: pass

    @_command([SE([LE("add"),
                   AE("add")],
                  [LE("query"),
                   AE("query")],
                  [LE("set"),
                   AE("set_")])])
    @_version(introduced="b1.3")
    def time(self, *,
             add: int | float | Annotated[str, Regex(r"^\d+(?:\.\d+)?[dst]?$")] | None = None,
             query: Literal['daytime', 'gametime', 'day'] | None = None,
             set_: Literal['day', 'night', 'noon', 'midnight', 'sunrise', 'sunset'] |
             int | float | Annotated[str, Regex(r"^\d+(?:\.\d+)?[dst]?$")] | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"),
               SE([AE("action", options=['clear', 'reset'])],
                  [AE("action", options=['title', 'subtitle', 'actionbar']),
                   AE("title")],
                  [AE("action", options=['times']),
                   AE("fade_in"),
                   AE("stay"),
                   AE("fade_out")])
               ])
    @_version(introduced="14w20a")
    def title(self, targets: _JavaPlayerTarget,
              action: Literal['clear', 'reset', 'title', 'subtitle', 'actionbar', 'times'],
              title: RawJson | None = None,
              fade_in: int | None = None,
              stay: int | None = None,
              fade_out: int | None = None) -> ExecutedCommand: pass

    @_command([AE("objective"),
               AE("action", True),
               AE("value", True)])
    @_version(introduced="14w06a")
    def trigger(self, objective: _JavaObjectiveName,
                action: Literal['add', 'set'] | None = None,
                value: int | None = None) -> ExecutedCommand: pass

    @_command([], cmd_name='warden_spawn_tracker', segment_name='warden_spawn_tracker clear')
    @_version(introduced="1.19ddes1")
    def warden_spawn_tracker_clear(self) -> ExecutedCommand: pass

    @_command([AE("warning_level")], cmd_name='warden_spawn_tracker', segment_name='warden_spawn_tracker set')
    @_version(introduced="1.19ddes1")
    def warden_spawn_tracker_set(self, warning_level: int) -> ExecutedCommand: pass

    @_command([AE("weather"), AE("duration", True)])
    @_version(introduced="12w32a")
    def weather(self, weather: Literal['clear', 'rain', 'thunder'],
                duration: Annotated[int, Range(0, 1999999999)] = 300) -> ExecutedCommand: pass

    @_command([SE([AE("action", options=['add', 'remove']),
                   AE("targets")],
                  [AE("action", options=['list', 'off', 'on', 'reload'])])
               ])
    @_version(introduced="b1.3")
    def whitelist(self, action: Literal['add', 'remove', 'list', 'off', 'on', 'reload'],
                  targets: _JavaPlayerTarget | None = None) -> ExecutedCommand: pass

    @_command([SE([LE("add"),
                   AE("add_distance"),
                   AE("add_time", True)],
                  [LE("center"),
                   AE("center_pos")],
                  [LE("damage amount"),
                   AE("damage_per_block")],
                  [LE("damage buffer"),
                   AE("damage_buffer_distance")],
                  [LE("get")],
                  [LE("set"),
                   AE("set_distance"),
                   AE("set_time", True)],
                  [LE("warning distance"),
                   AE("warning_distance")],
                  [LE("warning time"),
                   AE("warning_time")])
               ])
    @_version(introduced="14w17a")
    def worldborder(self, *,
                    add_distance: float | None = None,
                    add_time: Annotated[int, Range(0, Int.max)] | None = None,
                    center_pos: Coord2d | None = None,
                    damage_per_block: Annotated[float, Range(0, Float.max)] | None = None,
                    damage_buffer_distance: float | None = None,
                    set_distance: float | None = None,
                    set_time: Annotated[int, Range(0, Int.max)] | None = None,
                    warning_distance: Annotated[int, Range(0, Int.max)] | None = None,
                    warning_time: Annotated[int, Range(0, Int.max)] | None = None) -> ExecutedCommand: pass

    @_command([AE("targets"), AE("amount"), AE("unit", True)])
    @_version(introduced="b1.9pre5")
    def xp_add(self, targets: _JavaPlayerTarget,
               amount: int,
               unit: Literal['levels', 'points'] | None = None) -> ExecutedCommand: pass
    experience_add = xp_add

    @_command([AE("targets"), AE("amount"), AE("unit", True)])
    @_version(introduced="b1.9pre5")
    def xp_set(self, targets: _JavaPlayerTarget,
               amount: Annotated[int, Range(0, Int.max)],
               unit: Literal['levels', 'points'] | None = None) -> ExecutedCommand: pass
    experience_set = xp_set

    @_command([AE("targets"), AE("unit")])
    @_version(introduced="b1.5pre5")
    def xp_query(self, targets: _JavaPlayerTarget,
                 unit: Literal['levels', 'points']) -> ExecutedCommand: pass
    experience_query = xp_query


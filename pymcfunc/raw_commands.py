from __future__ import annotations

import warnings
from functools import wraps
from typing import Optional, Any, Callable, Tuple, TYPE_CHECKING, Annotated, Literal
from uuid import UUID

from pymcfunc.advancements import Advancement
from pymcfunc.command import ExecutedCommand, Command, SE, AE, Range, NoSpace, Element, Player, Regex, \
    PlayerName, LE, _JavaPlayerTarget, _JavaSingleTarget, ResourceLocation, RawJson, _BedrockSinglePlayerTarget, \
    _BedrockPlayerTarget, _BedrockTarget, _BedrockSingleTarget, Quoted
from pymcfunc.coord import BlockCoord
from pymcfunc.errors import FutureCommandWarning, DeprecatedCommandWarning, EducationEditionWarning
from pymcfunc.internal import base_class
from pymcfunc.nbt import Int, Path, Compound, NBT
from pymcfunc.selectors import BedrockSelector, JavaSelector
from pymcfunc.version import JavaVersion, BedrockVersion

if TYPE_CHECKING:
    from pymcfunc.func_handler import BaseFunctionHandler


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

    @command([
        SE([AE("command")],
           [AE("page", True)])
    ])
    @version(introduced="0.16.0b1")
    def help_(self,
              command: Annotated[str, NoSpace] | None = None,
              page: Annotated[int, Range(Int.min, Int.max)] | None = None) -> ExecutedCommand: pass

    @command([
        AE("target"),
        AE("ability", True),
        AE("value", True)
    ])
    @education_edition
    @version(introduced="0.16.0b1")
    def ability(self, target: _BedrockSinglePlayerTarget,
                ability: Literal["worldbuilder", "mayfly", "mute"] | None = None,
                value: bool | None = None) -> ExecutedCommand: pass

    @command([AE("lock", True)])
    @version(introduced="1.2.0")
    def alwaysday(self, lock: bool) -> ExecutedCommand: pass
    daylock = alwaysday

    @command([
        AE("target"),
        AE("intensity", True),
        AE("seconds", True),
        AE("shake_type", True)
    ])
    @version(introduced="1.16.100.57")
    def camerashake_add(self, target: _BedrockPlayerTarget = BedrockSelector.s(), *,
                        intensity: Annotated[float, Range(0, 4)] | None = None,
                        seconds: float | None = None,
                        shake_type: Literal["positional", "rotational"] | None = None) -> ExecutedCommand: pass

    @command([AE("target")])
    @version(introduced="1.16.210.54")
    def camerashake_stop(self, target: _BedrockPlayerTarget = BedrockSelector.s()) -> ExecutedCommand:
        pass

    @command([AE("value")],
             segment_name="changesetting allow-cheats")
    def changesetting_allow_cheats(self, value: bool) -> ExecutedCommand: pass

    @command([AE("value")])
    def changesetting_difficulty(self, value: Literal['peaceful', 'easy', 'normal', 'hard',
                                                      'p', 'e', 'n', 'h', 0, 1, 2, 3]) -> ExecutedCommand: pass

    @command([AE("targets", True),
              AE("item", True),
              AE("max_count", True)])
    @version(introduced="1.0.5.0")
    def clear(self, targets: _BedrockPlayerTarget = BedrockSelector.s(),
              item: str | None = None,
              max_count: Annotated[int, Range(-1, Int.max)] = -1) -> ExecutedCommand: pass

    @command([AE("player", True)])
    @version(introduced="1.16.100.57")
    def clearspawnpoint(self, player: _BedrockPlayerTarget = BedrockSelector.s()) -> ExecutedCommand: pass

    @command([AE("begin"),
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
    @version(introduced="0.16.0b1")
    def clone(self, begin: BlockCoord,
              end: BlockCoord,
              destination: BlockCoord, *,
              mask_mode: Literal['replace', 'masked', 'filtered'] = 'replace',
              clone_mode: Literal['force', 'move', 'normal'] = 'normal',
              tile_name: str | None = None,
              tile_data: Annotated[int, Range(-1, 65535)] | None = None,
              block_states: dict | None = None) -> ExecutedCommand: pass # TODO special handling for BlockStates syntax

    @command([AE("server_uri")])
    @version(introduced="v0.16.0b1")
    def wsserver(self, server_uri: str) -> ExecutedCommand: pass
    connect = wsserver

    @command([])
    @version(introduced="v0.16.0b1")
    def wsserver_out(self) -> ExecutedCommand: pass
    connect_out = wsserver_out

    @command([AE("target"),
              AE("amount"),
              AE("cause", True),
              SE([LE("entity"),
                  AE("damager")],
                 optional=True)])
    @version(introduced="1.18.10.26")
    def damage(self, target: _BedrockTarget,
               amount: Annotated[int, Range(Int.min, Int.max)],
               cause: Literal['all', 'anvil', 'block-explosion', 'charging', 'contact', 'drowning', 'enemy-attack',
                              'enemy-explosion', 'fall', 'falling-block', 'fire', 'fire-tick'],
               damager: _BedrockSingleTarget) -> ExecutedCommand: pass


class JavaRawCommands(BaseRawCommands):
    """
    A container for raw Minecraft commands that are specially for Java Edition.

    .. warning::
       Do not instantiate JavaRawCommands directly; use a :py:class:`JavaFunctionHandler` and access the commands via the ‘r’ attribute.
    """
    @staticmethod
    def command(order: list[Element], cmd_name: str | None = None, segment_name: str | None = None):
        def decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                return Command.command(self.fh, order, cmd_name, segment_name)(func)(*args, **kwargs)

            return wrapper

        return decorator

    def __getattribute__(self, item: str):
        res = super().__getattribute__(item)
        if 'cmd_info' in dir(res):
            return Command.command(self.fh, *res.cmd_info)(res)
        return res

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

    @command([AE("command", True)])
    #@version(introduced="12w17a")
    def help_(self, command: str) -> ExecutedCommand: pass

    @command([
        AE("targets"),
        SE([AE("mode", options=["everything"])],
           [AE("mode", options=["only"]),
            AE("advancement"),
            AE("criterion", True)],
           [AE("mode", options=["from", "through", "until"]),
            AE("advancement")])
    ], cmd_name="advancement")
    @version(introduced="17w13a")
    def advancement_grant(self, targets: _JavaPlayerTarget,
                          mode: Literal["everything", "only", "from", "through", "until"],
                          advancement: Advancement | None = None,
                          criterion: str | None = None) -> ExecutedCommand: pass

    @command([
        AE("targets"),
        SE([AE("mode", options=["everything"])],
           [AE("mode", options=["only"]),
            AE("advancement"),
            AE("criterion", True)],
           [AE("mode", options=["from", "through", "until"]),
            AE("advancement")])
    ], cmd_name="advancement")
    @version(introduced="17w13a")
    def advancement_revoke(self, targets: _JavaPlayerTarget,
                           mode: Literal["everything", "only", "from", "through", "until"],
                           advancement: Advancement | None = None,
                           criterion: str | None = None) -> ExecutedCommand: pass

    @command([
        AE("target"),
        AE("attribute"),
        LE("get"),
        AE("scale", True)
    ], segment_name="attribute")
    @version(introduced="20w17a")
    def attribute_get_total(self, target: _JavaSingleTarget,
                            attribute: ResourceLocation,
                            scale: float | None = None) -> ExecutedCommand: pass

    @command([
        AE("target"),
        AE("attribute"),
        LE("base"),
        SE([AE("mode", options=["get"]),
            AE("scale", True)],
           [AE("mode", options=["set"]),
            AE("value")])
    ], segment_name="attribute")
    @version(introduced="20w17a")
    def attribute_base(self, target: _JavaSingleTarget,
                       attribute: ResourceLocation,
                       mode: Literal["get", "set"],
                       scale: float | None = None,
                       value: float | None = None) -> ExecutedCommand: pass

    @command([
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
    @version(introduced="20w17a")
    def attribute_modifier(self, target: _JavaSingleTarget,
                           attribute: ResourceLocation,
                           mode: Literal["add", "remove", "value get"], *,
                           uuid: UUID | None = None,
                           name: Annotated[str, Regex(r"^[\w.+-]*$")] | None = None,
                           value: float | None = None,
                           add_mode: Literal["add", "multiply", "multiply_base"] | None = None,
                           scale: float | None = None) -> ExecutedCommand: pass

    @command([
        AE("targets"),
        AE("message", True)
    ])
    @version(introduced="a1.0.16")
    def ban(self, targets: Annotated[str, PlayerName] | Annotated[JavaSelector, Player],
            message: str = "Banned by an operator.") -> ExecutedCommand: pass

    @command([
        AE("targets"),
        AE("message", True)
    ], cmd_name="ban-ip")
    @version(introduced="a1.0.16")
    def ban_ip(self, targets: Annotated[str, Regex(r"^[\w.+-]*$")] | Annotated[JavaSelector, Player],
               message: str = "Banned by an operator.") -> ExecutedCommand: pass

    @command([AE("view", True)])
    @version(introduced="a1.0.16")
    def banlist(self, view: Literal["ips", "players"] | None = None) -> ExecutedCommand: pass

    @command([
        AE("id_"),
        AE("name")
    ])
    @version(introduced="18w05a")
    def bossbar_add(self, id_: ResourceLocation, name: RawJson) -> ExecutedCommand: pass

    @command([
        AE("id_"),
        AE("view")
    ])
    @version(introduced="18w05a")
    def bossbar_get(self, id_: ResourceLocation,
                    view: Literal["max", "players", "value", "visible"]) -> ExecutedCommand: pass

    @command([])
    @version(introduced="18w05a")
    def bossbar_list(self, id_: ResourceLocation) -> ExecutedCommand: pass

    @command([
        AE("id_")
    ])
    @version(introduced="18w05a")
    def bossbar_remove(self, id_: ResourceLocation) -> ExecutedCommand: pass

    @command([
        AE("id_"),
        SE([LE("colour"), AE("colour")],
           [LE("max_"), AE("max_")],
           [LE("name"), AE("name")],
           [LE("players"), AE("players", True)],
           [LE("style"), AE("style")],
           [LE("value"), AE("value")],
           [LE("visible"), AE("visible")])
    ])
    @version(introduced="18w05a")
    def bossbar_set(self, id_: ResourceLocation, *,
                    colour: Literal["blue", "green", "pink", "purple", "red", "white", "yellow"] | None = None,
                    max_: Annotated[int, Range(1, Int.max)] | None = None,
                    name: str | RawJson | None = None,
                    players: _JavaPlayerTarget | None = None,
                    style: Literal["notched_6", "notched_10", "notched_12", "notched_20", "progress"] | None = None,
                    value: Annotated[int, Range(0, Int.max)] | None = None,
                    visible: bool | None = None) -> ExecutedCommand: pass

    @command([AE("player", True),
              AE("item_name", True),
              AE("data", True),
              AE("max_count", True)])
    @version(introduced="17w45a") # TODO old format
    def clear(self, player: _JavaPlayerTarget = JavaSelector.s(),
              item_name: str | None = None,
              data: Annotated[int, Range(-1, Int.max)] = -1,
              max_count: Annotated[int, Range(0, Int.max)] = -1) -> ExecutedCommand: pass

    @command([AE("begin"),
              AE("end"),
              AE("destination"),
              SE([AE("mask_mode", True, options=["replace", "masked"]),
                  AE("clone_mode", True, options=["force", "move", "normal"])],
                 [AE("mask_mode", options=["filtered"]),
                  AE("filter_"),
                  AE("clone_mode", True, options=["force", "move", "normal"])
                  ])
              ])
    @version(introduced="14w03a")
    def clone(self, begin: BlockCoord,
              end: BlockCoord,
              destination: BlockCoord, *,
              mask_mode: Literal["replace", "masked", "filtered"] = "replace",
              clone_mode: Literal["force", "move", "normal"] = "normal",
              filter_: str | None = None) -> ExecutedCommand: pass

    @command([SE([LE("block"), AE("block")],
                 [LE("entity"), AE("entity")],
                 [LE("storage"), AE("storage")]),
              AE("path", True),
              AE("scale", True)])
    @version(introduced="17w45b")
    def data_get(self, *,
                 block: BlockCoord | None = None,
                 entity: _JavaSingleTarget | None = None,
                 storage: ResourceLocation | None = None,
                 path: Path | None = None,
                 scale: float | None = None) -> ExecutedCommand: pass

    @command([SE([LE("block"), AE("block")],
                 [LE("entity"), AE("entity")],
                 [LE("storage"), AE("storage")]),
              AE("nbt")])
    @version(introduced="17w45b")
    def data_merge(self, *,
                   block: BlockCoord | None = None,
                   entity: _JavaSingleTarget | None = None,
                   storage: ResourceLocation | None = None,
                   nbt: Compound) -> ExecutedCommand: pass

    @command([SE([LE("block"), AE("target_block")],
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
    @version(introduced="18w43a")
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

    @command([SE([LE("block"), AE("block")],
                 [LE("entity"), AE("entity")],
                 [LE("storage"), AE("storage")]),
              AE("path")])
    @version(introduced="17w45b")
    def data_remove(self, *,
                    block: BlockCoord | None = None,
                    entity: _JavaSingleTarget | None = None,
                    storage: ResourceLocation | None = None,
                    path: ResourceLocation) -> ExecutedCommand: pass

    @command([AE("name")])
    @version(introduced="17w46a")
    def datapack_disable(self, name: Annotated[str, Quoted, Regex(r"^[\w.+-]*$")]) -> ExecutedCommand: pass

    @command([AE("name"),
              SE([AE("priority", options=['first', 'last'])],
                 [AE("priority", options=['before', 'after']),
                  AE("existing")],
                 optional=True)])
    @version(introduced="17w46a")
    def datapack_enable(self, name: Annotated[str, Quoted, Regex(r"^[\w.+-]*$")],
                        priority: Literal['first', 'last', 'before', 'after'] | None = None,
                        existing: Annotated[str, Quoted, Regex(r"^[\w.+-]*$")] | None = None) -> ExecutedCommand: pass

    @command([AE("view", True, options=['available', 'enabled'])])
    @version(introduced="17w46a")
    def datapack_list(self, view: Literal['available', 'enabled'] | None = None) -> ExecutedCommand: pass


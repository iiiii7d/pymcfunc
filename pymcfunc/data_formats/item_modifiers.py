from __future__ import annotations

from typing import Literal, Union, Optional, TYPE_CHECKING
from uuid import UUID

from attr import define, field

from pymcfunc.command import ResourceLocation
from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.internal import base_class
from pymcfunc.data_formats.json_formats import IntRangeJson, NumberProviderRangeJson
from pymcfunc.data_formats.raw_json import JavaRawJson

if TYPE_CHECKING: from pymcfunc.data_formats.loot_tables import Entry
from pymcfunc.data_formats.nbt import Path, Compound
from pymcfunc.data_formats.number_providers import NumberProvider
from pymcfunc.data_formats.predicates import Predicate


@define(init=True)
@base_class
class ItemModifier(JsonFormat):
    function = property(lambda self: "")
    conditions: list[Predicate]

    JSON_FORMAT = {
        'function': str,
        'conditions': list[Predicate]
    }

@define(init=True)
class ApplyBonusItemModifier(ItemModifier):
    function = property(lambda self: "apply_bonus")
    enchantment: str
    formula: Literal['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops']
    parameters: tuple[int, float] | tuple[float] | None = None

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'enchantment': str,
        'formula': Literal['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops'],
        'parameters': Optional[Union[list[int, float], list[float]]]
    }

@define(init=True)
class CopyNameItemModifier(ItemModifier):
    function = property(lambda self: "copy_name")
    source: str = field(init=False, default="block_entity")

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'source': str,
    }

@define(init=True)
class CopyNBTItemModifier(ItemModifier):
    function = property(lambda self: "copy_nbt")
    source: Literal['block_entity', 'this', 'killer', 'killer_player'] | Source
    ops: list[NBTOperation]

    @define(init=True, frozen=True)
    @base_class
    class Source(JsonFormat):
        type: str = field(init=False)

        JSON_FORMAT = {
            'type': str
        }

    @define(init=True, frozen=True)
    class ContextSource(Source):
        type = property(lambda self: "context")
        target: Literal['block_entity', 'this', 'killer', 'killer_player']

        JSON_FORMAT = {
            'type': str,
            'target': Literal['block_entity', 'this', 'killer', 'killer_player']
        }

    @define(init=True, frozen=True)
    class StorageSource(Source):
        type = property(lambda self: "storage")
        source: ResourceLocation

        JSON_FORMAT = {
            'type': str,
            'target': str
        }

    @define(init=True, frozen=True)
    @base_class
    class NBTOperation(JsonFormat):
        source: Path
        target: Path
        op: Literal['replace', 'append', 'merge']

        JSON_FORMAT = {
            'source': str,
            'target': str,
            'op': Literal['copy', 'remove']
        }

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'source': Union[Source, ContextSource, StorageSource],
        'ops': Union[Literal['block_entity', 'this', 'killer', 'killer_player'], Source]
    }

@define(init=True)
class CopyStateItemModifier(ItemModifier):
    function = property(lambda self: "copy_state")
    block: str
    properties: list[str]

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'block': str,
        'properties': list[str]
    }

@define(init=True)
class EnchantRandomlyItemModifier(ItemModifier):
    function = property(lambda self: "enchant_randomly")
    enchantments: list[str]

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'enchantments': list[str]
    }

@define(init=True)
class EnchantWithLevelsItemModifier(ItemModifier):
    function = property(lambda self: "enchant_with_levels")
    treasure: bool
    levels: int | NumberProvider

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'treasure': bool,
        'levels': Union[int, NumberProvider]
    }

@define(init=True)
class ExplorationMapItemModifier(ItemModifier):
    function = property(lambda self: "exploration_map")
    destination: str
    decoration: str
    zoom: int
    search_radius: int = 50
    skip_existing_chunks = True

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'destination': str,
        'decoration': str,
        'zoom': int,
        'search_radius': int,
        'skip_existing_chunks': bool
    }

@define(init=True)
class ExplosionDecayItemModifier(ItemModifier):
    function = property(lambda self: "explosion_decay")

@define(init=True)
class FurnaceSmeltItemModifier(ItemModifier):
    function = property(lambda self: "furnace_smelt")

@define(init=True)
class FillPlayerHeadItemModifier(ItemModifier):
    function = property(lambda self: "fill_player_head")
    entity: Literal['this', 'killer', 'killer_player']

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'entity': Literal['this', 'killer', 'killer_player']
    }

@define(init=True)
class LimitCountItemModifier(ItemModifier):
    function = property(lambda self: "limit_count")
    limit: int | NumberProvider | IntRangeJson | NumberProviderRangeJson

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'limit': Union[int, NumberProvider, IntRangeJson, NumberProviderRangeJson]
    }

@define(init=True)
class LootingEnchantItemModifier(ItemModifier):
    function = property(lambda self: "looting_enchant")
    count: int | NumberProvider
    limit: int

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'count': Union[int, NumberProvider],
        'limit': int
    }

@define(init=True)
class SetAttributesItemModifier(ItemModifier):
    function = property(lambda self: "set_attributes")
    modifiers: list[Modifier]

    @define(init=True)
    class Modifier(JsonFormat):
        name: str
        attribute: str
        operation: Literal['addition', 'multiply_base', 'multiply_total']
        amount: float | NumberProvider
        id: UUID
        slot: Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet'] |\
            list[Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet']]

        JSON_FORMAT = {
            'name': str,
            'attribute': str,
            'operation': Literal['addition', 'multiply_base', 'multiply_total'],
            'amount': Union[float, NumberProvider],
            'id': str,
            'slot': Union[Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet'],
                          list[Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet']]]
        }

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'modifiers': list[Modifier]
    }

@define(init=True)
class SetBannerPatternItemModifier(ItemModifier):
    function = property(lambda self: "set_banner_pattern")
    patterns: list[Pattern]

    @define(init=True)
    class Pattern(JsonFormat):
        color: Literal['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray',
                       'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']
        pattern: str

        JSON_FORMAT = {
            'name': str,
            'color': Literal['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray',
                             'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'],
            'pattern': str,
        }

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'patterns': list[Pattern]
    }

@define(init=True)
class SetContentsItemModifier(ItemModifier):
    function = property(lambda self: "set_contents")
    entries: list[Entry]
    type: str

    @property
    def JSON_FORMAT(self):
        from pymcfunc.data_formats.loot_tables import Entry
        return {
            **ItemModifier.JSON_FORMAT,
            'entries': list[Entry],
            'type': str
        }

@define(init=True)
class SetDamageItemModifier(ItemModifier):
    function = property(lambda self: "set_damage")
    damage: float | NumberProvider
    add: bool

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'damage': Union[float, NumberProvider],
        'add': bool
    }

@define(init=True)
class SetEnchantmentsItemModifier(ItemModifier):
    function = property(lambda self: "set_enchantments")
    enchantments: dict[str, int | NumberProvider]
    add: bool

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'enchantments': dict[str, Union[int, NumberProvider]],
        'add': bool
    }

@define(init=True)
class SetLootTableItemModifier(ItemModifier):
    function = property(lambda self: "set_loot_table")
    name: str
    type: str
    seed: int | None = None

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'name': str,
        'seed': Optional[int],
        'type': str
    }

@define(init=True)
class SetLoreItemModifier(ItemModifier):
    function = property(lambda self: "set_lore")
    lore: list[str | JavaRawJson]
    entity: Literal['this', 'killer', 'killer_player']
    replace: bool

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'lore': list[Union[str, JavaRawJson]],
        'entity': Literal['this', 'killer', 'killer_player'],
        'replace': bool
    }

@define(init=True)
class SetNameItemModifier(ItemModifier):
    function = property(lambda self: "set_name")
    name: str | JavaRawJson
    entity: Literal['this', 'killer', 'killer_player']

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'name': Union[str, JavaRawJson],
        'entity': Literal['this', 'killer', 'killer_player']
    }

@define(init=True)
class SetNBTItemModifier(ItemModifier):
    function = property(lambda self: "set_nbt")
    nbt: Compound

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'nbt': str
    }

@define(init=True)
class SetPotionItemModifier(ItemModifier):
    function = property(lambda self: "set_potion")
    id: str

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'id': str
    }

@define(init=True)
class SetStewEffectItemModifier(ItemModifier):
    function = property(lambda self: "set_stew_effect")
    effects: list[Effect]

    @define(init=True, frozen=True)
    class Effect(JsonFormat):
        type: str
        duration: int | NumberProvider

        JSON_FORMAT = {
            'type': str,
            'duration': Union[int, NumberProvider]
        }

    JSON_FORMAT = {
        **ItemModifier.JSON_FORMAT,
        'effects': list[Effect]
    }

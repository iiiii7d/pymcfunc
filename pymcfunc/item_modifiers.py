from __future__ import annotations

from typing import Literal, Union, Optional, TYPE_CHECKING
from uuid import UUID

from attr import define, field

from pymcfunc.command import ResourceLocation
from pymcfunc.internal import base_class
from pymcfunc.json_format import IntRangeJson, NumberProviderRangeJson
from pymcfunc.rawjson import JavaRawJson

if TYPE_CHECKING: from pymcfunc.loot_tables import Entry
from pymcfunc.nbt import NBTFormat, List, String, Path, Int, Boolean, Float, Compound
from pymcfunc.number_providers import NumberProvider
from pymcfunc.predicates import Predicate


@define(init=True)
@base_class
class ItemModifier(NBTFormat):
    function = property(lambda self: "")
    conditions: list[Predicate]

    NBT_FORMAT = {
        'function': String,
        'conditions': List[Predicate]
    }

@define(init=True)
class ApplyBonusItemModifier(ItemModifier):
    function = property(lambda self: "apply_bonus")
    enchantment: str
    formula: Literal['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops']
    parameters: tuple[int, float] | tuple[float] | None = None

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'enchantment': String,
        'formula': Literal['binomial_with_bonus_count', 'uniform_bonus_count', 'ore_drops'],
        'parameters': Optional[Union[List[int, float], List[float]]]
    }

@define(init=True)
class CopyNameItemModifier(ItemModifier):
    function = property(lambda self: "copy_name")
    source: str = field(init=False, default="block_entity")

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'source': String,
    }

@define(init=True)
class CopyNBTItemModifier(ItemModifier):
    function = property(lambda self: "copy_nbt")
    source: Literal['block_entity', 'this', 'killer', 'killer_player'] | Source
    ops: list[NBTOperation]

    @define(init=True, frozen=True)
    @base_class
    class Source(NBTFormat):
        type: str = field(init=False)

        NBT_FORMAT = {
            'type': String
        }

    @define(init=True, frozen=True)
    class ContextSource(Source):
        type = property(lambda self: "context")
        target: Literal['block_entity', 'this', 'killer', 'killer_player']

        NBT_FORMAT = {
            'type': String,
            'target': Literal['block_entity', 'this', 'killer', 'killer_player']
        }

    @define(init=True, frozen=True)
    class StorageSource(Source):
        type = property(lambda self: "storage")
        source: ResourceLocation

        NBT_FORMAT = {
            'type': String,
            'target': String
        }

    @define(init=True, frozen=True)
    @base_class
    class NBTOperation(NBTFormat):
        source: Path
        target: Path
        op: Literal['replace', 'append', 'merge']

        NBT_FORMAT = {
            'source': String,
            'target': String,
            'op': Literal['copy', 'remove']
        }

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'source': Union[Source, ContextSource, StorageSource],
        'ops': Union[Literal['block_entity', 'this', 'killer', 'killer_player'], Source]
    }

@define(init=True)
class CopyStateItemModifier(ItemModifier):
    function = property(lambda self: "copy_state")
    block: str
    properties: list[str]

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'block': String,
        'properties': List[String]
    }

@define(init=True)
class EnchantRandomlyItemModifier(ItemModifier):
    function = property(lambda self: "enchant_randomly")
    enchantments: list[str]

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'enchantments': List[String]
    }

@define(init=True)
class EnchantWithLevelsItemModifier(ItemModifier):
    function = property(lambda self: "enchant_with_levels")
    treasure: bool
    levels: int | NumberProvider

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'treasure': Boolean,
        'levels': Union[Int, NumberProvider]
    }

@define(init=True)
class ExplorationMapItemModifier(ItemModifier):
    function = property(lambda self: "exploration_map")
    destination: str
    decoration: str
    zoom: int
    search_radius: int = 50
    skip_existing_chunks = True

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'destination': String,
        'decoration': String,
        'zoom': Int,
        'search_radius': Int,
        'skip_existing_chunks': Boolean
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

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'entity': Literal['this', 'killer', 'killer_player']
    }

@define(init=True)
class LimitCountItemModifier(ItemModifier):
    function = property(lambda self: "limit_count")
    limit: int | NumberProvider | IntRangeJson | NumberProviderRangeJson

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'limit': Union[Int, NumberProvider, IntRangeJson, NumberProviderRangeJson]
    }

@define(init=True)
class LootingEnchantItemModifier(ItemModifier):
    function = property(lambda self: "looting_enchant")
    count: int | NumberProvider
    limit: int

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'count': Union[Int, NumberProvider],
        'limit': Int
    }

@define(init=True)
class SetAttributesItemModifier(ItemModifier):
    function = property(lambda self: "set_attributes")
    modifiers: list[Modifier]

    @define(init=True)
    class Modifier(NBTFormat):
        name: str
        attribute: str
        operation: Literal['addition', 'multiply_base', 'multiply_total']
        amount: Float | NumberProvider
        id: UUID
        slot: Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet'] |\
            list[Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet']]

        NBT_FORMAT = {
            'name': String,
            'attribute': String,
            'operation': Literal['addition', 'multiply_base', 'multiply_total'],
            'amount': Union[Float, NumberProvider],
            'id': String,
            'slot': Union[Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet'],
                          List[Literal['mainhand', 'offhand', 'head', 'chest', 'legs', 'feet']]]
        }

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'modifiers': List[Modifier]
    }

@define(init=True)
class SetBannerPatternItemModifier(ItemModifier):
    function = property(lambda self: "set_banner_pattern")
    patterns: list[Pattern]

    @define(init=True)
    class Pattern(NBTFormat):
        color: Literal['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray',
                       'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']
        pattern: String

        NBT_FORMAT = {
            'name': String,
            'color': Literal['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray',
                             'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'],
            'pattern': String,
        }

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'patterns': List[Pattern]
    }

@define(init=True)
class SetContentsItemModifier(ItemModifier):
    function = property(lambda self: "set_contents")
    entries: list[Entry]
    type: str

    @property
    def NBT_FORMAT(self):
        from pymcfunc.loot_tables import Entry
        return {
            **ItemModifier.NBT_FORMAT,
            'entries': List[Entry],
            'type': String
        }

@define(init=True)
class SetDamageItemModifier(ItemModifier):
    function = property(lambda self: "set_damage")
    damage: float | NumberProvider
    add: bool

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'damage': Union[Float, NumberProvider],
        'add': Boolean
    }

@define(init=True)
class SetEnchantmentsItemModifier(ItemModifier):
    function = property(lambda self: "set_enchantments")
    enchantments: dict[str, int | NumberProvider]
    add: bool

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'enchantments': dict[String, Union[Int, NumberProvider]],
        'add': Boolean
    }

@define(init=True)
class SetLootTableItemModifier(ItemModifier):
    function = property(lambda self: "set_loot_table")
    name: str
    type: str
    seed: int | None = None

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'name': String,
        'seed': Optional[Int],
        'type': String
    }

@define(init=True)
class SetLoreItemModifier(ItemModifier):
    function = property(lambda self: "set_lore")
    lore: list[str | JavaRawJson]
    entity: Literal['this', 'killer', 'killer_player']
    replace: bool

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'lore': List[Union[String, JavaRawJson]],
        'entity': Literal['this', 'killer', 'killer_player'],
        'replace': Boolean
    }

@define(init=True)
class SetNameItemModifier(ItemModifier):
    function = property(lambda self: "set_name")
    name: str | JavaRawJson
    entity: Literal['this', 'killer', 'killer_player']

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'name': Union[String, JavaRawJson],
        'entity': Literal['this', 'killer', 'killer_player']
    }

@define(init=True)
class SetNBTItemModifier(ItemModifier):
    function = property(lambda self: "set_nbt")
    nbt: Compound

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'nbt': String
    }

@define(init=True)
class SetPotionItemModifier(ItemModifier):
    function = property(lambda self: "set_potion")
    id: str

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'id': String
    }

@define(init=True)
class SetStewEffectItemModifier(ItemModifier):
    function = property(lambda self: "set_stew_effect")
    effects: list[Effect]

    @define(init=True, frozen=True)
    class Effect(NBTFormat):
        type: str
        duration: int | NumberProvider

        NBT_FORMAT = {
            'type': String,
            'duration': Union[Int, NumberProvider]
        }

    NBT_FORMAT = {
        **ItemModifier.NBT_FORMAT,
        'effects': List[Effect]
    }

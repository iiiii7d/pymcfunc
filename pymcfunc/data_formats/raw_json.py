from __future__ import annotations

from typing import Literal, Optional, Union
from typing_extensions import Self
from uuid import UUID

from attr import field, define

from pymcfunc.command import ResourceLocation
from pymcfunc.data_formats.base_formats import JsonFormat
from pymcfunc.data_formats.coord import Coord
from pymcfunc.data_formats.nbt_path import Path
from pymcfunc.internal import base_class
from pymcfunc.proxies.selectors import JavaSelector, BedrockSelector


class JavaRawJson:
    def __init__(self, *components: int | float | str | bool | list[JavaTextComponent] | JavaTextComponent):
        self.components = [comp if isinstance(comp, JavaTextComponent)
                           else JavaPlainTextComponent(text='true' if comp else 'false') if isinstance(comp, bool)
                           else JavaPlainTextComponent(text=comp) for comp in components]

    def __str__(self):
        pass

    # TODO make JsonFormat
JRawJson = JavaRawJson

@base_class
@define(kw_only=True, init=True)
class JavaTextComponent(JavaRawJson, JsonFormat):
    extra: list[JavaRawJson] = field(default=list)
    color: Literal["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray",
                   "dark_gray", "blue", "green", "aqua", "red", "light_purple", "yellow", "white",
                   "reset"] | str | None = None
    font: ResourceLocation | None = None
    bold: bool | None = None
    italic: bool | None = None
    underlined: bool | None = None
    strikethrough: bool | None = None
    obfuscated: bool | None = None

    insertion: str | None = None
    click_event: ClickEvent | None = None
    hover_event: HoverEvent | None = None

    @property
    def clickEvent(self): return self.click_event
    @property
    def hoverEvent(self): return self.hover_event

    def format(self, *,
               color: Literal["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple",
                              "gold", "gray", "dark_gray", "blue", "green", "aqua", "red", "light_purple",
                              "yellow", "white", "reset"] | None = None,
               bold: bool | None = None,
               italic: bool | None = None,
               underlined: bool | None = None,
               strikethrough: bool | None = None,
               obfuscated: bool | None = None) -> Self:
        if color: self.color = color
        if bold: self.bold = bold
        if italic: self.italic = italic
        if underlined: self.underlined = underlined
        if strikethrough: self.strikethrough = strikethrough
        if obfuscated: self.obfuscated = obfuscated
        return self

    def f(self, formats: str) -> Self:
        colour_map = {
            '0': 'black',
            '1': 'dark_blue',
            '2': 'dark_green',
            '3': 'dark_aqua',
            '4': 'dark_red',
            '5': 'dark_purple',
            '6': 'gold',
            '7': 'gray',
            '8': 'dark_gray',
            '9': 'blue',
            'a': 'green',
            'b': 'aqua',
            'c': 'red',
            'd': 'light_purple',
            'e': 'yellow',
            'f': 'white',
        }
        fmt = {}
        for fmt_char in formats:
            if fmt_char in colour_map:
                fmt['color'] = colour_map[fmt_char]
            elif fmt_char == 'l':
                fmt['bold'] = True
            elif fmt_char == 'o':
                fmt['italic'] = True
            elif fmt_char == 'n':
                fmt['underlined'] = True
            elif fmt_char == 'm':
                fmt['strikethrough'] = True
            elif fmt_char == 'k':
                fmt['obfuscated'] = True
            else:
                raise ValueError(f'Unknown format character: {fmt_char}')
        return self.format(**fmt)

    def insert(self, text: str) -> Self:
        self.insertion = text
        return self

    def on_click(self, ce: ClickEvent) -> Self:
        self.click_event = ce
        return self

    def on_hover(self, he: HoverEvent) -> Self:
        self.hover_event = he
        return self

    def set_font(self, font: ResourceLocation) -> Self:
        self.font = font
        return self

    @base_class
    @define(kw_only=True, init=True)
    class ClickEvent(JsonFormat):
        action: str = property(lambda self: "")
        value: str

        JSON_FORMAT = {
            "action": str,
            "value": str
        }

    @define(kw_only=True, init=True)
    class OpenUrlClickEvent(ClickEvent):
        action: str = property(lambda self: "open_url")
    OpenUrl = OpenUrlClickEvent

    @define(kw_only=True, init=True)
    class OpenFileClickEvent(ClickEvent):
        action: str = property(lambda self: "open_file")
    OpenFile = OpenFileClickEvent

    @define(kw_only=True, init=True)
    class RunCommandClickEvent(ClickEvent):
        action: str = property(lambda self: "run_command")
    RunCommand = RunCommandClickEvent

    @define(kw_only=True, init=True)
    class SuggestCommandClickEvent(ClickEvent):
        action: str = property(lambda self: "suggest_command")
    SuggestCommand = SuggestCommandClickEvent

    @define(kw_only=True, init=True)
    class ChangePageClickEvent(ClickEvent):
        action: str = property(lambda self: "change_page")
    ChangePage = ChangePageClickEvent

    @define(kw_only=True, init=True)
    class CopyToClipboardClickEvent(ClickEvent):
        action: str = property(lambda self: "copy_to_clipboard")
    CopyToClipboard = CopyToClipboardClickEvent

    @base_class
    @define(kw_only=True, init=True)
    class HoverEvent(JsonFormat):
        action: str = property(lambda self: "")

        JSON_FORMAT = {
            "action": str
        }

    @define(kw_only=True, init=True)
    class ShowTextHoverEvent(HoverEvent):
        action: str = property(lambda self: "show_text")
        contents: JavaRawJson

        JSON_FORMAT = {
            "action": str,
            "contents": JavaRawJson
        }
    ShowText = ShowTextHoverEvent

    @define(kw_only=True, init=True)
    class ShowItemHoverEvent(HoverEvent):
        action: str = property(lambda self: "show_item")
        contents: Item

        @define(kw_only=True, init=True)
        class Item(JsonFormat):
            id: str
            count: int | None = None
            tag: str | None = None

            JSON_FORMAT = {
                "id": str,
                "count": int,
                "tag": str
            }

        JSON_FORMAT = {
            "action": str,
            "contents": Item
        }
    ShowItem = ShowItemHoverEvent

    @define(kw_only=True, init=True)
    class ShowEntityHoverEvent(HoverEvent):
        action: str = property(lambda self: "show_entity")
        contents: Entity

        @define(kw_only=True, init=True)
        class Entity(JsonFormat):
            type: str
            id: UUID
            name: JavaRawJson | None = None

            JSON_FORMAT = {
                "type": str,
                "id": UUID,
                "name": JavaRawJson
            }

        JSON_FORMAT = {
            "action": str,
            "contents": Entity
        }
    ShowEntity = ShowEntityHoverEvent

    JSON_FORMAT = {
        "extra": list[JavaRawJson],
        "color": Optional[
            Union[Literal["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray",
                          "dark_gray", "blue", "green", "aqua", "red", "light_purple", "yellow", "white",
                          "reset"], str]],
        "font": Optional[ResourceLocation],
        "bold": Optional[bool],
        "italic": Optional[bool],
        "underlined": Optional[bool],
        "strikethrough": Optional[bool],
        "obfuscated": Optional[bool],
        "insertion": Optional[str],
        "clickEvent": Optional[ClickEvent],
        "hoverEvent": Optional[HoverEvent]
    }
JComp = JavaTextComponent

@define(kw_only=True, init=True)
class JavaPlainTextComponent(JavaTextComponent):
    text: str

    JSON_FORMAT = {
        **JavaTextComponent.JSON_FORMAT,
        "text": str
    }

JPlainText = JavaPlainTextComponent

@define(kw_only=True, init=True)
class JavaTranslatedTextComponent(JavaTextComponent):
    translate: str
    with_: Optional[list[JavaTextComponent]]

    JSON_FORMAT = {
        **JavaTextComponent.JSON_FORMAT,
        "translate": str,
        "with": Optional[list[JavaTextComponent]]
    }
JTranslatedText = JavaTranslatedTextComponent

@define(kw_only=True, init=True)
class JavaScoreboardValueComponent(JavaTextComponent):
    score: Score

    @define(kw_only=True, init=True)
    class Score(JsonFormat):
        objective: str
        name: JavaSelector | Literal['*']
        value: str | None = None

        JSON_FORMAT = {
            **JavaTextComponent.JSON_FORMAT,
            "objective": str,
            "name": str,
            "value": str
        }

    JSON_FORMAT = {
        **JavaTextComponent.JSON_FORMAT,
        "score": Score,
    }
JScoreboardValue = JavaScoreboardValueComponent

@define(kw_only=True, init=True)
class JavaEntityNamesComponent(JavaTextComponent):
    selector: JavaSelector
    separator: JavaTextComponent | None = None

    JSON_FORMAT = {
        **JavaTextComponent.JSON_FORMAT,
        "selector": JavaSelector,
        "separator": JavaTextComponent
    }
JEntityNames = JavaEntityNamesComponent

@define(kw_only=True, init=True)
class JavaKeybindComponent(JavaTextComponent):
    key: str

    JSON_FORMAT = {
        **JavaTextComponent.JSON_FORMAT,
        "key": str
    }
JKeybind = JavaKeybindComponent

# TODO CommandStorage maybe?
@define(kw_only=True, init=True)
class JavaNBTValuesComponent(JavaTextComponent):
    nbt: Path
    interpret: bool | None = None
    separator: JavaTextComponent | None = None
    block: Coord | None = None
    entity: JavaSelector | None = None
    storage: ResourceLocation | None = None

    JSON_FORMAT = {
        **JavaTextComponent.JSON_FORMAT,
        "nbt": str,
        "interpret": Optional[bool],
        "separator": JavaTextComponent,
        "block": str,
        "entity": str,
        "storage": str
    }
JNBTValues = JavaNBTValuesComponent

class BedrockRawJson:
    def __init__(self, *components: BedrockTextComponent):
        self.components = components

    def __str__(self):
        pass
BRawJson = BedrockRawJson

@define(kw_only=True, init=True)
@base_class
class BedrockTextComponent(JsonFormat):
    pass
BComp = BedrockTextComponent

@define(kw_only=True, init=True)
class BedrockPlainTextComponent(BedrockTextComponent):
    text: str

    JSON_FORMAT = {
        "text": str
    }
BPlainText = BedrockPlainTextComponent

@define(kw_only=True, init=True)
class BedrockTranslatedTextComponent(BedrockTextComponent):
    translate: str
    with_: Optional[list[BedrockTextComponent]]

    JSON_FORMAT = {
        "translate": str,
        "with": Optional[list[BedrockTextComponent]]
    }
BTranslatedText = BedrockTranslatedTextComponent

@define(kw_only=True, init=True)
class BedrockScoreboardValueComponent(BedrockTextComponent):
    score: Score

    @define(kw_only=True, init=True)
    class Score(JsonFormat):
        objective: str
        name: BedrockSelector | Literal['*']
        value: str | None = None

        JSON_FORMAT = {
            "objective": str,
            "name": str,
            "value": str
        }

    JSON_FORMAT = {
        "score": Score,
    }
BScoreboardValue = BedrockScoreboardValueComponent

@define(kw_only=True, init=True)
class BedrockEntityNamesComponent(BedrockTextComponent):
    selector: BedrockSelector

    JSON_FORMAT = {
        "selector": BedrockSelector
    }
BEntityNames = BedrockEntityNamesComponent
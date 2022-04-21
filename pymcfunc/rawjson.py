from __future__ import annotations

from typing import Literal, Optional, Union, Self
from uuid import UUID

from attr import define, field

from pymcfunc.command import ResourceLocation
from pymcfunc.coord import Coord
from pymcfunc.internal import base_class
from pymcfunc.nbt import NBTFormat, String, Int, List, Path, Boolean
from pymcfunc.selectors import JavaSelector, BedrockSelector


class JavaRawJson:
    def __init__(self, *components: int | float | str | bool | list[JavaTextComponent] | JavaTextComponent):
        self.components = [comp if isinstance(comp, JavaTextComponent)
                           else JavaPlainTextComponent('true' if comp else 'false') if isinstance(comp, bool)
                           else JavaPlainTextComponent(comp) for comp in components]

    def __str__(self):
        pass
JRawJson = JavaRawJson
    
@define(init=True)
@base_class
class JavaTextComponent(JavaRawJson, NBTFormat):
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
               colour: Literal["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple",
                               "gold", "gray", "dark_gray", "blue", "green", "aqua", "red", "light_purple",
                               "yellow", "white", "reset"] | None = None,
               bold: bool | None = None,
               italic: bool | None = None,
               underlined: bool | None = None,
               strikethrough: bool | None = None,
               obfuscated: bool | None = None) -> Self:
        if colour: self.color = colour
        if bold: self.bold = bold
        if italic: self.italic = italic
        if underlined: self.underlined = underlined
        if strikethrough: self.strikethrough = strikethrough
        if obfuscated: self.obfuscated = obfuscated
        return self
    def f(self, *,
          c: Literal["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple",
                     "gold", "gray", "dark_gray", "blue", "green", "aqua", "red", "light_purple",
                     "yellow", "white", "reset"] | None = None,
          l: bool | None = None,
          o: bool | None = None,
          n: bool | None = None,
          m: bool | None = None,
          k: bool | None = None) -> Self:
        return self.format(colour=c, bold=l, italic=o, underlined=n, strikethrough=m, obfuscated=k)

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

    @define(init=True)
    @base_class
    class ClickEvent(NBTFormat):
        action: str = property(lambda self: "")
        value: str

        NBT_FORMAT = {
            "action": String,
            "value": String
        }

    @define(init=True)
    class OpenUrlClickEvent(ClickEvent):
        action: str = property(lambda self: "open_url")
    OpenUrl = OpenUrlClickEvent

    @define(init=True)
    class OpenFileClickEvent(ClickEvent):
        action: str = property(lambda self: "open_file")
    OpenFile = OpenFileClickEvent

    @define(init=True)
    class RunCommandClickEvent(ClickEvent):
        action: str = property(lambda self: "run_command")
    RunCommand = RunCommandClickEvent

    @define(init=True)
    class SuggestCommandClickEvent(ClickEvent):
        action: str = property(lambda self: "suggest_command")
    SuggestCommand = SuggestCommandClickEvent

    @define(init=True)
    class ChangePageClickEvent(ClickEvent):
        action: str = property(lambda self: "change_page")
    ChangePage = ChangePageClickEvent

    @define(init=True)
    class CopyToClipboardClickEvent(ClickEvent):
        action: str = property(lambda self: "copy_to_clipboard")
    CopyToClipboard = CopyToClipboardClickEvent

    @define(init=True)
    @base_class
    class HoverEvent(NBTFormat):
        action: str = property(lambda self: "")

        NBT_FORMAT = {
            "action": String
        }

    @define(init=True)
    class ShowTextHoverEvent(HoverEvent):
        action: str = property(lambda self: "show_text")
        contents: JavaRawJson

        NBT_FORMAT = {
            "action": String,
            "contents": JavaRawJson
        }
    ShowText = ShowTextHoverEvent

    @define(init=True)
    class ShowItemHoverEvent(HoverEvent):
        action: str = property(lambda self: "show_item")
        contents: Item

        @define(init=True)
        class Item(NBTFormat):
            id: str
            count: int | None = None
            tag: str | None = None

            NBT_FORMAT = {
                "id": String,
                "count": Int,
                "tag": String
            }

        NBT_FORMAT = {
            "action": String,
            "contents": Item
        }
    ShowItem = ShowItemHoverEvent

    @define(init=True)
    class ShowEntityHoverEvent(HoverEvent):
        action: str = property(lambda self: "show_entity")
        contents: Entity

        @define(init=True)
        class Entity(NBTFormat):
            type: str
            id: UUID
            name: JavaRawJson | None = None

            NBT_FORMAT = {
                "type": String,
                "id": UUID,
                "name": JavaRawJson
            }

        NBT_FORMAT = {
            "action": String,
            "contents": Entity
        }
    ShowEntity = ShowEntityHoverEvent

    NBT_FORMAT = {
        "extra": List[JavaRawJson],
        "color": Optional[
            Union[Literal["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray",
                          "dark_gray", "blue", "green", "aqua", "red", "light_purple", "yellow", "white",
                          "reset"], String]],
        "font": Optional[ResourceLocation],
        "bold": Optional[Boolean],
        "italic": Optional[Boolean],
        "underlined": Optional[Boolean],
        "strikethrough": Optional[Boolean],
        "obfuscated": Optional[Boolean],
        "insertion": Optional[String],
        "clickEvent": Optional[ClickEvent],
        "hoverEvent": Optional[HoverEvent]
    }
JComp = JavaTextComponent

@define(init=True)
class JavaPlainTextComponent(JavaTextComponent):
    text: str

    NBT_FORMAT = {
        **JavaTextComponent.NBT_FORMAT,
        "text": String
    }

JPlainText = JavaPlainTextComponent

@define(init=True)
class JavaTranslatedTextComponent(JavaTextComponent):
    translate: str
    with_: Optional[List[JavaTextComponent]]

    NBT_FORMAT = {
        **JavaTextComponent.NBT_FORMAT,
        "translate": String,
        "with": Optional[List[JavaTextComponent]]
    }
JTranslatedText = JavaTranslatedTextComponent

@define(init=True)
class JavaScoreboardValueComponent(JavaTextComponent):
    score: Score

    @define(init=True)
    class Score(NBTFormat):
        objective: str
        name: JavaSelector | Literal['*']
        value: str | None = None

        NBT_FORMAT = {
            **JavaTextComponent.NBT_FORMAT,
            "objective": String,
            "name": String,
            "value": String
        }

    NBT_FORMAT = {
        **JavaTextComponent.NBT_FORMAT,
        "score": Score,
    }
JScoreboardValue = JavaScoreboardValueComponent

@define(init=True)
class JavaEntityNamesComponent(JavaTextComponent):
    selector: JavaSelector
    separator: JavaTextComponent | None = None

    NBT_FORMAT = {
        **JavaTextComponent.NBT_FORMAT,
        "selector": JavaSelector,
        "separator": JavaTextComponent
    }
JEntityNames = JavaEntityNamesComponent

@define(init=True)
class JavaKeybindComponent(JavaTextComponent):
    key: str

    NBT_FORMAT = {
        **JavaTextComponent.NBT_FORMAT,
        "key": String
    }
JKeybind = JavaKeybindComponent

# TODO CommandStorage maybe?
@define(init=True)
class JavaNBTValuesComponent(JavaTextComponent):
    nbt: Path
    interpret: bool | None = None
    separator: JavaTextComponent | None = None
    block: Coord | None = None
    entity: JavaSelector | None = None
    storage: ResourceLocation | None = None

    NBT_FORMAT = {
        **JavaTextComponent.NBT_FORMAT,
        "nbt": String,
        "interpret": Optional[Boolean],
        "separator": JavaTextComponent,
        "block": String,
        "entity": String,
        "storage": String
    }
JNBTValues = JavaNBTValuesComponent

class BedrockRawJson:
    def __init__(self, *components: BedrockTextComponent):
        self.components = components

    def __str__(self):
        pass
BRawJson = BedrockRawJson

@define(init=True)
@base_class
class BedrockTextComponent(NBTFormat):
    pass
BComp = BedrockTextComponent

@define(init=True)
class BedrockPlainTextComponent(BedrockTextComponent):
    text: str

    NBT_FORMAT = {
        "text": String
    }
BPlainText = BedrockPlainTextComponent

@define(init=True)
class BedrockTranslatedTextComponent(BedrockTextComponent):
    translate: str
    with_: Optional[List[BedrockTextComponent]]

    NBT_FORMAT = {
        "translate": String,
        "with": Optional[List[BedrockTextComponent]]
    }
BTranslatedText = BedrockTranslatedTextComponent

@define(init=True)
class BedrockScoreboardValueComponent(BedrockTextComponent):
    score: Score

    @define(init=True)
    class Score(NBTFormat):
        objective: str
        name: BedrockSelector | Literal['*']
        value: str | None = None

        NBT_FORMAT = {
            "objective": String,
            "name": String,
            "value": String
        }

    NBT_FORMAT = {
        "score": Score,
    }
BScoreboardValue = BedrockScoreboardValueComponent

@define(init=True)
class BedrockEntityNamesComponent(BedrockTextComponent):
    selector: BedrockSelector

    NBT_FORMAT = {
        "selector": BedrockSelector
    }
BEntityNames = BedrockEntityNamesComponent
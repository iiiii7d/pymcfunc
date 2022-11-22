from __future__ import annotations

from typing import Annotated

from pkmc.nbt import Byte, Case, String, TypedCompound


class Item(TypedCompound):
    count: Annotated[Byte, Case.PASCAL]
    id: String | None
    slot: Byte | None

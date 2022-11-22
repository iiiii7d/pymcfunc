from typing import Annotated

from pkmc.nbt import Case, Compound, String, TypedCompound


class BlockState(TypedCompound):
    name: Annotated[String, Case.PASCAL]
    properties: Annotated[Compound[String], Case.PASCAL]

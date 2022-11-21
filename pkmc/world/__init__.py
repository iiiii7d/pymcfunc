from __future__ import annotations

from pathlib import Path
from uuid import UUID

from attr import define
from beartype import beartype

from pkmc.dimensions import Dimension
from pkmc.world.raids import RaidFile


@beartype
@define
class World:
    path: Path

    def advancements(self, player: UUID) -> None:
        pass

    def raids(self, dimension: Dimension) -> RaidFile:
        path = (
            self.path
            / {
                Dimension.OVERWORLD: "data/raids.dat",
                Dimension.NETHER: "DIM-1/data/raids.dat",
                Dimension.END: "DIM1/data/raids_end.dat",
            }[dimension]
        )
        return RaidFile.parse_file(path)

    def datapacks(self) -> None:
        pass

    def entities(self) -> None:
        pass

    def level_dat(self, old: bool = False) -> None:
        pass

    def player_data(self, player: UUID, old: bool = False) -> None:
        pass

    def poi(self) -> None:
        pass

    def region(self) -> None:
        pass

    def stats(self, player: UUID) -> None:
        pass

    @property
    def name(self) -> str:
        return self.path.name

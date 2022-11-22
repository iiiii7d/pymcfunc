from enum import Enum
from typing import TypeVar

from pkmc._type_utils import Generic
from pkmc.nbt import Compound, TypedCompound

T = TypeVar("T")


class B(Generic[T]):
    pass


def main():
    a = B[int]
    b = B[str]
    print(a.T())


if __name__ == "__main__":
    main()

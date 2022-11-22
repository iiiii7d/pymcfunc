from enum import Enum
from typing import TypeVar

from pkmc._type_utils import Generic
from pkmc.nbt import Compound, TypedCompound

T = TypeVar("T")


class A(TypedCompound, Generic[T]):
    a: T | None


class B(TypedCompound):
    e: Compound
    pass


def main():
    print(T.__dict__)


if __name__ == "__main__":
    main()

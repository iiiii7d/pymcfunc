from __future__ import annotations

from typing import (
    Annotated,
    Any,
    Final,
    Generic,
    MutableMapping,
    MutableSequence,
    Type,
    TypeVar,
    get_args,
)

from beartype import beartype
from beartype.vale import Is
from nbt.nbt import (
    NBTFile,
    TAG_Byte,
    TAG_Byte_Array,
    TAG_Compound,
    TAG_Double,
    TAG_Float,
    TAG_Int,
    TAG_List,
    TAG_Long,
    TAG_Short,
    TAG_String,
)


class Tag:
    pass


@beartype
class Byte(Tag, TAG_Byte):
    MIN: Final = -128
    MAX: Final = 127
    RANGE: Final = Annotated[int, Is[lambda x: Byte.MIN <= x <= Byte.MAX]]

    def __init__(
        self, value: RANGE | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(value, name, buffer)


@beartype
class Short(Tag, TAG_Short):
    MIN: Final = -65536
    MAX: Final = 65535
    RANGE: Final = Annotated[int, Is[lambda x: Short.MIN <= x <= Short.MAX]]

    def __init__(
        self, value: RANGE | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(value, name, buffer)


@beartype
class Int(Tag, TAG_Int):
    MIN: Final = -2147483648
    MAX: Final = 2147483647
    RANGE: Final = Annotated[int, Is[lambda x: Int.MIN <= x <= Int.MAX]]

    def __init__(
        self, value: RANGE | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(value, name, buffer)


@beartype
class Long(Tag, TAG_Long):
    MIN: Final = -9223372036854775808
    MAX: Final = 9223372036854775807
    RANGE: Final = Annotated[int, Is[lambda x: Long.MIN <= x <= Long.MAX]]

    def __init__(
        self, value: RANGE | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(value, name, buffer)


@beartype
class Float(Tag, TAG_Float):
    RANGE: Final = float

    def __init__(
        self, value: RANGE | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(value, name, buffer)


@beartype
class Double(Tag, TAG_Double):
    RANGE: Final = float

    def __init__(
        self, value: RANGE | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(value, name, buffer)


@beartype
class ByteArray(Tag, TAG_Byte_Array, MutableSequence[int]):
    RANGE: Final = Annotated[int, Is[lambda x: 0 <= x <= 255]]

    def __init__(self, name: str | None = None, buffer=None):
        super().__init__(name, buffer)

    def insert(self, key: str, value: Byte.RANGE):
        super().insert(key, value)

    def append(self, value: Byte.RANGE):
        super().append(value)


@beartype
class String(Tag, TAG_String):
    def __init__(self, value: str | None = None, name: str | None = None, buffer=None):
        super().__init__(value, name, buffer)


_T1 = TypeVar("_T1", bound=Tag)


@beartype
class List(Tag, TAG_List, Generic[_T1], MutableSequence[_T1]):
    @property
    def ele_type(self) -> Type[_T1] | None:
        # noinspection PyUnresolvedReferences
        try:
            return get_args(self.__orig_class__)[0]
        except IndexError:
            return None

    def __init__(
        self, value: list[_T1] | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(self.ele_type, value, name, buffer)


@beartype
class Compound(Tag, TAG_Compound, MutableMapping[str, Tag]):
    def __init__(self, name: str | None = None, buffer=None):
        super().__init__(name, buffer)

    pass


@beartype
class File(Compound, NBTFile):
    pass


_T2 = TypeVar("_T2", bound=Compound)


@beartype
class TypedCompound(Generic[_T2]):
    @classmethod
    def fields(cls) -> dict[str, Type[Tag]]:
        for c in cls.__mro__:
            fields = {}
            if issubclass(c, TypedCompound):
                c: Type[TypedCompound]
                fields.update(c.__annotations__)
        return fields

    __slots__ = ("val",)

    def __init__(self, val: _T2):
        self.val = val

    def __getitem__(self, item: str) -> Tag:
        return self.val[item]

    def __setitem__(self, key: str, value: Tag):
        self.val[key] = value

    def __delitem__(self, key: str):
        del self.val[key]

    def __getattr__(self, item: str) -> Tag | Any:
        if item in self.fields():
            return self[item]
        super().__getattribute__(item)

    def __setattr__(self, key: str, value: Tag | Any):
        if key in self.fields():
            self[key] = value
        super().__setattr__(key, value)

    def __delattr__(self, item: str):
        if item in self.fields():
            del self[item]
        super().__delattr__(item)

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import (
    Annotated,
    Any,
    Final,
    Generic,
    Literal,
    MutableMapping,
    MutableSequence,
    Optional,
    Type,
    TypeVar,
    get_args,
)

from beartype import beartype
from beartype.door import is_bearable
from beartype.vale import Is
from nbt.nbt import (
    TAG,
    NBTFile,
    TAG_Byte,
    TAG_Byte_Array,
    TAG_Compound,
    TAG_Double,
    TAG_Float,
    TAG_Int,
    TAG_Int_Array,
    TAG_List,
    TAG_Long,
    TAG_Long_Array,
    TAG_Short,
    TAG_String,
)


class Tag:
    @staticmethod
    def from_id(i: str | None) -> Type[Tag] | None:
        if i is None or i == 0:
            return None
        return {
            1: Byte,
            2: Short,
            3: Int,
            4: Long,
            5: Float,
            6: Double,
            7: ByteArray,
            8: String,
            9: List,
            10: Compound,
            11: IntArray,
            12: LongArray,
        }[i]


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

    def insert(self, key: str, value: ByteArray.RANGE):
        super().insert(key, value)

    def append(self, value: ByteArray.RANGE):
        super().append(value)


@beartype
class String(Tag, TAG_String):
    def __init__(self, value: str | None = None, name: str | None = None, buffer=None):
        super().__init__(value, name, buffer)


_T1 = TypeVar("_T1", bound=Optional[Tag])


@beartype
class List(Tag, TAG_List, Generic[_T1], MutableSequence[_T1]):
    @property
    def ele_type(self) -> Type[_T1] | None:
        # noinspection PyUnresolvedReferences
        try:
            return get_args(self.__orig_bases__)[0]
        except IndexError:
            return None

    def __init__(
        self, value: list[_T1] | None = None, name: str | None = None, buffer=None
    ):
        super().__init__(self.ele_type, value, name, buffer)


_T3 = TypeVar("_T3", bound=Tag)


@beartype
class Compound(Tag, TAG_Compound, Generic[_T3], MutableMapping[str, _T3]):
    def __init__(self, name: str | None = None, buffer=None):
        super().__init__(buffer, name)


@beartype
class IntArray(Tag, TAG_Int_Array, MutableSequence[Int.RANGE]):
    def __init__(self, name: str | None = None, buffer=None):
        super().__init__(name, buffer)

    def insert(self, key: str, value: Int.RANGE):
        super().insert(key, value)

    def append(self, value: Int.RANGE):
        super().append(value)


@beartype
class LongArray(Tag, TAG_Long_Array, MutableSequence[Long.RANGE]):
    def __init__(self, name: str | None = None, buffer=None):
        super().__init__(name, buffer)

    def insert(self, key: str, value: Long.RANGE):
        super().insert(key, value)

    def append(self, value: Long.RANGE):
        super().append(value)


@beartype
class File(Compound, NBTFile):
    def __init__(self, filename: Path | None = None, buffer=None, fileobj=None):
        NBTFile.__init__(self, str(filename), buffer, fileobj)

        def transform(tag: TAG) -> Tag:
            if isinstance(tag, TAG_Byte):
                return Byte(tag.value, tag.name)
            if isinstance(tag, TAG_Short):
                return Short(tag.value, tag.name)
            if isinstance(tag, TAG_Int):
                return Int(tag.value, tag.name)
            if isinstance(tag, TAG_Long):
                return Long(tag.value, tag.name)
            if isinstance(tag, TAG_Float):
                return Float(tag.value, tag.name)
            if isinstance(tag, TAG_Double):
                return Double(tag.value, tag.name)
            if isinstance(tag, TAG_Byte_Array):
                new = ByteArray(tag.name)
                new.value = tag.value
                return new
            if isinstance(tag, TAG_String):
                return String(tag.value, tag.name)
            if isinstance(tag, TAG_List):
                id_ = (
                    tag.tagID
                    if tag.tagID is not None and tag.tagID != 0
                    else tag.value[0].id
                    if len(tag) > 0
                    else None
                )
                new = List[Tag.from_id(id_)](tag.value, tag.name)
                new.value = (
                    None if tag.value is None else [transform(t) for t in tag.value]
                )
                return new
            if isinstance(tag, TAG_Compound):
                new = Compound(tag.name)
                new.tags = (
                    None if tag.tags is None else [transform(t) for t in tag.tags]
                )
                return new
            if isinstance(tag, TAG_Int_Array):
                new = IntArray(tag.name)
                new.value = tag.value
                return new
            if isinstance(tag, TAG_Long_Array):
                new = IntArray(tag.name)
                new.value = tag.value
                return new
            raise TypeError(f"Invalid tag {tag}")

        self.tags = None if self.tags is None else [transform(t) for t in self.tags]


_T2 = TypeVar("_T2", bound=Compound)


def raw_attr_name(attr: str, t: Type[Tag]) -> str:
    annos = get_args(t)
    if len(annos) < 2:
        return attr
    anno = annos[1]
    if isinstance(anno, str):
        return anno
    elif isinstance(anno, Case):
        if anno == Case.PASCAL:
            return "".join(x.title() for x in attr.split("_"))
        elif anno == Case.CAMEL:
            return "".join(
                (x.title() if i != 0 else x.lower())
                for i, x in enumerate(attr.split("_"))
            )
        elif anno == Case.UPPER:
            return attr.upper()
        elif anno == Case.NOCASE:
            return attr.replace("_", "")
    else:
        raise ValueError(f"Invalid annotation {anno}")


@beartype
class TypedCompound(Compound):
    def __init__(self, val: Compound):
        for field, ty in type(self).fields().items():
            field = raw_attr_name(field, ty)
            if field not in val.keys() and not is_bearable(None, ty):
                raise KeyError(f"No tag for {field}")
            elif field in val.keys():
                try:
                    field_val = val[field]
                    if issubclass(ty, TypedCompound) and isinstance(
                        field_val, Compound
                    ):
                        val[field] = ty(field_val)
                        continue
                except TypeError:
                    pass
                if not is_bearable(val[field], ty):
                    raise TypeError(
                        f"Invalid type for {field}, expected {ty.__name__} but got {type(val[field]).__name__}"
                    )
        super().__init__(val.name)
        self.tags = val.tags

    @classmethod
    def fields(cls) -> dict[str, Type[Tag]]:
        fields = {}
        for c in cls.__mro__:
            if issubclass(c, TypedCompound):
                c: Type[TypedCompound]
                fields.update(c.__annotations__)
        return fields

    def __getattr__(self, item: str) -> Tag | Any:
        if item in self.fields():
            attribute = raw_attr_name(item, self.fields()[item])
            return self[attribute]
        super().__getattribute__(item)

    def __setattr__(self, key: str, value: Tag | Enum | Any):
        if key in self.fields():
            attribute = raw_attr_name(key, self.fields()[key])
            self[attribute] = value
        if isinstance(value, Enum):
            value = value.value
        super().__setattr__(key, value)

    def __delattr__(self, item: str):
        if item in self.fields():
            attribute = raw_attr_name(item, self.fields()[item])
            del self[attribute]
        super().__delattr__(item)


@beartype
class TypedFile(TypedCompound):
    @classmethod
    def parse_file(cls, file: Path):
        val = File(file)
        return cls(val)

    def write_file(self, path: Path):
        if isinstance(self.val, File):
            self.val.write_file(path)
        else:
            raise TypeError(f"{type(self).__name__} is not an NBT file")


@beartype
class Boolean(Byte):
    def __init__(
        self,
        value: Literal[1, 0, True, False] | None = None,
        name: str | None = None,
        buffer=None,
    ):
        super().__init__(int(value), name, buffer)


class Case(Enum):
    PASCAL = 0
    CAMEL = 1
    UPPER = 2
    NOCASE = 3

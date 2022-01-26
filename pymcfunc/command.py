from __future__ import annotations

import inspect
from types import UnionType, NoneType
from typing import Callable, Any, Union, Type, Literal, Optional, _UnionGenericAlias, TypeVar, _LiteralGenericAlias, \
    get_args

from pymcfunc.raw_commands import ExecutedCommand
from pymcfunc.selectors import UniversalSelector


class Element: pass

class LiteralE(Element):
    content: str
    optional: bool
    def __init__(self, content: str, optional: bool=False):
        self.content = content
        self.optional = optional
LE = LiteralE

class ArgumentE(Element):
    name: str
    type: str
    optional: bool
    default: Any | None
    options: list[Any] | None
    def __init__(self, name: str):
        self.name = name
        self.type = Any
        self.optional = False
        self.default = None
        self.options = None
AE = ArgumentE

class SwitchE(Element):
    branches: tuple[list[Element], ...]
    def __init__(self, *branches: list[Element]):
        self.branches = branches
SE = SwitchE

class _Type:
    def convert(self, instance, varname: str): pass

class _OneTypeParamBase(_Type):
    type_param: type
    def __init__(self, type_param: type):
        self.type_param = type_param
    def __class_getitem__(cls, type_param: type):
        return cls(type_param)

    def __instancecheck__(self, instance):
        return self.__subclasscheck__(type(instance))
    def __subclasscheck__(self, subclass):
        return issubclass(subclass, self.type_param)

    def __eq__(self, other):
        if isinstance(other, type(self)): return self.type_param == other.type_param
        return False
    def __hash__(self):
        return hash(self.type_param)

    def __or__(self, other):
        return Union[self, other]
    def __ror__(self, other):
        return Union[other, self]

    def __repr__(self):
        return f"{type(self).__name__}[{self.type_param!r}]"

    def check(self, instance: type_param | Any, varname: str):
        if not self.__subclasscheck__(type(instance)):
            raise TypeError(f"Value for argument `{varname}` is not of type `{self.type_param.__name__}` (Got `{instance}`)")

    def convert(self, instance: type_param | Any, varname: str) -> type_param:
        self.check(instance, varname)
        return instance

class _OneTypeOneValueParamBase(_OneTypeParamBase):
    value: Any
    def __init__(self, type_param: type, value: Any):
        super().__init__(type_param)
        self.value = value
    def __class_getitem__(cls, i: tuple[type, Any]):
        type_param, value = i
        return cls(type_param, value)

    def __eq__(self, other):
        if isinstance(other, type(self)): return self.type_param == other.type_param and self.value == other.value
        return False
    def __hash__(self):
        return hash((self.type_param, self.value))

    def __repr__(self):
        return f"{type(self).__name__}[{self.type_param!r}, {self.value!r}]"

class Single(_OneTypeParamBase):
    type_param: Type[UniversalSelector]

    def __instancecheck__(self, instance: type_param | Any):
        return self.__subclasscheck__(type(instance)) and instance.singleonly

    def check(self, instance: type_param | Any, varname: str):
        super().check(instance, varname)
        if not instance.singleonly:
            raise ValueError(f"Value for argument `{varname}` selects multiple entities (Got `{instance}`)")

class Player(_OneTypeParamBase):
    type_param: Type[UniversalSelector]

    def __instancecheck__(self, instance: type_param | Any):
        return self.__subclasscheck__(type(instance)) and instance.playeronly

    def check(self, instance: type_param | Any, varname: str):
        super().check(instance, varname)
        if not instance.playeronly:
            raise ValueError(f"Value for argument `{varname}` selects entities too (Got `{instance}`)")


class Range(_OneTypeOneValueParamBase):
    type_param: str
    value: tuple[int | float, int | float]

    def __instancecheck__(self, instance: type_param | Any):
        return self.__subclasscheck__(type(instance)) and self.value[0] <= instance <= self.value[1]

    def check(self, instance: type_param | Any, varname: str):
        super().check(instance, varname)
        if not self.value[0] <= instance <= self.value[1]:
            raise ValueError(f"Value for argument `{varname}` is out of range {self.value[0]} <= x <= {self.value[1]} (Got `{instance}`)")

class QuotedStr(str, _Type):
    def convert(self, instance: str, _: str) -> str:
        return "\""+instance+"\""
class NoSpaceStr(str, _Type):
    def convert(self, instance: str, varname: str):
        if " " in instance:
            raise ValueError(f"Value for argument `{varname}` has spaces (Got `{instance}`)")
        return instance


class Command:
    order: list
    arg_namelist: list[str]
    args: dict[str, Element]
    kwargs: dict[str, Element]
    @classmethod
    def command(cls, order: list):
        def decorator(func: Callable[..., ExecutedCommand]):
            cmd = cls()
            cmd.order = order
            for name, arg in inspect.signature(func).parameters.items():
                if arg.POSITIONAL_OR_KEYWORD or arg.POSITIONAL_ONLY:
                    cmd.arg_namelist.append(name)
            cmd.args, cmd.kwargs = cls._process_order(order, func)
            return cmd
        return decorator

    def __call__(self, *args, **kwargs):
        pass

    _T = TypeVar("_T")
    @staticmethod
    def _check_and_process_arg(annotation: Type[Any],
                               value: _T,
                               varname: str) -> _T:
        if issubclass(type(annotation), _OneTypeParamBase):
            annotation: _OneTypeParamBase
            return annotation.convert(Command._check_and_process_arg(annotation.type_param, value, varname), varname)
        elif issubclass(type(annotation), _Type):
            annotation: _Type
            return annotation.convert(value, varname)
        elif issubclass(type(annotation), _LiteralGenericAlias):
            annotation: _LiteralGenericAlias
            if value not in get_args(annotation):
                raise ValueError(f"Value for argument `{varname} not in {', '.join(get_args(annotation))} (Got `{value}`)`")
            return value
        elif issubclass(type(annotation), (_UnionGenericAlias, UnionType)):
            annotation: _UnionGenericAlias
            try:
                return Command._check_and_process_arg(get_args(annotation)[0], value, varname)
            except Exception:
                return Command._check_and_process_arg(get_args(annotation)[1], value, varname)
        elif issubclass(type(annotation), NoneType):
            if value is not None: raise ValueError(f"Value for argument `{varname}` is not None (Got `{value}`)")
            return None
        else:
            if not issubclass(type(value), type(annotation)):
                raise ValueError(f"Value for argument `{varname}` is not of type `{type(annotation).__name__}` (Got `{value}`)")
            return value

    @staticmethod
    def _process_order(order: list | Element, func: Callable[..., ExecutedCommand]) -> tuple[dict[str, Element], dict[str, Element]]:
        if isinstance(order, list):
            args = {}; kwargs = {}
            for i in order:
                res_args, res_kwargs = Command._process_order(i, func)
                args.update(res_args)
                kwargs.update(res_kwargs)
            return args, kwargs
        elif isinstance(order, LE):
            return {}, {}
        elif isinstance(order, AE):
            arg = inspect.signature(func).parameters[order.name]
            if arg.POSITIONAL_OR_KEYWORD:
                return {order.name: order}, {order.name: order}
            elif arg.POSITIONAL_ONLY:
                return {order.name: order}, {}
            else:
                return {}, {order.name: order}
        elif isinstance(order, SE):
            args = {}; kwargs = {}
            for i in order.branches:
                res_args, res_kwargs = Command._process_order(i, func)
                args.update(res_args)
                kwargs.update(res_kwargs)
            return args, kwargs

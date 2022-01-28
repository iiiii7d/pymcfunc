from __future__ import annotations

import inspect
import re
from types import UnionType, NoneType
# noinspection PyUnresolvedReferences
from typing import Callable, Any, Union, Type, Literal, Optional, _UnionGenericAlias, TypeVar, _LiteralGenericAlias, \
    get_args, Pattern

from pymcfunc.errors import MultipleBranchesSatisfiedError, MissingError, RangeError, OptionError, SpaceError, \
    MissingArgumentError
from pymcfunc.func_handler import UniversalFuncHandler
from pymcfunc.raw_commands import ExecutedCommand, UniversalRawCommands
from pymcfunc.selectors import UniversalSelector


class Element: pass

class LiteralE(Element):
    content: str
    optional: bool
    def __init__(self, content: str):
        self.content = content
        self.optional = False
    def __class_getitem__(cls, name: str):
        ae = cls(name)
        ae.optional = True
        return ae
LE = LiteralE

class ArgumentE(Element):
    annotation: Type[Any] | None
    name: str
    optional: bool
    default: Any | None
    options: list[Any] | None
    def __init__(self, name: str):
        self.name = name
        self.optional = False
        self.default = None
        self.options = None
        self.annotation = None
    def __class_getitem__(cls, name: str):
        ae = cls(name)
        ae.optional = True
        return ae
AE = ArgumentE

class SwitchE(Element):
    branches: tuple[list[Element], ...]
    optional: bool
    def __init__(self, *branches: list[Element]):
        self.branches = branches
        self.optional = False
    def __class_getitem__(cls, *branches: list[Element]):
        ae = cls(*branches)
        ae.optional = True
        return ae
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

class Regex(_OneTypeOneValueParamBase):
    type_param: str
    value: Pattern
    def __instancecheck__(self, instance: type_param | Any):
        return self.__subclasscheck__(type(instance)) and re.search(self.value, instance) is not None

    def check(self, instance: type_param | Any, varname: str):
        super().check(instance, varname)
        if re.search(self.value, instance) is None:
            raise ValueError(f"Value for argument `{varname}` does not match pattern `{self.value}`(Got `{instance}`)")

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
    order: list[Element]
    arg_namelist: list[str]
    eles: dict[str, AE]
    name: str
    func: Callable[[UniversalRawCommands, ...], ExecutedCommand]
    @classmethod
    def command(cls, order: list, cmd_name: str | None = None):
        def decorator(func: Callable[[UniversalRawCommands, ...], ExecutedCommand]):
            cmd = cls()
            cmd.order = order
            cmd.func = func
            cmd.name = cmd_name or func.__name__.split("_")[0]
            for name, arg in inspect.signature(func).parameters.items():
                if name == "self": pass
                if arg.POSITIONAL_OR_KEYWORD or arg.POSITIONAL_ONLY:
                    cmd.arg_namelist.append(name)

                cmd.eles = cls._process_order(order, func)
            return cmd
        return decorator

    def __call__(self, rc: UniversalRawCommands, *args, **kwargs) -> ExecutedCommand:
        fh = rc.fh
        for i, arg in enumerate(args):
            kwargs[self.arg_namelist[i]] = arg

        cmd = ExecutedCommand(fh, self.name, "")
        fh.commands.append(cmd)
        return cmd

    def _process_arglist(self, args: dict[str, Any]):
        command = []
        defaults_queue = []
        prev_element_name = ""
        prev_default_element_name = ""
        for element in self.order:
            if isinstance(element, LE):
                if element.optional:
                    defaults_queue.append(element.content)
                    prev_default_element_name = "`" + element.content + "`"
                else:
                    command.extend(defaults_queue)
                    command.append(element.content)
                    prev_element_name = "`" + element.content + "`"
            elif isinstance(element, AE):
                element = self.eles[element.name]
                element: AE
                value = args[element.name] if element.name in args else element.default

                if not element.optional and value is None:
                    raise MissingArgumentError(element.name)
                if isinstance(value, str) and value == "":
                    raise ValueError(f"Parameter {element.name} is an empty string")

                if isinstance(value, bool): value = "true" if value else "false"
                if element.default == value:
                    if defaults_queue[-1] is None:
                        raise MissingError(prev_default_element_name, element.name)
                    defaults_queue.append(str(value) if value is not None else None)
                    prev_default_element_name = "parameter " + element.name
                else:
                    command.extend(defaults_queue)
                    command.append(str(value))
                    prev_element_name = "parameter " + element.name
            elif isinstance(element, SE):
                exceptions = []
                possible_branches = []
                for branch in element.branches:
                    try:
                        branch_output = Command.command(branch, self.name)(self.func)._process_arglist(args)
                        possible_branches.append((branch, branch_output))
                        # prev_element_name = "parameter "+branch.series[-1].name if isinstance(branch.series[-1], _Parameter) else "`"+str(branch.series[-1])+"`"
                        break
                    except Exception as e:
                        exceptions.append(e)
                else:
                    if not element.optional:
                        exceptions_string = '\n'.join(
                            b.syntax() + ": " + str(e) for b, e in zip(element.branches, exceptions))
                        raise ValueError(
                            f"No branches valid after {prev_element_name}\n\nSyntax:\n{self.syntax()}\n\n" +
                            f"Individual errors from each branch:\n{exceptions_string}")
                possible_branches = list(filter(lambda b, o: o != [], possible_branches))
                satisfied_params = []
                for branch, _ in possible_branches:
                    satisfied_branch_params = []
                    for ele in branch.series:
                        if isinstance(ele, _Parameter) and ele.name in params.keys():
                            satisfied_branch_params.append(ele.name)
                    satisfied_params.append(satisfied_branch_params)
                satisfied_params_string = []
                if len(possible_branches) >= 2:
                    for index, (branch, _) in enumerate(possible_branches):
                        satisfied_params_string.append(
                            f"{branch.syntax()}: params {', '.join(satisfied_params[index])} satisfied")
                    satisfied_params_string = "\n".join(satisfied_params_string)
                    raise MultipleBranchesSatisfiedError(
                        f"Multiple branches were satisfied. It is unclear which branch is intended.\n\n{satisfied_params_string}")
                if len(possible_branches) == 1:
                    command.extend(defaults_queue)
                    command.append(possible_branches[1])
                    prev_element_name = satisfied_params[0][-1]

        return " ".join(command)

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
    def _get_options(annotation: Type[Any]) -> list[Any]:
        if issubclass(type(annotation), _OneTypeParamBase):
            annotation: _OneTypeParamBase
            return Command._get_options(annotation.type_param)
        elif issubclass(type(annotation), _Type):
            annotation: _Type
            return []
        elif issubclass(type(annotation), _LiteralGenericAlias):
            annotation: _LiteralGenericAlias
            return list(get_args(annotation))
        elif issubclass(type(annotation), (_UnionGenericAlias, UnionType)):
            annotation: _UnionGenericAlias
            return [*get_args(annotation)[0], *get_args(annotation)[1]]
        else: return []

    @staticmethod
    def _process_order(order: list | Element, func: Callable[..., ExecutedCommand]) -> dict[str, Element]:
        if isinstance(order, list):
            eles = {}
            for i in order:
                eles.update(Command._process_order(i, func))
            return eles
        elif isinstance(order, LE):
            return {}
        elif isinstance(order, AE):
            arg = inspect.signature(func).parameters[order.name]
            order.default = order.default if arg.default == arg.empty else arg.default
            if arg.annotation != arg.empty:
                order.annotation = arg.annotation
                order.options = Command._get_options(arg.annotation) or None
            return {order.name: order}
        elif isinstance(order, SE):
            eles = {}
            for i in order.branches:
                eles.update(Command._process_order(i, func))
            return eles

class ExecutedCommand:
    def __init__(self, fh: UniversalFuncHandler, name: str, command_string: str):
        self.fh = fh
        self.name = name
        self.command_string = command_string


    def store_success(self):
        pass

    def store_result(self):
        pass
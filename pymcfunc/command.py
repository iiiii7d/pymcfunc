from __future__ import annotations

import inspect
import re
from types import UnionType, NoneType
# noinspection PyUnresolvedReferences
from typing import Callable, Any, Union, Type, Literal, Optional, _UnionGenericAlias, TypeVar, _LiteralGenericAlias, \
    get_args, Pattern, TYPE_CHECKING, Generic, _AnnotatedAlias, TypeAlias, Annotated
from uuid import UUID

from pymcfunc.errors import MultipleBranchesSatisfiedError, MissingError, MissingArgumentError

if TYPE_CHECKING: from pymcfunc.func_handler import BaseFunctionHandler
if TYPE_CHECKING: from pymcfunc.raw_commands import BaseRawCommands
from pymcfunc.selectors import BaseSelector, JavaSelector, BedrockSelector

# for eval
# noinspection PyUnresolvedReferences
from pymcfunc.advancements import Advancement

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
    def __init__(self, name: str, optional: bool = False, options: list[Any] | None = None):
        self.name = name
        self.optional = optional
        self.default = None
        self.options = options or None
        self.annotation = None
AE = ArgumentE

class SwitchE(Element):
    branches: tuple[list[Element], ...]
    optional: bool
    def __init__(self, *branches: list[Element], optional: bool = False):
        self.branches = branches
        self.optional = optional
    def __class_getitem__(cls, *branches: list[Element]):
        ae = cls(*branches)
        ae.optional = True
        return ae
SE = SwitchE

class Annotation:
    check: Callable[[Any, str], None] = lambda _, __, ___: None
    def convert(self, value: Any, varname: str) -> Any:
        self.check(value, varname)
        return value

class Single(Annotation):
    @staticmethod
    def check(instance: BaseSelector, varname: str):
        if not instance.singleonly:
            raise ValueError(f"Value for argument `{varname}` selects multiple entities (Got `{instance}`)")

class Player(Annotation):
    @staticmethod
    def check(instance: BaseSelector, varname: str):
        if not instance.playeronly:
            raise ValueError(f"Value for argument `{varname}` selects entities too (Got `{instance}`)")

class Regex(Annotation):
    def __init__(self, regex: str):
        self.regex = regex

    def check(self, instance: str, varname: str):
        if re.search(self.regex, instance) is None:
            raise ValueError(f"Value for argument `{varname}` does not match pattern `{self.regex}` (Got `{instance}`)")
PlayerName = Regex(r"^\w*$")

class Range(Annotation):
    def __init__(self, min_: int | float, max_: int | float):
        self.min = min_
        self.max = max_

    def check(self, instance: int | float, varname: str):
        super().check(instance, varname)
        if not self.min <= instance <= self.max:
            raise ValueError(f"Value for argument `{varname}` is out of range {self.min} <= x <= {self.max} (Got `{instance}`)")

class Quoted(Annotation):
    def convert(self, value: str, _: str) -> str:
        return "\""+value+"\""
class NoSpace(Annotation):
    @staticmethod
    def check(value: str, varname: str):
        if " " in value:
            raise ValueError(f"Value for argument `{varname}` has spaces (Got `{value}`)")

RawJson: TypeAlias = Union[dict, list]
ResourceLocation: TypeAlias = str
_JavaPlayerTarget: TypeAlias = Union[Annotated[str, PlayerName], UUID, Annotated[JavaSelector, Player]]
_JavaSingleTarget: TypeAlias = Union[Annotated[str, PlayerName], UUID, Annotated[JavaSelector, Single]]
_BedrockPlayerTarget: TypeAlias = Union[Annotated[str, PlayerName], Annotated[BedrockSelector, Player]]
_BedrockSingleTarget: TypeAlias = Union[Annotated[str, PlayerName], Annotated[BedrockSelector, Player]]
_BedrockTarget: TypeAlias = Union[Annotated[str, PlayerName], BedrockSelector]
_BedrockSinglePlayerTarget: TypeAlias = Union[Annotated[str, PlayerName], Annotated[BedrockSelector, Single, Player]]

class Command:
    order: list[Element]
    fh: BaseFunctionHandler
    arg_namelist: list[str]
    eles: dict[str, AE]
    name: str
    segment_name: str
    func: Callable[[BaseRawCommands, ...], ExecutedCommand]
    @classmethod
    def command(cls, fh: BaseFunctionHandler,
                order: list[Element],
                cmd_name: str | None = None,
                segment_name: str | None = None):
        def decorator(func: Callable[[BaseRawCommands, ...], ExecutedCommand]):
            cmd = cls()
            cmd.order = order
            cmd.fh = fh
            cmd.func = func
            cmd.name = cmd_name or func.__name__.split("_")[0]
            cmd.segment_name = segment_name or func.__name__.replace("_", " ")
            cmd.arg_namelist = []
            for name, arg in inspect.signature(func).parameters.items():
                if name == "self": pass
                if arg.POSITIONAL_OR_KEYWORD or arg.POSITIONAL_ONLY:
                    cmd.arg_namelist.append(name)

                cmd.eles = cls._process_order(order, func)
            return cmd
        return decorator

    def __call__(self, *args, **kwargs) -> ExecutedCommand:
        for i, arg in enumerate(args):
            kwargs[self.arg_namelist[i]] = arg

        cmd = ExecutedCommand(self.fh, self.name, self._process_arglist(kwargs))
        self.fh.commands.append(cmd)
        return cmd

    def syntax(self, root: bool = True) -> str:
        syntax = [self.segment_name] if root else []
        for element in self.order:
            if isinstance(element, LE):
                syntax.append(element.content)
            elif isinstance(element, AE):
                if element.options:
                    options = ":" + "|".join(str(o) for o in element.options)
                else:
                    options = ""
                if element.default is not None:
                    default = "=" + str(element.default)
                else:
                    default = ""
                param_syntax = element.name + options + default
                if element.default is None:
                    param_syntax = "<" + param_syntax + ">"
                else:
                    param_syntax = "[" + param_syntax + "]"
                syntax.append(param_syntax)
            elif isinstance(element, SE):
                syntax.append("{" + "/".join(Command.command(self.fh, b, self.name)(self.func).syntax(root=False) for b in element.branches) + "}")
                if element.optional: syntax[-1] = "[" + syntax[-1] + "]"
        return " ".join(syntax)

    def _process_arglist(self, args: dict[str, Any], root: bool = True):
        command = [self.segment_name] if root else []
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
                value = Command._check_and_process_arg(eval(inspect.signature(self.func).parameters[element.name].annotation),
                                                       value, element.name)
                if not element.optional and value == element.default:
                    raise MissingArgumentError(element.name)

                if isinstance(value, str) and value == "":
                    raise ValueError(f"Parameter {element.name} is an empty string")
                if element.options is not None and value not in element.options:
                    raise ValueError(
                        f"Value for argument `{element.name}` not in {', '.join(element.options)} (Got `{value}`)`")
                if isinstance(value, bool): value = "true" if value else "false"
                if element.default == value:
                    if len(defaults_queue) > 0 and defaults_queue[-1] is None:
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
                to_subcmd = lambda b: Command.command(self.fh, b, self.name)(self.func)
                for branch in element.branches:
                    try:
                        branch_output = to_subcmd(branch)._process_arglist(args, root=False)
                        possible_branches.append((branch, branch_output))
                        # prev_element_name = "parameter "+branch.series[-1].name if isinstance(branch.series[-1], _Parameter) else "`"+str(branch.series[-1])+"`"
                        break
                    except Exception as e:
                        exceptions.append(e)
                else:
                    if not element.optional:
                        exceptions_string = '\n'.join(
                            to_subcmd(b).syntax(root=False) + ": " + str(e) for b, e in zip(element.branches, exceptions))
                        raise ValueError(
                            f"No branches valid after {prev_element_name}\n\nSyntax:\n{self.syntax()}\n\n" +
                            f"Individual errors from each branch:\n{exceptions_string}")
                possible_branches = list(filter(lambda b: b[0] != [], possible_branches))
                satisfied_params = []
                for branch, _ in possible_branches:
                    satisfied_branch_params = []
                    for ele in branch:
                        if isinstance(ele, AE) and ele.name in args.keys():
                            satisfied_branch_params.append(ele.name)
                    satisfied_params.append(satisfied_branch_params)
                satisfied_params_string = []
                if len(possible_branches) >= 2:
                    for index, (branch, _) in enumerate(possible_branches):
                        satisfied_params_string.append(
                            f"{to_subcmd(branch).syntax()}: params {', '.join(satisfied_params[index])} satisfied")
                    satisfied_params_string = "\n".join(satisfied_params_string)
                    raise MultipleBranchesSatisfiedError(
                        f"Multiple branches were satisfied. It is unclear which branch is intended.\n\n{satisfied_params_string}")
                if len(possible_branches) == 1:
                    command.extend(defaults_queue)
                    command.append(possible_branches[0][1])
                    try: prev_element_name = satisfied_params[0][-1]
                    except Exception: pass
        return " ".join(command)

    _T = TypeVar("_T")
    @staticmethod
    def _check_and_process_arg(annotation: Type[Any],
                               value: _T,
                               varname: str) -> _T:
        if issubclass(type(annotation), _AnnotatedAlias):
            annotation: _AnnotatedAlias
            res = Command._check_and_process_arg(get_args(annotation)[0], value, varname)
            for anno in get_args(annotation)[1:]:
                anno.check(res, varname)
                res = anno.convert(res, varname)
            return res
        elif issubclass(type(annotation), _LiteralGenericAlias):
            annotation: _LiteralGenericAlias
            if value not in get_args(annotation):
                raise ValueError(f"Value for argument `{varname}` not in {', '.join(get_args(annotation))} (Got `{value}`)`")
            return value
        elif issubclass(type(annotation), (_UnionGenericAlias, UnionType)):
            annotation: _UnionGenericAlias
            exceptions = []
            for anno in get_args(annotation):
                try:
                    return Command._check_and_process_arg(anno, value, varname)
                except Exception as e:
                    exceptions.append(e)
            else:
                raise exceptions[-1]
        elif issubclass(type(annotation), NoneType):
            if value is not None: raise ValueError(f"Value for argument `{varname}` is not None (Got `{value}`)")
            return None
        else:
            if not issubclass(type(value), annotation):
                raise ValueError(f"Value for argument `{varname}` is not of type `{annotation}` (Got `{value}`)")
            return value

    @staticmethod
    def _get_options(annotation: Type[Any]) -> list[Any]:
        if issubclass(type(annotation), _AnnotatedAlias):
            annotation: Annotation
            return Command._get_options(get_args(_AnnotatedAlias)[0])
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
                order.options = order.options if order.options else (Command._get_options(arg.annotation) or None)
            return {order.name: order}
        elif isinstance(order, SE):
            eles = {}
            for i in order.branches:
                eles.update(Command._process_order(i, func))
            return eles

class ExecutedCommand:
    def __init__(self, fh: BaseFunctionHandler, name: str, command_string: str):
        self.fh = fh
        self.name = name
        self.command_string = command_string

    def store_success(self):
        pass

    def store_result(self):
        pass
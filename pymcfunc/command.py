from __future__ import annotations

import inspect
from typing import Callable, Any

from pymcfunc.raw_commands import ExecutedCommand


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

def

class Command:
    order: list
    args: dict[str, Element]
    kwargs: dict[str, Element]
    @classmethod
    def command(cls, order: list):
        def decorator(func: Callable[..., ExecutedCommand]):
            cmd = cls()
            cmd.order = order
            cmd.args, cmd.kwargs = cls._process_order(order, func)
            return cmd
        return decorator

    def __call__(self, *args, **kwargs):
        pass

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
                return {order.name: arg}, {order.name: arg}
            elif arg.POSITIONAL_ONLY:
                return {order.name: arg}, {}
            else:
                return {}, {order.name: arg}
        elif isinstance(order, SE):
            args = {}; kwargs = {}
            for i in order.branches:
                res_args, res_kwargs = Command._process_order(i, func)
                args.update(res_args)
                kwargs.update(res_kwargs)
            return args, kwargs

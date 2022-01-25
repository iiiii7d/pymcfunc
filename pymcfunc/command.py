from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any, Optional

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
    optional: bool
    def __init__(self, name: str, type_: type, optional: bool=False, default: Optional[Any]=None, options: Optional[list[Any]]=None):
        pass
AE = ArgumentE

class SwitchE(Element):
    branches: tuple[list[Element], ...]
    def __init__(self, *branches: list[Element]):
        self.branches = branches
SE = SwitchE

class Command:
    order: list
    @classmethod
    def command(cls, order: list):
        def decorator(func: Callable[..., ExecutedCommand]):
            cmd = cls()
            cmd.order = order
            return cmd
        return decorator

    def __call__(self, *args, **kwargs):
        pass
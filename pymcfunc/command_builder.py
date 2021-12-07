from __future__ import annotations
from typing import Any, List, Literal, Optional, Union

from pymcfunc.errors import OptionError, SpaceError

class _Parameter:
    def __init__(self, name: str, type_: type, default: Optional[Any]=None, options: List[Any]=[], spaces: Union[bool, Literal["q"]]="q"):
        self.name = name
        self.type_ = type_
        self.default = default
        self.options = options
        self.spaces = spaces

class _Branch:
    def __init__(self, num_branches: int):
        self.branches: List[CommandBuilder] = []
        for _ in range(num_branches):
            self.branches.append(CommandBuilder())

class CommandBuilder:
    """
    A command builder that takes in parameters and outputs a Minecraft command as string.
    """

    def __init__(self, name: Optional[str]=None):
        """
        Initialises the command builder.

        :param str name: The name of the command.
        """
        self.series: List[Union[str, Union[_Parameter, _Branch]]] = []
        if name: self.series.append(name)

    def syntax(self) -> str:
        """
        Generates the syntax string for the command.

        :return: The syntax string
        :rtype: str
        """
        syntax = []
        for element in self.series:
            if isinstance(element, str):
                syntax.append(element)
            elif isinstance(element, _Parameter):
                if element.options != []:
                    options = ":"+"|".join(str(o) for o in element.options)
                else: options = ""
                if element.default is not None:
                    default = "="+str(element.default)
                else: default = ""
                param_syntax = element.name+options+default
                if element.default is None: param_syntax = "<"+param_syntax+">"
                else: param_syntax = "["+param_syntax+"]"
                syntax.append(param_syntax)
            elif isinstance(element, _Branch):
                syntax.append("{"+"/".join(b.syntax() for b in element.branches)+"}")
        return " ".join(syntax)
    
    def add_literal(self, literal: str):
        """
        Adds a literal to the command builder's series.

        :param str literal: The literal to add
        """
        self.series.append(literal)

    def add_param(self, name: str, type_: type, default: Optional[Any]=None, options: List[Any]=[], spaces: Union[bool, Literal["q"]]="q"):
        """
        Adds a parameter to the command builder's series.

        :param str name: The name of the parameter
        :param type type_: The type of the parameter
        :param default: The default option, if the value is not specified. Required if None.
        :type default: the value in ``type_`` | None
        :param options: A list of possible values for the parameter. All values are allowed if empty.
        :type options: List[the value in ``type_``]
        :param spaces: Whether spaces are allowed in the parameter, if ``type_`` is ``str``. Input ``q`` if spaces are allowed in quotes.
        :type spaces: bool | Literal["q"]
        """
        self.series.append(_Parameter(name, type_, default, options, spaces))

    def add_switch(self, name: str, options: List[str], default: Optional[str]=None):
        """
        Adds a switch to the command builder's series.

        Like a parameter, but it's a string and there are always options.

        :param str name: The name of the switch.
        :param List[str] options: A list of possible values for the parameter.
        :param default: The default option, if the value is not specified. Required if None.
        :type default: str, optional
        """
        self.series.append(_Parameter(name, str, default, options))

    def add_branch(self, num_branches: int=2) -> List[CommandBuilder]:
        """
        Adds a branch to the command builder's series.

        :param int num_branches: The number of branches to return, if ``options`` is []
        """
        branch = _Branch(num_branches)
        self.series.append(branch)
        return branch.branches

    def build(self, **params: Any) -> str:
        """
        Takes in params and formats them into a Minecraft command according to the series.

        :param Any params: The parameters to input.
        :return: The Minecraft command.
        :rtype: str
        """
        command = []
        prev_element_name = ""
        for element in self.series:
            if isinstance(element, str):
                command.append(element)
                prev_element_name = "`"+element+"`"
            elif isinstance(element, _Parameter):
                value = params[element.name] if element.name in params else element.default
                if value is None:
                    raise ValueError(f"Parameter {element.name} is required")
                elif not isinstance(value, element.type_):
                    raise TypeError(f"Parameter {element.name} must be type {element.type_} (Got {type(value)}")
                if element.options != [] and value not in element.options:
                    raise OptionError(element.options, value)
                if not element.spaces and isinstance(value, str) and " " in value:
                    raise SpaceError(element.name, value) 
                elif element.spaces == "q" and isinstance(value, str) and " " in value:
                    value = "\""+value+"\""
                if isinstance(value, bool): command.append("true" if value else "false")
                else: command.append(str(value))
                prev_element_name = "parameter "+element.name
            elif isinstance(element, _Branch):
                exceptions = []
                for branch in element.branches:
                    try:
                        branch_output = branch.build(**params)
                        command.append(branch_output)
                        prev_element_name = "parameter "+branch.series[-1].name if isinstance(branch.series[-1], _Parameter) else "`"+str(branch.series[-1])+"`"
                        break
                    except Exception as e:
                        exceptions.append(e)
                else:
                    excs = '\n'.join(str(b)+": "+str(e) for b, e in zip(element.branches, exceptions))
                    raise ValueError(f"No branches valid after {prev_element_name}\n\nSyntax:\n{str(self)}\n\n" +
                    f"Individual errors from each branch:\n{excs}")

        return " ".join(command)
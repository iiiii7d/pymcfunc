from __future__ import annotations
from typing import Any, List, Literal, Optional, Union

from pymcfunc.errors import OptionError, SpaceError, MissingArgumentError, MultipleBranchesSatisfiedError, MissingError
from pymcfunc.selectors import UniversalSelector


class _Parameter:
    def __init__(self, name: str, type_: type, optional: bool=False, default: Optional[Any]=None, options: Optional[List[Any]]=None, spaces: Union[bool, Literal["q"]]=False, **kwargs):
        if options is None: options = []
        self.name = name
        self.optional = optional
        self.type_ = type_
        self.default = default
        self.options = options
        self.spaces = spaces
        self.attrs = kwargs

class _Branch:
    def __init__(self, num_branches: int):
        self.branches: List[CommandBuilder] = []
        for _ in range(num_branches):
            self.branches.append(CommandBuilder())

class _Literal:
    def __init__(self, literal: str, optional: bool=False):
        self.literal = literal
        self.optional = optional

class CommandBuilder:
    """
    A command builder that takes in parameters and outputs a Minecraft command as string.
    """

    def __init__(self, name: Optional[str]=None):
        """
        Initialises the command builder.

        :param str name: The name of the command.
        """
        self.series: List[Union[_Literal, Union[_Parameter, _Branch]]] = []
        if name: self.series.append(_Literal(name))

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
                if element.options:
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
        self.series.append(_Literal(literal))

    def add_param(self, name: str, type_: type, optional: bool=False, default: Optional[Any]=None, options: Optional[List[Any]]=None, spaces: Union[bool, Literal["q"]]=False, **kwargs):
        """
        Adds a parameter to the command builder's series.

        :param str name: The name of the parameter
        :param type type_: The type of the parameter
        :param bool optional: Whether the parameter is optional
        :param default: The default option, if the value is not specified. Required if None.
        :type default: the value in ``type_`` | None
        :param options: A list of possible values for the parameter. All values are allowed if empty.
        :type options: List[the value in ``type_``]
        :param spaces: Whether spaces are allowed in the parameter, if ``type_`` is ``str``. Input ``q`` if spaces are allowed in quotes.
        :type spaces: bool | Literal["q"]
        """
        if options is None: options = []
        self.series.append(_Parameter(name, type_, optional, default, options, spaces, **kwargs))

    def add_switch(self, name: str, options: List[str], optional: bool=False, default: Optional[str]=None):
        """
        Adds a switch to the command builder's series.

        Like a parameter, but it's a string and there are always options.

        :param str name: The name of the switch.
        :param bool optional: Whether the parameter is optional
        :param List[str] options: A list of possible values for the parameter.
        :param default: The default option, if the value is not specified. Required if None.
        :type default: str, optional
        """
        self.series.append(_Parameter(name, str, optional, default, options))

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
        defaults_queue = []
        prev_element_name = ""
        prev_default_element_name = ""
        for element in self.series:
            if isinstance(element, _Literal):
                if element.optional:
                    defaults_queue.append(element.literal)
                    prev_default_element_name = "`"+element.literal+"`"
                else:
                    command.extend(defaults_queue)
                    command.append(element.literal)
                    prev_element_name = "`"+element.literal+"`"
            elif isinstance(element, _Parameter):
                value = params[element.name] if element.name in params else element.default
                if not element.optional and value is None:
                    raise MissingArgumentError(element.name)
                elif not isinstance(value, element.type_):
                    raise TypeError(f"Parameter {element.name} must be type {element.type_} (Got {type(value)}")
                if element.options != [] and value not in element.options:
                    raise OptionError(element.options, value)
                if not element.spaces and isinstance(value, str) and " " in value:
                    raise SpaceError(element.name, value) 
                elif element.spaces == "q" and isinstance(value, str) and " " in value:
                    value = "\""+value+"\""
                if isinstance(value, bool): value = "true" if value else "false"
                if issubclass(value, UniversalSelector) and 'qty' in element.attrs and value.qty is not None and element.attrs['qty'] != value.qty:
                    raise ValueError(f"Parameter {element.name} allows target selector for {element.attrs['qty']} entities/players (Got `{value.qty}`)")
                if issubclass(value, UniversalSelector) and element.attrs['playeronly'] and not value.playeronly:
                    raise ValueError(
                        f"Parameter {element.name} allows players target selectors for (Got one for entities as well)")
                if element.default == value:
                    if defaults_queue[-1] is None:
                        raise MissingError(prev_default_element_name, element.name)
                    defaults_queue.append(str(value) if value is not None else None)
                    prev_default_element_name = "parameter "+element.name
                else:
                    command.extend(defaults_queue)
                    command.append(str(value))
                    prev_element_name = "parameter "+element.name
            elif isinstance(element, _Branch):
                exceptions = []
                possible_branches = []
                for branch in element.branches:
                    try:
                        branch_output = branch.build(**params)
                        possible_branches.append((branch, branch_output))
                        #prev_element_name = "parameter "+branch.series[-1].name if isinstance(branch.series[-1], _Parameter) else "`"+str(branch.series[-1])+"`"
                        break
                    except Exception as e:
                        exceptions.append(e)
                else:
                    exceptions_string = '\n'.join(b.syntax()+": "+str(e) for b, e in zip(element.branches, exceptions))
                    raise ValueError(f"No branches valid after {prev_element_name}\n\nSyntax:\n{self.syntax()}\n\n" +
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
                        satisfied_params_string.append(f"{branch.syntax()}: params {', '.join(satisfied_params[index])} satisfied")
                    satisfied_params_string = "\n".join(satisfied_params_string)
                    raise MultipleBranchesSatisfiedError(f"Multiple branches were satisfied. It is unclear which branch is intended.\n\n{satisfied_params_string}")
                if len(possible_branches) == 1:
                    command.extend(defaults_queue)
                    command.append(possible_branches[1])
                    prev_element_name = satisfied_params[0][-1]

        return " ".join(command)
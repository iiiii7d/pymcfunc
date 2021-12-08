from textwrap import dedent
from difflib import get_close_matches

from pymcfunc.version import JavaVersion


class SpaceError(Exception):
    """No spaces are allowed in a specific parameter."""
    def __init__(self, varname, value):
        msg = f"No spaces allowed in parameter '{varname}' (Got '{value}')"
        super().__init__(msg)

class OptionError(Exception):
    """The option given is not in the list of allowed options."""
    def __init__(self, choices, choice):
        if choice is not None:
            choice = "'"+str(choice)+"'"
        close_matches = get_close_matches(choice, choices)
        if len(close_matches) != 0: parentheses = f"(Got '{choice}', maybe you meant: {', '.join(close_matches)})"
        else: parentheses = f"(Got '{choice}')"
        msg = f"Choices allowed: {', '.join(choices)} {parentheses}"
        super().__init__(msg)

class MissingArgumentError(Exception):
    """An argument is missing."""
    def __init__(self, varname):
        super().__init__(f"Missing argument `{varname}`")

class MultipleBranchesSatisfiedError(Exception):
    """"Multiple branches are satisfied. It is unclear which branch is intended."""
    pass

class RangeError(Exception):
    """The value is out of the range specified."""
    pass

class MissingError(Exception):
    """A parameter that had been made mandatory due to another parameter is not stated, and that parameter has a default value of None."""
    def __init__(self, dep_name, indep_name):
        msg = f"Variable `{dep_name}` must be stated as variable `{indep_name}` is stated"
        super().__init__(msg)

'''class OnlyOneAllowed(Exception):
    """Only one parameter is allowed, but two were given."""
    def __init__(self, params, param):
        msg = f"Parameters: {', '.join(params)} (Got '{param}'')"
        super().__init__(msg)

class InvalidParameterError(Exception):
    """The parameter is invalid because another parameter is not set to a specific value."""
    def __init__(self, allowed_val, other_param_name, other_val, param_name):
        msg = dedent(f"""The parameter '{param_name}' is not available because of '{other_param_name}' being '{other_val}'
                         To make '{param_name}' valid, switch '{other_param_name}' to '{allowed_val}'""")
        super().__init__(msg)

class ReliantError(Exception):
    """The parameter is invalid because another parameter is not specified, or is None."""
    def __init__(self, indep_name, dep_name):
        msg = f"'{dep_name}' relies on '{indep_name}' not being its default value; try specifying parameter '{indep_name}'"
        super().__init__(msg)

class CaretError(Exception):
    """Not all coordinates of a set use ‘^’."""
    def __init__(self, coords, cause):
        msg = ""
        if cause == "tilde":
            msg = f"Tildes and carets cannot be in the same set of coordinates (Got '{coords}')"
        elif cause == "notall":
            msg = f"Not all values have '^' (Got '{coords}')"
        super().__init__(msg)

class MissingError(Exception):
    """A parameter that had been made mandatory due to another parameter is not stated, and that parameter has a default value of None."""
    def __init__(self, dep_name, indep_name, indep_val):
        msg = f"Variable '{dep_name}' must be stated as '{indep_name}''s value is '{indep_val}'"
        super().__init__(msg)'''

class FutureCommandWarning(Warning):
    pass

class DeprecatedCommandWarning(Warning):
    pass

class EducationEditionWarning(Warning):
    pass
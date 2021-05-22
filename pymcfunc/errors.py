from textwrap import dedent

class SpaceError(Exception):
    def __init__(self, varname, value):
        msg = f"No spaces allowed in parameter '{varname}' (Got '{value}'')"
        super().__init__(msg)

class OptionError(Exception):
    def __init__(self, choices, choice):
        if choice != None:
            choice = "'"+str(choice)+"'"
        msg = f"Choices allowed: {', '.join(choices)} (Got {choice})"
        super().__init__(msg)

class OnlyOneAllowed(Exception):
    def __init__(self, params, param):
        msg = f"Parameters: {', '.join(params)} (Got {param})"
        super().__init__(msg)

class InvalidParameterError(Exception):
    def __init__(self, allowed_val, other_param_name, other_val, param_name):
        msg = dedent(f"""The parameter {param_name} is not available because of {other_param_name} being '{other_val}'
                         To make {param_name} valid, switch {other_param_name} to {allowed_val}""")
        super().__init__(msg)

class ReliantError(Exception):
    def __init__(self, indep_name, dep_name):
        msg = f"{dep_name} relies on {indep_name} not being its default value; try specifying parameter {indep_name}"
        super().__init__(msg)

class CaretError(Exception):
    def __init__(self, coords, cause):
        if cause == "tilde":
            msg = f"Tildes and carets cannot be in the same set of coordinates (Got '{coords}')"
        elif cause == "notall":
            msg = f"Not all values have '^' (Got '{coords}')"
        super().__init__(msg)
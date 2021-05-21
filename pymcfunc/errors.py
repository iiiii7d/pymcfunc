class SpaceError(Exception):
    def __init__(self, varname, value):
        msg = f"No spaces allowed in parameter '{varname}' (Got '{value}'')"
        super().__init__(msg)

class OptionError(Exception):
    def __init__(self, choices, choice):
        msg = f"Choices allowed: {', '.join(choices)} (Got '{choice}')"
        super().__init__(msg)
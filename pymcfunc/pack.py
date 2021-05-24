import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_java import JavaFuncHandler
from pymcfunc.func_handler_bedrock import BedrockFuncHandler
import pymcfunc.selectors as selectors

class Pack:
    """A container for all functions.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack"""

    def __init__(self, edition: str="j"):
        internal.options(edition, ['j','b'])
        if not edition in ['j', 'b']:
            raise errors.OptionError(['j', 'b'], edition)
        self.edition = edition
        self.funcs = {}
        self.name = None
        self.sel = selectors.BedrockSelectors() if edition == "b" else selectors.JavaSelectors()

    def function(self, func):
        """Registers a Python function and translates it into a Minecraft function.    
        The decorator will run the function so you do not need to run the function again.
        The name of the Python function will be the name of the Minecraft function.
        The decorator calls the function being decorated with one argument being a PackageHandler.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.Pack.function"""
        m = JavaFuncHandler() if self.edition == 'j' else BedrockFuncHandler()
        func(m)
        fname = func.__name__
        self.funcs.update({fname: str(m)})
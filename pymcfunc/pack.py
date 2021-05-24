import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_java import JavaFuncHandler
from pymcfunc.func_handler_bedrock import BedrockFuncHandler
import pymcfunc.selectors as selectors

class Pack:
    def __init__(self, edition: str="j"):
        internal.options(edition, ['j','b'])
        if not edition in ['j', 'b']:
            raise errors.OptionError(['j', 'b'], edition)
        self.edition = edition
        self.funcs = {}
        self.name = None
        self.sel = selectors.BedrockSelectors() if edition == "b" else selectors.JavaSelectors()

    def function(self, func):
        m = JavaFuncHandler() if self.edition == 'j' else BedrockFuncHandler()
        func(m)
        fname = func.__name__
        self.funcs.update({fname: str(m)})
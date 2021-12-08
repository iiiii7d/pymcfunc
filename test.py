import pymcfunc as pmf

p = pmf.pack.JavaPack("name", version="3")

@p.function()
def test_function(f: pmf.func_handler.JavaFuncHandler):
    pass
print(p.funcs)
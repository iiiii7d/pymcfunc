import pymcfunc as pmf

def test_pytest():
    p = pmf.pack.JavaPack("name", version="3")

    @p.function()
    def test_function(f: pmf.functions.JavaFunctionHandler):
        f.r.list()
    print(p.funcs)
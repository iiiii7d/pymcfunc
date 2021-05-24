import pymcfunc as pmf

def test_pytest():
    p = pmf.Pack()

    @p.function
    def mcfuncjava(f: pmf.JavaFuncHandler):
        f.say('a')
        f.tell('@p', 'b')
        f.help()
        f.setblock("1 2 3", "assefsdaf")
        f.fill('1 2 3', '4 5 6', "assefsdaf")
        f.clone('1 2 3', '4 5 6', '7 8 9')
        f.kill("@p")
        f.give("@p", "a")
        f.gamemode("survival")
        f.gamerule("doDaylightCycle", True)

    b = pmf.Pack('b')

    @b.function
    def mcfuncbedrock(f: pmf.BedrockFuncHandler):
        f.say('a')
        f.tell('@p', 'b')
        f.setblock("1 2 3", "assefsdaf")
        f.fill('1 2 3', '4 5 6', "assefsdaf")
        f.clone('1 2 3', '4 5 6', '7 8 9')
        f.kill("@p")
        f.give("@p", "3")
        f.gamemode(0)
        f.gamerule("maxCommandChainLength", 3)

    print(p.funcs)
    print(b.funcs)

    print(p.sel.e(distance=p.sel.range(4, 5)))
    print(b.sel.e(l=5))

    print(pmf.coords(4, "~5", 6))

test_pytest()
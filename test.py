import pymcfunc as pmf

def test_pytest():
    p = pmf.Pack()

    @p.function
    def mcfuncjava(f: pmf.JavaFuncHandler):
        f.r.say('a')
        f.r.tell('@p', 'b')
        f.r.tellraw('@p', {})
        f.r.help()
        f.r.seed()
        f.r.setblock("1 2 3", "assefsdaf")
        f.r.fill('1 2 3', '4 5 6', "assefsdaf")
        f.r.clone('1 2 3', '4 5 6', '7 8 9')
        f.r.kill("@p")
        f.r.give("@p", "a")
        f.r.gamemode("survival")
        f.r.gamerule("doDaylightCycle", True)
        f.r.teleport(destxyz="1 2 3")
        f.r.experience("add", amount=3)
        f.r.effect_give("@s", "asdfasdf")
        f.r.effect_clear("@s")
        f.r.enchant("@s", "asfasdf")
        f.r.setworldspawn(angle="2 3")
        f.r.spawnpoint()
        f.r.function("asdf")
        f.r.locate("asfasdf")

    b = pmf.Pack('b')

    @b.function
    def mcfuncbedrock(f: pmf.BedrockFuncHandler):
        f.r.say('a')
        f.r.tell('@p', 'b')
        f.r.tellraw('@p', {})
        f.r.help()
        f.r.seed()
        f.r.setblock("1 2 3", "assefsdaf")
        f.r.fill('1 2 3', '4 5 6', "assefsdaf")
        f.r.clone('1 2 3', '4 5 6', '7 8 9')
        f.r.kill("@p")
        f.r.give("@p", "3")
        f.r.gamemode(0)
        f.r.gamerule("maxCommandChainLength", 3)
        f.r.teleport(destxyz="1 2 3")
        f.r.experience(3, level=True)
        f.r.effect_give("@s", "asdfasdf")
        f.r.effect_clear("@s")
        f.r.enchant("@s", "asfasdf")
        f.r.setworldspawn()
        f.r.spawnpoint(pos="1 2 3")
        f.r.function("asdf")
        f.r.locate("asfasdf")

    print(p.funcs)
    print(b.funcs)

    print(p.sel.e(distance=p.sel.range(4, 5)))
    print(b.sel.e(l=5))

    print(pmf.coords(4, "~5", 6))

test_pytest()
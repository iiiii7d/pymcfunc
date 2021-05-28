import pymcfunc as pmf
import time

def test_pytest():
    start = time.time()
    p = pmf.Pack()

    @p.function
    def mcfuncjava(f: pmf.JavaFuncHandler):
        f.r.say('a')
        f.r.tell('@p', 'b')
        f.r.tellraw('@p', {})
        f.r.title("@s", "title", text="2")
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
        f.r.time_add(3)
        f.r.time_query("gametime")
        f.r.time_set('midnight')
        f.r.particle("asdfasd", 100, 100)
        f.r.schedule("asdfaf", duration="3")
        f.r.playsound("asdf", "neutral", "@p", minVolume=0.5)
        f.r.stopsound("@p")
        f.r.weather("clear")
        f.r.difficulty("h")
        f.r.kick("@s", "asfasfasdf")
        f.r.deop("@s")
        f.r.op("@s")
        f.r.list_(uuid=True)
        f.r.reload()
        f.r.me("asdf")
        f.r.tag("@p", "add", name="234")
        f.r.spreadplayers("1 2", 3.0, 3.0, True, "@p")
        f.r.replaceitem("entity", "3", 3, target="@p")
        f.r.whitelist('on')
        f.r.stop()
        f.r.scoreboard_objectives("modify_displayname", objective="asdf", displayName="234523")
        f.r.scoreboard_players("operation", target="@p", objective="asdfasdf", operation="><", source="@r", sourceObjective="32")
        f.r.execute(
            as_="@p",
            in_="overworld",
            align="xyz",
            facingentity={
                "target": "@r",
                "anchor": "eyes"
            },
            store={
                "store": "result",
                "mode": "bossbar",
                "id": "abc",
                "value": "max"
            },
            if_={
                "mode": "score",
                "target": "@r",
                "objective": "abc",
                "comparer": ">",
                "source": "@s",
                "sourceObjective": "3"
            },
            run=lambda sf: [sf.r.say("yes"), sf.r.say("no")]
        )

    b = pmf.Pack('b')

    @b.function
    def mcfuncbedrock(f: pmf.BedrockFuncHandler):
        f.r.say('a')
        f.r.tell('@p', 'b')
        f.r.tellraw('@p', {})
        f.r.title("@s", "title", text={})
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
        f.r.xp(3, level=True)
        f.r.effect_give("@s", "asdfasdf")
        f.r.effect_clear("@s")
        f.r.enchant("@s", "asfasdf")
        f.r.setworldspawn()
        f.r.spawnpoint(pos="1 2 3")
        f.r.function("asdf")
        f.r.locate("asfasdf")
        f.r.time_add(3)
        f.r.time_query("gametime")
        f.r.time_set('midnight')
        f.r.particle("asdfasd", "1 2 3")
        f.r.schedule("asdfaf", mode="cuboid", pos1="1 2 3", pos2="4 5 6")
        f.r.playsound("asdf", minVolume=0.5)
        f.r.stopsound("@p")
        f.r.weather("clear")
        f.r.difficulty(3)
        f.r.kick("@s", "asfasfasdf")
        f.r.deop("@s")
        f.r.op("@s")
        f.r.list_()
        f.r.reload()
        f.r.me("asdf")
        f.r.tag("@p", "add", name="234")
        f.r.spreadplayers("1 2", 3.0, 3.0, "@p")
        f.r.replaceitem("block", 3, "asdfaf", pos="2 3 3")
        f.r.whitelist('remove', target="@p")
        f.r.stop()
        f.r.scoreboard_objectives("add", objective="asdf", displayName="234523")
        f.r.scoreboard_players("operation", target="@p", objective="asdfasdf", operation="><", selector="@r", selectorObjective="32")
        f.r.execute("@s", "1 2 3", 
            lambda sf: [sf.r.say("yes"), sf.r.say("no")])

    print(p.funcs['mcfuncjava'])
    print("======================")
    print(b.funcs['mcfuncbedrock'])

    print(p.sel.e(distance=p.sel.range(4, 5)))
    print(b.sel.e(l=5))

    print(pmf.coords(4, "~5", 6))

    print(time.time()-start)

test_pytest()

# scoreboard execute
import pymcfunc as pmf
import time

def test_pytest():
    start = time.time()
    p = pmf.Pack("testpack")

    adv = p.advancement('abc', None)
    adv.set_icon('string')
    adv.set_display('title', 'asdfasdf')
    adv.set_parent(None)
    adv.criterion('abc').impossible()
    adv.criterion('def').brewed_potion()
    adv.set_requirements(['abc', 'def'])
    adv.reward('experience', 1)

    @p.function
    @p.t.tag("abc")
    @p.t.on_load
    @p.t.repeat_every_tick
    @p.t.repeat_every(3)
    @p.t.repeat(3)
    @adv.on_reward
    def mcfuncjava(f: pmf.JavaFuncHandler):
        f.clear()
        f.comment("abcd")
        f.r.say('a')
        f.r.tell('@p', 'b')
        f.r.tellraw('@p', {})
        f.r.title("@s", "title", text="2")
        f.r.help()
        f.r.seed()
        f.r.setblock("1 2 3", "assefsdaf")
        f.r.fill('1 2 3', '4 5 6', "assefsdaf")
        f.r.clone('1 2 3', '4 5 6', '7 8 9')
        f.r.summon("asdfasdf")
        f.r.clear("@p")
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
        f.r.execute(as_="@p", in_="overworld", align="xyz",
            facingentity={"target": "@r", "anchor": "eyes"},
            store={"store": "result", "mode": "bossbar", "id": "abc", "value": "max"},
            if_={"mode": "score", "target": "@r", "objective": "abc",
                "comparer": ">", "source": "@s", "sourceObjective": "3"},
            run=lambda sf: [sf.r.say("yes"), sf.r.say("no")]
        )

        f.r.advancement("grant", '@p', 'only', 'asf', '4')
        f.r.attribute('@p', 'asdf', 'modifier_value_get', uuid="asdfsdf")
        f.r.ban('@p')
        f.r.ban_ip('2345')
        f.r.banlist()
        f.r.bossbar_add("asdf", "we")
        f.r.bossbar_get("asdfasd", "max")
        f.r.bossbar_list()
        f.r.bossbar_remove("asdf"),
        f.r.bossbar_set("asdf", "color", color="white")
        f.r.data_get(block="asdfsd")
        f.r.data_merge({}, block="3")
        f.r.data_remove("sdf", block="12431")
        f.r.data_modify("prepend", "from", "asasdfds", block="2 3 4", sourceBlock="5 6 7")
        f.r.datapack('enable', 'asdfs', priority='after', existing='egefwewerre')
        f.r.debug('start')
        f.r.defaultgamemode('survival')
        f.r.forceload('add', chunk="1 2", chunk2="3 4")
        f.r.locatebiome("desert")
        f.r.loot("replace", "fish", targetEntity="@p", targetSlot="asdf", sourceLootTable="sdfa", sourcePos="1 2 4", sourceTool="j")
        f.r.pardon('@p')
        f.r.pardon_ip('2345')
        f.r.publish('8080')
        f.r.recipe('give', '@p', 'asdf')
        f.r.save_all()
        f.r.save_on()
        f.r.save_off()
        f.r.setidletimeout(3)
        f.r.spectate("@p", "@r")
        f.r.team('modify', team='asdfasf', option='color', value='gray')
        f.r.tm("asdfa")
        f.r.trigger("asdfa", 'set', 7)
        f.r.worldborder_add(1, 2)
        f.r.worldborder_center("1 2 3")
        f.r.worldborder_damage(distance=3)
        f.r.worldborder_get()
        f.r.worldborder_set(1, 2)
        f.r.worldborder_warning(3)

        val = f.v('val', '@p')
        val2 = f.v('val2', '@p', trigger=True)
        val.swap(val2)
        val += 2
        val -= 2
        val2 *= 2
        val2 /= 2
        val.higher(val2)
        val2.lower(val)
        val %= val2
        val.show('sidebar')
        f.r.execute(
            if_=val > val2,
            unless=val.in_range('3..4'),
            store=val2.store('result')
        )
        #del val
        #del val2

        armourstand = f.entity('ArmourStand', '@e[type=armor_stand]')
        armourstand.display_name('armour')
        armourstand.data_set_value('a', 'b')
        armourstand.pitch(3)
        armourstand.yaw(3)
        armourstand.move(destxyz='1 2 3')
        armourstand.force('x', 3)
        armourstand.remove()
        armourstand.set_armour_slot('head', 'abc')
        armourstand.remove_armour_slot('head')
        armourstand.move_limb('Head', 'x', 3)
        armourstand.mess()

    b = pmf.Pack('test2', 'b')

    @b.function
    def mcfuncbedrock(f: pmf.BedrockFuncHandler):
        f.clear()
        f.comment("abcd")
        f.r.say('a')
        f.r.tell('@p', 'b')
        f.r.tellraw('@p', {})
        f.r.title("@s", "title", text={})
        f.r.help()
        f.r.setblock("1 2 3", "assefsdaf")
        f.r.fill('1 2 3', '4 5 6', "assefsdaf")
        f.r.clone('1 2 3', '4 5 6', '7 8 9')
        f.r.summon("asdfasdf")
        f.r.clear("@p", "asdfa", maxCount=3)
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

        f.r.ability('@p', "asdfasd", True)
        f.r.agent('transfer', slotNum='3', destSlotNum='2', quantity=3)
        f.r.alwaysday(True)
        f.r.camerashake_add('@p', shakeType='positional')
        f.r.camerashake_stop('@p')
        f.r.changesetting(difficulty='p')
        f.r.clearspawnpoint("@p")
        f.r.closewebsocket()
        f.r.connect("adf")
        f.r.event("@e", 'a')
        f.r.fog('@p', "push", "as", fogId="2")
        f.r.gametest_runthis()
        f.r.gametest_run('a')
        f.r.gametest_runall('e')
        f.r.gametest_clearall(3)
        f.r.gametest_pos()
        f.r.gametest_create('asdf')
        f.r.gametest_runthese()
        f.r.getchunkdata('asdf', '1 2', 3)
        f.r.getchunks('asdf')
        f.r.getspawnpoint('@p')
        f.r.globalpause(True)
        f.r.immutableworld('true')
        f.r.listd()
        f.r.mobevent("asdf", True)
        f.r.music_add("asdfa")
        f.r.music_queue("asdfasdf", 1, 2, "loop")
        f.r.music_stop(3)
        f.r.music_volume(5)
        f.r.permissions('list')
        f.r.playanimation('@p', 'adsf')
        f.r.querytarget("@p")
        f.r.ride_start_riding("@p", '@e')
        f.r.ride_stop_riding("@p")
        f.r.ride_evict_riders("@e")
        f.r.ride_summon_rider("@e", "sdfasdf")
        f.r.ride_summon_ride("@p", "asdfasdf")
        f.r.save('query')
        f.r.setmaxplayers(1)
        f.r.structure_save("asdfasd", "1 2 3", "4 5 6", includesBlocks=True)
        f.r.structure_load("asdfsdf", "7 8 9", animationMode="layer_by_layer", seed=3)
        f.r.structure_delete("asdfasd")
        f.r.testfor("@p")
        f.r.testforblock("1 2 3", "asdfa")
        f.r.testforblocks("1 2 3", "4 5 6", "7 8 9")
        f.r.tickingarea_add_cuboid("1 2 3", "4 5 6")
        f.r.tickingarea_add_circle("1 2 3", 4)
        f.r.tickingarea_remove(pos="1 2 3")
        f.r.tickingarea_remove(all_=True)
        f.r.tickingarea_list()
        f.r.toggledownfall()
        f.r.worldbuilder()

        val = f.v('val', '@p')
        val2 = f.v('val2', '@p')
        val.swap(val2)
        val += 2
        val -= 2
        val2 *= 2
        val2 /= 2
        val.higher(val2)
        val2.lower(val)
        val %= val2
        val.show('sidebar')
        del val
        del val2
    
    print(p.funcs['mcfuncjava'])
    print("======================")
    print(b.funcs['mcfuncbedrock'])

    print(pmf.sel.cuboid((1, 2, 3), (4, 5, 6)))
    print(p.sel.e(distance=p.sel.range(4, 5)))
    print(b.sel.e(l=5))

    print(pmf.coords(4, "~5", 6))

    print(
        pmf.rt.java('§#abcdefHex §eyellow'),
        pmf.rt.java('§h[extra] Extras'),
        pmf.rt.java('§i[insert] Insertion §j[abc] Font'),
        pmf.rt.java('§k§l§m§n§o Formatting'),
        pmf.rt.java('§t[blah blah] ClickEvent'),
        pmf.rt.java('§z[minecraft:sheep|uuid|asdfasdf] HoverEvent'),
        pmf.rt.java('§l§oCancelling formatting§xlabc'),
        pmf.rt.java('§lResetting §rabc'),
        pmf.rt.java('¶t[msg|a|b] ¶s[@p|abc] ¶e[@e] ¶k[keybind] ¶n[path|block|~ ~ ~]'),
        sep='\n'
    )
    print(pmf.rt.bedrock('¶t[msg|a|b] ¶s[@p|abc] ¶e[@e] normal text'))

    print(p.tags)
    print(p.advancements)

    print(time.time()-start)
    finish = time.time()
    #p.build(6, 'b')

    print(time.time()-finish)

test_pytest()
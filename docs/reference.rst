Reference
=========
.. py:currentmodule:: pymcfunc

.. py:attribute:: __version__
      :type: str
      
      The version.

Syntax Guide
------------

* **<arg>** - Mandatory argument
* **[arg]** - Optional argument
* **arg1/arg2** - Pick one argument
* **arg:val1|val2** - Pick one value
* **arg1=val:arg2** Only valid if another argument is a specific value

Pack
----

.. py:class:: Pack

   A container for all functions.

   .. versionadded:: 0.0

   .. py:attribute:: edition
      :type: str

      The edition of the pack. Either 'j' or 'b'.

      .. versionadded:: 0.0

   .. py:attribute:: funcs
      :type: dict

      The list of functions, denoted by ``{func_name: commands}``

      .. versionadded:: 0.0

   .. py:attribute:: name
      :type: str

      For future use

   .. py:attribute:: sel
      :type: UniversalSelectors

      A UniversalSelectors object. Will be :py:class:`BedrockSelectors` for Bedrock, :py:class:`JavaSelectors` for Java.
      
      .. versionadded:: 0.0

   .. py:method:: __init__(edition: str="j")

      Initialises the pack.

      .. versionadded:: 0.0

      :param str edition: The version of the pack, either 'j' for Java Edition, or 'b' for Bedrock.
      :raises OptionError: if ``edition`` is neither 'j' nor 'b'

   .. py:decoratormethod:: function()

      Registers a Python function and translates it into a Minecraft function.

      The decorator will run the function so you do not need to run the function again.

      The name of the Python function will be the name of the Minecraft function.

      The decorator calls the function being decorated with one argument being a PackageHandler.

      .. code-block:: python
         
         import pymcfunc as pmf

         p = pmf.Pack()
         
         @p.function
         def func(f: pmf.JavaFuncHandler):
             f.r.say('a')
             # youf commands here...

      .. versionadded:: 0.0

Function Handlers
-----------------

.. py:class:: UniversalFuncHandler

   The function handler that is inherited by both :py:class:`JavaFuncHandler` and :py:class:`BedrockFuncHandler`.

   This includes commands and features that are the same for both Java and Bedrock edition.

   .. warning::
      It is highly recommended to use either :py:class:`BedrockFuncHandler` or :py:class:`JavaFuncHandler` for extended support of commands for your edition.

   .. versionadded:: 0.0

   .. description:: Operations

   * **str(a)** - Returns a linebreaked string of Minecraft commands.
   * **set(a) list(a) tuple(a)** - Returns a list of Minecraft commands.

   .. py:attribute:: commands
      :type: list

      The list of Minecraft commands.

      .. versionadded:: 0.0

   .. py:attribute:: sel
      :type: UniversalSelectors

      A UniversalSelectors instance.

      .. versionadded:: 0.1

   .. py:attribute:: r
      :type: UniversalRawCommands

      A UniversalRawCommands instance.

      .. versionadded:: 0.1

.. py:class:: UniversalRawCommands

   A container for raw Minecraft commands that are the same for both Java and Bedrock.

   .. versionadded:: 0.1

   .. warning::
      Do not instantiate UniversalRawCommands directly; use a FuncHandler and access the commands via the 'r' attribute.

   .. py:attribute:: fh
      :type: UniversalFuncHandler

      References back to the function handler that it is in.

      .. versionadded:: 0.1

   .. py:method:: say(message: str)
      
      Adds a ``say`` command.

      .. versionadded:: 0.0

      **Syntax:** *say <message>*

      :param str message: ``message``
      :returns: The command
      :rtype: str

   .. py:method:: tell(target: str, message: str)
                  msg(target: str, message: str)
                  w(target: str, message: str)

      Adds a ``tell`` command.

      .. versionadded:: 0.0

      **Syntax:** *tell <target> <message>*

      :param str target: ``target``
      :param str message: ``message``
      :returns: The command
      :rtype: str

   .. py:method:: tellraw(target: str, message: dict)

      Adds a ``tellraw`` command.

      .. versionadded:: 0.1

      **Syntax:** *tellraw <target> <message>*

      :param str target: ``target``
      :param dict message: ``message``
      :returns: The command
      :rtype: str

   .. py:method:: title(target: str, mode: str, text: Union[str, dict]=None, fadeIn: int=None, stay: int=None, fadeOut: int=None)

      Adds a ``title`` or ``titleraw`` (BE only) command.

      .. versionadded:: 0.1

      **Syntax:** *title <target> ...*
    
      * *... <mode:clear|reset>*
      * *... <mode:title|subtitle|actionbar> <text>*
      * *... <mode:times> <fadeIn> <stay> <fadeOut>*

      :param str target: ``target``
      :param str mode: ``mode:clear|reset|title|subtitle|actionbar|times``
      :param text: ``text`` (can be str in BE only)
      :type text: dict or str
      :param int fadeIn: ``fadeIn``
      :param int stay: ``stay``
      :param int fadeOut: ``fadeOut``
      :returns: The command
      :rtype: str

   .. py:method:: help()

      Adds a ``help`` command.

      .. versionadded:: 0.0

      **Syntax:** *help*

      :returns: The command
      :rtype: str

   .. py:method:: kill(target: str)

      Adds a ``kill`` command.

      .. versionadded:: 0.0

      **Syntax:** *kill <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: gamemode(mode: Union[int, str], target: str="@s")

      Adds a ``gamemode`` command.

      .. versionadded:: 0.1

      **Syntax:** *gamemode <mode> [target]*

      :param str mode: ``mode``
      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: gamerule(rule: str, value: Union[bool, int]=None)

      Adds a ``gamerule`` command.

      .. versionadded:: 0.1

      **Syntax:** *gamerule <rule> [value]*

      A complete list of game rules are available at https://minecraft.fandom.com/wiki/Game_rule#List_of_game_rules.

      :param str rule: ``rule``
      :param value: ``value``
      :type value: bool or int
      :returns: The command
      :rtype: str

   .. py:method:: seed()

      Adds a ``seed`` command.

      .. versionadded:: 0.1

      **Syntax:** *seed*

      :returns: The command
      :rtype: str

   .. py:method:: enchant(target: str, enchantment: str, level: int=1)

      Adds an ``enchant`` command.

      .. versionadded:: 0.1

      **Syntax:** *enchant <target> <enchantment> [level]*

      :param str target: ``target``
      :param str enchantment: ``enchantment``
      :param int level: ``level``
      :returns: The command
      :rtype: str

   .. py:method:: function(name: str)

      Adds a ``function`` command.
      
      .. versionadded:: 0.1

      **Syntax:** *function <name>*

      :param str name: ``name``
      :returns: The command
      :rtype: str

   .. py:method:: locate(name: str)

      Adds a ``locate`` command.

      .. versionadded:: 0.1

      **Syntax:** *locate <name>*

      :param str name: ``name``
      :returns: The command
      :rtype: str

   .. py:method:: time_add(amount: int)

      Adds a ``time add`` command.

      .. versionadded:: 0.1

      **Syntax:** *time add <amount>*

      :param str name: ``amount``
      :returns: The command
      :rtype: str

   .. py:method:: time_query(query: str)

      Adds a ``time query`` command.

      .. versionadded:: 0.1

      **Syntax:** *time query <query:daytime|gametime|day>*

      :param str name: ``query:daytime|gametime|day``
      :returns: The command
      :rtype: str

   .. py:method:: time_set(amount: Union[int, str])

      Adds a ``time set`` command.

      .. versionadded:: 0.1

      **Syntax:** *time set <amount>*

      :param str amount: ``amount`` (day|night|noon|midnight, + |sunrise|sunset for BE)
      :param int amount: ``amount``
      :returns: The command
      :rtype: str

   .. py:method:: kick(target: str, reason: str=None)

      Adds a ``kick`` command.

      .. versionadded:: 0.1

      **Syntax:** *kick <target> [reason]*

      :param str target: ``target``
      :param str reason: ``reason``
      :returns: The command
      :rtype: str

   .. py:method:: op(target: str)

      Adds an ``op`` command.
   
      .. versionadded:: 0.1
   
      **Syntax:** *op <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: deop(target: str)

      Adds an ``deop`` command.
   
      .. versionadded:: 0.1
   
      **Syntax:** *deop <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: reload()

      Adds a ``reload`` command.

      .. versionadded:: 0.1

      **Syntax:** *reload*

      :returns: The command
      :rtype: str

   .. py:method:: me(text: str)

      Adds a ``me`` command.

      .. versionadded:: 0.1

      **Syntax:** *me <text>*

      :param str text: ``text``
      :returns: The command
      :rtype: str

   .. py:method:: tag(target: str, mode: str, name: str=None)

      Adds a ``tag`` command.

      .. versionadded:: 0.1

      **Syntax:** *tag <target> <mode:add|list|remove> <mode=add|remove:name>*

      :param str target: ``target``
      :param str mode: ``mode:add|list|remove``
      :param str name: ``mode=add|remove:name``
      :returns: The command
      :rtype: str

   .. py:method:: whitelist(mode: str, target: str=None)

      Adds a ``whitelist`` command.

      .. versionadded:: 0.1
   
      **Syntax:** *whitelist <mode:add|list|on|off|reload|remove> <mode=add|remove:target>*
   
      :param str mode: ``mode:add|list|on|off|reload|remove``
      :param str target: ``mode=add|remove:target``
      :returns: The command
      :rtype: str

   .. py:method:: stop()

      Adds a ``stop`` command.

      **Syntax:** *stop*

      :returns: The command
      :rtype: str

.. py:class:: BedrockFuncHandler(UniversalFuncHandler)

   The Beckrock Edition function handler.

   .. py:attribute:: sel
      :type: BedrockSelectors

      A Selectors object.
      
      .. versionadded:: 0.0

   .. py:attribute:: r
      :type: BedrockRawCommands

      A BedrockRawCommands instance.

      .. versionadded:: 0.1

.. py:class:: BedrockRawCommands(UniversalRawCommands)

   A container for raw Minecraft commands that are specially for Bedrock Edition.

   .. versionadded:: 0.1

   .. warning::
      Do not instantiate BedrockRawCommands directly; use a FuncHandler and access the commands via the 'r' attribute.

   .. py:attribute:: fh
      :type: BedrockFuncHandler

      References back to the function handler that it is in.

      .. versionadded:: 0.1

   .. py:method:: setblock(pos: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace")

      Adds a ``setblock`` command.

      .. versionadded:: 0.0

      **Syntax:** *setblock <pos> <tileName> [tileData/blockStates] [mode:destroy|keep|replace]*

      :param str pos: ``pos``
      :param str tileName: ``tileName``
      :param int tiledata: ``tileData``
      :param list blockStates: ``blockStates``
      :param str mode: ``mode:destroy|keep|replace``
      :returns: The command
      :rtype: str

   .. py:method:: fill(pos1: str, pos2: str, tileName: str, tileData: int=0, blockStates: list=None, mode="replace", replaceTileName: str=None, replaceDataValue: int=None)

      Adds a ``fill`` command.

      .. versionadded:: 0.0

      **Syntax:** *fill <pos1> <pos2> <tileName> [tileData/blockStates] [mode:destroy|hollow|keep|outline|replace] [mode=replace:replaceTileName] [mode=replace:replaceDataValue]*

      :param str pos: ``pos``
      :param str tileName: ``tileName``
      :param int tiledata: ``tileData``
      :param list blockStates: ``blockStates``
      :param str mode: ``mode:destroy|hollow|keep|outline|replace``
      :param str replacTileName: ``mode=replace:replaceTileName``
      :param int replaceDataValue: ``mode=replace:replaceDataValue``
      :returns: The command
      :rtype: str

   .. py:method:: clone(pos1: str, pos2: str, dest: str, maskMode="replace", cloneMode: str="normal", tileName: str=None, tileData: int=0, blockStates: list=None)

      Adds a ``clone`` command.

      .. versionadded:: 0.0

      **Syntax:** *clone <pos1> <pos2> <dest> [maskMode:replace|masked] [cloneMode:force|move|normal] <maskMode=filtered:tileName> <maskMode=filtered:tileData/blockStates>*

      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str dest: ``dest``
      :param str maskMode: ``maskMode:replace|masked``
      :param str cloneMode: ``cloneMode:force|move|normal``
      :param str tileName: ``maskMode=filtered:tileName``
      :param int tileData: ``maskMode=filtered:tileData``
      :param list blockStates: ``maskMode=filtered:blockStates``
      :returns: The command
      :rtype: str

   .. py:method:: give(target: str, item: str, amount: int=1, data: int=0, components: dict=None)

      Adds a ``give`` command.

      .. versionadded:: 0.0

      **Syntax:** *give <target> <item> [amount] [data] [components]*

      :param str target: ``target``
      :param str item: ``item``
      :param int amount: ``amount``
      :param int data: ``data``
      :param dict components: ``components``
      :returns: The command
      :rtype: str

   .. py:method:: summon(entity: str, pos: str="~ ~ ~", event: str=None, nameTag: str=None)

      Adds a ``summon`` command.

      .. versionadded:: 0.1

      **Syntax:** *summon <entity> ...*

      * *[pos] [event] [nameTag]*
      * *<nameTag> [pos]*

      :param str entity: ``entity``
      :param str pos: ``pos``
      :param str event: ``event``
      :param str nameTag: ``nameTag``
      :returns: The command
      :rtype: str

   .. py:method:: clear(target: str="@s", item: str=None, data: int=-1, maxCount: int=-1)

      Adds a ``clear`` command.

      .. versionadded:: 0.1

      **Syntax:** *clear [target] [item] [data] [maxCount]*

      :param str target: ``target``
      :param str item: ``item``
      :param int data: ``data``
      :param int maxCount: ``maxCount``
      :returns: The command
      :rtype: str

   .. py:method:: teleport(destxyz: str=None, destentity: str=None, target: str="@s", facing: str=None, rotation: str=None, checkForBlocks: bool=False)
                  tp(destxyz: str=None, destentity: str=None, target: str="@s", facing: str=None, rotation: str=None, checkForBlocks: bool=False)

      Adds a ``teleport`` command.

      .. versionadded:: 0.1

      **Syntax:**

      * *teleport <destxyz> ...* / *teleport <target> <destxyz>...*

        * *[checkForBlocks]*
        * *[rotation] [checkForBlocks]*
        * *facing [facing] [checkForBlocks]*
    
      * *teleport <destentity> ...* / *teleport <target> <destentity>...*

        * *[checkForBlocks]*

      :param str destxyz: ``destxyz``
      :param str destentity: ``destentity``
      :param str target: ``target``
      :param str facing: ``facing``
      :param str rotation: ``rotation``
      :param bool checkForBlocks: ``checkForBlocks``
      :returns: The commmand
      :rtype: str

   .. py:method:: xp(amount: int, level: bool=False, target: str="@s")

      Adds an ``xp`` command.

      .. versionadded:: 0.1

      **Syntax:**
      
      * *xp <amount> [target]* if level=False
      * *xp <amount>L [target]* if level=True

      :param str amount: ``amount``
      :param bool level: Appends 'L' at the end of ``amount``
      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: effect_give(target: str, effect: str, seconds: int=30, amplifier: int=0, hideParticles: bool=False)

      Adds an ``effect`` (give) command.

      .. versionadded:: 0.1

      **Syntax:** *<target> <effect> [seconds] [amplifier] [hideParticles]*

      :param str target: ``target``
      :param str effect: ``effect``
      :param int seconds: ``seconds``
      :param int amplifier: ``amplifier``
      :param bool hideParticles: ``hideParticles``
      :returns: The command
      :rtype: str

   .. py:method:: effect_clear(target: str)

      Adds an ``effect`` (clear) command.

      .. versionadded:: 0.1

      **Syntax:** *effect <target> clear*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: setworldspawn(pos: str="~ ~ ~")

      Adds a ``setworldspawn`` command.

      .. versionadded:: 0.1

      **Syntax:** *setworldspawn [pos]*

      :param str pos: ``pos``
      :returns: The command
      :rtype: str

   .. py:method:: spawnpoint(target: str="@s", pos: str="~ ~ ~")

      Adds a ``spawnpoint`` command.

      .. versionadded:: 0.1

      **Syntax:** *spawnpoint [target] [pos]*

      :param str target: ``target``
      :param str pos: ``pos``
      :returns: The command
      :rtype: str

   .. py:method:: particle(name: str, pos: str)

      Adds a ``particle`` command.

      .. versionadded:: 0.1

      **Syntax:** *particle <name> <pos>*

      :param str name: ``name``
      :param str pos: ``pos``
      :returns: The command
      :rtype: str

   .. py:method:: schedule(path: str, mode: str, pos1: str=None, pos2: str=None, center: str=None, radius: int=None, tickingAreaName: str=None)

      Adds a ``schedule`` command.

      .. versionadded:: 0.1

      **Syntax:** *schedule on_area_loaded add ...*

      * *<pos1> <pos2> <path>* when mode=cuboid
      * *<mode:circle> <center> <radius> <path>*
      * *<mode:tickingarea> <tickingAreaName> <path>*

      :param str path: ``path``
      :param str mode: ``mode``
      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str center: ``center``
      :param int radius: ``radius``
      :param str tickingAreaName: ``tickingAreaName``
      :returns: The command
      :rtype: str

   .. py:method:: playsound(sound: str, target: str="@p", pos: str="~ ~ ~", volume: float=1.0, pitch: float=1.0, minVolume: float=None)

      Adds a ``playsound`` command.

      .. versionadded:: 0.1

      **Syntax:** *<sound> [target] [pos] [volume] [pitch] [minVolume]*

      :param str sound: ``sound``
      :param str target: ``target``
      :param str pos: ``pos``
      :param str volume: ``volume``
      :param str pitch: ``pitch``
      :param str minVolume: ``minVolume``
      :returns: The command
      :rtype: str

   .. py:method:: stopsound(target: str, sound: str=None)

      Adds a ``stopsound`` command.

      .. versionadded:: 0.1

      **Syntax:** *stopsound <target> [sound]*

      :param str target: ``target``
      :param str sound: ``sound``
      :returns: The command
      :rtype: str

   .. py:method:: weather(mode: str, duration: str=5)

      Adds a ``weather`` command.

      .. versionadded:: 0.1

      **Syntax:** *weather <mode:clear|rain|thunder|query> <mode=clear|rain|thunder:duration>*

      :param str mode: ``mode:clear|rain|thunder|query``
      :param int duration: ``mode=clear|rain|thunder:duration``
      :returns: The command
      :rtype: str

   .. py:method:: difficulty(difficulty: Union[str, int])

      Adds a ``difficulty`` command.

      .. versionadded:: 0.1

      **Syntax:** *difficulty <difficulty>*

      :param str difficulty: ``difficulty``
      :returns: The command
      :rtype: str

   .. py:method:: list_()

      Adds a ``list`` command.

      .. versionadded:: 0.1

      **Syntax:** *list*

      :returns: The command
      :rtype: str

   .. py:method:: spreadplayers(center: str, dist: float, maxRange: float, target: str)

      Adds a ``spreadplayers`` command.

      .. versionadded:: 0.1

      **Syntax:** *spreadplayers <center> <dist> <maxRange> <target>*

      :param str center: ``center``
      :param float dist: ``float``
      :param float maxRange: ``maxRange``
      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: replaceitem(self, mode: str, slotId: int, itemName: str, pos: str=None, target: str=None, slotType: str=None, itemHandling: str=None, amount: int=1, data: int=0, components: dict=None)

      Adds a ``replaceitem`` command.

      .. versionadded:: 0.1

      **Syntax:** *replaceitem <mode:block|entity> <pos/target> ...*

      * *slot.container <slotId> <itemName> [amount] [data] [components]* or
      * *slot.container <slotId> <replaceMode:destroy|keep> <itemName> [amount] [data] [components]* when mode=block
      * *<slotType> <slotId> <itemName> [amount] [data] [components]* or
      * *<slotType> <slotId> <itemHandling:destroy|keep> <itemName> [amount] [data] [components]* when mode=entity

      :param str mode: ``mode:block|entity``
      :param str slotId: ``slotId``
      :param str pos: ``pos``
      :param str target: ``target``
      :param str slotType: ``slotType``
      :param str itemHandling: ``itemHandling:destroy|keep``
      :param int amount: ``amount``
      :param int data: ``data``
      :param dict components: ``components``
      :returns: The command
      :rtype: str

   .. py:method:: allowlist(mode: str, target: str=None)

      Alias of :py:func:`UniversalRawCommands.whitelist`.

      .. versionadded:: 0.1

   .. py:method:: scoreboard_objectives(mode: str, objective: str=None, displayName: str=None, slot: str=None, sortOrder: str=None)

      Adds a ``scoreboard objectives`` command.

      .. versionadded:: 0.1

      **Syntax:** *scoreboard objectives ...*

      * *<mode:add> <objective> dummy [displayName]*
      * *<mode:list>*
      * *<mode:remove> <objective>*
      * *<mode:setdisplay> <slot:list|sidebar|belowname> [objective] [slot=list|sidebar:sortOrder:ascending|descending]*

      :param str mode: ``mode:add|list|remove|setdisplay``
      :param str objective: ``objective``
      :param str displayName: ``displayName``
      :param str slot: ``slot:list|sidebar|belowname``
      :param str sortOrder: ``slot=list|sidebar:sortOrder:ascending|descending``
      :returns: The command
      :rtype: str

   .. py:method:: scoreboard_players(mode: str, target: str=None, objective: str=None, minv: Union[int, str]=None, maxv: Union[int, str]=None, count: int=None, operation: str=None, selector: str=None, selectorObjective: str=None)

      Adds a ``scoreboard players`` command.

      .. versionadded:: 0.1

      **Syntax:** *scoreboard players ...*

      * *<mode:list> [target]*
      * *<mode:reset> <target> [objective]*
      * *<mode:test|random> <target> <objective> <minv> [maxv]*
      * *<mode:set|add|remove> <target> <objective> <count>*
      * *<mode:operation> <target> <objective> <operation:+=|-=|*=|/=|%=|<|>|><> <selector> <selectorObjective>*

      :param str mode: ``mode:list|reset|test|random|set|add|remove|operation``
      :param str target: ``target``
      :param str objective: ``objective``
      :param int minv: ``minv`` (can be * when mode=test)
      :param int maxv: ``maxv`` (can be * when mode=test)
      :param int count: ``count``
      :param str operation: ``operation:+=|-=|*=|/=|%=|<|>|><``
      :param str selector: ``selector``
      :param str selectorObjective: ``selectorObjective``
      :returns: The command
      :rtype: str

   .. py:method:: execute(target: str, pos: str, run: Callable[[BedrockFuncHandler], Union[Union[list, tuple], None]], detectPos: str=None, block: str=None, data: int=None)

      Adds an ``execute`` command.

      .. versionadded:: 0.1

      **Syntax** *execute <target> <pos> ...*

      * *<run>*
      * *detect <detectPos> <block> <data> <run>*

      :param str target: ``target``
      :param str pos: ``pos``
      :param str run: ``run``
      :param str detectPos: ``detectPos``
      :param str block: ``block``
      :param int data: ``data``

      .. code-block:: python
         
         import pymcfunc as pmf
         p = pmf.Pack('b')
    
         @p.function
         def func(f: pmf.BedrockFuncHandler):
             f.r.execute("@e[type=sheep]", "~ ~ ~", 
                 lambda sf: sf.r.say("baah"))

             f.r.execute("@e[type=cow]", "~ ~ ~",
                 lambda sf: [
                     sf.r.say("moo")
                     sf.r.tp(destxyz="~ ~5 ~")
                 ])

             def chargeCreepers(sf: pmf.BedrockFuncHandler):
                 sf.r.summon("lightning_bolt")
             f.r.execute("@e[type=creeper]", "~ ~ ~", chargeCreepers)

   .. py:method:: ability(target: str, ability: str=None, value: bool=None)

      Adds an ``ability`` command.

      .. versionadded:: 0.2

      **Syntax:** *ability <target> [ability] [value]*

      :param str target: ``target``
      :param str abililty: ``ability``
      :param str value: ``value``
      :returns: The command
      :rtype: str

   .. py:method:: agent(mode: str, direction: str=None, slotNum: str=None, destSlotNum: str=None, pos: str=None, item: str=None, quantity: int=None, turnDirection: str=None)

      Adds an ``agent`` command.

      .. versionadded:: 0.2

      **Syntax:** *agent ...*

      * *<mode:move|attack|destroy|dropall|inspect|inspectdata|detect|detectredstone|till> <direction:forward|back|left|right|up|down>*
      * *<mode:turn> <turnDirection:left|right>*
      * *<mode:drop> <slotNum> <quantity> <directon:forward|back|left|right|up|down>*
      * *<mode:transfer> <slotNum> <quantity> <destSlotNum>*
      * *<mode:create>*
      * *<mode:tp> <pos>*
      * *<mode:collect> <item>*
      * *<mode:place> <slotNum> <direction:forward|back|left|right|up|down>*
      * *<mode:getitemcount|getitemspace|getitemdetail> <slotNum>*

      :param str directon: ``direction:forward|back|left|right|up|down``
      :param str slotNum: ``slotNum``
      :param str destSlotNum: ``destSlotNum``
      :param str item: ``item``
      :param int quantity: ``quantity``
      :param str turnDirection: ``turnDirection``
      :returns: The command
      :rtype: str

   .. py:method:: alwaysday(lock: bool=None)
                  daylock(lock: bool=None)

      Adds an ``alwaysday`` command.

      .. versionadded:: 0.2

      **Syntax:** *alwaysday [lock]**

      :param bool lock: ``lock``
      :return: The command
      :rtype: str

   .. py:method:: camerashake_add(target: str, intensity: float=1, seconds: float=1, shakeType: str=None)

      Adds a ``camerashake add`` command.

      .. versionadded:: 0.2

      **Syntax:** *camerashake add <target> [intensity] [seconds] [shakeType:positional|rotational]*

      :param str target: ``target``
      :param float intensity: ``intensity``
      :param float seconds: ``seconds``
      :param str shakeType: ``shakeType:positional|rotational``
      :return: The command
      :rtype: str

   .. py:method:: camerashake_stop(target: str)

      Adds a ``camerashake stop`` command.

      .. versionadded:: 0.2

      **Syntax:** *camerashake stop <target>*

      :param str target: ``target``
      :return: The command
      :rtype: str

   .. py:method:: changesetting(allow_cheats: bool=None, difficulty: Union[str, int]=None)

      Adds a ``changesetting`` command.

      .. versionadded:: 0.2

      **Syntax:** *changesetting ...*

      * *allow-cheats <allow_cheats>*
      * *difficulty <difficulty>*

      :param bool allow_cheats: ``allow_cheats``
      :param difficulty: ``difficulty``
      :type difficulty: str or int
      :returns: The command
      :rtype: str

   .. py:method:: clearspawnpoint(target: str)

      Adds a ``clearspawnpoint`` command.

      .. versionadded:: 0.2

      **Syntax:** *clearspawnpoint <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: closwebsocket()

      Adds a ``closewebsocket`` command.

      .. versionadded:: 0.2

      **Syntax:** *closewebsocket*

      :returns: The command
      :rtype: str

   .. py:method:: connect(serverUri: str)

      Adds a ``connect`` command.

      .. versionadded:: 0.2

      **Syntax:** *connect <serverUri>*

      :param str serverUri: ``serverUri``
      :returns: The command
      :rtype: str

   .. py:method:: event(target: str, event: str)

      Adds an ``event`` method.

      .. versionadded:: 0.2

      **Syntax:** *event <target> <event>*

      :param str target: ``target``
      :param str event: ``event``
      :returns: The command
      :rtype: str

   .. py:method:: fog(target: str, mode: str, userProvidedId: str, fogId: str=None)

      Adds a ``fog`` method.

      .. versionadded:: 0.2

      **Syntax:** *fog <target> <mode:push|pop|remove> <mode=push:fogId> <userProvidedId>*

      :param str target: ```target``
      :param str mode: ``mode:push|pop|remove``
      :param str userProvidedId: ``userProvidedId``
      :param str fogId: ``mode=push:fogId``
      :returns: The command
      :rtype: str

   .. py:method:: gametest_runthis()

      Adds a ``gametest runthis`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest runthis*

      :returns: The command
      :rtype: str

   .. py:method:: gametest_run(name: str, rotationSteps: int=None)

      Adds a ``gametest run`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest run <name> [rotationSteps]*

      :param str name: ``name``
      :param int rotationSteps: ``rotationSteps``
      :returns: The command
      :rtype: str

   .. py:method:: gametest_runall(tag: str, rotationSteps: int=None)
                  gametest_runset(tag: str, rotationSteps: int=None)

      Adds a ``gametest runall`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest runall <tag> [rotationSteps]*

      :param str tag: ``tag``
      :param int rotationSteps: ``rotationSteps``
      :returns: The command
      :rtype: str

   .. py:method:: gametest_clearall(self, radius: int=None)

      Adds a ``gametest clearall`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest [radius]*

      :param int radius: ``radius``
      :returns: The command
      :rtype: str

   .. py:method:: gametest_pos()

      Adds a ``gametest pos``` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest pos*

      :returns: The command
      :rtype: str

   .. py:method:: gametest_create(name: str, width: int=None, height: int=None, depth: int=None)

      Adds a ``gametest create`` command.

      .. versionadded:: 0.2

      **Syntax:**  *gametest create <name> [wdth] [height] [depth]*

      :param str name: ``name``
      :param int width: ``width``
      :param int height: ``height``
      :param int depth: ``depth``
      :returns: The command
      :rtype: str

   .. py:method:: gametest_runthese()

      Adds a ``gametest runthese`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest runthese*

      :returns: The command
      :rtype: str

   .. py:method:: getchunkdata(dimension: str, chunkPos: str, height: int)

      Adds a ``getchunkdata`` command.

      .. versionadded:: 0.2

      **Syntax:** *getchunkdata <dimension> <chunkPos> <height>*

      :param str dimension: ``dimension``
      :param str chunkPos: ``chunkPos``
      :param int height: ``height```
      :returns: The command
      :rtype: str

   .. py:method:: getchunks(dimension: str)

      Adds a ``getchunks`` command.

      .. versionadded:: 0.2

      **Syntax:** *getchunks <dimension>*

      :param str dimension: ``dimension``
      :returns: The command
      :rtype: str

   .. py:method:: getspawnpoint(target: str)

      Adds a ``getspawnpoint`` command.

      .. versionadded:: 0.2

      **Syntax:** *getspawnpoint <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: globalpause(pause: bool)

      Adds a ``globalpause`` command.

      .. versionadded:: 0.2

      **Syntax:** *globalpause <pause>*

      :param bool pause: ``pause``
      :returns: The command
      :rtype: str

   .. py:method:: immutableworld(immutable: bool=None)

      Adds an ``immutableworld`` command.
      
      .. versionadded:: 0.2

      **Syntax:** *immutableworld [immutable]*

      :param bool immutable: ``immutable``
      :returns: The command
      :rtype: str

   .. py:method:: listd()

      Adds a ``listd`` command.

      .. versionadded:: 0.2

      **Syntax:** *listd*

      :returns: The command
      :rtype: str

   .. py:method:: mobevent(event: str, value: bool=None)

      Adds a ``mobevent`` command.

      .. versionadded:: 0.2

      **Syntax:** *mobevent <event> [value]*

      :param str event: ``event``
      :param bool value: ``value``
      :returns: The command
      :rtype: str

   .. py:method:: music_add(name: str, volume: float=None, fadeSeconds: float=None, repeatMode: str=None)

      Adds a ``music add`` command.

      .. versionadded:: 0.2

      **Syntax:** *music add <name> [volume] [fadeSeconds] [repeatMode:loop|play_once]*

      :param str name: ``name``
      :param float volume: ``volume``
      :param float fadeSeconds: ``fadeSeconds``
      :param str repeatMode: ``repeatMode:loop|play_once``
      :returns: The command
      :rtype: str

   .. py:method:: music_queue(name: str, volume: float=None, fadeSeconds: float=None, repeatMode: str=None)

      Adds a ``music queue`` command.

      .. versionadded:: 0.2

      **Syntax:** *music queue <name> [volume] [fadeSeconds] [repeatMode:loop|play_once]*

      :param str name: ``name``
      :param float volume: ``volume``
      :param float fadeSeconds: ``fadeSeconds``
      :param str repeatMode: ``repeatMode:loop|play_once``
      :returns: The command
      :rtype: str

   .. py:method:: music_stop(fadeSeconds: float=None)

      Adds a ``music stop`` command.

      .. versionadded:: 0.2

      **Syntax:** *music stop [fadeSeconds]*

      :param float fadeSeconds: ``fadeSeconds``
      :returns: The command
      :rtype: str

   .. py:method:: music_volume(volume: float)

      Adds a ``music volume`` command.

      .. versionadded:: 0.2

      **Syntax:** *music float <volume>*

      :param float volume: ``volume``
      :returns: The command
      :rtype: str

   .. py:method:: permissions(mode: str)

      Adds a ``permissions`` command.

      .. versionadded:: 0.2

      **Syntax:** *permissions <mode>*

      :param str mode: ``mode``
      :returns: The command
      :rtype: str
   
   .. py:method:: playanimation(target: str, animation: str, next_state: str=None, blend_out_time: float=None, stop_expression: str=None, controller: str=None)

      Adds a ``playanimation`` command.

      .. versionadded:: 0.2

      **Syntax:** *playanimation <target> <animation> [next_state] [blend_out_time] [stop_expression] [controller]

      :param str target: ``target``
      :param str animation: ``animation``
      :param str next_state: ``next_state``
      :param float blend_out_time: ``blend_out_time``
      :param str controller: ``controller``
      :returns: The command
      :rtype: str

   .. py:method:: querytarget(target: str)

      Adds a ``querytarget`` command.

      .. versionadded:: 0.2

      **Syntax:** *querytarget <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: ride_start_riding(rider: str, ride: str, teleportWhich: str="teleport_rider", fillMode: str="until_full")

      Adds a ``ride start_riding`` command.

      .. versionadded:: 0.2

      **Syntax:** *ride <rider> start_riding <ride> [teleportWhich:teleport_ride|teleport_rider] [fillMode:if_group_fits|until_full]*

      :param str rider: ``rider``
      :param str ride: ``ride``
      :param str teleportWhich: ``teleportWhich:teleport_ride|teleport_rider``
      :param str fillMode: ``fillMode:if_group_fits|until_full``
      :returns: The command
      :rtype: str

   .. py:method:: ride_stop_riding(rider: str)

      Adds a ``ride stop_riding`` command.

      .. versionadded:: 0.2

      **Syntax:** *ride <rider> stop_riding*

      :param str rider: ``rider``
      :returns: The command
      :rtype: str

   .. py:method:: ride_evict_riders(ride: str)

      Adds a ``ride evict_riders`` command.

      .. versionadded:: 0.2

      **Syntax:** *ride <ride> evict_riders*

      :param str ride: ``ride``
      :returns: The command
      :rtype: str

   .. py:method:: ride_summon_rider(self, ride: str, entity: str, event: str=None, nameTag: str=None)

      Adds a ``ride summon_riders`` command.

      .. versionadded:: 0.2

      **Syntax:** *ride <ride> summon_rider <entity> [event] [nameTag]*

      :param str ride: ``ride``
      :param str entity: ``entity``
      :param str event: ``event``
      :param str nameTag: ``nameTag``
      :returns: The command
      :rtype: str
      
   .. py:method:: ride_summon_ride(self, rider: str, entity: str, rideMode: str='reassign_rides', event: str=None, nameTag: str=None)

      Adds a ``ride summon_ride`` command.

      .. versionadded:: 0.2

      **Syntax:** *ride <rider> summon_ride <entity> [rideMode:skip_riders|no_ride_change|reassign_rides] [event] [nameTag]*

      :param str rider: ``rider``
      :param str entity: ``entity``
      :param str rideMode: ``rideMode:skip_riders|no_ride_change|reassign_rides``
      :param str event: ``event``
      :param str nameTag: ``nameTag``
      :returns: The command
      :rtype: str

   .. py:method:: save(mode: str)

      Adds a ``save`` command.

      .. versionadded:: 0.2

      **Syntax:** *save <mode:hold|query|resume>*

      :param str mode: ``mode:hold|query|resume``
      :returns: The command
      :rtype: str

   .. py:method:: setmaxplayers(maxPlayers: int):

      Adds a ``setmaxplayers`` command.

      .. versionadded:: 0.2

      **Syntax:** *setmaxplayers <maxPlayers>*

      :param str maxPlayers: ``maxPlayers``
      :returns: The command
      :rtype: str

   .. py:method:: structure_save(name: str, pos1: str, pos2: str, includesEntities: bool=True, saveMode: str='disk', includesBlocks: bool=True)

      Adds a ``structure save`` command.

      .. versionadded:: 0.2

      **Syntax:** *structure save <name> <pos1> <pos2> [includesEntities] [saveMode:disk|memory] [includesBlocks]*

      :param str name: ``name``
      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str includesEntities: ``includesEntities``
      :param str saveMode: ``saveMode:disk|memory``
      :param str includesBlocks: ``includesBlocks``
      :returns: The command
      :rtype: str

   .. py:method:: structure_load(self, name: str, pos: str, rotation: str='0_degrees', mirror: str='none', animationMode: str=None, \
                                 animationSeconds: float=1, includesEntities: bool=True, includesBlocks: bool=True, integrity: float=100, seed: str=None)

      Adds a ``strcture load`` command.

      .. versionadded:: 0.2

      **Syntax:** *structure load <name> <pos> [rotation:0_degrees|90_degrees|180_degrees|270_degrees] [mirror:x|z|xz|none] ...*

      * *...*
      * *[animationMode:block_by_block|layer_by_layer] [animationSeconds] ...*

      *[includesEntities] [includesBlocks] [integrity] [seed]*

      :param str name: ``name``
      :param str pos: ``pos``
      :param str rotation: ``rotation:0_degrees|90_degrees|180_degrees|270_degrees`` 
      :param str mirror: ``mirror:x|z|xz|none``
      :param str animationMode: ``animationMode:block_by_block|layer_by_layer``
      :param float animationSeconds: ``animationSeconds``
      :param bool includesEntities: ``includesEntities``
      :param bool includesBlocks: ``includesBlocks``
      :param float integrity: ``integrity``
      :param str seed: ``seed``
      :returns: The command
      :rtype: str

   .. py:method:: structure_delete(name: str)

      Adds a ``structure delete``

      .. versionadded:: 0.2

      **Syntax:** *structure delete <name>*

      :param str name: ``name``
      :returns: The command
      :rtype: str

   .. py:method:: testfor(target: str)

      Adds a ``testfor`` command.

      .. versionadded:: 0.2

      **Syntax:** *testfor <target>*

      :param str target: ``target``
      :returns: The command
      :rtype: str

   .. py:method:: testforblock(pos: str, name: str, dataValue: int=None)

      Adds a ``testforblock`` command.

      .. versionadded:: 0.2

      **Syntax:** *testforblock <pos> <name> [dataValue]*

      :param str pos: ``pos``
      :param str name: ``name``
      :param str dataValue: ``dataValue``
      :returns: The command
      :rtype: str

   .. py:method:: testforblocks(pos1: str, pos2: str, dest: str, mode: str='all')

      Adds a ``testforblocks`` command.

      .. versionadded:: 0.2

      **Syntax:** *testforblocks <pos1> <pos2> <dest> <mode:all|masked>*

      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str dest: ``dest``
      :param str mode: ``mode:all|masked``
      :returns: The command
      :rtype: str

   .. py:method:: tickingarea_add_cuboid(pos1: str, pos2: str, name: str=None)

      Adds a ``tickingarea add`` command.

      .. versionadded:: 0.2

      **Syntax:** *tickingarea add <pos1> <pos2> [name]*

      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str name: ``name``
      :returns: The command
      :rtype: str

   .. py:method:: tickingarea_add_circle(pos: str, radius: int, name: str=None)

      Adds a ``tickingarea add circle`` command.

      .. versionadded:: 0.2

      **Syntax:** *tickingarea add circle <pos> <radius> [name]*

      :param str pos: ``pos``
      :param int radius: ``radius``
      :param str name: ``name``
      :returns: The command
      :rtype: str

   .. py:method:: tickingarea_remove(name: str=None, pos: str=None, all_: bool=False)

      Adds a ``tickingarea remove`` command.

      .. versionadded:: 0.2

      **Syntax:** *tickingarea ...*

      * *remove_all* if all_=True
      * *<name/pos>* if all_=False

      :param str name: ``name``
      :param str pos: ``pos``
      :param bool all_: ``all_``
      :returns: The command
      :rtype: str

   .. py:method:: tickingarea_list(all_dimensions: bool=False)

      Adds a ``tickingarea list`` command.

      .. versionadded:: 0.2

      **Syntax:** *tickingarea ...*
      
      * *list all-dimensions* if all_dimensions=True
      * *list* if all_dimensions=False

      :param bool all_dimensions: ``all_dimensions``
      :returns: The command
      :rtype: str

   .. py:method:: toggledownfall()

      Adds a ``toggledownfall`` command.

      .. versionadded:: 0.2

      **Syntax:** *toggledownfall*

      :returns: The command
      :rtype: str

   .. py:method:: worldbuilder()
                  wb()

      Adds a ``worldbuilder`` command.

      .. versio


.. py:class:: JavaFuncHandler(UniversalFuncHandler)

   The Java Edition function handler.

   .. py:attribute:: sel
      :type: JavaSelectors

      A Selectors object.
      
      .. versionadded:: 0.0

   .. py:attribute:: r
      :type: JavaRawCommands

       A JavaRawCommands instance.

       .. versionadded:: 0.1

.. py:class:: JavaRawCommands(UniversalRawCommands)

   A container for raw Minecraft commands that are specially for Java Edition.

   .. versionadded:: 0.1

   .. warning::
      Do not instantiate JavaRawCommands directly; use a FuncHandler and access the commands via the 'r' attribute.

   .. py:attribute:: fh
      :type: JavaFuncHandler

      References back to the function handler that it is in.

      .. versionadded:: 0.1

   .. py:method:: setblock(pos: str, block: str, mode="replace")

      Adds a ``setblock`` command.

      .. versionadded:: 0.0

      **Syntax:** *setblock <pos> <block> [mode:destroy|keep|replace]*

      :param str pos: ``pos``
      :param str block: ``block``
      :param str mode: ``mode:destroy|keep|replace``
      :returns: The command
      :rtype: str

   .. py:method:: fill(pos1: str, pos2: str, block: str, mode="replace", filterPredicate: str=None)

      Adds a ``fill`` command.

      .. versionadded:: 0.0

      **Syntax:** *fill <pos1> <pos2> <block> [mode:destroy|hollow|keep|outline|replace] [mode=replace:filterPredicate]*

      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str block: ``block``
      :param str mode: ``mode:destroy|hollow|keep|outline|replace``
      :param str filterPredicate: ``mode=replace:filterPredicate``
      :returns: The command
      :rtype: str

   .. py:method:: clone(pos1: str, pos2: str, dest: str, maskMode="replace", filterPredicate: str=None, cloneMode: str="normal")

      Adds a ``clone`` method.

      .. versionadded:: 0.0

      **Syntax:** *clone <pos1> <pos2> <dest> [maskMode:replace|masked] <maskMode=masked:filterPredicate> [cloneMode:force|move|normal]*

      :param str pos1: ``pos1``
      :param str pos2: ``pos2``
      :param str dest: ``dest``
      :param str maskMode: ``maskMode:replace|masked``
      :param str filterPredicate: ``maskMode=masked:filterPredicate``
      :param str cloneMode: ``cloneMode:force|move|normal``
      :returns: The command
      :rtype: str

   .. py:method:: give(target: str, item: str, count: int=1)

      Adds a ``give`` command.

      .. versionadded:: 0.0

      **Syntax:** *give <target> <item> [count]*

      :param str target: ``target``
      :param str item: ``item``
      :param int count: ``count``
      :returns: The command
      :rtype: str

   .. py:method:: summon(entity: str, pos: str="~ ~ ~", nbt: dict=None)

      Adds a ``summon`` command.

      .. versionadded:: 0.1

      **Syntax:** *summon <entity> [pos] [nbt]*

      :param str entity: ``entity``
      :param str pos: ``pos``
      :param dict nbt: ``nbt``
      :returns: The command
      :rtype: str

   .. py:method:: clear(target: str="@s", item: str=None, maxCount: int=None)

      Adds a ``clear`` command.

      .. versionadded:: 0.1

      **Syntax:** *clear [target] [item] [maxCount]*

      :param str target: ``target``
      :param str item: ``item``
      :param int maxCount: ``maxCount``
      :returns: The command
      :rtype: str

   .. py:method:: teleport(destentity: str=None, destxyz: str=None, target: str="@s", rotation: str=None, faceMode: str=None, facing: str=None, anchor: str="eyes")
                  tp(destentity: str=None, destxyz: str=None, target: str="@s", rotation: str=None, faceMode: str=None, facing: str=None, anchor: str="eyes")

      Adds a ``teleport`` command.
   
      .. versionadded:: 0.1
   
      **Syntax:** *teleport <target> ...* / *teleport ...*
   
      * *<destentity>*
      * *<destxyz> [rotation]*
      * *<destxyz> facing <facing>* when faceMode=entity
      * *<destxyz> facing entity <facing> [anchor:eyes|feet]* when faceMode=location
   
      :param str destentity: ``destentity``
      :param str destxyz: ``destxyz``
      :param str target: ``target``
      :param str rotation: ``rotation``
      :param str faceMode: ``faceMode:entity|location``
      :param str facing: ``facing``
      :param str anchor: ``anchor:eyes|plant``
      :return: The command
      :rtype: str

   .. py:method:: experience(mode: str, target: str="@s", amount: int=None, measurement="points")
                  xp(mode: str, target: str="@s", amount: int=None, measurement="points")

      Adds an ``experience`` command.

      .. versionadded:: 0.1

      **Syntax:** *experience ...*

      * *<mode:add|set> <target> <amount> [measurement:levels|points]*
      * *<mode:query> <target> <measurement:levels|points>*

      :param str mode: ``mode:add|set|query``
      :param str target: ``target``
      :param int amount: ``amount``
      :param str measurement: ``measurement:levels|points``
      :return: The command
      :rtype: str

   .. py:method:: effect_give(target: str, effect: str, seconds: int=30, amplifier: int=0, hideParticles: bool=False)

      Adds an ``effect give`` command.

      .. versionadded:: 0.1

      **Syntax:** *effect give <target> <effect> [seconds] [amplifier] [hideParticles]*

      :param str target: ``target``
      :param str effect: ``effect``
      :param int seconds: ``seconds``
      :param int amplifier: ``amplifier``
      :param bool hideParticles: ``hideParticles``
      :return: The command
      :rtype: str

   .. py:method:: effect_clear(target: str="@s", effect: str=None)

      Adds an ``effect clear`` method.

      .. versionadded:: 0.1

      **Syntax:** *effect clear [target] [effect]*

      :param str target: ``target``
      :param str effect: ``effect``
      :return: The command
      :rtype: str

   .. py:method:: setworldspawn(pos: str="~ ~ ~", angle: str=None)

      Adds a ``setworldspawn`` command.

      .. versionadded:: 0.1

      **Syntax:** *setworldspawn [pos] [angle]*

      :param str pos: ``pos``
      :param str angle: ``angle``
      :return: The command
      :rtype: str

   .. py:method:: spawnpoint(target: str="@s", pos: str="~ ~ ~", angle: str=None)

      Adds a ``spawnpoint`` command.

      .. versionadded:: 0.1

      **Syntax:** *spawnpoint [target] [pos] [angle]*

      :param str target: ``target``
      :param str pos: ``pos``
      :param str angle: ``angle``
      :return: The command
      :rtype: str

   .. py:method:: particle(self, name: str, speed: float, count: int, params: str=None, pos: str="~ ~ ~", delta: str="~ ~ ~", mode: str="normal", viewers: str=None)

      Adds a ``particle`` command.

      .. versionadded:: 0.1

      **Syntax:** *particle <name> [params] [pos] [delta] <speed> <count> [mode:force|normal] [viewers]*

      :param str name: ``name``
      :param float speed: ``speed``
      :param int count: ``count``
      :param str params: ``params``
      :param str pos: ``pos``
      :param str delta: ``delta``
      :param str mode: ``mode:force|normal``
      :param str viewers: ``viewers``
      :return: The command
      :rtype: str

   .. py:method:: schedule(name: str, clear: bool=False, duration: str=None, mode: str="replace")

      Adds a ``schedule`` command.

      .. versionadded:: 0.1

      **Syntax:** *schedule ...*

      * *function <name> <duration> [mode:append|replace]*
      * *clear <name>*

      :param str name: ``name``
      :param bool clear: ``clear``
      :param str mode: ``mode:append|replace``
      :return: The command
      :rtype: str

   .. py:method:: playsound(sound: str, source: str, target: str, pos: str="~ ~ ~", volume: float=1.0, pitch: float=1.0, minVolume: float=None)

      Adds a ``playsound`` command.

      .. versionadded:: 0.1

      **Syntax:** *playsound <sound> <source:master|music|record|weather|block|hostile|neutral|player|ambient|voice> <targets> <pos> <volume> <pitch> <minVolume>*

      :param str sound: ``sound``
      :param str source: ``source:master|music|record|weather|block|hostile|neutral|player|ambient|voice``
      :param str target: ``target``
      :param str pos: ``pos``
      :param float volume: ``volume``
      :param float pitch: ``pitch``
      :param float minVolume: ``minVolume``
      :return: The command
      :rtype: str

   .. py:method:: stopsound(target: str, source: str="*", sound: str=None)

      Adds a ``stopsound`` command.

      .. versionadded:: 0.1

      **Syntax:** *stopsound <target> [source:master|music|record|weather|block|hostile|neutral|player|ambient|voice] [sound]*

      :param str target: ``target``
      :param str source: ``source``
      :param str sound: ``sound``
      :return: The command
      :rtype: str

   .. py:method:: weather(mode: str, duration: str=5)

      Adds a ``weather`` command.

      .. versionadded:: 0.1

      **Syntax:** *weather <mode:clear|rain|thunder> [duration]*

      :param str mode: ``mode``
      :param int duration: ``duration``
      :return: The command
      :rtype: str

   .. py:method:: difficulty(difficulty: str)

      Adds a ``difficulty`` command.

      .. versionadded:: 0.1

      **Syntax:** *difficulty <difficulty>*

      :param str difficulty: ``difficulty``
      :return: The command
      :rtype: str

   .. py:method:: list_(uuid: bool=False)

      Adds a ``list`` command.

      .. versionadded:: 0.1

      **Syntax** *list* if uuid=False; *list uuid* if uuid=True

      :param bool uuid: ``uuid``
      :return: The command
      :rtype: str

   .. py:method:: spreadplayers(center: str, dist: float, maxRange: float, respectTeams: bool, target: str, maxHeight: float=None)

      Adds a ``spreadplayers`` command.

      .. versionadded:: 0.1

      **Syntax**: *spreadplayers <center> <dist> <maxRange> ...*

      * *<respectTeams> <targets>*
      * *under <maxHeight> <respectTeams>*

      :param str center: ``center``
      :param float dist: ``dist``
      :param float maxRange: ``maxRange``
      :param bool respectTeams: ``respectTeams``
      :param str target: ``target``
      :param float maxHeight: ``maxheight``
      :return: The command
      :rtype: str

   .. py:method:: replaceitem(mode: str, slot: str, item: str, pos: str=None, target: str=None, count: int=1)

      Adds a ``replaceitem`` command.

      .. versionadded:: 0.1

      **Syntax**: *replaceitem <mode:block|entity> <pos/target> <slot> <item> [count]*

      :param str mode: ``mode:block|entity``
      :param str slot: ``slot``
      :param str item: ``item``
      :param str pos: ``pos``
      :param str target: ``target``
      :param int count: ``count``
      :return: The command
      :rtype: str

   .. py:method:: scoreboard_objectives(mode: str, objective: str=None, criterion: str=None, displayName: str=None, renderType: str=None, slot: str=None)

      Adds a ``scoreboard objectives`` command.

      .. versionadded:: 0.1

      **Syntax**: *scoreboard objectives ...*

      * *<mode:add> <objective> <criterion> [displayName]*
      * *<mode:list>*
      * *<mode:modify(_displayname)|modify(_rendertype)> <objective> ...*

        * *displayName <displayName>* when mode=modify_displayname*
        * *renderType <renderType:hearts|integer>* when mode=modify_rendertype*

      * *<mode:remove> <objective>*
      * *<mode:setdisplay> <slot> [objective]*

      :param str mode: ``mode:add|list|modify|remove|setdisplay``
      :param str objective: ``objective``
      :param str criterion: ``criterion``
      :param str displayName: ``displayName``
      :param str renderType: ``renderType``
      :param str slot: ``slot``
      :return: The command
      :rtype: str

   .. py:method:: scoreboard_players(mode: str, target: str=None, objective: str=None, score: int=None, operation: str=None, source: str=None, sourceObjective: str=None)

      Adds a ``scoreboard players`` command.

      .. versionadded:: 0.1

      **Syntax**: *scoreboard players ...*

      * *<mode:add|set|remove> <target> <objective> <score>*
      * *<mode:enable|get> <target> <objective>*
      * *<mode:reset> <target> [objective]*
      * *<mode:list> [target]*
      * *<mode:operation> <target> <objective> <operation:+=|-=|*=|/=|%=|<|>|><> <source> <sourceObjective>*

      :param str mode: ``mode:add|set|remove|enable|get|reset|list|operation``
      :param str target: ``target``
      :param str objective: ``objective``
      :param int score: ``score``
      :param str operation: ``operation:+=|-=|*=|/=|%=|<|>|><``
      :param str source: ``source``
      :param str sourceObjective: ``sourceObjective``
      :return: The command
      :rtype: str

   .. py:method:: execute(**subcommands)
      
      Adds an ``execute`` command.

      .. versionadded:: 0.1

      **Syntax:** *execute ...*

      * Key is *mode*, value is *value-NAME*, subvalue is *value.SUBVAL*, next subcommand is *-> sc*
      * *<mode:align> <value-axes> -> sc*
      * *<mode:anchored> <value-anchor:eyes|feet> -> sc*
      * *<mode:as(_)|at|positionedentity|rotatedentity> <value-target> -> sc*
      * *<mode:facing(xyz)|positionedxyz|rotatedxyz> <value-pos> -> sc*
      * *<mode:facing(entity)> entity <value.target> <value.anchor:eyes|feet> -> sc*
      * *<mode:in(_)> <value-dimension> -> sc*
      * *<mode:store> <value.store:result|success> ...*

        * *<value.mode:block> <value.pos> <value.path> <value.type:byte|short|int|long|float|double> <value.scale> -> sc*
        * *<value.mode:bossbar> <value.id> <value.value:value|max> -> sc*
        * *<value.mode:score> <value.target> <value.objective> -> sc*
        * *<value.mode:entity|storage> <value.target> <value.path> <value.type:byte|short|int|long|float|double> <value.scale> -> sc*

      * *<mode:if(_)|unless> ...*

        * *<value.mode:block> <value.pos> <value.block> -> sc*
        * *<value.mode:blocks> <value.pos1> <value.pos2> <value.destination> <value.scanMode:all|masked> -> sc*
        * *<value.mode:data> <value.check:block> <value.sourcexyz> <value.path> -> sc*
        * *<value.mode:data> <value.check:entity|storage> <value.path> -> sc*
        * *<value.mode:entity> <value.entity> -> sc*
        * *<value.mode:predicate> <value.predicate> -> sc*
        * *<value.mode:score> <value.target> <value.targetObjective> <value.comparer:<|<=|=|>|>=> <value.source> <value.sourceObjective> -> sc*
        * *<value.mode:score> <value.target> <value.targetObjective> <value.comparer:matches> <value.range> -> sc*
      * *<mode:run> <value-function> -> sc*

      **subcommands kwargs format:**

      .. code-block :: python

         align = axes: str,
         anchored = anchor: str (eyes|feet),
         as_/at = target: str,
         facingxyz = pos: str,
         facingentity = {
             "target": str,
             "anchor": str
         },
         in_ = dimension: str,
         positionedxyz/rotatedxyz = pos: str,
         positionedentity/rotatedentity = target: str,
         store = {
             "store": str (result|success),
             "mode": str (block|bossbar|entity|score|storage),
             "pos": str (when mode=block),
             "entity": str (when mode=entity,score,storage),
             "id": str (when mode=bossbar),
             "value": str (value|max when mode=bossbar),
             "objective": str (when mode=score),
             "path": str (when mode=block,entity,storage),
             "type": str (byte|short|int|long|float|double when mode=block,entity,storage),
             "scale": str (when mode=block,entity,storage)
         },
         if_/unless = {
             "mode": str (block|blocks|data|entity|predicate|score),
             "pos": str (when mode=block),
             "block": str (when mode=block),
             "pos1": str (when mode=blocks),
             "pos2": str (when mode=blocks),
             "destination": str (when mode=blocks),
             "scanMode": str (all|masked when mode=blocks),
             "check": str (block|entity|storage when mode=data),
             "sourcexyz": str (when check=block),
             "sourceentity": str (when check=entity/storage),
             "path": str (when mode=data),
             "entity": str (when mode=entity),
             "predicate": str (when mode=predicate),
             "target": str (when mode=score),
             "objective": str (when mode=score),
             "comparer": str (<|<=|=|>|>=|matches when mode=score),
             "source": str (when comparer!=matches),
             "sourceObjective": str (when comparer!=matches),
             "range": Union[int, str] (when comparer=matches)
         },
         run = function(sf): ...

      :param dict **subcommands: The subcommands to run. If the ``run`` subcommand is included, make sure it is the last kwarg.
      :returns: The command(s).
      :rtype: list or tuple or str

      .. code-block:: python
         
         import pymcfunc as pmf
         p = pmf.Pack()
    
         @p.function
         def func(f: pmf.JavaFuncHandler):
             f.r.execute(
                 as = "@e[type=sheep]",
                 run = lambda sf: say.r.say("baah")
             )

             f.r.execute(
                 as = "@e[type=cow]",
                 run = lambda sf: [
                     sf.r.say("moo")
                     sf.r.tp(destxyz="~ ~5 ~")
                 ])

             def chargeCreepers(sf: pmf.JavaFuncHandler):
                 sf.r.summon("lightning_bolt")
             f.r.execute(
                 as = "@e[type=sheep]",
                 run = chargeCreepers
             )

Coords
------

.. py:function:: coords(x: Union[Union[int, float], str], y: Union[Union[int, float], str], z: Union[Union[int, float], str])

   Translates values into coordinates, with extra validaton.

   .. note::
      It might be better to input values asking for coordinates directly in a string.
      This function is more for dynamic values.

   .. versionadded:: 0.0

   :param x: The x coordinate
   :param y: The y coordinate
   :param z: The z coordinate
   :type x: int or float or str
   :type y: int or float or str
   :type z: int or float or str
   :returns: The coordinate
   :rtype: str
   :raises CaretError: if ``^`` and ``~`` are in the same set of coordinates
   :raises CaretError: if not all coordinates have ``^``

Selectors
---------

.. py:function:: 

.. py:class:: UniversalSelectors

   The universal selector class.

   Every function has a ``**kwargs``, which is used for selector arguments. The list of selector arguemnts are in the respective specialised classes.
   If an argument is repeatable, you can express multiple values of the same argument in lists, sets, or tuples.

   .. warning::
      It is highly recommended to use either :py:class:`BedrockSelectors` or :py:class:`JavaSelectors` for your edition.

   .. versionadded:: 0.0

   .. py:method:: select(var, **kwargs)

      Returns a selector, given the selector variable and optional arguments.

      .. versionadded:: 0.0

      :param str var: The selector variable, choose from ``p, r, a, e, s``
      :param dict kwargs: The selector arguments
      :returns: The selector
      :rtype: str

   .. py:method:: nearest_player(**kwargs)
                  p(**kwargs)
      
      Alias of ``select('p', **kwargs)``.

      .. versionadded:: 0.0

   .. py:method:: random_player(**kwargs)
                  r(**kwargs)

      Alias of ``select('r', **kwargs)``.

      .. versionadded:: 0.0

   .. py:method:: all_players(**kwargs)
                  a(**kwargs)
    
      Alias of ``select('a', **kwargs)``.

      .. versionadded:: 0.0

   .. py:method:: all_entities(**kwargs)
                  e(**kwargs)

      Alias of ``select('a', **kwargs)``.

      .. versionadded:: 0.0

   .. py:method:: executor(**kwargs)
                  s(**kwargs)

      Alias of ``select('s', **kwargs)``.

      .. versionadded:: 0.0

.. py:class:: BedrockSelectors(UniversalSelectors)

   The Bedrock Edition selector class.

   * **Selector arguments (unchanged)** - x, y, z, dx, dy, dz, scores, tag, c, m, name, type, family
   * **Selector arguments (changed)**

     * lmax -> l
     * lmin -> lm
     * rmax -> r
     * rmin -> rm
     * rxmax -> rx
     * rxmin -> rxm
     * rymax -> ry
     * rymin -> rym

   * **Selector arguments (aliases)** - Argument names that set multiple vanilla values

     * l -> l lm
     * r -> r rm
     * rx -> rx rxm
     * ry -> ry rym

   * **Repeatable** - type, family

.. py:class:: JavaSelectors(UniversalSelectors)

   The Java Edition selector class.

   * **Selector arguments** - x, y, z, distance, dx, dy, dz, scores, tag, team, limit, sort, level, gamemode, name, x_rotation, y_rotation, type, nbt, advancements, predicate
   * **Repeatable** - type, tag, nbt, advancements, predicate

   .. py:method:: range(minv=0, maxv=inf)

   Returns a range of values, as it is represented in Minecraft commands.

   :param int minv: The minimum value
   :param int maxv: The maximum value
   :return: The range
   :rtype: str
   :raises ValueError: if the minimum is bigger than the maximum
   :raises ValueError: if minv is still 0 and maxv is still inf

Errors
------

.. py:currentmodule:: pymcfunc.errors

.. py:exception:: SpaceError

   No spaces are allowed in a specific parameter.

   .. versionadded:: 0.0

.. py:exception:: OptionError

   The option given is not in the list of allowed options.

   .. versionadded:: 0.0

.. py:exception:: OnlyOneAllowed

   Only one parameter is allowed, but two were given.

   .. versionadded:: 0.0

.. py:exception:: InvalidParameterError

   The parameter is invalid because another parameter is at its default value of None.

   .. versionadded:: 0.0

.. py:exception:: CaretError

   Not all coordinates of a set use '^'.

   .. versionadded:: 0.0

.. py:exception:: MissingError

   A parameter that had been made mandatory due to another parameter is not stated, and that parameter has a default value of None.

   .. versionadded: 0.1
Reference
=========
.. py:currentmodule:: pymcfunc

.. py:attribute:: __version__
   :type: str
   
   The version.

   Versions go in this format: **x.y.z**

   * **x**: Projects built for different x versions are incompatitable. If 'x' is 0, is is a development release.
   * **y**: Features have been added from the previous y version.
   * **z**: Minor bug fixes.

Syntax Guide
------------

* **<arg>** - Mandatory argument
* **[arg]** - Optional argument
* **arg1/arg2** - Pick one argument
* **arg:val1|val2** - Pick one value
* **arg1=val:arg2** - Only valid if another argument is a specific value
* **{const <arg>}** - A group

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

   .. py:attribute:: tags
      :type: dict

      The list of tags.

      .. versionadded:: 0.3

   .. py:attribute:: t
      :type: JavaFunctionTags

      An instance of a JavaFunctionTags class. Java Edition only.

      .. versionadded:: 0.3

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

   .. py:method:: build(name: str, pack_format: int, describe: str, datapack_folder: str='.')

      Builds the pack.

      .. warning::
         Java Edition only.

      .. versionadded:: 0.3

      **Format numbering**
    
      * **4** - 1.13–1.14.4
      * **5** - 1.15–1.16.1
      * **6** - 1.16.2–1.16.5
      * **7** - 1.17

      :param str name: The name of the pack
      :param int format: The format number
      :param str describe: The pack describe
      :param str datapack_folder: The directory of the datapack folder. Do not include a slash at the end
      :raises TypeError: if the pack is for Bedrock

Tags & Events
-------------

.. py:class:: JavaFunctionTags

   A container of decorators that handle tagging and events.

   .. versionadded:: 0.3

   .. warning::
      Do not instantiate JavaFunctionTags directly; use a Pack and access the commands via the 't' attribute.

   .. py:attribute:: p
      :type: Pack

      References back to the pack that it is in.

      .. versionadded:: 0.3

   .. py:decoratormethod:: tag(tag: str)

      Applies a tag to the function. When the tag is run with ``/function``, all functions under this tag will run.

      .. versionadded:: 0.3

      :param str tag: The tag name.

   .. py:decoratormethod:: on_load()

      Applies a 'load' tag to the function. Alias of ``@pmf.JavaFunctionTags.tag('load')``.

      Functions with the tag will be run when the datapack is loaded.

      .. versionadded:: 0.3

   .. py:decoratormethod:: repeat_every_tick()

      Applies a 'tick' tag to the function. Alias of ``@pmf.JavaFunctionTags.tag('tick')``.

      Functions with the tag will be run every tick.

      .. versionadded:: 0.3

   .. py:decoratormethod:: repeat_every(ticks: int)

      The function will be run on a defined interval.

      .. versionadded:: 0.3

      :param int ticks: The interval to run the function

   .. py:decoratormethod:: repeat(n: int)

      The function will be run a defined number of times. 

      .. versionadded:: 0.3

      :param int n: The number of times to run the function

Function Handlers
-----------------

.. py:currentmodule:: pymcfunc.fh

.. py:class:: UniversalFuncHandler

   The function handler that is inherited by both :py:class:`JavaFuncHandler` and :py:class:`BedrockFuncHandler`.

   This includes commands and features that are the same for both Java and Bedrock edition.

   .. warning::
      It is highly recommended to use either :py:class:`BedrockFuncHandler` or :py:class:`JavaFuncHandler` for extended support of commands for your edition.

   .. versionadded:: 0.0

   .. describe:: Operations

   * **str(a)** - Returns a linebreaked string of Minecraft commands.
   * **list(a) tuple(a)** - Returns a list of Minecraft commands.

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

   .. py:method:: clear()
      
      Clears the command list.

      .. versionadded:: 0.3

   .. py:method:: comment(comment: str)

      Adds a comment.

      .. versionadded:: 0.3

      :param str comment: The comment.

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

   .. py:method:: v(name: str, target: str)

      Creates a variable.

      .. versionadded:: 0.3

      :param str name: The name of the variable
      :param str target: Whom to create the variable for.
      :returns: The variable object
      :rtype: BedrockVariable

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

   .. py:method:: v(name: str, target: str, trigger: bool=False)

      Creates a variable.

      .. versionadded:: 0.3

      :param str name: The name of the variable
      :param str target: Whom to create the variable for.
      :param bool trigger: Whether to make the variable a trigger.
      :returns: The variable object
      :rtype: JavaVariable

Raw commands
------------

.. py:currentmodule:: pymcfunc.rawcommands

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

   .. py:method:: tellraw(target: str, message: Union[dict, list])

      Adds a ``tellraw`` command.

      .. versionadded:: 0.1

      **Syntax:** *tellraw <target> <message>*

      :param str target: ``target``
      :param message: ``message``
      :type message: dict or list[dict]
      :returns: The command
      :rtype: str

   .. py:method:: title(target: str, mode: str, text: Union[str, Union[dict, list]]=None, fadeIn: int=None, stay: int=None, fadeOut: int=None)

      Adds a ``title`` or ``titleraw`` (BE only) command.

      .. versionadded:: 0.1

      **Syntax:** *title <target> ...*
    
      * *... <mode:clear|reset>*
      * *... <mode:title|subtitle|actionbar> <text>*
      * *... <mode:times> <fadeIn> <stay> <fadeOut>*

      :param str target: ``target``
      :param str mode: ``mode:clear|reset|title|subtitle|actionbar|times``
      :param text: ``text`` (can be str in BE only)
      :type text: dict or list[dict] or str
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

   .. py:method:: replaceitem(mode: str, slotId: int, itemName: str, pos: str=None, target: str=None, slotType: str=None, itemHandling: str=None, amount: int=1, data: int=0, components: dict=None)

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

      Adds an ``execute` command.

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

      **Syntax:** *alwaysday [lock]*

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

   .. py:method:: closewebsocket()

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

   .. py:method:: gametest_clearall(radius: int=None)

      Adds a ``gametest clearall`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest [radius]*

      :param int radius: ``radius``
      :returns: The command
      :rtype: str

   .. py:method:: gametest_pos()

      Adds a ``gametest pos`` command.

      .. versionadded:: 0.2

      **Syntax:** *gametest pos*

      :returns: The command
      :rtype: str

   .. py:method:: gametest_create(name: str, width: int=None, height: int=None, depth: int=None)

      Adds a ``gametest create`` command.

      .. versionadded:: 0.2

      **Syntax:**  *gametest create <name> [width] [height] [depth]*

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

      **Syntax:** *permissions <mode:list|reload>*

      :param str mode: ``mode:list|reload``
      :returns: The command
      :rtype: str
   
   .. py:method:: playanimation(target: str, animation: str, next_state: str=None, blend_out_time: float=None, stop_expression: str=None, controller: str=None)

      Adds a ``playanimation`` command.

      .. versionadded:: 0.2

      **Syntax:** *playanimation <target> <animation> [next_state] [blend_out_time] [stop_expression] [controller]*

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

   .. py:method:: ride_summon_rider(ride: str, entity: str, event: str=None, nameTag: str=None)

      Adds a ``ride summon_riders`` command.

      .. versionadded:: 0.2

      **Syntax:** *ride <ride> summon_rider <entity> [event] [nameTag]*

      :param str ride: ``ride``
      :param str entity: ``entity``
      :param str event: ``event``
      :param str nameTag: ``nameTag``
      :returns: The command
      :rtype: str
      
   .. py:method:: ride_summon_ride(rider: str, entity: str, rideMode: str='reassign_rides', event: str=None, nameTag: str=None)

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

   .. py:method:: setmaxplayers(maxPlayers: int)

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

   .. py:method:: structure_load(name: str, pos: str, rotation: str='0_degrees', mirror: str='none', animationMode: str=None, \
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

      .. versionadded:: 0.2

      **Syntax:** *worldbuilder*

      :returns: The command
      :rtype: str

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

   .. py:method:: particle(name: str, speed: float, count: int, params: str=None, pos: str="~ ~ ~", delta: str="~ ~ ~", mode: str="normal", viewers: str=None)

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

   .. py:method:: schedule(name: str, clear: bool=False, duration: int=None, mode: str="replace")

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

        * *displayName <displayName>* when mode=modify_displayname
        * *renderType <renderType:hearts|integer>* when mode=modify_rendertype

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
      
      Adds an ``execute` command.

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
             "target": str (when mode=entity,score,storage),
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

   .. py:method:: item(mode: str, slot: str, pos: str=None, target: str=None, replaceMode: str=None, item: str=None, count: int=None, sourcexyz: str=None, sourceentity: str=None, sourceSlot: str=None, modifier: str=None)
      
      Adds an ``item`` command.

      .. versionadded:: 0.2

      **Syntax:** *item <mode:modify|replace> {block <pos>|entity <target>} <slot> ...*

      * *<modifier>* if mode=modify
      * *<replaceMode:with> <item> [count]* if mode=replace
      * *<replaceMode:from> {block <sourcexyz>|entity <sourceentity>} <sourceSlot> [modifier]* if mode=replace

      :param str mode: ``mode:modify|replace``
      :param str pos: ``pos``
      :param str target: ``target``
      :param str replaceMode: ``replaceMode:with|from``
      :param str item: ``item``
      :param int coutn: ``count``
      :param str sourcexyz: ``sourcexyz``
      :param str sourceentity: ``sourceentity``
      :param str sourceSlot: ``sourceSlot``
      :param str modifier: ``modifier``
      :returns: The command
      :rtype: str

   .. py:method:: advancement(task: str, target: str, mode: str, advancement: str=None, criterion: str=None)
      
      Adds an ``advancement`` command.

      .. versionadded:: 0.2

      **Syntax:** *advancement <task:grant|revoke> <target> ...*

      * *<mode:everything>*
      * *<mode:only> <advancement> [criterion]*
      * *<mode:from|through|until> <advancement>*
      
      :param str task: ``task:grant|revoke``
      :param str target: ``target``
      :param str mode: ``mode:everything|only|from|through|until``
      :param str advancement: ``advancement``
      :param str criterion: ``criterion``
      :returns: The command
      :rtype: str

   .. py:method:: attribute(target: str, attribute: str, mode: str, scale: int=None, uuid: str=None, name: str=None, value: str=None, addMode: str=None)

      Adds an ``attribute`` command.

      .. versionadded:: 0.2

      **Syntax:** *attribute <target> <attribute> ...*

      * *<mode:get|base(_)get> [scale]*
      * *<mode:base(_)set> <value>*
      * *<mode:modifier(_)add> <uuid> <name> <value> <addMode:add|multiply|multiply_base>*
      * *<mode:modifier(_)remove> <uuid>*
      * *<mode:modifier(_)value(_)get> <uuid> [scale]*

      :param str target: ``target``
      :param str attribute: ``attribute``
      :param str mode: ``mode:get|base(_)get|base(_)set|modifier(_)add|modifier(_)remove|modifier(_)value(_)get``
      :param int scale: ``scale``
      :param str uuid: ``uuid``
      :param str name: ``name``
      :param str value: ``value``
      :param str addMode: ``addMode:add|multiply|multiply_base``
      :returns: The command
      :rtype: str

   .. py:method:: ban(target: str, reason: str=None)

      Adds a ``ban`` command.

      .. versionadded:: 0.2

      **Syntax:** *ban <target> [reason]*

      :param str target: ``target``
      :param str reason: ``reason``
      :returns: The command
      :rtype: str

   .. py:method:: ban_ip(target: str, reason: str=None)

      Adds a ``ban-ip`` command.

      .. versionadded:: 0.2

      **Syntax:** *ban-ip <target> [reason]*

      :param str target: ``target``
      :param str reason: ``reason``
      :returns: The command
      :rtype: str

   .. py:method:: banlist(get="players")

      Adds a ``banlist`` command.

      .. versionadded:: 0.2

      **Syntax:** *banlist <get:players|ips>*

      :param str get: ``get:players|ips``
      :returns: The command
      :rtype: str

   .. py:method:: bossbar_add(barId: str, name: str)

      Adds a ``bossbar add`` command.

      .. versionadded:: 0.2

      **Syntax:** *bossbar add <barId> <name>*

      :param str barId: ``barId``
      :param str name: ``name``
      :returns: The command
      :rtype: str

   .. py:method:: bossbar_get(barId: str, get: str)

      Adds a ``bossbar get`` command.

      .. versionadded:: 0.2

      **Syntax:** *bossbar get <barId> <get:max|players|value|visible>*

      :param str barId: ``barId``
      :param str get: ``get``
      :returns: The command
      :rtype: str

   .. py:method:: bossbar_list()

      Adds a ``bossbar list`` command.

      .. versionadded:: 0.2

      **Syntax:** *bossbar list*

      :returns: The command
      :rtype: str

   .. py:method:: bossbar_remove(barId: str)

      Adds a ``bossbar remove`` command.

      .. versionadded:: 0.2

      **Syntax:** *bossbar remove <barId>*

      :param str barId: ``barId``
      :returns: The command
      :rtype: str

   .. py:method:: bossbar_set(barId: str, mode: str, color: str=None, maxv: int=None, name: str=None, target: str=None, style: str=None, value: int=None, visible: bool=None)

      Adds a ``bossbar set`` command.

      .. versionadded:: 0.2

      **Syntax:** *bossbar set <barId>*

      * *<mode:color> <color:blue|green|pink|purple|red|white|yellow>*
      * *<mode:max> <maxv>*
      * *<mode:name> <name>*
      * *<mode:players> [target]*
      * *<mode:style> <style:notched_6|notched_10|notched_12|notched_20|progress>*
      * *<mode:value> <value>*
      * *<mode:visible> <visible>*

      :param str barId: ``barId``
      :param str mode: ``mode:color|max|name|players|style|value|visible``
      :param str color: ``color:blue|green|pink|purple|red|white|yellow``
      :param str maxv: ``maxv``
      :param str name: ``name``
      :param str target: ``target``
      :param str style: ``style:notched_6|notched_10|notched_12|notched_20|progress``
      :param str value: ``value``
      :param str visible: ``visible``
      :returns: The command
      :rtype: str

   .. py:method:: data_get(block: str=None, entity: str=None, storage: str=None, path: str=None, scale: float=None)

      Adds a ``data get`` command.

      .. versionadded:: 0.2

      **Syntax:** *data get {block <pos>|entity <target>|storage <storage>} [path] [scale]*

      :param str block: ``block``
      :param str entity: ``entity``
      :param str storage: ``storage``
      :param str path: ``path``
      :param str scale: ``scale``
      :returns: The command
      :rtype: str

   .. py:method:: data_remove(path: str, block: str=None, entity: str=None, storage: str=None)

      Adds a ``data remove`` command.

      .. versionadded:: 0.2

      **Syntax:** *data remove {block <pos>|entity <target>|storage <storage>} <path>*

      :param str path: ``path``
      :param str block: ``block``
      :param str entity: ``entity``
      :param str storage: ``storage``
      :returns: The command
      :rtype: str

   .. py:method:: data_merge(nbt: dict, block: str=None, entity: str=None, storage: str=None)

      Adds a ``data merge`` command.

      .. versionadded:: 0.2

      **Syntax:** *data merge {block <pos>|entity <target>|storage <storage>} <nbt>*

      :param str nbt: ``nbt``
      :param str block: ``block``
      :param str entity: ``entity``
      :param str storage: ``storage``
      :returns: The command
      :rtype: str

   .. py:method:: data_modify(mode: str, sourceMode: str, path: str, block: str=None, entity: str=None, storage: str=None, index: str=None, sourceBlock: str=None, sourceEntity: str=None, sourceStorage: str=None, sourcePath: str=None, value: str=None)

      Adds a ``data modify`` command.

      .. versionadded:: 0.2

      **Syntax:** *data modify {block <pos>|entity <target>|storage <storage>} <path> <mode:append|insert|merge|prepend|set> <mode=insert:index> ...*

      * *<sourceMode:from> {block <sourcePos>|entity <sourceTarget>|storage <sourceStorage>} [sourcePath]*
      * *<sourceMode:value> <value>*

      :param str mode: ``mode:append|insert|merge|prepend|set``
      :param str sourceMode: ``sourceMode:from|value``
      :param str path: ``path``
      :param str block: ``block``
      :param str entity: ``entity``
      :param str storage: ``storage``
      :param str index: ``mode=insert:index``
      :param str sourceBlock: ``sourceBlock``
      :param str sourceEntity: ``sourceEntity``
      :param str sourceStorage: ``sourceStorage`` 
      :param str sourcePath: ``sourcePath``
      :param str value: ``value``
      :returns: The command
      :rtype: str

   .. py:method:: datapack(mode: str, name: str=None, priority: str=None, existing: str=None, listMode: str=None)

      Adds a ``datapack`` command.

      .. versionadded:: 0.2

      **Syntax:** *datapack ...*

      * *<mode:disable> <name>*
      * *<mode:enable> <name> [priority:first|last|before|after] [priority=before|after:existing]*
      * *<mode:list> [listMode:available|enabled]*

      :param str mode: ``mode:disable|enable|list``
      :param str name: ``name``
      :param str priority: ``priority:first|last|before|after``
      :param str existing: ``existing``
      :param str listMode: ``listMode:available|enabled``
      :returns: The command
      :rtype: str

   .. py:method:: debug(mode: str)

      Adds a ``debug`` command.

      .. versionadded:: 0.2

      **Syntax:** *debug <mode:start|stop|report|function>*

      :param str mode: ``mode:start|stop|report|function``
      :returns: The command
      :rtype: str

   .. py:method:: defaultgamemode(mode: str)

      Adds a ``defaultgamemode`` command.

      .. versionadded:: 0.2

      **Syntax:** *defaultgamemode <mode:survival|creative|adventure|spectator>*

      :param str mode: ``mode:survival|creative|adventure|spectator``
      :returns: The command
      :rtype: str

   .. py:method:: forceload(mode: str, chunk: str=None, chunk2: str=None)

      Adds a ``forceload`` command.

      .. versionadded:: 0.2

      **Syntax:** *forceload ...*

      * *<mode:add|remove> <chunk> [chunk2]*
      * *<mode:remove(_)all>*
      * *<mode:query> [chunk]*

      :param str mode: ``mode:add|remove|remove_all|query``
      :param str chunk: ``chunk``
      :param str chunk2: ``chunk2``
      :returns: The command
      :rtype: str

   .. py:method:: locatebiome(biomeId: str)

      Adds a ``locatebiome`` command.

      .. versionadded:: 0.2

      **Syntax:** *locatebiome <biomeId>*

      :param str biomeId: ``biomeId``
      :returns: The command
      :rtype: str
    
   .. py:method:: loot(targetMode: str, sourceMode: str, targetPos: str=None, targetEntity: str=None, targetSlot: str=None, \
                  targetCount: int=None, sourceLootTable: str=None, sourcePos: str=None, sourceEntity: str=None, sourceTool: str=None)
      
      Adds a ``loot`` command.

      .. versionadded:: 0.2

      **Syntax:** *loot ...*

      * *<targetMode:spawn> <targetPos>...*
      * *<targetMode:replace> {entity <targetEntity>|block <targetPos>}...*
      * *<targetMode:give> <targetEntity>...*
      * *<targetMode:insert> <targetPos>...*

      *...*

      * *<sourceMode:fish> <sourceLootTable> <sourcePos> [sourceTool]*
      * *<sourceMode:loot> <sourceLootTable>*
      * *<sourceMode:kill> <sourceEntity>*
      * *<sourceMode:mine> <sourcePos> [sourceTool]*

      :param str targetMode: ``targetMode:spawn|replace|give|insert``
      :param str targetPos: ``targetPos``
      :param str targetEntity: ``targetEntity``
      :param str targetSlot: ``targetSlot``
      :param int targetCount: ``targetCount``
      :param str sourceMode: ``sourceMode:fish|loot|kill|mine``
      :param str sourceLootTable: ``sourceLootTable``
      :param str sourcePos: ``sourcePos``
      :param str sourceEntity: ``sourceEntity``
      :param str sourceTool: ``sourceTool``
      :returns: The command
      :rtype: str

   .. py:method:: pardon(target: str, reason: str=None)

      Adds a ``pardon`` command.

      .. versionadded:: 0.2

      **Syntax:** *pardon <target> [reason]*

      :param str target: ``target``
      :param str reason: ``reason``
      :returns: The command
      :rtype: str

   .. py:method:: pardon_ip(target: str, reason: str=None)

      Adds a ``pardon-ip`` command.

      .. versionadded:: 0.2

      **Syntax:** *pardon-ip <target> [reason]*

      :param str target: ``target``
      :param str reason: ``reason``
      :returns: The command
      :rtype: str

   .. py:method:: publish(port: int)

      Adds a ``publish`` command.

      .. versionadded:: 0.2

      **Syntax:** *publish <port>*

      :param int port: ``port``
      :returns: The command
      :rtype: str

   .. py:method:: recipe(mode: str, target: str, recipe: str)

      Adds a ``recipe`` command.

      .. versionadded:: 0.2

      **Syntax:** *recipe <mode:give|take> <target> <recipe>*

      :param str mode: ``mode:give|take``
      :param str target: ``target``
      :param str recipe: ``recipe`` (can be *)
      :returns: The command
      :rtype: str

   .. py:method:: save_all(flush: bool=False)

      Adds a ``save all`` command.

      .. versionadded:: 0.2

      **Syntax:**

      * *save-all flush* if flush=True
      * *save-all* if flush=False

      :param bool flush: ``flush``
      :returns: The command
      :rtype: str

   .. py:method:: save_on()

      Adds a ``save-on`` command.

      .. versionadded:: 0.2

      **Syntax:** *save-on*

      :param bool flush: ``flush``
      :returns: The command
      :rtype: str

   .. py:method:: save_off()

      Adds a ``save-off`` command.

      .. versionadded:: 0.2

      **Syntax:** *save-off*

      :param bool flush: ``flush``
      :returns: The command
      :rtype: str

   .. py:method:: seed()

      Adds a ``seed`` command.

      .. versionadded:: 0.1

      .. versionchanged:: 0.2
         Shifted from :py:class:`UniversalRawCommands` to :py:class:`JavaRawCommands`

      **Syntax:** *seed*

      :returns: The command
      :rtype: str

   .. py:method:: setidletimeout(mins: int)

      Adds a ``setidletimeout`` command.

      .. versionadded:: 0.2

      **Syntax:** *setidletimeout <mins>*

      :param int mins: ``mins``
      :returns: The command
      :rtype: str

   .. py:method:: spectate(target: str=None, spectator: str=None)

      Adds a ``spectate`` command.

      .. versionadded:: 0.2
   
      **Syntax:** *spectate [target] [spectator]*

      :param str target: ``target``
      :param str specttaor: ``spectator``
      :returns: The command
      :rtype: str

   .. py:method:: team(mode: str, team: str=None, members: str=None, displayName: str=None, option: str=None, value=None)

      Adds a ``team`` command.

      .. versionadded:: 0.2

      **Syntax:** *team ...*

      * *<mode:add> [displayName]*
      * *<mode:empty|remove> <team>*
      * *<mode:join> <team> [members]*
      * *<mode:list> [team]*
      * *<mode:modify> [team] ...*
        
        * *<option:collisionRule> <value:always|never|pushOtherTeams|pushOwnTeam>*
        * *<option:color> <value:aqua|black|blue|gold|gray|green|light_purple|red|reset|yellow|white|dark_aqua|dark_blue|dark_gray|dark_green|dark_purle|dark_red>*
        * *<option:deathMessageVisibility|nametagVisibility> <value:always|never|hideForOtherTeams|hideForOwnTeam>*
        * *<option:friendlyFire|seeFriendlyInvisibles> <value:True|False>*
        * *<option:displayName|prefix|suffix> <value>*

      :param str mode: ``mode:add|empty|remove|join|list|team``
      :param str team: ``team``
      :param str members: ``members``
      :param str displayName: ``displayName``
      :param str option: ``option:collisionRule|color|deathMessageVisibility|nametagVisibility|friendlyFire|seeFriendlyInvisibles|displayName|prefix|suffix``
      :param str value: ``value``
      :returns: The command
      :rtype: str

   .. py:method:: teammsg(message: str)
                  tm(message: str)
      
      Adds a ``teammsg`` command.

      .. versionadded:: 0.2

      **Syntax:** *teammsg <message>*

      :param str message: ``message``
      :returns: The command
      :rtype: str

   .. py:method:: trigger(objective: str, mode: str=None, value: int=None)

      Adds a ``trigger`` command.

      .. versionadded:: 0.2

      **Syntax:** *trigger <objective> ...*

      * *<mode:(None)>*
      * *<mode:add|set> <value>*

      :param str objective: ``objective``
      :param str mode: ``mode``
      :param inr value: ``value``
      :returns: The command
      :rtype: str

   .. py:method:: worldborder_add(distance: float, duration: int=0)

      Adds a ``worldborder add`` command.

      .. versionadded:: 0.2

      **Syntax:** *worldborder add <distance> [duration]*

      :param float distance: ``distance``
      :param int duration: ``duration``
      :returns: The command
      :rtype: str

   .. py:method:: worldborder_center(pos: str)

      Adds a ``worldborder center`` command.

      .. versionadded:: 0.2

      **Syntax:** *worldborder center <pos>*

      :param str pos: ``pos``
      :returns: The command
      :rtype: str

   .. py:method:: worldborder_damage(damagePerBlock: float=None, distance: float=None)

      Adds a ``worldborder damage`` command.

      .. versionadded:: 0.2

      **Syntax:** *worldborder damage {amount <damagePerBlock>|buffer <distance>}*

      :param str damagePerBlock: ``damagePerBlock``
      :param str distance: ``distance``
      :returns: The command
      :rtype: str

   .. py:method:: worldborder_get()

      Adds a ``worldborder get`` command.

      .. versionadded:: 0.2

      **Syntax:** *worldborder get*

      :returns: The command
      :rtype: str

   .. py:method:: worldborder_set(distance: float=None, duration: int=0)

      Adds a ``worldborder set`` command.

      .. versionadded:: 0.2

      **Syntax:** *worldborder set <distance> [duration]*

      :param float distance: ``distance``
      :param int duration: ``duration``
      :returns: The command
      :rtype: str

   .. py:method:: worldborder_warning(distance: float=None, duration: int=None)

      Adds a ``worldborder warning`` command.

      .. versionadded:: 0.2

      **Syntax:** *worldborder warning {distance <distance>|time <duration>}*

      :param float distance: ``distance``
      :param int duration: ``duration``
      :returns: The command
      :rtype: str


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

Variables
---------

.. py:currentmodule:: pymcfunc.variables

.. py:class:: BedrockVariable

   Represents a variable in Bedrock Edition.

   .. warning::
      Do not instantiate BedrockVariable directly; use a FuncHandler and access the commands by calling 'v()'.
   
   .. versionadded: 0.3

   .. describe:: Operations   

      * **a += b** - Adds a value or another variable to this variable
      * **a -= b** - Subtracts a value or another variable from this variable
      * **a *= b** - Multiplies this variable by a value or another variable
      * **a /= b** - Divides this variable by a value by another variable (and rounds the result)
      * **a //= b** - ditto
      * **a %= b** - Sets this variable to the remainder of a / b
      * **del a** - Removes the variable from the scoreboard for the target(s)

   .. py:attribute:: fh
      :type: UniversalFuncHandler

      References back to the function handler that it is in.

      .. versionadded:: 0.3

   .. py:attribute:: name
      :type: str

      The name of the variable.

      .. versionadded:: 0.3

   .. py:attribute:: target
      :type: str

      The target(s) that the variable is attached to.

      .. versionadded:: 0.3

   .. py:method:: in_range(minv: int, maxv: int=None)   

      Tests a value if it is within a certain range.

      .. versionadded:: 0.3

      :param int minv: The minimum value
      :param int maxv: The maximum value

   .. py:method:: set(other: Union['BedrockVariable', int])

      Sets this variable to a value or that of another variable

      .. versionadded:: 0.3

      :param other: The other value or variable
      :type other: BedrockVariable or int

   .. py:method:: random(minv: int, maxv: int=None)

      Sets this variable to a random number.

      .. versionadded:: 0.3

      :param int minv: The minimum value
      :param int maxv: The maximum value

   .. py:method:: higher(other: 'BedrockVariable')

      Sets this variable to the higher of the two variables.

      .. versionadded:: 0.3

      :param BedrockVariable other: The other variable

   .. py:method:: lower(other: 'BedrockVariable')

      Sets this variable to the lower of the two variables.

      .. versionadded:: 0.3

      :param BedrockVariable other: The other variable

   .. py:method:: swap(other: 'BedrockVariable')

      Swaps the value of the two variables.

      .. versionadded:: 0.3

      :param BedrockVariable other: The other variable

   .. py:method:: show(slot: str, sortOrder: str=None)

      Shows the variable in a slot.

      .. versionadded:: 0.3

      :param str slot: The slot to show it in.
      :param str sortOrder: The sort order, if ``slot`` is ``list`` or ``sidebar``

.. py:class:: JavaVariable

   Represents a variable in Java Edition.

   .. warning::
      Do not instantiate JavaVariable directly; use a FuncHandler and access the commands by calling 'v()'.
   
   .. versionadded: 0.3

   .. describe:: Operations   

      * **a += b** - Adds a value or another variable to this variable
      * **a -= b** - Subtracts a value or another variable from this variable
      * **a *= b** - Multiplies this variable by a value or another variable
      * **a /= b** - Divides this variable by a value by another variable (and rounds the result)
      * **a //= b** - ditto
      * **a %= b** - Sets this variable to the remainder of a / b
      * **a == b** - Returns a dict for use in :py:meth:`JavaRawCommands.execute`
      * **a > b** - ditto
      * **a >= b** - ditto
      * **a < b** - ditto
      * **a <= b** - ditto
      * **del a** - Removes the variable from the scoreboard for the target(s)

      **Comparers example**
      
      .. code-block:: python

         f.r.execute(
             if_=var1 > var2
         )

   .. py:attribute:: fh
      :type: UniversalFuncHandler

      References back to the function handler that it is in.

      .. versionadded:: 0.3

   .. py:attribute:: name
      :type: str

      The name of the variable.

      .. versionadded:: 0.3

   .. py:attribute:: target
      :type: str

      The target(s) that the variable is attached to.

      .. versionadded:: 0.3

   .. py:method:: in_range(r: Union[str, int])

      For use in :py:meth:`JavaRawCommands.execute`. Finds whether this variable is in a specified range.

      .. versionadded:: 0.3

      :param r: The range. Can be a range or a single number.
      :type r: str or int
      :returns: The dict for use in ``if_`` or ``unless``.
      :rtype: dict

      .. code-block:: python

         f.r.execute(
             unless=var1.in_range('3..4'),
             if_=var2.in_range('7')
         )
    
   .. py:method:: store(mode: str)

       For use in :py:meth:`JavaRawCommands.execute`. Stores a result or success in this variable.

       .. versionadded:: 0.3

       :param str mode: Must be either ``result`` or ``success``.
       :returns: The dict for use in ``store``.
       :rtype: dict

       .. code-block:: python

         f.r.execute(
             store=var.store('result')
         )

   .. py:method:: set(other: Union['JavaVariable', int])

      Sets this variable to a value or that of another variable

      .. versionadded:: 0.3

      :param other: The other value or variable
      :type other: JavaVariable or int

   .. py:method:: higher(other: 'JavaVariable')

      Sets this variable to the higher of the two variables.

      .. versionadded:: 0.3

      :param JavaVariable other: The other variable

   .. py:method:: lower(other: 'JavaVariable')

      Sets this variable to the lower of the two variables.

      .. versionadded:: 0.3

      :param JavaVariable other: The other variable

   .. py:method:: swap(other: 'JavaVariable')

      Swaps the value of the two variables.

      .. versionadded:: 0.3

      :param JavaVariable other: The other variable

   .. py:method:: show(slot: str)

      Shows the variable in a slot.

      .. versionadded:: 0.3

      :param str slot: The slot to show it in.

Entities
--------

.. py:currentmodule:: pymcfunc.ent

.. py:class:: Entity

   An entity object. This will reference and control entities that match a selector.

   .. warning::
      Do not instantiate Entity directly; use a FuncHandler and access the commands by calling `entity()`

   .. versionadded:: 0.4

   .. py:attribute:: fh
      :type: FunctionHandler

      The function handler that this object is a part of.

      .. versionadded:: 0.4

   .. py:attribute:: target
      :type: str

      The target used to select the entities.

      .. versionadded:: 0.4

   .. py:method:: __init__(fh, target: str)

      Initialises the entity.

      .. versionadded:: 0.4

      :param UniversalFunctionHandler fh: The function handler that the object is a part of
      :param str target: The target used to select the entities

   .. py:method:: display_name(name: str)

      Sets the display name of the entities.

      .. versionadded:: 0.4

      :param str name: The name to display.

   .. py:method:: data_set_value(attr: str, val: Any)

      Sets an NBT data value.

      .. versionadded:: 0.4

      :param str attr: The attribute key.
      :param Any val: The value.

   .. py:method:: pitch(val: float)
      
      Rotates the entity, such that it is rotating vertically.

      .. versionadded:: 0.4

      :param float val: The value to pitch it by.

   .. py:method:: yaw(val: float)
      
      Rotates the entity, such that it is rotating horizontally.

      .. versionadded:: 0.4

      :param float val: The value to yaw it by.

   .. py:method:: move(destxyz: Optional[str]=None, destentity: Optional[str]=None, **kwargs)

      Moves the entity.

      .. versionadded:: 0.4

      :param str destxyz: The coordinates to move to
      :param str destentity: The selector for the entity to move to
      :param **kwargs: Additional parameters for the tp command

   .. py:method:: force(axis: str, velocity: float)

      Apply force to the entity.

      .. versionadded:: 0.4

      :param str axis: The axis in which the force is applied on
      :param float velocity: The velocity of the force
      
   .. py:method:: remove()

      Remove the entity.

      .. versionadded:: 0.4

.. py:class:: Mob(Entity)

   A special type of entity, for mobs.

   .. versionadded:: 0.4

   .. py:method:: set_armour_slot(slot: str, item_id: str, count: int=1, tag: Optional[dict]=None)

      Sets the armour slot of the mob.

      .. versionadded:: 0.4

      :param str slot: The slot to set. Can be one of `feet`, `legs`, `chest`, `head`
      :param str item_id: The ID of the armour
      :param int count: The count of the armour
      :param dict tag: Tags for the armour

   .. py:method:: remove_armour_slot(slot: str)

      Removes armour from an armour slot.

      .. versionadded:: 0.4

      :param str slot: The slot to set. Can be one of `feet`, `legs`, `chest`, `head`
      

Selectors
---------

.. py:currentmodule:: pymcfunc.sel

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

.. py:method:: cuboid(pos1: Sequence[int], pos2: Sequence[int], dims: str='xyz')

   Finds the northwest-bottommost corner and the volume/area/length of a cuboid, area or line, given two corners.

   This function is mainly for selector arguments, namely x, y, z, dx, dy and dz.

   .. versionadded:: 0.3

   :param Sequence[int] pos1: The first corner
   :param Sequence[int] pos2: The second corner
   :param str dims: The axes to find. Can be any combination of x, y and z, but no repeating.
   
   .. code-block:: python
      
      >>> import pymcfunc as pmf
      >>> pmf.sel.cuboid((1,2,3),(4,5,6))
      {'x': 1, 'dx': 3, 'y': 2, 'dy': 3, 'z': 3, 'dz': 3}
      >>> s = pmf.JavaSelectors()
      >>> s.all_entities(**pmf.sel.cuboid((1,2,3),(4,5,6)))
      '@e[x=1,dx=3,y=2,dy=3,z=3,dz=3]'

Raw JSON text
-------------
.. py:currentmodule:: pymcfunc.rt

.. py:function:: java(text: str, format_symbol: str="§", content_symbol: str="¶")

   Converts a string of text into Java raw JSON text.

   .. versionadded:: 0.3

   **Formatting symbols**

   * **§#XXXXXX** - Hex code
   * **§0-9, a-f** - Colours
   * **§h[text]** - Extras to append after the segment of text
   * **§i[text]** - String to be inserted into chat when clicked
   * **§j[text]** - Sets the font
   * **§k** - Obfuscate
   * **§l** - Bold
   * **§m** - Strikethrough
   * **§n** - Underline
   * **§o** - Italics
   * **§p[url]** - Opens URL when text is clicked
   * **§q[file]** - Opens file (might not work) when text is clicked
   * **§r** - Reset all formatting
   * **§s[command]** - Sends a command to chat input / runs the command when text is clicked
   * **§t[value]** - Appends a value to chat input when text is clicked
   * **§u[page]** - Changes the page in books when text is clicked
   * **§v[value]** - Copies value to clipboard when text is clicked
   * **§w[text]** - Shows text when text is hovered
   * **§xX** - Removes formatting of X
   * **§y[item id|optional count|optional tag]** - Shows item when hovered
   * **§z[entity type|entity uuid|optional entity name]** - Shows entity when hovered

   **Content symbols**

   * **¶t[identifier|params...|...]** - Translated text
   * **¶s[name|objective|optional value]** - Value from scoreboard
   * **¶e[selector|optional separator text]** - Entity name
   * **¶k[identifier]** - Keybind
   * **¶n[path|type|val|optional interpret|optional separator text]** - NBT value (choose 'type' from block, entity, storage, 'interpet' from true, false)

   :param str text: The text
   :param str format_symbol: The format symbol, defaults to §
   :param str content_symbol: The content symbol, defaults to ¶
   :returns: The JSON text
   :rtype: list[dict] or dict

.. py:function:: bedrock(text: str, content_symbol: str="¶")

   Converts a string of text into Bedrock raw JSON text.

   .. versionadded:: 0.3

   **Content symbols**

   * **¶t[identifier|params...|...]** - Translated text
   * **¶s[name|objective|optional value]** - Value from scoreboard
   * **¶e[selector|optional separator text]** - Entity name

   :param str text: The text
   :param str content_symbol: The content symbol, defaults to ¶
   :returns: The JSON text
   :rtype: list[dict] or dict

Advancements
------------

.. py:currentmodule:: pymcfunc.advancements

.. py:class:: Advancement
   
   An advancement in Java Edition.

   .. versionadded:: 0.4
   
   .. py:attribute:: p
      :type: Pack

      References back to the pack that it is in.

      .. versionadded:: 0.4

   .. py:attribute:: name
      :type: str

      The name of the advancement.

      .. versionadded:: 0.4

   .. py:attribute:: namespaced
      :type: str

      The namespaced name of the advancement.

      .. versionadded:: 0.4

   .. py:attribute:: value
      :type: dict

      The value of the advancement as a reference to ``advancements[name]`` in the pack.

      .. versionadded:: 0.4

   .. py:method:: __init__(p, name: str, parent: Union[str, 'Advancement'])

      Initialises the advancement.

      .. versionadded:: 0.4

      :param Pack p: The pack that the advancement is attached to
      :param str name: The name of the pack
      :param parent: The parent of the advancement
      :type parent: str or Advancement

   .. py:method:: set_icon(item_name: str, nbt: Optional[dict]=None)

      Sets the icon of the advancement.

      .. versionadded:: 0.4

      :param str item_name: The name of the item
      :param dict nbt: The NBT data of the item.

   .. py:method:: set_display(attr: str, value: Any)
      
      Sets display parameters for the advancement.

      * **attr: type(val)**
      * icon:
      * title: 
      * frame: 
      * background:
      * description:
      * show_toast: bool
      * announce_to_chat: bool
      * hidden: bool

      .. versionadded:: 0.4

      :param str attr: The attribute name
      :param Any value: The value for the attribute

   .. py:method:: set_parent(parent: Union[str, 'Advancement'])

      Sets the parent for the advancement.

      .. versionadded:: 0.4

      :param parent: The parent of the advancement
      :type parent: str or Advancement

   .. py:method:: criterion(name: str)

      Creates and returns a new criterion for the advancement.

      .. versionadded:: 0.4

      :param str name: The name of the criterion.
      :return: The criterion.
      :rtype: Criterion

   .. py:method:: set_requirements(*criterion_lists: List[Union[str, 'Criterion']])

      Sets the requirements for the advancement.
    
      .. versionadded:: 0.4
      
      :param *criterion_lists: Made of params that are lists of criterion names (AND list of OR lists)
      :type *criterion_lists: List[str or Criterion]

   .. py:method:: reward(item: str, value: Any)

      Sets the reward for the advancement.

      * **item: type(value)**
      * recipes: str
      * loot: str
      * experience: int
      * function: str

      .. versionadded:: 0.4
      
      :param str item: The reward type that is set
      :param Any value: The value for the reward type

   .. py:decoratormethod:: on_reward()

      The function with the tag will be called when the achievement is gotten.

      .. versionadded:: 0.4

.. py:class:: Criterion

   A criterion for an advancement.

   .. warning::
      Do not instantiate this class directly, access it in :py:class:`Achievement` via `criterion()`.

   .. versionadded:: 0.4

   Note: RangeDicts come in the form of ``{"min": num, "max": num}``

   .. py:attribute:: name
      :type: str

      The name of the criterion.

      .. versionadded:: 0.4

   .. py:attribute:: ach
      :type: str

      The achievement that this criterion is under.

      .. versionadded:: 0.4
 
   .. py:attribute:: value
      :type: dict

      The value of the criterion as a reference to ``advancements[ach_name]['criteria'][criterion_name]`` in the pack.

      .. versionadded:: 0.4

   .. py:method:: __init__(ach, name: str)
      
      Initialises the criterion.

      .. versionadded:: 0.4

      :param Achievement ach: The achievement that the criterion is under
      :param str name: The name of the criterion.

   .. py:method:: bee_nest_destroyed(block: Optional[str]=None, item: Optional[dict]=None, num_bees_inside: Optional[int]=None, player: Optional[Union[List[str], dict]]=None)
      
      Sets the criterion's trigger to ``bee_nest_destroyed``.

      .. versionadded:: 0.4

      :param str block: The block that is destroyed
      :param str item: The item used to destroy the block
      :param int num_bees_inside: The number of bees inside the block
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: bred_animals(child: Optional[Union[List[str], dict]]=None, parent: Optional[Union[List[str], dict]]=None, partner: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``bred_animals``

      .. versionadded:: 0.4

      :param child: Tags for the child, or list of predicates
      :type child: List[str] or dict
      :param parent: Tags for the parent, or list of predicates
      :type parent: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: brewed_potion(potion: Optional[str]=None, player: Optional[Union[List[str], dict]]=None)
      
      Sets the criterion's trigger to ``brewed_potion``

      .. versionadded:: 0.4

      :param str potion: The potion brewed
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: changed_dimension(from_: Optional[str]=None, to: Optional[str]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``changed_dimension``

      .. versionadded:: 0.4

      :param str from_: The dimension that the player came from, can be one of ``overworld``, ``the_nether``, ``the_end``
      :param str to: The dimension that the player went to, can be one of ``overworld``, ``the_nether``, ``the_end``
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: channeled_lightning(*victims: Union[List[str], dict], player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``chanelled_lightning``

      .. versionadded:: 0.4

      :param *victims: Tags for the victims, or list of predicates
      :type *victims: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: construct_beacon(level: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``construct_beacon``.

      .. versionadded:: 0.4

      :param level: The level of the beacon. Can be exact value or range
      :type level: int or RangeDict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: consume_item(item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``consume_item``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item consumed
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: cured_zombie_villager(villager: Optional[Union[List[str], dict]]=None, zombie: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``cured_zombie_villager``.

      .. versionadded:: 0.4

      :param villager: Tags for the villager, or list of predicates
      :type villager: List[str] or dict
      :param zombie: Tags for the zombie, or list of predicates
      :type zombie: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: effects_changed(source: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``effects_changed``. Used together with :py:meth:`effects_changed_effect`

      .. versionadded:: 0.4

      :param source: Tags for the source, or list of predicates
      :type source: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: effects_changed_effect(effect_name: Optional[str]=None, amplifier: Optional[Union[int, RangeDict]]=None, duration: Optional[Union[int, RangeDict]]=None)

      An effect, for when the criterion is ``effects_changed``. Used together with :py:meth:`effects_changed`

      .. versionadded:: 0.4

      :param str effect_name: The name of the effect
      :param amplifier: The amplifier of the effect
      :type amplfier: int or RangeDict
      :param duration: The duration of the effect
      :type duration: int or RangeDict

   .. py:method:: enchanted_item(item: Optional[dict]=None, levels: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``enchanted_item``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item enchanted
      :param levels: The number of levels enchanted. Can be exact value or range
      :type levels: int or RangeDict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: enter_block(block: Optional[str]=None, state: Optional[Dict[str, str]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``enter_block``.

      .. versionadded:: 0.4

      :param str block: The block entered
      :param dict state: The states of the block, given in key: value pairs
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: entity_hurt_player(damage: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``entity_hurt_player``.

      .. versionadded:: 0.4

      :param dict damage: Tags for damage
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: entity_killed_player(entity: Optional[Union[List[str], dict]]=None, killing_blow: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``entity_killed_player``.

      .. versionadded:: 0.4

      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param dict killing_blow: Tags for killing blow
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: filled_bucket(item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

       Sets the criterion's trigger to ``entity_killed_player``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item filled
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: fishing_rod_hooked(entity: Optional[Union[List[str], dict]]=None, item: Optional[dict]=None, rod: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``fishing_rod_hooked``.

      .. versionadded:: 0.4

      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param dict item: Tags for the item caught
      :param dict rod: Tags for the rod
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: hero_of_the_village(location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``hero_of_the_village``.

      .. versionadded:: 0.4

      :param dict location: Tags for the location
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: impossible()

      Sets the criterion's trigger to ``impossible``.

      .. versionadded:: 0.4

   .. py:method:: inventory_changed(*items: dict, empty_slots: Optional[Union[int, RangeDict]]=None, full_slots: Optional[Union[int, RangeDict]]=None, occupied_slots: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``impossible``.

      .. versionadded:: 0.4

      :param dict *items: A list of tags for items
      :param empty_slots: The number of empty slots. Can be an exact value or range
      :type empty_slots: int or RangeDict
      :param full_slots: The number of full slots. Can be an exact value or range
      :type full_slots: int or RangeDict
      :param occupied_slots: The number of occupied slots. Can be an exact value or range
      :type occupied_slots: int or RangeDict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: item_durability_changed(delta: Optional[Union[int, RangeDict]]=None, durability: Optional[Union[int, RangeDict]]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``item_durability_changed``.

      .. versionadded:: 0.4

      :param delta: The amount of durability gained/lost. Can be an exact value or range
      :type delta: int or RangeDict
      :param durability: The durability of the item. Can be an exact value or range
      :type durability: int or RangeDict
      :param dict item: Tags for the item
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: item_used_on_block(location: Optional[dict]=None, item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``item_used_on_block``.

      .. versionadded:: 0.4

      :param dict location: Tags for the location of the block
      :param dict item: Tags for the item
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: killed_by_crossbow(*victims: Union[List[str], dict], unique_entity_types: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``item_used_on_block``.

      .. versionadded:: 0.4

      :param victims: A list of tags for the victims, or lists of predicates
      :type victims: List[str] or dict
      :param unique_entity_types: The number of unique types of entities that are victims. Can be an exact value or range.
      :type unique_entity_types: int or RangeDict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: levitation(absolute_distance: Optional[RangeDict]=None, horizontal_distance: Optional[RangeDict]=None, x_distance: Optional[RangeDict]=None, y_distance: Optional[RangeDict]=None, \
                             z_distance: Optional[RangeDict]=None, duration: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``levitation``.

      .. versionadded:: 0.4

      :param RangeDict absolute_distance: The absolute distance levitated
      :param RangeDict horizontal_distance: The horizontal distance levitated
      :param RangeDict x_distance: The distance in the x axis levitated
      :param RangeDict y_distance: The distance in the y axis levitated
      :param RangeDict z_distance: The distance in the z axis levitated
      :param duration: The duration levitated. Can be an exact value or range.
      :type duration: int or RangeDict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: lightning_strike(lightning: Optional[Union[List[str], dict]]=None, bystander: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``lightning_strike``.

      .. versionadded:: 0.4

      :param lightning: Tags for the lightning, or list of predicates
      :type lightning: List[str] or dict
      :param bystander: Tags for the bystander, or list of predicates
      :type bystander: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: location(location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)
      
      Sets the criterion's trigger to ``location``.

      .. versionadded:: 0.4

      :param dict location: Tags for the location
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict
    
   .. py:method:: nether_travel(entered: Optional[dict]=None, exited: Optional[dict]=None, absolute_distance: Optional[RangeDict]=None, horizontal_distance: Optional[RangeDict]=None, \
                                x_distance: Optional[RangeDict]=None, y_distance: Optional[RangeDict]=None, z_distance: Optional[RangeDict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``nether_travel``.

      .. versionadded:: 0.4

      :param dict entered: Tags for the entered
      :param dict exited: Tags for the exited
      :param RangeDict absolute_distance: The absolute distance travelled
      :param RangeDict horizontal_distance: The horizontal distance travelled
      :param RangeDict x_distance: The distance in the x axis travelled
      :param RangeDict y_distance: The distance in the y axis travelled
      :param RangeDict z_distance: The distance in the z axis travelled
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: placed_block(block: Optional[str]=None, item: Optional[dict]=None, location: Optional[dict]=None, state: Optional[Dict[str, str]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``placed_block``.

      .. versionadded:: 0.4

      :param str block: The block placed
      :param dict item: Tags for the item used
      :param dict location: Tags for the location of the block
      :param dict state: The states of the block, given in key: value pairs
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dic

   .. py:method:: player_generates_container_loot(loot_table: Optional[str]=None, player: Optional[Union[List[str], dict]]=None)
      
      Sets the criterion's trigger to ``player_generates_container_loot``.

      .. versionadded:: 0.4

      :param str loot_table: The resource location of the loot table used.
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: player_hurt_entity(damage: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``player_hurt_entity``.

      .. versionadded:: 0.4

      :param dict damage: Tags for damage
      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: player_interacted_with_entity(item: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``player_interacted_with_entity``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item used
      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: player_killed_entity(entity: Optional[Union[List[str], dict]]=None, killing_blow: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``player_killed_entity``.

      .. versionadded:: 0.4

      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param dict killing_blow: Tags for killing blow
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: recipe_unlocked(recipe: Optional[str]=None, player: Optional[Union[List[str], dict]]=None)
      
      Sets the criterion's trigger to ``recipe_unlocked``.

      .. versionadded:: 0.4

      :param str recipe: The recipe unlocked
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: shot_crossbow(item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``shot_crossbow``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item used
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: slept_in_bed(location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``slept_in_bed``.

      .. versionadded:: 0.4

      :param dict location: Tags for the location
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: slide_down_block(block: Optional[str]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``slept_in_bed``.

      .. versionadded:: 0.4

      :param str block: The block slid down on
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: start_riding(player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``slept_in_bed``.

      .. versionadded:: 0.4

      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: summoned_entity(entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)
      
      Sets the criterion's trigger to ``slept_in_bed``.

      .. versionadded:: 0.4

      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict
    
   .. py:method:: tame_animal(entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``tame_animal``.

      .. versionadded:: 0.4

      :param entity: Tags for the entity, or list of predicates
      :type entity: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: target_hit(signal_strength: Optional[int]=None, projectile: Optional[str]=None, shooter: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``target_hit``.

      .. versionadded:: 0.4

      :param int signal_strength: The signal strength output by the target block
      :param str projectile: The projectile
      :param shooter: Tags for the shooter, or list of loot tables
      :type shooter: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: thrown_item_picked_up_by_entity(item: Optional[dict]=None, entity: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``thrown_item_picked_up_by_entity``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item picked up
      :param entity: Tags for the entity, or list of loot tables
      :type entity: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: tick(player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``thrown_item_picked_up_by_entity``.

      .. versionadded:: 0.4

      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: used_ender_eye(distance: Optional[Union[int, RangeDict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``used_ender_eye``.

      .. versionadded:: 0.4

      :param distance: The distance travelled by the ender eye. Can be an exact value or range
      :type distance: int or RangeDict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: used_totem(item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)
     
      Sets the criterion's trigger to ``used_totem``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item used
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: using_item(item: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``using_item``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item used
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: villager_trade(item: Optional[dict]=None, villager: Optional[Union[List[str], dict]]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``villager_trade``.

      .. versionadded:: 0.4

      :param dict item: Tags for the item traded
      :param villager: Tags for the villager, or list of predicates
      :type villager: List[str] or dict
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

   .. py:method:: voluntary_exile(location: Optional[dict]=None, player: Optional[Union[List[str], dict]]=None)

      Sets the criterion's trigger to ``voluntary_exile``.

      .. versionadded:: 0.4

      :param dict location: Tags for the locaton
      :param player: Tags for the player, or list of predicates
      :type player: List[str] or dict

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
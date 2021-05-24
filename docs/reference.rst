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
         def mcfuncjava(f: pmf.JavaFuncHandler):
             f.say('a')
             # youf commands here...

      .. versionadded:: 0.0

Function Handlers
-----------------

.. py:class:: UniversalFuncHandler

   The function handler that is inherited by both :py:class:`JavaFuncHandler` and :py:class:`BedrockFuncHandler`.

   This includes commands that are the same for both Java and Bedrock edition.

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

.. py:class:: BedrockFuncHandler(UniversalFuncHandler)

   The Beckrock Edition function handler.

   .. py:attribute:: sel
   :type: BedrockSelectors

      A Selectors object.
      
      .. versionadded:: 0.0

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

.. py:class:: JavaFuncHandler(UniversalFuncHandler)

   The Java Edition function handler.

   .. py:attribute:: sel
   :type: JavaSelectors

      A Selectors object.
      
      .. versionadded:: 0.0

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

.. py:exception:: OptionError

   The option given is not in the list of allowed options.

.. py:exception:: OnlyOneAllowed

   Only one parameter is allowed, but two were given.

.. py:exception:: InvalidParameterError

   The parameter is invalid because another parameter is at its default value of None.

.. py:exception:: CaretError

   Not all coordinates of a set use '^'.
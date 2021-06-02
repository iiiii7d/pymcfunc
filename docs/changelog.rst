Changelog
=========

* **v0.2 ()**

  * Added /advancement, /attribute, /ban, /ban-ip, /banlist, /bossbar, /data, /datapack, /debug,
    /defaultgamemode, /forceload, /locatebiome, /loot, /pardon, /pardon-ip, /publish, /recipe, /save-all,
    /save-on, /save-off, /setidletimeout, /spectate, /team, /teammsg, /trigger, /worldborder in JavaRawCommands
  * Added /ability, /agent, /alwaysday, /camerashake, /changesetting, /clearspawnpoint, /closewebsocket, /connect,
    /event, /fog, /gametest, /getchunkdata, /getchunks, /getspawnpoint, /globalpause, /immutableworld, /listd,
    /mobevent, /music, /permissions, /playanimation, /querytarget, /ride, /save, /setmaxplayers, /structure, /testfor,
    /testforblock, /testforblocks, /tickingarea, /toggledownfall, /worldbuilder in BedrockRawCommands
  * basically added all the other commands (except for Edu Edition commands)
  * moved /seed from UniversalRawCommands to JavaRawCommands

* **v0.1 (28/5/21)**

  * Added /gamemode, /gamerule, /seed, /summon, /clear, /tellraw, /teleport, /experience,
    /effect, /enchant, /setworldspawn, /spawnpoint, /function, /locate, /time, /particle, /schedule,
    /playsound, /stopsound, /weather, /difficulty, /kick, /deop, /op, /list, /reload, /me, /tag,
    /spreadplayers, /replaceitem, /whitelist, /stop, /scoreboard, /execute

    * and all aliases
    * basically those that are in both versions (but might not have same functionality though)

* **v0.0 (24/5/21)**

  * Added Pack, FuncHandlers, Selectors, coords
  * Added support for /say, /help, /tell, /w, /msg, /kill, /setblock, /fill, /clone, /give
  * Added all selectors & arguments
  * Added ``pymcfunc.coords()``
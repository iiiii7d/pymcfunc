import json
import re

import pymcfunc.errors as errors
import pymcfunc.internal as internal
from pymcfunc.func_handler_universal import UniversalFuncHandler, UniversalRawCommands
from pymcfunc.selectors import JavaSelectors

class JavaFuncHandler(UniversalFuncHandler):
    """The Java Edition function handler.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler"""
    sel = JavaSelectors()

    def __init__(self):
        self.commands = []
        self.r = JavaRawCommands(self)

class JavaRawCommands(UniversalRawCommands):
    def setblock(self, pos: str, block: str, mode="replace"):
        """**Syntax:** *setblock <pos> <block> [mode:destroy|keep|replace]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        optionals = internal.defaults((mode, "replace"))

        cmd = f"setblock {pos} {block} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, block: str, mode="replace", filterPredicate: str=None):
        """**Syntax:** *fill <pos1> <pos2> <block> [mode:destroy|hollow|keep|outline|replace] [mode=replace:filterPredicate]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.fill"""
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace' and filterPredicate != None:
            raise errors.InvalidParameterError(mode, 'mode', filterPredicate, 'filterPredicate')
        optionals = internal.defaults((mode, "replace"), (filterPredicate, None))

        cmd = f"fill {pos1} {pos2} {block} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", filterPredicate: str=None, cloneMode: str="normal"):
        """**Syntax:** *clone <pos1> <pos2> <dest> [maskMode:replace|masked] <maskMode=masked:filterPredicate> [cloneMode:force|move|normal]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.clone"""
        internal.options(maskMode, ['masked', 'filtered', 'replace'])
        internal.options(cloneMode, ['forced', 'move', 'normal'])
        if maskMode != 'filtered' and filterPredicate != None:
            raise errors.InvalidParameterError(maskMode, 'maskMode', filterPredicate, 'filterPredicate')
        if maskMode == 'filtered' and filterPredicate != None:
            optionals = f"filtered {filterPredicate} " + internal.defaults((cloneMode, "normal"))
        else:
            optionals = internal.defaults((maskMode, "replace"), (cloneMode, "normal"))
        
        cmd = f"clone {pos1} {pos2} {dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def give(self, target: str, item: str, count: int=1):
        """**Syntax:** *give <target> <item> [count]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((count, 1))

        cmd = f"give {target} {item} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def summon(self, entity: str, pos: str="~ ~ ~", nbt: dict=None):
        """**Syntax:** *summon <entity> [pos] [nbt]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.summon"""
        nbt = json.dumps(nbt) if isinstance(nbt, dict) else nbt
        optionals = internal.defaults((pos, "~ ~ ~"), (nbt, None))

        cmd = f"summon {entity} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clear(self, target: str="@s", item: str=None, maxCount: int=None):
        """**Syntax:** *clear [target] [item] [maxCount]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.clear"""
        internal.reliant('item', maxCount, None, 'data', maxCount, None)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (maxCount, None))

        cmd = f"clear {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def teleport(self, destentity: str=None, destxyz: str=None, target: str="@s", rotation: str=None, faceMode: str=None, facing: str=None, anchor: str="eyes"):
        """**Syntax:** *teleport <target> ...* / *teleport ...*
        * *<destentity>*
        * *<destxyz> [rotation]*
        * *<destxyz> facing <facing>* when faceMode=entity
        * *<destxyz> facing entity <facing> [anchor:eyes|feet]* when faceMode=location\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.teleport"""
        internal.check_spaces('target', target)
        dest = internal.pick_one_arg((destentity, None, 'destentity'), (destxyz, None, 'destxyz'), optional=False)
        target = "" if target == "@s" else target+" "
        internal.check_invalid_params('entity', 'faceMode', faceMode, ('anchor', anchor, "eyes"))
        internal.reliant('destxyz', destxyz, None, 'rotation', rotation, None)
        internal.reliant('destxyz', destxyz, None, 'faceMode', faceMode, None)
        if destentity == None:
            if faceMode != None:
                internal.options(faceMode, ['location', 'entity'])
                if facing == None:
                    raise ValueError("facing must not be None if faceMode is specified")
                internal.options(anchor, ['eyes', 'feet'])
                faceMode = "facing" if faceMode == "location" else "facing entity"
                optionals = f"{faceMode} {facing} {internal.defaults((anchor, 'eyes'))}"
            else:
                optionals = ""
        else:
            optionals = ""

        cmd = f"teleport {target}{dest} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    tp = teleport

    def experience(self, mode: str, target: str="@s", amount: int=None, measurement="points"):
        """**Syntax:** *experience ...*
        * *<mode\:add|set> <target> <amount> [measurement:levels|points]*
        * *<mode\:query> <target> <measurement\:levels|points>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.experience"""
        internal.options(measurement, ['points', 'levels'])
        internal.options(mode, ['add', 'set', 'query'])
        internal.multi_check_invalid_params(['add', 'set'], "mode", mode, ("amount", amount, None))
        if mode != "query" and amount == None:
            raise ValueError("amount must not be None if mode is add or set")
        amount = "" if amount == None else str(amount)+" "
        if mode != "query": measurement = internal.defaults((measurement, 'points'))
        cmd = f"experience {mode} {target} {amount}{measurement}".strip()
        self.fh.commands.append(cmd)
        return cmd
    xp = experience
        
    def effect_give(self, target: str, effect: str, seconds: int=30, amplifier: int=0, hideParticles: bool=False):
        """**Syntax:** *effect give <target> <effect> [seconds] [amplifier] [hideParticles]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.effect_give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((seconds, 30), (amplifier, 0), (hideParticles, False))

        cmd = f"effect give {target} {effect} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def effect_clear(self, target: str="@s", effect: str=None):
        """**Syntax:** *effect clear [target] [effect]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.effect_clear"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((effect, None))

        cmd = f"effect clear {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def setworldspawn(self, pos: str="~ ~ ~", angle: str=None):
        """**Syntax:** *setworldspawn [pos] [angle]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spawnpoint"""
        optionals = internal.defaults((pos, "~ ~ ~"), (angle, None))

        cmd = f"setworldspawn {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spawnpoint(self, target: str="@s", pos: str="~ ~ ~", angle: str=None):
        """**Syntax:** *spawnpoint [target] [pos] [angle]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spawnpoint"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((pos, "~ ~ ~"), (angle, None))

        cmd = f"spawnpoint {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    
    def particle(self, name: str, speed: float, count: int, params: str=None, pos: str="~ ~ ~", delta: str="~ ~ ~", mode: str="normal", viewers: str=None):
        """**Syntax:** *particle <name> [params] [pos] [delta] <speed> <count> [mode:force|normal] [viewers]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.particle"""
        optionals = internal.defaults((mode, "normal"), (viewers, None))
        if params != None:
            name = f"{name} {params}"
        cmd = f"particle {name} {pos} {delta} {speed} {count} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def schedule(self, name: str, clear: bool=False, duration: str=None, mode: str="replace"):
        """**Syntax:** *schedule ...*
        * *function <name> <duration> [mode:append|replace]*
        * *clear <name>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.schedule"""
        internal.check_invalid_params(False, 'clear', clear, ('duration', duration, None), dep_mandatory=True)
        if clear:
            cmd = f"schedule clear {name}".strip()
        else:
            optionals = internal.defaults((mode, 'replace'))
            cmd = f"schedule function {name} {duration} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def playsound(self, sound: str, source: str, target: str, pos: str="~ ~ ~", volume: float=1.0, pitch: float=1.0, minVolume: float=None):
        """**Syntax:** *playsound <sound> <source\:master|music|record|weather|block|hostile|neutral|player|ambient|voice> <targets> <pos> <volume> <pitch> <minVolume>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.playsound"""
        internal.check_spaces('target', target)
        internal.options(source, ['master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice'])
        optionals = internal.defaults((pos, "~ ~ ~"), (volume, 1.0), (pitch, 1.0), (minVolume, None))
        
        cmd = f"playsound {sound} {source} {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def stopsound(self, target: str, source: str="*", sound: str=None):
        """**Syntax:** *stopsound <target> [source:master|music|record|weather|block|hostile|neutral|player|ambient|voice] [sound]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.stopsound"""
        internal.check_spaces('target', target)
        internal.options(source, ['master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice', '*'])
        optionals = internal.defaults((source, "*"), (sound, None))

        cmd = f"stopsound {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def weather(self, mode: str, duration: str=5):
        """**Syntax:** *weather <mode\:clear|rain|thunder> [duration]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.weather"""
        internal.options(mode, ['clear', 'rain', 'thunder'])
        cmd = f"weather {mode} {duration}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def difficulty(self, difficulty: str=None):
        """**Syntax:** *difficulty <difficulty>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.difficulty"""
        if difficulty == None:
            cmd = "difficulty"
        else:
            internal.options(difficulty, ['easy', 'hard', 'normal', 'peaceful', 'e', 'h', 'n', 'p'])
        cmd = f"difficulty {difficulty}"
        self.fh.commands.append(cmd)
        return cmd

    def list_(self, uuid: bool=False):
        """**Syntax** *list* if uuid=False; *list uuid* if uuid=True\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.list_"""
        cmd = "list" if not uuid else "list uuid"
        self.fh.commands.append(cmd)
        return cmd

    def spreadplayers(self, center: str, dist: float, maxRange: float, respectTeams: bool, target: str, maxHeight: float=None):
        """**Syntax**: *spreadplayers <center> <dist> <maxRange> ...*
        * *<respectTeams> <targets>*
        * *under <maxHeight> <respectTeams>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spreadplayers"""
        if maxHeight != None:
            maxHeight = "under "+maxHeight+" "
        else:
            maxHeight = ""
        cmd = f"spreadplayers {center} {dist} {maxRange} {maxHeight}{respectTeams} {target}"
        self.fh.commands.append(cmd)
        return cmd

    def replaceitem(self, mode: str, slot: str, item: str, pos: str=None, target: str=None, count: int=1):
        """**Syntax**: *replaceitem <mode\:block|entity> <pos/target> <slot> <item> [count]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.replaceitem"""
        internal.options(mode, ['block', 'entity'])
        internal.check_invalid_params('block', 'mode', mode,
            ('pos', pos, None),
            dep_mandatory=True)
        internal.check_invalid_params('entity', 'mode', mode,
            ('target', target, None),
            dep_mandatory=True)

        pos_target = target if target != None else pos
        optionals = internal.defaults((count, 1))
        cmd = f"replaceitem {mode} {pos_target} {slot} {item} {optionals}"
        self.fh.commands.append(cmd)
        return cmd

    def scoreboard_objectives(self, mode: str, objective: str=None, criterion: str=None, displayName: str=None, renderType: str=None, slot: str=None):
        """**Syntax**: *scoreboard objectives ...*
        * *<mode\:add> <objective> <criterion> [displayName]*
        * *<mode\:list>*
        * *<mode\:modify(_displayname)|modify(_rendertype)> <objective> ...*
          * *displayName <displayName>* when mode=modify_displayname*
          * *renderType <renderType\:hearts|integer>* when mode=modify_rendertype*
        * *<mode\:remove> <objective>*
        * *<mode\:setdisplay> <slot> [objective]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.scoreboard_objectives"""
        internal.options(mode, ['add', 'list', 'modify_displayname', 'modify_rendertype', 'remove', 'setdisplay'])
        internal.multi_check_invalid_params(['add', 'modify_displayname', 'modify_rendertype', 'remove', 'setdisplay'], 'mode', mode, ('objective', objective, None))
        if mode != 'setdisplay' and objective == None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode, ('criterion', criterion, None), dep_mandatory=True)
        internal.multi_check_invalid_params(['add', 'modify_displayname'], 'mode', mode, ('displayName', displayName, None))
        if mode != 'add' and displayName == None:
            raise errors.MissingError('displayName', 'mode', mode)
        internal.check_invalid_params('modify_rendertype', 'mode', mode, ('renderType', renderType, None), dep_mandatory=True)
        if renderType != None:
            internal.options(renderType, ['hearts', 'integer'])
        internal.check_invalid_params('setdisplay', 'mode', mode, ('slot', slot, None), dep_mandatory=True)

        if mode == "list":
            suffix = ""
        elif mode == "add":
            optionals = internal.defaults((displayName, None))
            suffix = f"{objective} {criterion} {optionals}"
        elif mode == "modify_displayname":
            suffix = f"{objective} displayName {displayName}"
        elif mode == "modify_rendertype":
            suffix = f"{objective} renderType {renderType}"
        elif mode == "remove":
            suffix = objective
        elif mode == "setdisplay":
            optionals = internal.defaults((objective, None))
            suffix = f"{slot} {objective}"

        cmd = f"scoreboard objectives {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def scoreboard_players(self, mode: str, target: str=None, objective: str=None, score: int=None, operation: str=None, source: str=None, sourceObjective: str=None):
        """**Syntax**: *scoreboard players ...*
        * *<mode\:add|set|remove> <target> <objective> <score>*
        * *<mode\:enable|get> <target> <objective>*
        * *<mode\:reset> <target> [objective]*
        * *<mode\:list> [target]*
        * *<mode\:operation> <target> <objective> <operation:+=|-=|*=|/=|%=|<|>|><> <source> <sourceObjective>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.scoreboard_players"""
        internal.options(mode, ['add', 'enable', 'get', 'list', 'operation', 'remove', 'reset', 'set'])
        if mode in ['add', 'enable', 'get', 'operation', 'remove', 'reset', 'set'] and target == None:
            raise errors.MissingError('target', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'enable', 'get', 'operation', 'remove', 'reset', 'set'], 'mode', mode, ('objective', objective, None))
        if mode in ['add', 'enable', 'get', 'operation', 'remove', 'set'] and objective == None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'remove', 'set'], 'mode', mode, ('score', score, None), dep_mandatory=True)
        internal.check_invalid_params('operation', 'mode', mode, 
            ('operation', operation, None),
            ('source', source, None),
            ('sourceObjective', sourceObjective, None),
            dep_mandatory=True)
        if operation != None:
            internal.options(operation, ['+=', '-=', '*=', '/=', '%=', '<', '>', '><'])

        if mode == "add":
            suffix = f"{target} {objective} {score}"
        elif mode == "enable" or mode == "get":
            suffix = f"{target} {objective}"
        elif mode == "list":
            optionals = internal.defaults((target, None))
            suffix = optionals
        elif mode == "operation":
            suffix = f"{target} {objective} {operation} {source} {sourceObjective}"
        elif mode == "remove" or mode == "set":
            suffix = f"{target} {objective} {score}"
        elif mode == "reset":
            optionals = internal.defaults((objective, None))
            suffix = f"{target} {optionals}"

        cmd = f"scoreboard objectives {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def execute(self, **subcommands):
        """
        **Syntax:** *execute ...*
        * Key is *mode*, value is *value-NAME*, subvalue is *value.SUBVAL*, next subcommand is *-> sc*
        * *<mode\:align> <value-axes> -> sc*
        * *<mode\:anchored> <value-anchor\:eyes|feet> -> sc*
        * *<mode\:as(_)|at|positionedentity|rotatedentity> <value-target> -> sc*
        * *<mode\:facing(xyz)|positionedxyz|rotatedxyz> <value-pos> -> sc*
        * *<mode\:facing(entity)> entity <value.target> <value.anchor\:eyes|feet> -> sc*
        * *<mode\:in(_)> <value-dimension> -> sc*
        * *<mode\:store> <value.store\:result|success> ...*
          * *<value.mode\:block> <value.pos> <value.path> <value.type\:byte|short|int|long|float|double> <value.scale> -> sc*
          * *<value.mode\:bossbar> <value.id> <value.value\:value|max> -> sc*
          * *<value.mode\:score> <value.target> <value.objective> -> sc*
          * *<value.mode\:entity|storage> <value.target> <value.path> <value.type\:byte|short|int|long|float|double> <value.scale> -> sc*
        * *<mode\:if(_)|unless> ...*
          * *<value.mode\:block> <value.pos> <value.block> -> sc*
          * *<value.mode\:blocks> <value.pos1> <value.pos2> <value.destination> <value.scanMode\:all|masked> -> sc*
          * *<value.mode\:data> <value.check\:block> <value.sourcexyz> <value.path> -> sc*
          * *<value.mode\:data> <value.check\:entity|storage> <value.path> -> sc*
          * *<value.mode\:entity> <value.entity> -> sc*
          * *<value.mode\:predicate> <value.predicate> -> sc*
          * *<value.mode\:score> <value.target> <value.targetObjective> <value.comparer:<|<=|=|>|>=> <value.source> <value.sourceObjective> -> sc*
          * *<value.mode\:score> <value.target> <value.targetObjective> <value.comparer\:matches> <value.range> -> sc*
        * *<mode\:run> <value-function> -> sc*

        **subcommands kwargs format:
        ```
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
        positionedentity/rotatedxyz = target: str,
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
        run = function(sf): ...```\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.execute
        """
        if "run" in subcommands.keys() and list(subcommands.keys()).index('run') != len(subcommands.keys())-1:
            raise ValueError("'run' subcommand must be last subcommand")
        
        class subcommandhandler:
            @staticmethod
            def s_align(v):
                if not re.search(r"^(?!.*(.).*\1)[xyz]+$", v):
                    raise ValueError(f"Axes are invalid (Got '{v}')")
                return v+" "
            
            @staticmethod
            def s_anchor(v):
                internal.options(v, ['eyes', 'feet'])
                return v+" "

            @staticmethod
            def s_as_(v):
                internal.check_spaces('as', v)
                return v+" "
            @staticmethod
            def s_at(v):
                internal.check_spaces('at', v)
                return v+" "

            @staticmethod
            def s_facingxyz(v):
                return v+" "
            @staticmethod
            def s_facingentity(v):
                internal.options(v['anchor'], ['eyes', 'feet'])
                return f"entity {v['target']} {v['anchor']} "

            s_in_ = s_facingxyz
            s_positionedxyz = s_facingxyz
            s_rotatedxyz = s_facingxyz

            @staticmethod
            def s_positionedentity(v):
                internal.check_spaces('positionedentity', v)
                return f"as {v} "
            s_rotatedentity = s_positionedentity

            @staticmethod
            def s_store(v):
                internal.options(v['store'], ['result', 'success'])
                internal.options(v['mode'], ['block', 'bossbar', 'entity', 'score', 'storage'])
                prefix = f"{v['store']} {v['mode']}"
                if 'type' in v.keys():
                    internal.options(v['type'], ['byte', 'short', 'int', 'long', 'float', 'double'])
                if v['mode'] == 'block':
                    return f"{prefix} {v['pos']} {v['path']} {v['type']} {v['scale']} "
                elif v['mode'] == 'bossbar':
                    internal.options(v['value'], ['max', 'value'])
                    return f"{prefix} {v['id']} {v['value']} "
                elif v['mode'] in ['entity', 'storage']:
                    return f"{prefix} {v['target']} {v['path']} {v['type']} {v['scale']} "
                elif v['mode'] == 'score':
                    return f"{prefix} {v['target']} {v['objective']} "

            @staticmethod
            def s_if_(v):
                internal.options(v['mode'], ['block', 'blocks', 'data', 'entity', 'predicate', 'score'])
                prefix = v['mode']
                if v['mode'] == "block":
                    return f"{prefix} {v['pos']} {v['block']} "
                elif v['mode'] == "blocks":
                    return f"{prefix} {v['pos1']} {v['pos2']} {v['dest']} {v['scanMode']} "
                elif v['mode'] == "entity":
                    return f"{prefix} {v['entity']} "
                elif v['mode'] == "predicate":
                    return f"{prefix} {v['predicate']} "
                elif v['mode'] == "data":
                    internal.options(v['check'], ['block', 'entity', 'storage'])
                    source_sourcePos = v['sourcePos'] if v['check'] == 'block' else v['source']
                    return f"{prefix} {v['check']} {source_sourcePos} {v['path']} "
                elif v['mode'] == "score":
                    internal.options(v['comparer'], ['<', '<=', '=', '>', '>=', 'matches'])
                    internal.check_spaces('target', v['target'])
                    if v['comparer'] == "range":
                        return f"{prefix} matches {v['range']} "
                    else:
                        return f"{prefix} {v['comparer']} {v['source']} {v['sourceObjective']} "
            s_unless = s_if_

            @staticmethod
            def s_run(v):
                return ""


        cmd = "execute "
        for k, v in subcommands.items():
            scn = k if not k.endswith("_") else k[:-1]
            if scn.endswith("xyz") or scn.endswith("entity"):
                scn = scn.replace("xyz", "").replace("entity", "")
            cmd += scn + " " + getattr(subcommandhandler, 's_'+k)(v)

        if 'run' in subcommands.keys():
            sf = JavaFuncHandler()
            result = subcommands['run'](sf)
            if isinstance(result, (list, tuple)):
                result = map(lambda j: (cmd+j).strip(), result)
                self.fh.commands.extend(result)
                return result
            elif isinstance(result, str):
                self.fh.commands.append((cmd+result).strip())
                return result
            else:
                result = sf.commands
                result = map(lambda j: (cmd+j).strip(), result)
                self.fh.commands.extend(result)
                return result
            

        else:
            self.fh.commands.append(cmd.strip())
            return cmd.strip()

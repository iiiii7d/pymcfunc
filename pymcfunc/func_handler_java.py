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
        if mode != 'replace' and filterPredicate is not None:
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
        if maskMode != 'filtered' and filterPredicate is not None:
            raise errors.InvalidParameterError(maskMode, 'maskMode', filterPredicate, 'filterPredicate')
        if maskMode == 'filtered' and filterPredicate is not None:
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
        if destentity is None:
            if faceMode is not None:
                internal.options(faceMode, ['location', 'entity'])
                if facing is None:
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
        if mode != "query" and amount is None:
            raise ValueError("amount must not be None if mode is add or set")
        amount = "" if amount is None else str(amount)+" "
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
        if params is not None:
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
        if difficulty is None:
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
        if maxHeight is not None:
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

        pos_target = target if target is not None else pos
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
        if mode != 'setdisplay' and objective is None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode, ('criterion', criterion, None), dep_mandatory=True)
        internal.multi_check_invalid_params(['add', 'modify_displayname'], 'mode', mode, ('displayName', displayName, None))
        if mode != 'add' and displayName is None:
            raise errors.MissingError('displayName', 'mode', mode)
        internal.check_invalid_params('modify_rendertype', 'mode', mode, ('renderType', renderType, None), dep_mandatory=True)
        if renderType is not None:
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
        if mode in ['add', 'enable', 'get', 'operation', 'remove', 'reset', 'set'] and target is None:
            raise errors.MissingError('target', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'enable', 'get', 'operation', 'remove', 'reset', 'set'], 'mode', mode, ('objective', objective, None))
        if mode in ['add', 'enable', 'get', 'operation', 'remove', 'set'] and objective is None:
            raise errors.MissingError('objective', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'remove', 'set'], 'mode', mode, ('score', score, None), dep_mandatory=True)
        internal.check_invalid_params('operation', 'mode', mode, 
            ('operation', operation, None),
            ('source', source, None),
            ('sourceObjective', sourceObjective, None),
            dep_mandatory=True)
        if operation is not None:
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

    def item(self, mode: str, slot: str, pos: str=None, target: str=None, replaceMode: str=None, item: str=None, count: int=None, sourcexyz: str=None, sourceentity: str=None, sourceSlot: str=None, modifier: str=None):
        """**Syntax:** *item <mode\:modify|replace> {block <pos>|entity <target>} <slot> ...*
        * *<modifier>* if mode=modify
        * *<replaceMode\:with> <item> [count]* if mode=replace
        * *<replaceMode\:from> {block <sourcexyz>|entity <sourceentity>} <sourceSlot> [modifier]* if mode=replace\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.item"""
        internal.options(mode, ['modify', 'replace'])
        if mode == "modify" and modifier is None:
            raise errors.MissingError('modifier', 'mode', mode)
        
        internal.check_invalid_params('replace', 'mode', mode,
            ('replaceMode', replaceMode, None))
        if replaceMode is not None:
            internal.options(replaceMode, ['from', 'with'])
        internal.check_invalid_params('with', 'replaceMode', replaceMode,
            ('item', item, None),
            dep_mandatory=True)
        internal.check_invalid_params('with', 'replaceMode', replaceMode,
            ('count', count, None))
        internal.check_invalid_params('from', 'replaceMode', replaceMode,
            ('sourceSlot', sourceSlot, None),
            dep_mandatory=True)
        internal.check_invalid_params('from', 'replaceMode', replaceMode,
            ('sourceSlot', sourceSlot, None))

        target_pos = internal.pick_one_arg((target, None, 'target'), (pos, None, 'pos'), optional=False)
        
        target_pos = ("block " if pos is not None else "entity ") + target_pos
        

        if mode == "modify":
            suffix = modifier
        elif replaceMode == "with":
            optionals = internal.defaults((count, None))
            suffix = f"with {item} {optionals}"
        else:
            source = internal.pick_one_arg((sourcexyz, None, 'sourcexyz'), (sourceentity, None, 'sourceentity'), optional=True)
            source = ("block " if sourcexyz is not None else "entity ") + source
            optionals = internal.defaults((modifier, None))
            suffix = f"from {source} {sourceSlot} {optionals}"

        cmd = f"item {mode} {target_pos} {slot} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def advancement(self, task: str, target: str, mode: str, advancement: str=None, criterion: str=None):
        """**Syntax:** *advancement <task\:grant|revoke> <target> ...*
        * *<mode\:everything>*
        * *<mode\:only> <advancement> [criterion]*
        * *<mode\:from|through|until> <advancement>*\n
        https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.advancement"""
        internal.options(task, ['grant', 'revoke'])
        internal.options(mode, ['everything', 'only', 'from', 'through', 'until'])
        internal.multi_check_invalid_params(['only', 'from', 'through', 'until'], 'mode', mode, 
            ('advancement', advancement, None),
            dep_mandatory=True)
        internal.check_invalid_params('only', 'mode', mode, ('criterion', criterion, None))
        
        if mode == "everything":
            suffix = ""
        else:
            optionals = internal.defaults((criterion, None))
            suffix = f"{advancement} {optionals}"
        cmd = f"advancement {task} {target} {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def attribute(self, target: str, attribute: str, mode: str, scale: int=None, uuid: str=None, name: str=None, value: str=None, addMode: str=None):
        """**Syntax:** *attribute <target> <attribute> ...*
        * *<mode\:get|base(_)get> [scale]*
        * *<mode\:base(_)set> <value>*
        * *<mode\:modifier(_)add> <uuid> <name> <value> <addMode\:add|multiply|multiply_base>
        * *<mode\:modifier(_)remove> <uuid>
        * *<mode\:modifier(_)value(_)get> <uuid> [scale]\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.attribute"""
        internal.options(mode, ['get', 'base_get', 'base_set', 'modifier_add', 'modifier_remove', 'modifier_value_get'])
        internal.multi_check_invalid_params(['get', 'base_get', 'modifier_value_get'], 'mode', mode,
            ('scale', scale, None))
        internal.multi_check_invalid_params(['modifier_add', 'modifier_remove', 'modifier_value_get'], 'mode', mode,
            ('uuid', uuid, None),
            dep_mandatory=True)
        internal.check_invalid_params('modifier_add', 'mode', mode,
            ('name', name, None),
            ('addMode', addMode, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['base_set', 'modifier_add'], 'mode', mode,
            ('value', value, None),
            dep_mandatory=True)
        if addMode is not None:
            internal.options(addMode, ['add', 'multiply', 'multiply_base'])
        
        if mode == "modifier_add":
            suffix = f"{uuid} {name} {value} {addMode}"
        elif mode in ['modifier_remove', 'modifier_value_get']:
            optionals = internal.defaults((scale, None))
            suffix = f"{uuid} {optionals}"
        elif mode in ['get', 'base_get']:
            suffix = internal.defaults((scale, None))
        elif mode == "base_set":
            suffix = value
        mode = mode.replace('_', ' ')
        cmd = f"attribute {target} {attribute} {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ban(self, target: str, reason: str=None):
        """**Syntax:** *ban <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.ban"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((reason, None))
        cmd = f"ban {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def ban_ip(self, target: str, reason: str=None):
        """**Syntax:** *ban-ip <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.ban_ip"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((reason, None))
        cmd = f"ban-ip {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def banlist(self, get="players"):
        """**Syntax:** *banlist <get\:players|ips>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.banlist"""
        internal.options(get, ['ips', 'players'])
        optionals = internal.defaults((get, "players"))
        cmd = f"banlist {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_add(self, barId: str, name: str):
        """**Syntax:** *bossbar add <barId> <name>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_add"""
        cmd = f"bossbar add {barId} {name}"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_get(self, barId: str, get: str):
        """**Syntax:** *bossbar get <barId> <get\:max|players|value|visible>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_get"""
        internal.options(get, ['max', 'players', 'value', 'visible'])
        cmd = f"bossbar get {barId} {get}"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_list(self):
        """**Syntax:** *bossbar list*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_list"""
        cmd = "bossbar list"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_remove(self, barId: str):
        """**Syntax:** *bossbar remove <barId>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_remove"""
        cmd = f"bossbar remove {barId}"
        self.fh.commands.append(cmd)
        return cmd

    def bossbar_set(self, barId: str, mode: str, color: str=None, maxv: int=None, name: str=None, target: str=None, style: str=None, value: int=None, visible: bool=None):
        """**Syntax:** *bossbar set <barId>*
        * *<mode\:color> <color\:blue|green|pink|purple|red|white|yellow>*
        * *<mode\:max> <maxv>*
        * *<mode\:name> <name>*
        * *<mode\:players> [target]*
        * *<mode\:style> <style\:notched_6|notched_10|notched_12|notched_20|progress>*
        * *<mode\:value> <value>*
        * *<mode\:visible> <visible>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.bossbar_set"""
        internal.options(mode, ['color', 'max', 'name', 'players', 'style', 'value', 'visible'])
        internal.check_invalid_params('color', 'mode', mode,
            ('color', color, None),
            dep_mandatory=True)
        if color is not None:
            internal.options(color, ['blue', 'green', 'pink', 'purple', 'red', 'white', 'yellow'])
        internal.check_invalid_params('max', 'mode', mode,
            ('maxv', maxv, None),
            dep_mandatory=True)
        internal.check_invalid_params('name', 'mode', mode,
            ('name', name, None),
            dep_mandatory=True)
        internal.check_invalid_params('players', 'mode', mode,
            ('target', target, None))
        internal.check_invalid_params('style', 'mode', mode,
            ('style', style, None),
            dep_mandatory=True)
        if style is not None:
            internal.options(style, ['notched_6', 'notched_10', 'notched_12', 'notched_20', 'progress'])
        internal.check_invalid_params('value', 'mode', mode,
            ('value', value, None),
            dep_mandatory=True)
        internal.check_invalid_params('visible', 'mode', mode,
            ('visible', visible, None),
            dep_mandatory=True)

        v = internal.pick_one_arg(
            (color, None, 'color'),
            (maxv, None, 'maxv'),
            (name, None, 'name'),
            (target, None, 'target'),
            (style, None, 'style'),
            (value, None, 'value'),
            (visible, None, 'visible')
        )
        cmd = f"bossbar set {barId} {mode} {v}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_get(self, block: str=None, entity: str=None, storage: str=None, path: str=None, scale: float=None):
        """**Syntax:** *data get {block <pos>|entity <target>|storage <storage>} [path] [scale]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_get"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        internal.reliant('path', path, None, 'scale', scale, None)
        optionals = internal.defaults((path, None), (scale, None))

        cmd = f"data get {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_remove(self, path: str, block: str=None, entity: str=None, storage: str=None):
        """**Syntax:** *data remove {block <pos>|entity <target>|storage <storage>} <path>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_remove"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        cmd = f"data get {target} {path}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_merge(self, nbt: dict, block: str=None, entity: str=None, storage: str=None):
        """**Syntax:** *data merge {block <pos>|entity <target>|storage <storage>} <nbt>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_merge"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        cmd = f"data merge {target} {json.dumps(nbt)}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def data_modify(self, mode: str, sourceMode: str, path: str, block: str=None, entity: str=None, storage: str=None, index: str=None, sourceBlock: str=None, sourceEntity: str=None, sourceStorage: str=None, sourcePath: str=None, value: str=None):
        """**Syntax:** *data modify {block <pos>|entity <target>|storage <storage>} <path> <mode\:append|insert|merge|prepend|set> <mode=insert:index> ...*
        * *<sourceMode\:from> {block <sourcePos>|entity <sourceTarget>|storage <sourceStorage>} [sourcePath]*
        * *<sourceMode\:value> <value>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.data_modify"""
        target = internal.pick_one_arg(
            (block, None, 'block'),
            (entity, None, 'entity'),
            (storage, None, 'storage'),
            optional=False
        )
        source = internal.pick_one_arg(
            (sourceBlock, None, 'block'),
            (sourceEntity, None, 'entity'),
            (sourceStorage, None, 'storage')
        )
        internal.options(mode, ['append', 'insert', 'merge', 'prepend', 'set'])
        internal.check_invalid_params('insert', 'mode', mode,
            ('index', index, None),
            dep_mandatory=True)
        internal.options(sourceMode, ['from', 'value'])
        internal.check_invalid_params('from', 'sourceMode', sourceMode,
            ('source', source, None),
            dep_mandatory=True)
        internal.check_invalid_params('from', 'sourceMode', sourceMode,
            ('sourcePath', sourcePath, None))
        internal.check_invalid_params('value', 'sourceMode', sourceMode,
            ('value', value, None))
        
        if sourceMode == "from":
            optionals = internal.defaults((sourcePath, None))
            suffix = f"{source} {optionals}"
        else:
            suffix = value
        if mode == "index":
            mode = f"{mode} {index}"
        target = ('block ' if block is not None else 'entity ' if entity is not None else 'storage') + target
        source = ('block ' if sourceBlock is not None else 'entity ' if sourceEntity is not None else 'storage') + source
        cmd = f"data modify {target} {path} {mode} {sourceMode} {suffix}"
        self.fh.commands.append(cmd)
        return cmd

    def datapack(self, mode: str, name: str=None, priority: str=None, existing: str=None, listMode: str=None):
        """**Syntax:** *datapack ...*
        * *<mode\:disable> <name>*
        * *<mode\:enable> <name> [priority:first|last|before|after] [priority=before|after:existing]*
        * *<mode\:list> [listMode:available|enabled]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.datapack"""
        internal.options(mode, ['disable', 'enable', 'list'])
        internal.multi_check_invalid_params(['disable', 'enable'], 'mode', mode,
            ('name', name, None),
            dep_mandatory=True)
        internal.check_invalid_params('enable', 'mode', mode,
            ('priority', priority, None),
            dep_mandatory=None)
        if priority is not None:
            internal.options(priority, ['first', 'last', 'before', 'after'])
        internal.multi_check_invalid_params(['before', 'after'], 'priority', priority,
            ('existing', existing, None),
            dep_mandatory=True)
        internal.check_invalid_params('list', 'mode', listMode,
            ('listMode', listMode, None),
            dep_mandatory=True)
        if listMode is not None:
            internal.options(listMode, ['available', 'ended'])

        if mode == "list":
            suffix = listMode
        elif mode == "disable":
            suffix = name
        else:
            optionals = internal.defaults((priority, None), (existing, None))
            suffix = f"{name} {optionals}"
        cmd = f"datapack {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def debug(self, mode: str):
        """**Syntax:** *debug <mode\:start|stop|report|function>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.debug"""
        internal.options(mode, ['start', 'stop', 'report', 'function'])
        cmd = f"debug {mode}"
        self.fh.commands.append(cmd)
        return cmd

    def defaultgamemode(self, mode: str):
        """**Syntax:** *defaultgamemode <mode\:survival|creative|adventure|spectator>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.defaultgamemode"""
        internal.options(mode, ['survival', 'creative', 'adventure', 'spectator'])
        cmd = f"defaultgamemode {mode}"
        self.fh.commands.append(cmd)
        return cmd

    def forceload(self, mode: str, chunk: str=None, chunk2: str=None):
        """**Syntax:** *forceload ...*
        * *<mode\:add|remove> <chunk> [chunk2]*
        * *<mode\:remove(_)all>*
        * *<mode\:query> [chunk]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.forceload"""
        internal.options(mode, ['add', 'remove', 'remove_all', 'query'])
        internal.multi_check_invalid_params(['add', 'remove', 'query'], 'mode', mode,
            ('chunk', chunk, None))
        if mode in ['add', 'remove'] and chunk is None:
            raise errors.MissingError('chunk', 'mode', mode)
        internal.multi_check_invalid_params(['add', 'remove'], 'mode', mode,
            ('chunk2', chunk2, None))

        if mode == "remove_all":
            suffix = ""
        elif mode == "query":
            suffix = internal.defaults((chunk, None))
        else:
            optionals = internal.defaults((chunk2, None))
            suffix = f"{chunk} {optionals}"

        mode = mode.replace('_', ' ')
        cmd = f"forceload {mode} {suffix}"
        self.fh.commands.append(cmd)
        return cmd

    def locatebiome(self, biomeId: str):
        """**Syntax:** *locatebiome <biomeId>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.locatebiome"""
        cmd = f"locatebiome {biomeId}"
        self.fh.commands.append(cmd)
        return cmd
    
    def loot(self, targetMode: str, sourceMode: str, targetPos: str=None, targetEntity: str=None, targetSlot: str=None, \
             targetCount: int=None, sourceLootTable: str=None, sourcePos: str=None, sourceEntity: str=None, sourceTool: str=None):
        """ **Syntax:** *loot ...*

        * *<targetMode\:spawn> <targetPos>...*
        * *<targetMode\:replace> {entity <targetEntity>|block <targetPos>}...*
        * *<targetMode\:give> <targetEntity>...*
        * *<targetMode\:insert> <targetPos>...*\n
        *...*
        * *<sourceMode\:fish> <sourceLootTable> <sourcePos> [sourceTool]*
        * *<sourceMode\:loot> <sourceLootTable>*
        * *<sourceMode\:kill> <sourceEntity>*
        * *<sourceMode\:mine> <sourcePos> [sourceTool]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.loot"""
        internal.options(targetMode, ['spawn', 'replace', 'give', 'insert'])
        internal.multi_check_invalid_params(['spawn', 'replace', 'insert'], 'targetMode', targetMode,
            ('targetPos', targetPos, None))
        if targetMode in ['spawn', 'insert'] and targetPos is None:
            raise errors.MissingError('targetPos', 'targetMode', targetMode)
        internal.multi_check_invalid_params(['give', 'replace'], 'targetMode', targetMode,
            ('targetEntity', targetEntity, None))
        if targetMode == 'give' and targetEntity is None:
            raise errors.MissingError('targetEntity', 'targetMode', targetMode)
        internal.check_invalid_params('replace', 'targetMode', targetMode,
            ('targetSlot', targetSlot, None),
            dep_mandatory=True)
        internal.check_invalid_params('replace', 'targetMode', targetMode,
            ('targetCount', targetCount, None))
        targetPosEntity = internal.pick_one_arg(
            (targetPos, None, 'targetPos'),
            (targetEntity, None, 'targetEntity')
        )
        targetPosEntity = ('block ' if targetPos is not None else 'entity ') + targetPosEntity

        if targetMode in ['spawn', 'insert']:
            target = f"{targetMode}, {targetPos}".strip()
        elif targetMode == "give":
            target = f"{targetMode} {targetEntity}".strip()
        else:
            optionals = internal.defaults((targetCount, None))
            target = f"{targetMode} {targetPosEntity} {targetSlot} {optionals}".strip()

        internal.multi_check_invalid_params(['fish', 'loot'], 'sourceMode', sourceMode,
            ('sourceLootTable', sourceLootTable, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['fish', 'mine'], 'sourceMode', sourceMode,
            ('sourcePos', sourcePos, None),
            dep_mandatory=True)
        internal.check_invalid_params('kill', 'sourceMode', sourceMode,
            ('sourceEntity', sourceEntity, None),
            dep_mandatory=True)
        internal.multi_check_invalid_params(['fish', 'mine'], 'sourceMode', sourceMode,
            ('sourceTool', sourceTool, None))

        if sourceMode == 'fish':
            optionals = internal.defaults((sourceTool, None))
            source = f"{sourceMode} {sourceLootTable} {sourcePos} {optionals}".strip()
        elif sourceMode == 'loot':
            source = f"{sourceMode} {sourceLootTable}".strip()
        elif sourceMode == 'kill':
            source = f"{sourceMode} {sourceEntity}".strip()
        else:
            optionals = internal.defaults((sourceTool, None))
            source = f"{sourceMode} {optionals}".strip()

        cmd = f"loot {target} {source}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def pardon(self, target: str, reason: str=None):
        """**Syntax:** *pardon <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.pardon"""
        internal.check_spaces('target', target)
        cmd = f"pardon {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def pardon_ip(self, target: str, reason: str=None):
        """**Syntax:** *pardon-ip <target> [reason]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.pardon_ip"""
        internal.check_spaces('target', target)
        cmd = f"pardon-ip {target}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def publish(self, port: int):
        """**Syntax:** *publish <port>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.publish"""
        cmd = f"publish {port}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def recipe(self, mode: str, target: str, recipe: str):
        """**Syntax:** *recipe <mode\:give|take> <target> <recipe>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.recipe"""
        internal.options(mode, ['give', 'take'])
        internal.check_spaces('target', target)
        cmd = f"recipe {mode} {target} {recipe}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def save_all(self, flush: bool=False):
        """**Syntax:**
        * *save-all flush* if flush=True
        * *save-all* if flush=False\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.save_all"""
        if flush: cmd = "save-all flush"
        else: cmd = "save-all"
        self.fh.commands.append(cmd)
        return cmd

    def save_on(self):
        """**Syntax:** *save-on*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.save_on"""
        self.fh.commands.append("save-on")
        return "save-on"

    def save_off(self):
        """**Syntax:** *save-off*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.save_off"""
        self.fh.commands.append("save-off")
        return "save-off"

    def seed(self):
        """**Syntax:** *seed*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.seed"""
        self.fh.commands.append("seed")
        return "seed"

    def setidletimeout(self, mins: int):
        """**Syntax:** *setidletimeout <mins>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.setidletimeout"""
        cmd = f"setidletimeout {mins}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spectate(self, target: str=None, spectator: str=None):
        """**Syntax:** *spectate [target] [spectator]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.spectate"""
        internal.reliant('target', target, None, 'spectator', spectator, None)
        optionals = internal.defaults((target, None), (spectator, None))
        cmd = f"spectate {optionals}".strip()
        return cmd

    def team(self, mode: str, team: str=None, members: str=None, displayName: str=None, option: str=None, value=None):
        """**Syntax:** *team ...*
        * *<mode\:add> [displayName]*
        * *<mode\:empty|remove> <team>*
        * *<mode\:join> <team> [members]*
        * *<mode\:list> [team]*
        * *<mode\:modify> [team] ...*
          * *<option\:collisionRule> <value\:always|never|pushOtherTeams|pushOwnTeam>*
          * *<option\:color> <value\:aqua|black|blue|gold|gray|green|light_purple|red|reset|yellow|white|dark_aqua|dark_blue|dark_gray|dark_green|dark_purle|dark_red>*
          * *<option\:deathMessageVisibility|nametagVisibility> <value\:always|never|hideForOtherTeams|hideForOwnTeam>*
          * *<option\:friendlyFire|seeFriendlyInvisibles> <value\:True|False>*
          * *<option\:displayName|prefix|suffix> <value>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.team"""
        internal.options(mode, ['add', 'empty', 'join', 'leave', 'list', 'modify', 'remove'])
        internal.multi_check_invalid_params(['add', 'empty', 'join', 'list', 'modify', 'remove'], 'mode', mode,
            ('team', team, None))
        if mode in ['add', 'empty', 'join', 'modify', 'remove'] and team is None:
            raise errors.MissingError('team', 'mode', mode)
        internal.multi_check_invalid_params(['join', 'leave'], 'mode', mode,
            ('members', members, None))
        if mode == 'leave' and members is None:
            raise errors.MissingError('members', 'mode', mode)
        internal.check_invalid_params('add', 'mode', mode,
            ('displayName', displayName, None))
        internal.check_invalid_params('modify', 'mode', mode,
            ('option', option, None),
            ('value', value, None),
            dep_mandatory=True)
        if option is not None:
            internal.options(option, ['collisionRule', 'color', 'deathMessageVisibility', 'displayName', 'friendlyFire', 'nametagVisibility', 'prefix', 'seeFriendlyInvisibles', 'suffix'])
            VALS = {
                "collisionRule": ['always', 'never', 'pushOtherTeams', 'pushOwnTeam'],
                "color": ['aqua', 'black', 'blue', 'gold', 'gray', 'green', 'light_purple', 'red', 'reset', 'yellow', 'white', 'dark_aqua', 'dark_blue', 'dark_gray', 'dark_green', 'dark_purle', 'dark_red'],
                "deathMessageVisibility": ['always', 'never', 'hideForOtherTeams', 'hideForOwnTeam'],
                "nameTagVisibility": ['always', 'never', 'hideForOtherTeams', 'hideForOwnTeam'],
            }
            if option in VALS.keys():
                internal.options(value, VALS[option])
        
        if mode == "add":
            optionals = internal.defaults((displayName, None))
            suffix = f"{team} {optionals}"
        elif mode in ['empty', 'remove']:
            suffix = team
        elif mode == "join":
            optionals = internal.defaults((members, None))
            suffix = f"{team} {optionals}"
        elif mode == "leave":
            suffix = members
        elif mode == "list":
            suffix = internal.defaults((team, None))
        else:
            suffix = f"{team} {option} {value}"

        cmd = f"team {mode} {suffix}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def teammsg(self, message: str):
        """**Syntax:** *teammsg <message>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.teammsg"""
        cmd = f"teammsg {message}".strip()
        self.fh.commands.append(cmd)
        return cmd
    tm = teammsg

    def trigger(self, objective: str, mode: str=None, value: int=None):
        """**Syntax:** *trigger <objective> ...*
        * *<mode\:(None)>*
        * *<mode\:add|set> <value>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.trigger"""
        internal.reliant('mode', mode, None, 'value', value, None)
        internal.unstated('mode', mode, ['add', 'set'], 'value', value, None)
        if mode is not None:
            internal.options(mode, ['add', 'set'])
        optionals = internal.defaults((mode, None), (value, None))
        cmd = f"trigger {objective} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_add(self, distance: float, duration: int=0):
        """**Syntax:** *worldborder add <distance> [duration]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_add"""
        optionals = internal.defaults((duration, 0))
        cmd = f"worldborder add {distance} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_center(self, pos: str):
        """**Syntax:** *worldborder center <pos>*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_center"""
        cmd = f"worldborder center {pos}"
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_damage(self, damagePerBlock: float=None, distance: float=None):
        """**Syntax:** *worldborder damage {amount <damagePerBlock>|buffer <distance>}*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_damage"""
        value = internal.pick_one_arg(
            (damagePerBlock, None, 'damagePerBlock'),
            (distance, None, 'distance'),
            optional=False
        )

        middle = "amount" if damagePerBlock is not None else "buffer"
        cmd = f"worldborder damage {middle} {value}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_get(self):
        """**Syntax:** *worldborder get*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_get"""
        cmd = "worldborder get"
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_set(self, distance: float=None, duration: int=0):
        """**Syntax:** *worldborder set <distance> [duration]*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_set"""
        optionals = internal.defaults((duration, 0))
        cmd = f"worldborder add {distance} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def worldborder_warning(self, distance: float=None, duration: int=None):
        """**Syntax:** *worldborder warning {distance <distance>|time <duration>}*\n
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaRawCommands.worldborder_warning"""
        value = internal.pick_one_arg(
            (distance, None, 'distance'),
            (duration, None, 'duration'),
            optional=False
        )

        middle = "distance" if distance is not None else "time"
        cmd = f"worldborder warning {middle} {value}".strip()
        cmd = "worldborder get"
        self.fh.commands.append(cmd)
        return cmd
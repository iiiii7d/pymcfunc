import json

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
        """Adds a /setblock command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.setblock"""
        internal.options(mode, ['destroy', 'keep', 'replace'])
        optionals = internal.defaults((mode, "replace"))

        cmd = f"setblock {pos} {block} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def fill(self, pos1: str, pos2: str, block: str, mode="replace", filterPredicate: str=None):
        """Adds a /fill command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.fill"""
        internal.options(mode, ['destroy', 'hollow', 'keep', 'outline', 'replace'])
        if mode != 'replace' and filterPredicate != None:
            raise errors.InvalidParameterError(mode, 'mode', filterPredicate, 'filterPredicate')
        optionals = internal.defaults((mode, "replace"), (filterPredicate, None))

        cmd = f"fill {pos1} {pos2} {block} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clone(self, pos1: str, pos2: str, dest: str, maskMode="replace", filterPredicate: str=None, cloneMode: str="normal"):
        """Adds a /clone command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.clone"""
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
        """Adds a /give command.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaFuncHandler.give"""
        internal.check_spaces('target', target)
        optionals = internal.defaults((count, 1))

        cmd = f"give {target} {item} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def summon(self, entity: str, pos: str="~ ~ ~", nbt: dict=None):
        nbt = json.dumps(nbt) if isinstance(nbt, dict) else nbt
        optionals = internal.defaults((pos, "~ ~ ~"), (nbt, None))

        cmd = f"summon {entity} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def clear(self, target: str="@s", item: str=None, maxCount: int=None):
        internal.reliant('item', maxCount, None, 'data', maxCount, None)
        internal.check_spaces('target', target)
        optionals = internal.defaults((target, "@s"), (item, None), (maxCount, None))

        cmd = f"clear {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def teleport(self, destentity: str=None, destxyz: str=None, target: str="@s", rotation: str=None, faceMode: str=None, facing: str=None, anchor: str="eyes"):
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
        internal.check_spaces('target', target)
        optionals = internal.defaults((seconds, 30), (amplifier, 0), (hideParticles, False))

        cmd = f"effect give {target} {effect} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
        
    def effect_clear(self, target: str="@s", effect: str=None):
        internal.check_spaces('target', target)
        optionals = internal.defaults((effect, None))

        cmd = f"effect clear {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def setworldspawn(self, pos: str="~ ~ ~", angle: str=None):
        optionals = internal.defaults((pos, "~ ~ ~"), (angle, None))

        cmd = f"setworldspawn {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def spawnpoint(self, target: str="@s", pos: str="~ ~ ~", angle: str=None):
        internal.check_spaces('target', target)
        optionals = internal.defaults((pos, "~ ~ ~"), (angle, None))

        cmd = f"spawnpoint {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd
    
    def particle(self, name: str, speed: float, count: int, params: str=None, pos: str="~ ~ ~", delta: str="~ ~ ~", mode: str="normal", viewers: str=None):
        optionals = internal.defaults((mode, "normal"), (viewers, None))
        if params != None:
            name = f"{name} {params}"
        cmd = f"particle {name} {pos} {delta} {speed} {count} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def schedule(self, name: str, clear=False, duration: str=None, mode: str="replace"):
        internal.check_invalid_params(False, 'clear', clear, ('duration', duration, None), dep_mandatory=True)
        if clear:
            cmd = f"schedule clear {name}".strip()
        else:
            optionals = internal.defaults((mode, 'replace'))
            cmd = f"schedule function {name} {duration} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def playsound(self, sound: str, source: str, target: str, pos: str="~ ~ ~", volume: float=1.0, pitch: float=1.0, minVolume: float=None):
        internal.check_spaces('target', target)
        internal.options(source, ['master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice'])
        optionals = internal.defaults((pos, "~ ~ ~"), (volume, 1.0), (pitch, 1.0), (minVolume, None))
        
        cmd = f"playsound {sound} {source} {target} {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def stopsound(self, target: str, source: str="*", sound: str=None):
        internal.check_spaces('target', target)
        internal.options(source, ['master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice', '*'])
        optionals = internal.defaults((source, "*"), (sound, None))

        cmd = f"stopsound {optionals}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def weather(self, mode: str, duration: str=5):
        internal.options(mode, ['clear', 'rain', 'thunder'])
        cmd = f"weather {mode} {duration}".strip()
        self.fh.commands.append(cmd)
        return cmd

    def difficulty(self, difficulty: str=None):
        if difficulty == None:
            cmd = "difficulty"
        else:
            internal.options(difficulty, ['easy', 'hard', 'normal', 'peaceful', 'e', 'h', 'n', 'p'])
        cmd = f"difficulty {difficulty}"
        self.fh.commands.append(cmd)
        return cmd

    def list(self, uuid: bool=False):
        cmd = "list" if not uuid else "list uuid"
        self.fh.commands.append(cmd)
        return cmd

    def spreadplayers(self, center: str, dist: float, maxRange: float, respectTeams: bool, target: str, maxHeight: float=None):
        if maxHeight != None:
            maxHeight = "under "+maxHeight+" "
        else:
            maxHeight = ""
        cmd = f"spreadplayers {center} {dist} {maxRange} {maxHeight}{respectTeams} {target}"
        self.fh.commands.append(cmd)
        return cmd

    def replaceitem(self, mode: str, slot: str, item: int, pos: str=None, target: str=None, count: int=1):
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
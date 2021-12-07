from typing import Optional, Dict, Union
import pymcfunc_old.internal as internal
NumberProvider = dict
RangeDict = Dict[str, Union[int, NumberProvider]]

class Predicate:
    """A predicate.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate"""
    def __init__(self, p, name: str, value: Optional[dict]=None):
        self.p = p
        self.name = name
        self.namespaced = self.p.name + ":" + self.name
        self.p.predicates[name] = {}
        if value is None: self.value = self.p.predicates[self.name]
        else: self.value = value

    def alternative(self) -> 'Predicate':
        """Returns a subpredicate. The predicate would be true if either the main predicate or the subpredicate is true.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.alternative"""
        self.value['condition'] = "alternative"
        if 'terms' not in self.value.keys():
            self.value['terms'] = []
        self.value['terms'].append({})
        index = int(len(self.value['terms'])-1)
        return Predicate(self.p, "", value=self.value['terms'][index])

    def inverted(self) -> 'Predicate':
        """Returns a subpredicate. The predicate would be true if the opposite of the subpredicate is false.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.inverted"""
        self.value['condition'] = "inverted"
        self.value['term'] = {}
        return Predicate(self.p, "", value=self.value['term'])

    def block_state_property(self, block: str, properties: Optional[Dict[str, str]]=None):
        """Sets the predicate's condition to ``block_state_property``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.block_state_property"""
        self.value['condition'] = "block_state_property"
        self.value['block'] = block
        if properties is not None: self.value['properties'] = properties

    def damage_source_properties(self, **tags: dict):
        """Sets the predicate's condition to ``damage_source_properties``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.damage_source_properties"""
        self.value['condition'] = "damage_source_properties"
        self.value['predicate'] = tags
    
    def entity_properties(self, entity: str, **tags: dict):
        """Sets the predicate's condition to ``entity_properties``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.entity_properties"""
        self.value['condition'] = "entity_properties"
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value['entity'] = entity
        self.value['predicate'] = tags

    def entity_scores(self, entity: str, **scores: Union[int, Dict[str, Union[int, NumberProvider]]]):
        """Sets the predicate's condition to ``entity_scores``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.entity_scores"""
        self.value['condition'] = "entity_scores"
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value['entity'] = entity
        for _, v in scores.items():
            if not isinstance(v, dict):
                continue
            internal.check_range(v)
        self.value['scores'] = scores

    def killed_by_player(self, inverse: bool=False):
        """Sets the predicate's condition to ``killed_by_player``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.killed_by_player"""
        self.value['condition'] = "killed_by_player"
        self.value['inverse'] = inverse

    def location_check(self, offset_x: Optional[int]=None, offset_y: Optional[int]=None, offset_z: Optional[int]=None, **predicate: dict):
        """Sets the predicate's condition to ``location_check``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.location_check   """
        self.value['condition'] = "location_check"
        if offset_x is not None: self.value['offsetX'] = offset_x
        if offset_y is not None: self.value['offsetY'] = offset_y
        if offset_z is not None: self.value['offsetZ'] = offset_z
        self.value['predicate'] = predicate

    def match_tool(self, **predicate: dict):
        """Sets the predicate's condition to ``match_tool``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.match_tool"""
        self.value['condition'] = "match_tool"
        self.value['predicate'] = predicate

    def random_chance(self, chance: float):
        """Sets the predicate's condition to ``random_chance``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.random_chance"""
        self.value['condition'] = "random_chance"
        self.value['chance'] = chance

    def random_chance_with_looting(self, chance: float, looting_multiplier: float):
        """Sets the predicate's condition to ``random_chance_with_looting``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.random_chance_with_looting"""
        self.value['condition'] = "random_chance_with_looting"
        self.value['chance'] = chance
        self.value['looting_multiplier'] = looting_multiplier
    
    def reference(self, predicate: Union[str, 'Predicate']):
        """References another predicate.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.reference"""
        self.value['condition'] = "reference"
        if isinstance(predicate, type(self)):
            self.value['name'] = predicate.namespaced
        else:
            self.value['name'] = predicate

    def survives_explosion(self):
        """Sets the predicate's condition to ``survives_explosion``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.survives_explosion"""
        self.value['condition'] = "survives_explosion"

    def table_bonus(self, enchantment: int, chances: list):
        """Sets the predicate's condition to ``table_bonus``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.table_bonus"""
        self.value['condition'] = "table_bonus"
        self.value['enchantment'] = enchantment
        self.value['chances'] = chances

    def time_check(self, value: Union[int, RangeDict], period: Optional[int]=None):
        """Sets the predicate's condition to ``time_check``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.time_check"""
        self.value['condition'] = "time_check"
        internal.check_range(value)
        self.value['value'] = value
        if period is not None: self.value['period'] = period

    def weather_check(self, raining: bool=False, thunder: bool=False):
        """Sets the predicate's condition to ``weather_check``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.weather_check"""
        self.value['condition'] = "weather_check"
        self.value['raining'] = raining
        self.value['thunder'] = thunder

    def value_check(self, value: Union[int, NumberProvider], range_: Union[int, RangeDict]):
        """Sets the predicate's condition to ``value_check``.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.predicates.Predicate.value_check"""
        internal.check_range(range_)
        self.value['range'] = range_
        self.value['value'] = value

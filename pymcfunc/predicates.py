from typing import Optional, Dict, Union
import pymcfunc.internal as internal
NumberProvider = dict


class Predicate:
    def __init__(self, p, name: str, value: Optional[dict]=None):
        self.p = p
        self.name = name
        self.namespaced = self.p.name + ":" + self.name
        self.p.predicates[name] = {}
        if value is None: self.value = self.p.predicates[self.name]
        else: self.value = value

    def alternative(self) -> 'Predicate':
        self.value['condition'] = "alternative"
        if 'terms' not in self.value.keys():
            self.value['terms'] = []
        index = int(len(self.value['terms'])-1)
        return Predicate(self.p, "", value=self.value['terms'][index])

    def inverted(self) -> 'Predicate':
        self.value['condition'] = "inverted"
        self.value['term'] = {}
        return Predicate(self.p, "", value=self.value['term'])

    def block_state_property(self, block: str, properties: Optional[Dict[str, str]]=None):
        self.value['condition'] = "block_state_property"
        self.value['block'] = block
        if properties is not None: self.value['properties'] = properties

    def damage_source_properties(self, **tags: dict):
        self.value['condition'] = "damage_source_properties"
        self.value['predicate'] = tags
    
    def entity_properties(self, entity: str, **tags: dict):
        self.value['condition'] = "entity_properties"
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value['entity'] = entity
        self.value['predicate'] = tags

    def entity_scores(self, entity: str, **scores: Union[int, Dict[str, Union[int, NumberProvider]]]):
        self.value['condition'] = "entity_scores"
        internal.options(entity, ['this', 'killer', 'killer_player'])
        self.value['entity'] = entity
        for _, v in scores.items():
            if not isinstance(v, dict):
                continue
            internal.check_range(v)
        self.value['scores'] = scores

    def killed_by_player(self, inverse: bool=False):
        self.value['condition'] = "killed_by_player"
        self.value['inverse'] = inverse

    def location_check(self, offset_x: Optional[int]=None, offset_y: Optional[int]=None, offset_z: Optional[int]=None, **predicate: dict):
        self.value['condition'] = "location_check"
        if offset_x is not None: self.value['offsetX'] = offset_x
        if offset_y is not None: self.value['offsetY'] = offset_y
        if offset_z is not None: self.value['offsetZ'] = offset_z
        self.value['predicate'] = predicate

    def match_tool(self, **predicate: dict):
        self.value['condition'] = "match_tool"
        self.value['predicate'] = predicate

    def random_chance(self, chance: float):
        self.value['condition'] = "random_chance"
        self.value['chance'] = chance

    def random_chance_with_looting(self, chance: float, looting_multiplier: float):
        self.value['condition'] = "random_chance_with_looting"
        self.value['chance'] = chance
        self.value['looting_multiplier'] = looting_multiplier
    
    def reference(self, predicate: Union[str, 'Predicate']):
        self.value['condition'] = "reference"
        if isinstance(predicate, type(self)):
            self.value['name'] = predicate.namespaced
        else:
            self.value['name'] = predicate

    def survives_explosion(self):
        self.value['condition'] = "survives_explosion"

    def table_bonus(self, enchantment: int, chances: list):
        self.value['condition'] = "table_bonus"
        self.value['enchantment'] = enchantment
        self.value['chances'] = chances

    def time_check(self, value: Union[int, Dict[str, Union[int, NumberProvider]]], period: Optional[int]=None):
        self.value['condition'] = "time_check"
        if isinstance(value, dict):
            for k, v in value:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        self.value['value'] = value
        if period is not None: self.value['period'] = period

    def weather_check(self, raining: bool=False, thunder: bool=False):
        self.value['condition'] = "weather_check"
        self.value['raining'] = raining
        self.value['thunder'] = thunder

    def value_check(self, value: Union[int, NumberProvider], range_: Union[int, Dict[str, Union[int, NumberProvider]]]):
        if isinstance(range_, dict):
            for k, v in range_:
                if k not in ['min', 'max']:
                    raise KeyError(f"Invalid key: {k}")
        self.value['range'] = range_
        self.value['value'] = value

from typing import Any
import pymcfunc.internal as internal

class Predicate:
    def __init__(self, p, name: str, condition: str):
        self.p = p
        self.name = name
        internal.options(condition, ['alternative', 'block_state_property', 'damage_source_properties',
                                     'entity_properties', 'entity_scores', 'inverted', 'killed_by_player',
                                     'location_check', 'match_tool', 'random_chance', 'random_chance_with_looting',
                                     'reference', 'survives_explosion', 'table_bonus', 'time_check', 'weather_check', 'value_check'])
        self.p.predicates[name] = {'condition': condition}
        self.value = self.p.predicates[self.name]

    def set_content(self, key: str, value: Any):
        self.value[key] = value


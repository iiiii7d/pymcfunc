from typing import Union

class BedrockVariable:
    """Represents a variable in Bedrock Edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable"""
    def __init__(self, fh, name: str, target: str):
        self.fh = fh
        self.name = name
        self.target = target
        self.fh.r.scoreboard_objectives('add', objective=name)
        #self.fh.r.scoreboard_players('set', target=target, objective=name, count=0)

    def __iadd__(self, other: Union['BedrockVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='+=', selector=other.target, selectorObjective=other.name)
        if other < 0:
            self.__isub__(other)
        else:
            self.fh.r.scoreboard_players('add', target=self.target, objective=self.name, count=other)
        return self

    def __isub__(self, other: Union['BedrockVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='-=', selector=other.target, selectorObjective=other.name)
        elif other < 0:
            self.__iadd__(other)
        else:
            self.fh.r.scoreboard_players('remove', target=self.target, objective=self.name, count=other)
        return self

    def __imul__(self, other: Union['BedrockVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='*=', selector=other.target, selectorObjective=other.name)
        else:
            temp = type(self)(self.fh, self.name+'temp', self.target)
            temp.set(other)
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='*=', selector=temp.target, selectorObjective=temp.name)
            del temp
        return self

    def __itruediv__(self, other: Union['BedrockVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='*=', selector=other.target, selectorObjective=other.name)
        else:
            temp = type(self)(self.fh, self.name+'temp', self.target)
            temp.set(other)
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='/=', selector=temp.target, selectorObjective=temp.name)
            del temp
        return self
    __ifloordiv__ = __itruediv__

    def __imod__(self, other: Union['BedrockVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='%=', selector=other.target, selectorObjective=other.name)
        else:
            temp = type(self)(self.fh, self.name+'temp', self.target)
            temp.set(other)
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='%=', selector=temp.target, sselectorbjective=temp.name)
            del temp
        return self

    def remove(self, full: bool=False):
        if full:
            self.fh.r.scoreboard_objectives('remove', objective=self.name)
        else:
            self.fh.r.scoreboard_players('reset', target=self.target, objective=self.name)

    def in_range(self, minv: int, maxv: int=None):
        """Tests a value if it is within a certain range.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.in_range"""
        self.fh.r.scoreboard_players('test', target=self.target, objective=self.name, minv=minv, maxv=maxv)

    def set(self, other: Union['BedrockVariable', int]):
        """Sets this variable to a value or that of another variable
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.set"""
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='=', source=other.target, sourceObjective=other.name)
        else:
            self.fh.r.scoreboard_players('set', target=self.target, objective=self.name, count=other)

    def random(self, minv: int, maxv: int=None):
        """Sets this variable to a random number.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.random"""
        self.fh.r.scoreboard_players('random', target=self.target, objective=self.name, minv=minv, maxv=maxv)

    def higher(self, other: 'BedrockVariable'):
        """Sets this variable to the higher of the two variables.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.higher"""
        self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                     operation='>', selector=other.target, selectorObjective=other.name)

    def lower(self, other: 'BedrockVariable'):
        """Sets this variable to the lower of the two variables.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.lower"""
        self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                     operation='<', selector=other.target, selectorObjective=other.name)

    def swap(self, other: 'BedrockVariable'):
        """Swaps the value of the two variables.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.swap"""
        self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                     operation='><', selector=other.target, selectorObjective=other.name)

    def show(self, slot: str, sort_order: str=None):
        """Shows the variable in a slot.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.BedrockVariable.show"""
        self.fh.r.scoreboard_objectives('setdisplay', slot=slot, objective=self.name, sortOrder=sort_order)

class JavaVariable:
    """Represents a variable in Java Edition.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable"""
    def __init__(self, fh, name: str, target: str, trigger: bool=False):
        self.fh = fh
        self.name = name
        self.target = target
        criterion = 'dummy' if not trigger else 'trigger'
        self.fh.r.scoreboard_objectives('add', objective=name, criterion=criterion)
        #self.fh.r.scoreboard_players('set', target=target, objective=name, score=0)

    def __iadd__(self, other: Union['JavaVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='+=', source=other.target, sourceObjective=other.name)
        if other < 0:
            self.__isub__(other)
        else:
            self.fh.r.scoreboard_players('add', target=self.target, objective=self.name, score=other)
        return self

    def __isub__(self, other: Union['JavaVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='-=', source=other.target, sourceObjective=other.name)
        elif other < 0:
            self.__iadd__(other)
        else:
            self.fh.r.scoreboard_players('remove', target=self.target, objective=self.name, score=other)
        return self

    def __imul__(self, other: Union['JavaVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='*=', source=other.target, sourceObjective=other.name)
        else:
            temp = type(self)(self.fh, self.name+'temp', self.target)
            temp.set(other)
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='*=', source=temp.target, sourceObjective=temp.name)
            del temp
        return self

    def __itruediv__(self, other: Union['JavaVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='*=', source=other.target, sourceObjective=other.name)
        else:
            temp = type(self)(self.fh, self.name+'temp', self.target)
            temp.set(other)
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='/=', source=temp.target, sourceObjective=temp.name)
            del temp
        return self
    __ifloordiv__ = __itruediv__

    def __imod__(self, other: Union['JavaVariable', int]):
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='%=', source=other.target, sourceObjective=other.name)
        else:
            temp = type(self)(self.fh, self.name+'temp', self.target)
            temp.set(other)
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='%=', source=temp.target, sourceObjective=temp.name)
            del temp
        return self

    def remove(self, full: bool=False):
        if full:
            self.fh.r.scoreboard_objectives('remove', objective=self.name)
        else:
            self.fh.r.scoreboard_players('reset', target=self.target, objective=self.name)

    @staticmethod
    def _comparers(self, other: Union['JavaVariable', int], mode: str):
        if isinstance(other, type(self)):
            return {
                'mode': 'score',
                'target': self.target,
                'objective': self.name,
                'comparer': mode,
                'source': other.target,
                'sourceObjective': other.name
            }
        else:
            rangeTemplates = {
                '=': f'{other}',
                '<': f'..{other}',
                '<=': f'..{other-1}',
                '>': f'{other}..',
                '>=': f'{other+1}',
            } if not isinstance(other, str) else {
                '=': f'{other}'
            }
            return {
                'mode': 'score',
                'target': self.target,
                'objective': self.name,
                'comparer': 'matches',
                'range': rangeTemplates[mode]
            }

    def __eq__(self, other: Union['JavaVariable', int]):
        return self._comparers(self, other, '=')

    def __lt__(self, other: Union['JavaVariable', int]):
        return self._comparers(self, other, '<')

    def __le__(self, other: Union['JavaVariable', int]):
        return self._comparers(self, other, '<=')

    def __gt__(self, other: Union['JavaVariable', int]):
        return self._comparers(self, other, '>')

    def __ge__(self, other: Union['JavaVariable', int]):
        return self._comparers(self, other, '>=')

    def in_range(self, r: Union[str, int]):
        """For use in JavaRawCommands.execute(). Finds whether this variable is in a specified range.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.in_range"""
        return self.__eq__(r)

    def store(self, mode: str):
        """For use in JavaRawCommands.execute(). Stores a result or success in this variable.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.store"""
        return {
            'store': mode,
            'mode': 'score',
            'target': self.target,
            'objective': self.name
        }

    def set(self, other: Union['JavaVariable', int]):
        """Sets this variable to a value or that of another variable.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.set"""
        if isinstance(other, type(self)):
            self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                         operation='=', source=other.target, sourceObjective=other.name)
        else:
            self.fh.r.scoreboard_players('set', target=self.target, objective=self.name, score=other)

    def higher(self, other: 'JavaVariable'):
        """Sets this variable to the higher of the two variables.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.higher"""
        self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                     operation='>', source=other.target, sourceObjective=other.name)

    def lower(self, other: 'JavaVariable'):
        """Sets this variable to the lower of the two variables.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.lower"""
        self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                     operation='<', source=other.target, sourceObjective=other.name)

    def swap(self, other: 'JavaVariable'):
        """Swaps the value of the two variables.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.swap"""
        self.fh.r.scoreboard_players('operation', target=self.target, objective=self.name,
                                     operation='><', source=other.target, sourceObjective=other.name)

    def show(self, slot: str):
        """Shows the variable in a slot.
        More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.JavaVariable.show"""
        self.fh.r.scoreboard_objectives('setdisplay', objective=self.name, slot=slot)
'''
A collection of interfaces from which 
our requirement validation can be built.
'''

import regex as re
from math import inf

from Coma.Result import Result


class FormatInterface:
    def __init__(self) -> None:
        pass
    def Validate(self, x) -> Result:
        pass 
    

class RegexInterface(FormatInterface):
    def __init__(self, expression: str) -> None:
        super().__init__()
        self.expression = re.compile(expression)
    
    def Validate(self, x: str) -> Result:
        if type(x) != str:
            return Result.Fail('not a string', value=x)

        result = self.expression.match(x)
        if not result:
            return Result.Fail('regex doesn\'t match', value=result)
        return Result.Succeed(result)


class NumericInterface(FormatInterface):
    def __init__(self, min_value, max_value, inf) -> None:
        super().__init__()
        self.max_value = inf if max_value is None else max_value
        self.min_value = -inf if min_value is None else min_value

    def Validate(self, x) -> Result:
        if x < self.min:
            return Result.Fail(f'value below minimum value {self.min_value}')
        elif x > self.max:
            return Result.Fail(f'value above maximum value {self.max_value}')
        return Result.Succeed(x)


LENGTH_ERROR = 'Coma {} format cannot have {} when fixed_length given'
class LengthInterface(FormatInterface):
    def __init__(self, fixed_length: int | None,
                       min_length: int | None, 
                       max_length: int | None) -> None:
        super().__init__()
        # ensure the length requirements aren't ambiguous
        if fixed_length is not None:
            if min_length is not None:
                msg = LENGTH_ERROR.format(self.__class__.__name__, 'min_length')
                raise ValueError(msg)
            elif max_length is not None:
                msg = LENGTH_ERROR.format(self.__class__.__name__, 'max_length')
                raise ValueError(msg)
            self.min_length = fixed_length
            self.max_length = fixed_length
        else:
            self.min_length = min_length if min_length is not None else 0
            self.max_length = max_length if max_length is not None else inf
            
    def Validate(self, x) -> Result:
        length = len(x)
        if length < self.min_length:
            reason = f'length {length} below min length {self.min_length}'
            return Result.Fail(reason, value=x)
        elif length > self.max_length:
            reason = f'length {length} above max length {self.max_length}'
            return Result.Fail(reason, value=x)
        return Result.Succeed(x)

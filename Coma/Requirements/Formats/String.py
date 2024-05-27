from math import inf

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface

length_error_msg = 'Coma String format cannot have {} when fixed_length given'

class String(FormatInterface):
    def __init__(self, fixed_length=None, 
                       min_length=None, 
                       max_length=None) -> None:
        '''
        Ensure the length requirements aren't ambiguous
        '''
        if fixed_length is not None:
            if min_length is not None:
                raise ValueError(length_error_msg.format('min_length'))
            elif max_length is not None:
                raise ValueError(length_error_msg.format('max_length'))
            self.min_length = fixed_length
            self.max_length = fixed_length
        else:
            self.min_length = min_length if min_length is not None else 0
            self.max_length = max_length if max_length is not None else inf
            
    def Validate(self, x: str) -> Result:
        if type(x) != str:
            return Result.Fail('not a string', value=x)
        
        length = len(x)
        if length < self.min_length:
            reason = 'length {length} below min_length {self.min_length}'
            return Result.Fail(reason, value=x)
        elif length > self.max_length:
            reason = 'length {length} above max_length {self.max_length}'
            return Result.Fail(reason, value=x)
        return Result.Succeed(x)

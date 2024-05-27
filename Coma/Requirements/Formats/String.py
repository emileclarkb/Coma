from math import inf

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import LengthInterface

length_error_msg = 'Coma String format cannot have {} when fixed_length given'

class String(LengthInterface):
    def __init__(self, fixed_length=None, 
                       min_length=None, 
                       max_length=None) -> None:
        super().__init__(fixed_length, min_length, max_length)
            
    def Validate(self, x: str) -> Result:
        if type(x) != str:
            return Result.Fail('not a string', value=x)
        return super().Validate(x)

from math import inf

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface


class Integer(FormatInterface):
    def __init__(self, min_value: int = None, max_value: int = None) -> None:
        super().__init__()
        self.max_value = inf if max_value is None else max_value
        self.min_value = -inf if min_value is None else min_value
    
    def Validate(self, x: int) -> Result:
        if type(x) != int:
            return Result.Fail('not an integer', value=x)
        return super().Validate(x)

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface


class Float(FormatInterface):
    def __init__(self, min_value: float = None, max_value: float = None) -> None:
        super().__init__()
        inf = float('inf')
        self.max_value = inf if max_value is None else max_value
        self.min_value = -inf if min_value is None else min_value
    
    def Validate(self, x: float) -> Result:
        if type(x) != float:
            return Result.Fail('not a float', value=x)
        elif x < self.min:
            return Result.Fail('value below minimum value {self.min_value}')
        elif x > self.max:
            return Result.Fail('value above maximum value {self.max_value}')
        return Result.Succeed(x)

from Coma.Requirements.Result import Result
from Coma.Requirements.Format.Interfaces import FormatInterface


class Float(FormatInterface):
    def __init__(self, min_value: float = None, max_value: float = None) -> None:
        super().__init__(min_value, max_value, float('inf'))
    
    def Validate(self, x: float) -> Result:
        if type(x) != float:
            return Result.Fail('not a float', value=x)
        return super().Validate(x)

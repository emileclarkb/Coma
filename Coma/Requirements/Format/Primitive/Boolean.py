from Coma.Result import Result
from Coma.Requirements.Format.Interfaces import FormatInterface


class Boolean(FormatInterface):
    def __init__(self) -> None:
        super().__init__()
    
    def Validate(self, x: bool) -> Result:
        if type(x) != bool:
            return Result.Fail('not a boolean', value=x)
        return Result.Succeed(x)

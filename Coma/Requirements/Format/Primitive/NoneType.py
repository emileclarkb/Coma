from Coma.Result import Result
from Coma.Requirements.Format.Interfaces import FormatInterface


class NoneType(FormatInterface):
    def __init__(self) -> None:
        super().__init__()
    
    def Validate(self, x) -> Result:
        if type(x) != type(None):
            return Result.Fail('not None', value=x)
        return Result.Succeed(x)

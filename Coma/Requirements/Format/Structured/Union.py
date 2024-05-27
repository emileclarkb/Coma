from Coma.Requirements.Result import Result
from Coma.Requirements.Format.Interfaces import FormatInterface


class Union(FormatInterface):
    def __init__(self, *types: FormatInterface) -> None:
        super().__init__()
        self.types = types
    
    def Validate(self, x) -> Result:
        for t in self.types:
            result = t.Validate(x)
            if result: return result
        return Result.Fail('value doesn\'t match any type in Union')

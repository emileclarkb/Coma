# import re
import regex as re

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface


class MatchRegex(FormatInterface):
    def __init__(self, expression: str) -> None:
        print(expression)
        self.expression = re.compile(expression)
    
    def Validate(self, x: str) -> Result:
        if type(x) != str:
            return Result.Fail('not a string', value=x)

        result = self.expression.match(x)
        if not result:
            return Result.Fail('regex doesn\'t match', value=result)
        return Result.Succeed(result)

'''
A collection of interfaces from which 
our requirement validation can be built.
'''

import regex as re

from Coma.Requirements.Result import Result

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


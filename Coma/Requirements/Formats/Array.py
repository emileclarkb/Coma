from typing import Any

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface, LengthInterface


class Array(LengthInterface):
    def __init__(self, format: FormatInterface,
                       fixed_length=None, 
                       min_length=None, 
                       max_length=None) -> None:
        super().__init__(fixed_length, min_length, max_length)
    
    def Validate(self, x: list[Any]) -> Result:
        if type(x) != list:
            return Result.Fail('not a list', value=x)
        # if we get an error from now on, don't just fail
        # store the reason and move on (return the reasons at the end)
        fail_reasons = []
        result = []
        
        # check x meets the length requirements
        length_result = super().Validate(x)
        if not length_result: fail_reasons.extend(length_result.reasons)
        
        for i, value in enumerate(x):
            format_result = format.Validate(value)
            
            # if we've already failed there's no use saving to `result`
            # so from here we simply aim to collect more reasons for failure
            if format_result and not fail_reasons:
                result.append(format_result.value)
            # if the `if` statement failed then we can guarantee we're in a
            # failed state, so we should just free anything in `result`
            else:
                if result: del result
                msg = f'errors in Array, position {i}'
                fail_reasons.append({msg, format_result.reasons})
    
         # check everything was successful         
        if fail_reasons: return Result.Fail(fail_reasons)
        return Result.Succeed(result)

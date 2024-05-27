from typing import Any, List

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface


class Struct(FormatInterface):
    def __init__(self, formats: List[FormatInterface]) -> None:
        super().__init__()
        self.formats = formats
    
    def Validate(self, x: List[Any]) -> Result:
        if type(x) != list:
            return Result.Fail('not a list', value=x)
        # if we get an error from now on, don't just fail
        # store the reason and move on (return the reasons at the end)
        fail_reasons = []
        result = []
        
        # ensure `x` and `self.formats` have one-to-one correspondence
        length = len(x)
        formats_length = len(self.formats)
        if length != formats_length:
            # we will still attempt to check the failures on the things we can
            # so reset our estimate of how many elements can be checked
            length = min(length, formats_length)
            # also add to `fail_reasons` so we can enter a failed state
            msg = 'struct has {} elements, expected {}'
            msg = msg.format(length, formats_length)
            fail_reasons.append(msg)
            
        for i in range(length):
            # match up a value and format
            # NOTE: Is this method good? I'm completely assuming that 
            #       despite the length difference, they still pair up
            #       and correspond but that's not always true. Honestly
            #       more often than note I'd suspect its not true.
            #       So if this ends up being annoying just remove this please
            # TODO: Read Note above
            value = x[i]
            format = self.formats[i]

            valid = format.Validate(value)
            
            # if we've already failed there's no use saving to `result`
            # so from here we simply aim to collect more reasons for failure
            if valid and not fail_reasons:
                result.append(valid.value)
            # if the `if` statement failed then we can guarantee we're in a
            # failed state, so we should just free anything in `result`
            else:
                if result: del result
                msg = f'errors in Struct, index {i}'
                fail_reasons.append({msg, valid.reasons})
       
        if fail_reasons: return Result.Fail(fail_reasons)
        return Result.Succeed(result)

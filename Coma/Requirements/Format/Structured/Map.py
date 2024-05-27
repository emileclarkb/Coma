from Coma.Requirements.Result import Result
from Coma.Requirements.Format.Interfaces import FormatInterface


class Map(FormatInterface):
    def __init__(self, map: dict[str, FormatInterface], 
                       wildcards: FormatInterface = None) -> None:
        super().__init__()
        self.map = map
        self.wildcards = wildcards
        
    
    def Validate(self, x: dict) -> Result:
        if type(x) != dict:
            return Result.Fail('not a dictionary', value=x)
        # if we get an error from now on, don't just fail
        # store the reason and move on (return the reasons at the end)
        fail_reasons = []
        result = {}
        
        for key, value in x.items():
            # also keep track of our local failures
            key_fail_reasons = []
            
            format = self.map.get(key)
            valid = None
            # this is a known key in our map
            if format is not None:
                valid = format.Validate(value)
            # the key is not known, but wildcards are supported
            elif self.wildcards is not None:
                valid = self.wildcards.Validate(value)
            # the key is not known and wildcards are forbidden
            else:
                key_fail_reasons.append(f'unknown key {key}')
            
            # we can skip this step if no validation occurred
            # (aka unknown key and wildcards forbidden)
            if valid is not None:
                # check if validation failed
                # (we only need to save our reasons if we aren't
                #  already in failed state, aka `fail_reasons` exists)
                if valid: 
                    if not fail_reasons: result[key] = valid.value
                else:
                    # we don't need this anymore so we will free it
                    # (the `result` symbol will only be referenced
                    #  if `fail_reasons` is empty, and from now on it 
                    #  won't be. So (theoretically) no errors will occur)
                    # if result: del result 
                    key_fail_reasons.extend(valid.reasons)
            
            # package up our failures and give the to the main `fail_reasons`
            if key_fail_reasons:
                msg = f'errors in Map, key \"{key}\"'
                fail_reasons.append({msg: key_fail_reasons})
            
        if fail_reasons: return Result.Fail(fail_reasons)
        return Result.Succeed(result)

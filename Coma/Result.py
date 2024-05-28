from typing import Any, List


class Result:
    def __init__(self, success: bool, value: Any, 
                       reasons: str | List[str] = None) -> None:
        self.success = success
        self.value = value
        # the reasons we failed (optional)
        if reasons is not None and not isinstance(reasons, list):
            self.reasons = [reasons]
        else:
            self.reasons = reasons

    # ie. "if result: blah blah blah" :)
    def __bool__(self):
        return self.success

    @classmethod
    def Succeed(cls, value: Any, reasons: str | List[str] = 'ok') -> 'Result':
        return cls(True, value, reasons=reasons)
    
    @classmethod
    def Fail(cls, reasons: str | List[str], value=None) -> 'Result':
        return cls(False, value, reasons=reasons)

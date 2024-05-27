from typing import Any


class Result:
    def __init__(self, success: bool, value: Any, reason=None) -> None:
        self.success = success
        self.value = value
        self.reason = reason    # the reason we failed (optional)

    # ie. if result: blah blah blah :)
    def __bool__(self):
        return self.success

    @classmethod
    def Succeed(cls, value: Any, reason='ok') -> 'Result':
        return cls(True, value, reason=reason)
    
    @classmethod
    def Fail(cls, reason: str, value=None) -> 'Result':
        return cls(False, value, reason=reason)

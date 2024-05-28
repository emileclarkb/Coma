from typing import Any, List
import pprint

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

    def __str__(self) -> str:
        s = []
        s.append(f'Success: {self.success}')
        s.append(f'Reasons: {self.reasons[0]}')
        for reason in self.reasons[1:]: 
            s.append(' '*9 + str(reason))
        
        if self.success:
            s.append('') # empty line
        # pretty_value = pprint.pformat(self.value)
        pretty_value = Result.PrettyString(self.value, 0, use_repr=False)
        s.extend(pretty_value)
        
        return '\n'.join(s)
    
    @staticmethod
    def PrettyString(object: dict, base_indent: int, 
                     use_repr: bool = False) -> List[str]:
        show = repr if use_repr else str
        s = []
        if type(object) == dict:
            for key, value in object.items():
                # s.append(f'{key}: {repr(value)}')
                
                indent = len(key) + 3
                pretty_value = Result.PrettyString(value, base_indent + indent,
                                                   use_repr=use_repr)
                header = pretty_value[0]
                header = header.strip()
                s.append(f'{key}: {header}')
                s.extend(pretty_value[1:])
        elif type(object) == list:
            length = len(object)
            if not length: s = '[]'
            for i, value in enumerate(object):
                pretty_value = Result.PrettyString(value, base_indent + 1,
                                                   use_repr=use_repr)
                pretty_value = '\n'.join(pretty_value)
                text = f' {pretty_value}'
                if i != length - 1: text += ','
                s.append(text)
            s[0] = '[' + s[0][1:]
            s[-1] = s[-1] + ']'
        else: s.append(show(object))
        return s
                
    def __repr__(self) -> str:
        return f'Result({self.success}, {self.value}, reasons={self.reasons})'

    def __bool__(self):
        return self.success
    
    @classmethod
    def Succeed(cls, value: Any, reasons: str | List[str] = 'ok') -> 'Result':
        return cls(True, value, reasons=reasons)
    
    @classmethod
    def Fail(cls, reasons: str | List[str], value=None) -> 'Result':
        return cls(False, value, reasons=reasons)

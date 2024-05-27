from typing import Optional, List

from Coma.Requirements.Result import Result
from Coma.Requirements.Formats import FormatInterface
from Coma.Requirements.Formats.MatchRegex import MatchRegex


class VersionStruct:
    def __init__(self, string: str,
                       versions: tuple[int, ...], 
                       prefix: Optional[str],
                       postfix: Optional[str]) -> None:
        self.string = string
        self.versions = versions
        self.prefix = prefix
        self.postfix = postfix
        
    def __str__(self) -> str:
        return self.string

# TODO: allow prefixes/postfixes to have replacements (ie map to replacements)
# TODO: use prefix/postfix_required instead of prefix/postfix_optional
#       it makes more sense for humans
# class Version(FormatInterface):
class Version(MatchRegex):
    def __init__(self, version_numbers = 3, 
                       max_version_digits = None,
                       delimiter = '.',
                       prefixes: List[str] = None,
                       prefix_optional = True,
                       prefix_case_sensitive = True,
                       postfixes: List[str] = None,
                       postfix_optional = True,
                       postfix_case_sensitive = True) -> None:
        self.version_numbers = version_numbers
        self.max_version_digits = max_version_digits
        self.delimiter = delimiter
        
        version_regex = Version.GetVersionRegex(version_numbers,
                                                     max_version_digits,
                                                     delimiter) 
        prefix_regex = Version.GetAffixRegex('prefix',
                                                  prefixes,
                                                  prefix_optional,
                                                  prefix_case_sensitive)
        postfix_regex = Version.GetAffixRegex('postfix',
                                                   postfixes,
                                                   postfix_optional,
                                                   postfix_case_sensitive)
        expression = f'^{prefix_regex}{version_regex}{postfix_regex}$'
        super().__init__(expression)
        
        
        self.prefixes = prefixes
        self.prefix_optional = prefix_optional
        self.prefix_case_sensitive = prefix_case_sensitive
        
        self.postfixes = postfixes
        self.postfix_optional = postfix_optional
        self.postfix_case_sensitive = postfix_case_sensitive
        
        
        
    @staticmethod
    def GetAffixRegex(name: str,
                      affixes: List[str],
                      optional: bool,
                      case_sensitive: bool) -> str:
        '''
        case_expr = '?i:' if not case_sensitive else ''
        # TODO: remove this comment below
        # optional_expr = '?' if optional else ''
        affix_expr = '|'.join(affixes)
        
        # we make this expression optional intentionally,
        # because if it fails to match we can return Result.Fail()
        # and specify the issue being the prefix/postfix! (smart right!)
        expr = f'({case_expr}{affix_expr})?'
        # expr = f'({case_expr}{affix_expr}){optional_expr}'
        # expr = f'(?P<{name}>({case_expr}{affix_expr})){optional_expr}'
        '''
        
        '''
        affix_expr = '|'.join(affixes)
        expr = f'((?i:{affix_expr})?)'
        '''
        
        expr = '([^0-9]*)'
        return expr
    
    @staticmethod
    def GetVersionRegex(version_numbers: int,
                        max_version_digits: int,
                        delimiter: str) -> str:
        # "max_version_digits is None" means there is no maximum
        '''        
        version_expr = '(\d+)' if max_version_digits is None \
                               else f'(\d{{1,{max_version_digits}}})'
        # copy the expression "version_numbers" times, then join
        
        expr = delimiter.join([version_expr] * version_numbers)
        '''
        # version_expr = '\d+'
        expr = f'(?:(\d+){delimiter})*(\d+)'
        return expr
    
    @staticmethod
    def CheckValueAllowed(value: str, allowed_values: List[str], 
                          case_sensitive: bool, value_name: str) -> Result:
        lowercase_value = value.lower()
        lowercase_matches_found = []
        for allowed in allowed_values:
            # partially matching (just need to check the case now)
            if allowed.lower() == lowercase_value:
                # keep track of our partial matches
                lowercase_matches_found.append(allowed)
                
                # case insensitive means this partial match is good enough
                if not case_sensitive:
                    return Result.Succeed(None)
                # case sensitive but we found a complete match
                elif allowed == value:
                    return Result.Succeed(None)
                
        # we need to fail because the case sensitivity was broken
        # (we are guaranteed to be case_sensitive if we got to this point btw)
        if lowercase_matches_found:
            expected = [f'\"{match}\"' for match in lowercase_matches_found]
            if len(expected) > 1: expected[-1] = f'or {expected[-1]}'
            expected = ', '.join(expected)
            
            error_header = f'{value_name} case sensitivity broken, '
            error_msg = f'expected {expected}, got \"{value}\"'
            return Result.Fail(error_header + error_msg)
        
        # completely invalid value given 
        # (doesn't even partially match any of the allowed)
        return Result.Fail(f'{value_name} invalid, got \"{value}\"')
    
    def Validate(self, x: str) -> Result:
        if type(x) != str:
            return Result.Fail('not a string', value=x)
        
        '''
        # we need these to create a VersionStruct
        version_string = x  # save the unedited string for later
        versions = []
        version_prefix = None
        version_postfix = None
        '''
        
        result = super().Validate(x)
        if not result: return result
        
        groups = result.value.groups()
        # TODO: remove this debug section:
        print('#'*15)
        print(groups)
        print(result.value.captures(2))
        print('#'*15)
        prefix = groups[0]
        postfix = groups[-1]
        
        # get subcaptures and then add the final version number manually
        versions = result.value.captures(2)
        versions.append(groups[2])
        
        
        length = len(versions)
        if length != self.version_numbers:
            error_msg = 'version failed, allowed version numbers {}, got {}'
            return Result.Fail(error_msg.format(self.version_numbers, length))
        
        # TODO: use the same method for case sensitivity!
        if prefix is None and not self.prefix_optional:
            return Result.Fail('version failed, no prefix given')
        elif postfix is None and not self.postfix_optional:
            return Result.Fail('version failed, no postfix given')
        
        
        # TODO: save these results, don't return them just yet!
        #       then we can return all the results we need at the end!!
        # ensure the case sensitivity was met
        prefix_result = Version.CheckValueAllowed(prefix,
                                                  self.prefixes,
                                                  self.prefix_case_sensitive,
                                                  'prefix') 
        if not prefix_result: return prefix_result   
        
        postfix_result = Version.CheckValueAllowed(postfix,
                                                   self.postfixes,
                                                   self.postfix_case_sensitive,
                                                   'postfix') 
        if not postfix_result: return postfix_result       
                       
        
        # validation succeeded, we can now create the version struct
        version = VersionStruct(x,
                                versions,
                                prefix,
                                postfix)
        return Result.Succeed(version)
        
        
        '''
        # validate the prefix
        if self.prefixes is not None:
            for prefix in self.prefixes:
                if not self.prefix_case_sensitive:
                    prefix = prefix.lower()
                
                # prefix match
                if x.startswith(prefix):
                    version_prefix = prefix
                    # remove the prefix so we can continue parsing
                    x = x.removeprefix(prefix)
                    break
                
            # validation failed: no prefix given (and a prefix is required)
            if version_prefix == None and not self.prefix_optional:
                return Result.Fail('no prefix')

        # validation succeeded, we can now create the version struct
        version = VersionStruct(version_string,
                                versions,
                                version_prefix,
                                version_postfix)
        return Result.Succeed(version)
        '''

# TODO: Remove this (use pip instead)
import os, sys
sys.path.append(f'{os.getcwd()}\\..\\..\\Coma\\Repo')

from Coma import Coma
from Coma.Providers import GitHub, GitLab, BitBucket

from Repo.Coma.Requirements.Formats.Complex.Version import Version



'''
Constaints:
    - delimiter must be a single character (otherwise it will be interpretted
        as multiple delimiters that are all value, ie "abc" -> ["a","b","c"])
    - for delimiter "." use "\." instead to avoid regex issues
    - prefix and postfix cannot contain digits
'''
def main():
    # version_postfixes = ['-alpha', '-beta', '-release']
    version_prefixes = ['Alpha-', 'Beta-', 'Release-']
    version_format = Version(prefixes = version_prefixes,
                             prefix_optional = True,
                             prefix_case_sensitive = False,
                             version_numbers = 2, 
                             max_version_digits = 1,
                             delimiter = '\.',
                             postfixes = [],
                             postfix_optional = False)
    '''
    postfix invalid, got ""
    '''
    version = 'alpha-1.2'
    # version = 'v1.2.3-alpha'
    result = version_format.Validate(version)
    print(f'Success: {result.success}')
    print(f'Reasons: {result.reasons[0]}')
    for reason in result.reasons[1:]: print(' '*9 + reason)
    print()
    if not result.success: return 1
    print(f'String: {result.value.string}')
    print(f'Versions: {result.value.versions}')
    print(f'Prefix: {result.value.prefix}')
    print(f'Postfix: {result.value.postfix}')
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

import os, sys
sys.path.append(f'{os.getcwd()}\\Repo')

import json
from Coma.Requirements import Format


'''
# TODO: Why is description mapping to an empty list when the others are ['ok']?
# TODO: Is this a bad thing or a bug? (try find what caused it)

Success: False
Reasons: {'errors in Map, key "description"': []}
         {'errors in Map, key "maintained"': ['ok']}
         {'errors in Map, key "latest_version"': ['ok']}
         {'errors in Map, key "versions"': ['ok']}
'''
def main():
    version_postfixes = ['-alpha', '-beta', '-release']
    version_format = Format.Version(prefixes = ['v'],
                                    prefix_optional = False,
                                    prefix_case_sensitive = False,
                                    version_numbers = 3, 
                                    max_version_digits = 3,
                                    delimiter = '\.',
                                    postfixes = version_postfixes,
                                    postfix_optional = True,
                                    postfix_case_sensitive = True)
    
    metadata_format = Format.Map({
        'description': Format.String(max_length=30),
        'maintained': Format.Boolean(),
        'latest_version': version_format,
        'versions': Format.Array(version_format)
    })
    
    
    content = None
    # get the metadata to validate
    with open('Repo/Tests/metadata.json', 'r') as f:
        content = json.load(f)
    
    result = metadata_format.Validate(content)
    print(f'Success: {result.success}')
    print(f'Reasons: {result.reasons[0]}')
    for reason in result.reasons[1:]: print(' '*9 + str(reason))
    print()
    if not result.success: return 1
    for key, value in result.value.items():
        if type(value) != list:
            print(f'{key}: {repr(value)}')
            continue
        
        print(f'{key}: [{str(value[0])}', end='')
        indent = ' ' * (len(key) + 3)
        length = len(value)
        for i in range(length - 1):
            text = f',\n{indent}{str(value[i+1])}'
            print(text, end='')
        # final element
        print(']')
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

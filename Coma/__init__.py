from typing import List

# import requests

from Coma.Core.Component import Component

from Coma.Core.Providers.GitHub import GitHub
from Coma.Core.Providers.GitLab import GitLab
from Coma.Core.Providers.BitBucket import BitBucket

class Coma:
    PROVIDERS = {
        'GitHub': GitHub(),
        'GitLab': GitLab(),
        'BitBucket': BitBucket()
    }

    def __init__(self) -> None:
        pass

    def NewComponent(self, name: str, author: str) -> Component:
        component = Component(name, author)
        component.providers = dict.fromkeys(self.PROVIDERS)
        return component

    '''
    Find out which providers (ie github, gitlab, bitbucket)
    are hosting this component
    '''
    def FillProviders(self, component: Component) -> List[str]:
        for provider_name in component.providers.keys():
            provider = self.PROVIDERS[provider_name]
            component.providers[provider_name] = provider.Exists(component)


    def GetReleases():
        pass

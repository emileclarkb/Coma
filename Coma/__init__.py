from typing import List, Union

# import requests

from Coma.Types import Component
from Coma.Providers import Provider
from Coma.Requirements import Requirement


class Coma:
    def __init__(self, providers: List[Provider]) -> None:
        self.providers = {provider.name: provider for provider in providers}
        self.requirements = []

    def RequireFile(self, name: str, fallback=None, format=None) -> None:
        requirement = Requirement(name, fallback, format)
        self.requirements.append(requirement)
    
    def NewComponent(self, name: str, author: str) -> Component:
        component = Component(name, author)
        component.providers = dict.fromkeys(self.providers)
        return component

    '''
    Find out which providers (ie github, gitlab, bitbucket)
    are hosting this component
    '''
    def FillProviders(self, component: Component) -> List[str]:
        for provider_name in component.providers.keys():
            provider = self.providers[provider_name]
            component.providers[provider_name] = provider.Exists(component)


    def GetReleases(self):
        pass


    # Check to see if the data returned by all providers
    # for the component is the same (matches)
    def CheckProvidersMatch(self, component: Component) -> bool:
        return None

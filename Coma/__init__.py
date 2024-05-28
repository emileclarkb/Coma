from typing import List

from Coma.Result import Result
from Coma.GitManager import GitManager
from Coma.Types import Component
from Coma.Providers import Provider
from Coma.Requirements import Requirement
from Coma.Requirements.Format.Interfaces import FormatInterface


class Coma:
    def __init__(self, providers: List[Provider]) -> None:
        self.providers = {provider.name: provider for provider in providers}
        self.requirements = []

    def RequireFile(self, name: str, fallback=None, 
                          format: FormatInterface = None) -> None:
        requirement = Requirement(name, fallback, format)
        self.requirements.append(requirement)
    
    def NewComponent(self, name: str, author: str) -> Component:
        component = Component(name, author)
        component.providers = dict.fromkeys(self.providers)
        return component


    def RequirementsMet(self, component: Component) -> bool:
        for requirement in self.requirements:
            # Todo: use default branch name here instead
            

    '''
    Find out which providers (ie github, gitlab, bitbucket)
    are hosting this component
    '''
    def FillProviders(self, component: Component) -> List[str]:
        for provider_name in component.providers.keys():
            provider = self.providers[provider_name]
            component.providers[provider_name] = provider.GetData(component)

    # TODO: put methods like this into the component class
    def GetFirstAvailable(self, component: Component) -> List[str]:
        for provider_name in component.providers.keys():
            provider = self.providers[provider_name]
            return provider.GetData(component)

    def GetReleases(self):
        pass


    # Check to see if the data returned by all providers
    # for the component is the same (matches)
    def CheckProvidersMatch(self, component: Component) -> bool:
        return None

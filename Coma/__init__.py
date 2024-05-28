
import json
import toml
from typing import List

from Coma.Result import Result
# from Coma.GitManager import GitManager
from Coma.Types import Component
from Coma.Providers import Provider
from Coma.Requirements import Requirement
from Coma.Requirements.Format.Interfaces import FormatInterface


class Coma:
    def __init__(self, providers: List[Provider]) -> None:
        self.providers = {provider.name: provider for provider in providers}
        self.requirements = []

    def RequireFile(self, name: str, type: str,
                          fallback=None, 
                          format: FormatInterface = None) -> None:
        requirement = Requirement(name, type, fallback, format)
        self.requirements.append(requirement)
    
    def NewComponent(self, author: str, name: str) -> Component:
        component = Component(author, name)
        component.providers = dict.fromkeys(self.providers)
        return component

    '''
    Verify something is a package by checking all requirements are met
    '''
    def IsPackage(self, component: Component) -> Result:
        good_results = []
        bad_results = []
        for requirement in self.requirements:
            # Todo: use default branch name here instead
            # Todo: actually implement this (don't just use GitHub)
            provider = self.providers['GitHub']
            result = provider.GetFile(component, 'master', requirement.name)
            if result:
                if requirement.type == 'json':
                    result.value = json.loads(result.value)
                elif requirement.type == 'toml':
                    result.value = toml.loads(result.value)
                valid = requirement.format.Validate(result.value)
                if valid:
                    good_results.append(valid)
                else:
                    failure = Result.Fail(valid.reasons, value=result.value)
                    bad_results.append(failure)
            else:
                bad_results.append(result)
        if bad_results: return Result.Fail('not a package', value=bad_results)
        return Result.Succeed(good_results)
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

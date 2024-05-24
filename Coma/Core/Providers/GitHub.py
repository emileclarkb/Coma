import requests
from typing import List

from Coma.Core.Branch import Branch
from Coma.Core.Commit import Commit
from Coma.Core.Release import Release
from Coma.Core.Component import Component
from Coma.Core.Providers import Provider, ProviderData


class GitHubData(ProviderData):
    name = 'GitHub'
    def __init__(self, exists=True) -> None:
        super().__init__(exists=exists)

class GitHub(Provider):
    name = 'GitHub'
    def __init__(self) -> None:
        super().__init__()

    def GetRepoPath(self, component: Component):
        name, author = component.Unpack()
        return f'https://api.github.com/repos/{name}/{author}'

    def Exists(self, component: Component) -> bool:
        result = requests.get(self.GetRepoPath(component))
        exists = True if result.status_code == 200 else False
        return GitHubData(exists=exists)

    def GetBranches(self, component: Component) -> List[Branch]:
        name, author = component.Unpack()
        url = 'https://api.github.com/repos/{}/{}/branches'
        result = requests.get(url.format(name, author))

        branches = []
        for branch in result.json():
            try:
                sha = branch['commit']['sha']
                url = branch['commit']['url']
                commit = Commit(sha, url)
                new_branch = Branch(branch['name'], commit)
                branches.append(new_branch)
            except KeyError as e:
                print(e)
        return branches

    def GetReleases(self, component: Component) -> List[Release]:
        name, author = component.Unpack()
        url = 'https://api.github.com/repos/{}/{}/releases'
        result = requests.get(url.format(name, author))

        releases = []
        for release in result.json():
            try:
                new_release = Release(release['tag_name'])
                releases.append(new_release)
            except KeyError as e:
                print(e)
        return releases

import requests
from typing import List, Optional, Union

from Coma.Types import Author, Branch, Commit, Release, Component
from Coma.Providers.ProviderApi import Provider, ProviderData


class GitHubData(ProviderData):
    name = 'GitHub'
    def __init__(self, clone_url: str, website: str, owner: Author, 
                       default_branch: str, contributors: List[Author],
                       num_contributors: int) -> None:
        super().__init__()
        
        # TODO: provider = GITHUB() OBJECT REFERENCE HERE
        # THIS SHOULD CHANGE DEPENDING ON WHICH PROVIDER MADE THIS OBJECT
        
        self.clone_url = clone_url
        self.website = website
        self.owner = owner
        self.contributors = contributors
        self.num_contributors = num_contributors
        
        '''
        Variables beyond this section are not necessary for the app,
        but they are necessary internally. So ProviderData objects
        might need to have an alternative class that handles their
        data being cropped and given to the app.
        '''
        
        self.default_branch = default_branch
        
        # the maximum number of contributors we're willing to display
        # TODO: make this a config option OUTSIDE of Coma, 
        #       that way Karma can change it too
        self.MAX_CONTRIBUTORS = 5
        

class GitHub(Provider):
    name = 'GitHub'
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def ParseAuthor(json_content) -> Author:
        name = json_content['login']
        website =  json_content['html_url']
        avatar_url = json_content['avatar_url']
        return Author(name, website, avatar_url)

    @staticmethod
    def GetData(component: Component) -> Optional[GitHubData]:
        path = 'https://api.github.com/repos/{}/{}'
        path = path.format(component.author, component.name)
        result = requests.get(path)
        if not result.ok: return None
        content = result.json()        

        clone_url = content['clone_url']
        website = content['html_url']
        owner = GitHub.ParseAuthor(content['owner'])
        default_branch = content['default_branch']
        contrib_url = content['contributors_url']
        contributors, num_contributors = GitHub.GetContributors(contrib_url)
        data = GitHubData(clone_url, website, owner, default_branch,
                          contributors, num_contributors)
        
    # The contributor list INCLUDES the owner
    @staticmethod
    def GetContributors(url: str, max=None) -> Optional[tuple[List[Author], int]]:
        result = requests.get(url)
        if not result.ok: return None
        content = result.json()
        
        num_contributors = len(content)
        contributors = []
        for i, contributor in enumerate(content):
            # we've reached the maximum number of 
            # contributors we're allowed to parse
            if max is not None and i+1 >= max:
                break
            contributors.append(GitHub.ParseAuthor(contributor))
        return contributors, num_contributors
                
    @staticmethod
    def GetReleases(component: Component) -> Optional[List[Release]]:
        path = 'https://api.github.com/repos/{}/{}/tags'
        path = path.format(component.author, component.name)
        result = requests.get(path)
        if not result.ok: return None

        releases = []
        for release in result.json():
            commit = Commit(release['commit']['sha'], release['commit']['url'])
            zipball_url = release['zipball_url']
            tarball_url = release['tarball_url']
            new_release = Release(release['name'], commit,
                                  zipball_url=zipball_url, 
                                  tarball_url=tarball_url)
            releases.append(new_release)
        return releases
    '''
    def GetReleases(self, component: Component) -> List[Release]:
        path = 'https://api.github.com/repos/{}/{}/releases'
        path = path.format(component.author, component.name)
        result = requests.get(path)

        releases = []
        for release in result.json():
            try:
                new_release = Release(release['tag_name'])
                releases.append(new_release)
            except KeyError as e:
                print(e)
        return releases
    '''
    
    @staticmethod
    def GetBranches(component: Component) -> Optional[List[Branch]]:
        path = 'https://api.github.com/repos/{}/{}/branches'
        path = path.format(component.author, component.name)
        result = requests.get(path)
        if not result.ok: return None

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
    
    @staticmethod
    def GetFileContent(component: Component, branch: str, 
                       filename: str) -> Optional['json']:
        path = 'https://raw.githubusercontent.com/{}/{}/{}/{}'
        path = path.format(component.author, component.name, branch, filename)
        result = requests.get(path)
        return result.content if result.ok else None          filename: str) -> Optional['json']:
        
    
    @staticmethod
    def GetReadme(component: Component, branch: str) -> Optional[str]:
        result = GitHub.GetFileContent(component, branch, 'README.md')
        if result is None:
            result = GitHub.GetFileContent(component, branch, 'README')
        
    '''
    # TODO: reference ProviderData.default_branch instead of taking paramater
    @staticmethod
    def GetMetadata(component: Component, branch: str, 
                    file_name: str) -> Optional[Union[tuple, list]]:
        path = 'https://raw.githubusercontent.com/{}/{}/{}/{}'
        path = path.format(component.author, component.name, branch, file_name)
        result = requests.get(path)
        return result.content if result.ok else None
    '''

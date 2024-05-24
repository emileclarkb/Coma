import re
import requests

from Coma.Core.Component import Component
from Coma.Core.Providers import Provider, ProviderData


REDIRECTION = '<html><body>You are being <a href='    \
              '\"https://gitlab.com/users/sign_in\">' \
              'redirected</a>.</body></html>'

class GitLabData(ProviderData):
    name = 'GitLab'
    def __init__(self, project_id: str, exists=True) -> None:
        super().__init__(exists=exists)
        self.project_id = project_id

    @classmethod
    def DoesNotExist(cls) -> 'ProviderData':
        data = cls(None, exists=False)
        return data


class GitLab(Provider):
    name = 'GitLab'
    def __init__(self) -> None:
        super().__init__()

    def GetRepoPath(self, component: Component) -> str:
        return f'https://gitlab.com/{component.author}/{component.name}'

    def GetProjectId(self, content: str) -> str:
        project_id = re.search('\"project_id\":(\d+),', content)
        print(f'Project Id: {project_id}')
        return project_id

        # '"project_id":47682153,'

    def Exists(self, component: Component) -> GitLabData:
        path = self.GetRepoPath(component)
        print(path)
        result = requests.get(path)
        print(result.status_code)
        if result.status_code != 200: return GitLabData.DoesNotExist()

        project_id = self.GetProjectId(result.content)
        return GitLabData(project_id)

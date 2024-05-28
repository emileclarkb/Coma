import re
import requests
from typing import Optional

from Coma.Types import Component
from Coma.Providers.ProviderApi import Provider, ProviderData


class GitLabData(ProviderData):
    name = 'GitLab'
    def __init__(self, project_id: str,) -> None:
        super().__init__()
        self.project_id = project_id


class GitLab(Provider):
    name = 'GitLab'
    def __init__(self) -> None:
        super().__init__()

    def GetRepoPath(self, component: Component) -> str:
        return f'https://gitlab.com/{component.author}/{component.name}'

    def GetProjectId(self, content: str) -> str:
        project_id = re.search('\"project_id\":(\d+),', content)
        print(f'Project Id: {project_id}') # TODO: (Debug) Remove
        return project_id

        # '"project_id":47682153,'

    def GetData(self, component: Component) -> Optional[GitLabData]:
        path = self.GetRepoPath(component)
        result = requests.get(path)
        if not result.ok: return None

        project_id = self.GetProjectId(result.content)
        return GitLabData(project_id)

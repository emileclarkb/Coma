import os
from shutil import rmtree
from pathlib import Path

from Coma.Types import Component, Commit


'''
Storage Directory Structure:


username (dir)
    component_1 (dir)
        VERSION_1
        VERSION_2
        ...
    component_2 (dir)
        VERSION_1
        VERSION_2
        ...
    ...
    component_n (dir)
        VERSION_1
        VERSION_2
        ...
    
    
Or if we ARE keeping the git repo
ONLY DO THIS IF YOU COMPLETELY TRUST THE SOURCE CODE

        
username (dir)
    component_1 (dir)
        VERSIONS_FILE (this file is a mapping between versions and their commit sha)
        GIT_REPO      (can change version at will)

    component_2 (dir)
    ...
    component_n (dir)
'''
class GitManager:
    def __init__(self, storage_path: str, keep_git=True) -> None:
        self.storage_path = storage_path
        self.keep_git = keep_git
        if not os.path.exists(storage_path):
            msg = 'Component storage path does not exist, path: {storage_path}'
            raise FileNotFoundError(msg)
    
    def GetCloneLocation(self, component: Component) -> str:
        # TODO: change component to have a version number (for what we are targetting)
        relative_loc = f'{component.author}/{component.name}/{VERSION}'
        return os.path.join(self.storage_path, relative_loc)
    
    def EnsurePathExists(path: str) -> None:
        Path(path).mkdir(parents=True, exist_ok=True)
    
    # returns status: pass (True), fail (False)
    def Clone(self, component: Component) -> bool:
        # TODO: do something better than os.system, 
        #       use subprocess so you can capture stdout and stderr
        # TODO: implement component.source (see: GitHubData)
        clone_path = self.GetCloneLocation(component)
        os.system(f'git clone {component.source.clone_url} {clone_path}')
    
    def ResetToCommit(self, component: Component, commit: Commit, 
                            purge_git=False) -> None:
        # TODO: do something better than os.system, 
        #       use subprocess so you can capture stdout and stderr
        cwd = os.getcwd()
        
        os.chdir(self.GetCloneLocation(component))
        os.system(f'git reset --hard {commit.sha}')
        
        if purge_git:
            self.PurgeGitFromCwd()
        
        os.chdir(cwd) # reset back to where we were
        
    @staticmethod
    def PurgeGitFromCwd(self) -> None:
        rmtree('.git')
        os.remove('.gitignore')
        # TODO: add more (ie for gitlab CI/CD)
        
        

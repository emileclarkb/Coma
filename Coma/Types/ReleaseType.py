from Coma.Types.CommitType import Commit

class Release:
    def __init__(self, name: str, commit: Commit, 
                       zipball_url=None, tarball_url=None) -> None:
        self.name = name
        self.commit = commit
        self.zipball_url = zipball_url
        self.tarball_url = tarball_url
    def __str__(self) -> str:
        return f'Release({self.name})'

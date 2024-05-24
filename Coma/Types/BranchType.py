from Coma.Types.CommitType import Commit

class Branch:
    def __init__(self, name: str, commit: Commit) -> None:
        self.name = name
        self.commit = commit

    def __str__(self) -> str:
        return f'Branch(name={self.name}, Commit({self.commit.sha}))'

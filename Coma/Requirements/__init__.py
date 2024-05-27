class Requirement:
    def __init__(self, name: str, fallback: str, format) -> None:
        self.name = name
        self.fallback = fallback
        self.format = format

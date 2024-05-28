class Requirement:
    def __init__(self, name: str, type:str, 
                       fallback: str, format) -> None:
        self.name = name
        self.type = type
        self.fallback = fallback
        self.format = format

class Component:
    def __init__(self, name: str, author: str) -> None:
        self.name = name
        self.author = author

        # the provider that is currently selected
        self.source = None
        # list of providers that are hosting this component
        self.providers = {}

    def Unpack(self):
        return self.name, self.author

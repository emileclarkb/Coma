from typing import Optional


class ProviderData:
    name = 'Provider'
    def __init__(self) -> None:
        pass

class Provider:
    name = 'Provider'
    def __init__(self) -> None:
        pass

    ''' Override '''
    def Exists(self, _) -> Optional[ProviderData]:
        return None

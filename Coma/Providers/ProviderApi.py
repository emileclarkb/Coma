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
    def GetData(self, _) -> Optional[ProviderData]:
        return None


class ProviderData:
    name = 'Provider'
    def __init__(self, exists=True) -> None:
        self.exists = exists

    @classmethod
    def DoesNotExist(cls) -> 'ProviderData':
        data = cls(exists=False)
        return data




class Provider:
    name = 'Provider'
    def __init__(self) -> None:
        pass

    ''' Override '''
    def Exists(self, _) -> ProviderData:
        return ProviderData.DoesNotExist()

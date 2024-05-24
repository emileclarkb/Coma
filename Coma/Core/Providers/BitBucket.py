from Coma.Core.Component import Component
from Coma.Core.Providers import Provider, ProviderData


class BitBucketData(ProviderData):
    name = 'BitBucket'
    def __init__(self, exists=True) -> None:
        super().__init__(exists=exists)

class BitBucket(Provider):
    name = 'BitBucket'
    def __init__(self) -> None:
        super().__init__()

    def Exists(self, component: Component) -> ProviderData:
        return BitBucketData.DoesNotExist()

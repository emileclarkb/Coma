from typing import Optional

from Coma.Types import Component
from Coma.Providers.ProviderApi import Provider, ProviderData


class BitBucketData(ProviderData):
    name = 'BitBucket'
    def __init__(self) -> None:
        super().__init__()

class BitBucket(Provider):
    name = 'BitBucket'
    def __init__(self) -> None:
        super().__init__()

    def GetData(self, component: Component) -> Optional[BitBucketData]:
        return None

from abc import ABC, abstractmethod

class ProviderInterface(ABC):

    @abstractmethod
    async def check_latest_digest(self, project: str, repository: str, tag: str) -> str:
        pass
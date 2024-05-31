from app.registry_providers.harbor_provider import HarborProvider
from app.singleton import Singleton
import asyncio

@Singleton
class RegistryService:
    def __init__(self):
        self.providers = {}

        domain = 'pp4l1660.c1.de1.container-registry.ovh.net'
        harbor_provider = HarborProvider()
        self.providers[domain] = harbor_provider

    def check_for_latest_digest(self, domain, project, repository, tag):
        provider = self.providers[domain]
        print(f'Provider domain {domain}')
        digest = asyncio.run(provider.check_latest_digest(project, repository, tag)) or 'not found'
        return digest

    def is_registry_supported(self, domain: str) -> bool:
        supported = domain in self.providers
        return supported

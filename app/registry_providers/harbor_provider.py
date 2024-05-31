import base64
import json

from harborapi import HarborClient
from httpx import HTTPStatusError

from app.models.registry_creds import RegistryCreds
from app.registry_providers.provider_interface import ProviderInterface
from app.services.kub_client import KubeClient


class HarborProvider(ProviderInterface):
    def __init__(self):
        self.registry_creds = []
        self._initialize_client()

    def _initialize_client(self):
        secret = str(KubeClient.instance().core_api.read_namespaced_secret("regcred", "default").data)
        secret = secret.replace("\'", "\"")

        secret_json = json.loads(secret)
        secret_key = secret_json.get('.dockerconfigjson')
        secret_decoded = base64.b64decode(secret_key).decode('utf-8')

        decoded_secret_json = json.loads(secret_decoded)

        url = list(decoded_secret_json['auths'].keys())[0]
        print(f'Harbor url parsed from secret: {url}')
        username = decoded_secret_json['auths'][url]['username']
        password = decoded_secret_json['auths'][url]['password']

        harbor_registry_creds = RegistryCreds(url=f'https://{url}/api/v2.0', username=username, password=password)
        self.registry_creds.append(harbor_registry_creds)
        self.harbor_client = HarborClient(url=f'https://{url}/api/v2.0', username=username, password=password) or None

    async def check_latest_digest(self, project: str, repository: str, tag: str) -> str:
        try:
            result = self.harbor_client.get_artifact(project_name=project, repository_name=repository, reference=tag)
            print(f'Result {result.digest}')
            return result.digest
        except HTTPStatusError as e:
            print(f'Error retrieving latest digest from harbor: str(e.response.content))')
            return str(e.response.status_code)

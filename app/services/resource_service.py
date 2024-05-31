import json

from app.models.found_res import FoundRes
from app.services.kub_client import KubeClient
from app.singleton import Singleton
from datetime import datetime


@Singleton
class ResourceService:
    def __init__(self):
        self.resources = []
        print('Singleton instance of ResourceService has been created.')

    def fetch_annotated_resources(self, app):
        print(f'Run task at {datetime.now()}')
        with app.app_context():
            self.resources.clear()

            print("Listing Pods with their IPs:")
            ret = KubeClient.instance().core_api.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:

                if i.metadata.annotations and "image.pod.updater" in i.metadata.annotations:
                    print("Found annotation!")

                    container_name = i.metadata.annotations["image.pod.updater"]
                    print(f'Extracted container_name: {container_name}')

                    for container in i.spec.containers:
                        if container.name == container_name:
                            print(f'Container name: {container.name}')
                            print(f'Image: {container.image}')

                            for container_status in i.status.container_statuses:
                                if container_status.name == container_name:
                                    print(f'Found container status for container_name: {container_name}')

                                    image_splits = container.image.split('/')
                                    image_domain = image_splits[0]
                                    image_project_name = image_splits[1]
                                    image_repository_name = image_splits[2].split(':')[0]
                                    image_reference = image_splits[2].split(':')[1]
                                    image_digest = container_status.image_id.split(":")[1]

                                    self.resources.append(
                                        FoundRes(name=i.metadata.name,
                                                 namespace=i.metadata.namespace,
                                                 image_domain=image_domain,
                                                 image_project_name=image_project_name,
                                                 image_repository_name=image_repository_name,
                                                 image_reference=image_reference,
                                                 time_added=datetime.utcnow().isoformat(), latest_checked=None,
                                                 current_digest=container_status.image_id.split(":")[1])
                                    )
                        else:
                            print(f'Container name does not match with annotated one.')

            print('Pods found with annotation:')
            print(str([p.to_dict() for p in self.resources]))

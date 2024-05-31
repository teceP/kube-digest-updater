from datetime import datetime

from kubernetes.client import V1Pod

from app.helpers.helper import Helper
from app.models.found_res import FoundRes
from app.services.kub_client import KubeClient
from app.services.registry_service import RegistryService
from app.services.resource_service import ResourceService

resource_service = ResourceService.instance()
registry_service = RegistryService.instance()
kube_client = KubeClient.instance()


def periodic_fetch_annotated_resources(self):
    ## get all new information and store in kube_client lists
    kube_client.gather_all_apps_with_annotation()
    for t in kube_client.targets:
        print(f'Target: {t}')
        app_name = t['name']
        namespace = t['namespace']
        containers = t['containers'].split(',')

        pods = kube_client.pods_for_app_name(app_name=app_name, namespace=namespace)

        for pod in pods:

            print(f'Check in pod {pod.metadata.name} ...')
            for container_status in pod.status.container_statuses:
                print(f'Check if container \'{container_status.name}\' in \'{containers}\' ...')
                container_name = container_status.name
                if container_name in containers:
                    print('Containername is in containername-list.')

                    image = container_status.image
                    image_id = container_status.image_id
                    print(f'Current container image: {container_status.image}')
                    print(f'Current container image ID: {container_status.image_id}')

                    domain: str = Helper.get_domain_from_image_id(image_id)

                    print(f'Parsed domain: {str(domain)}')
                    is_registry_supported = registry_service.is_registry_supported(
                        domain=domain)

                    if is_registry_supported:
                        print(f'Registry {domain} is supported')

                        project = Helper.get_project_from_image_id(image_id)
                        repository = Helper.get_repository_from_image_id(image_id)
                        tag = Helper.get_tag_from_image(image)

                        print(f'Image parsed. domain={domain}, project={project}, repository={repository}, tag={tag}')

                        digest = registry_service.check_for_latest_digest(domain=domain, project=project,
                                                                          repository=repository,
                                                                          tag=tag)
                        print(f'Latest digest found by registry service: {digest}')

                        current_digest = Helper.get_sha_from_image_id(image_id)
                        print(f'Current deployt digest: {current_digest}')

                        print(f'{digest}')
                        print(f'{current_digest}')

                        are_digest_same = digest == current_digest
                        print(f'Are digest same? {str(are_digest_same)}')
                        pod_name = pod.metadata.name
                        namespace = pod.metadata.namespace

                        if not are_digest_same:

                            print(f'Pod restart will be executed on pod \'{pod_name}\' in namespace \'{namespace}\'')
                            kube_client.redeploy_pod(pod_name=pod_name, namespace=namespace)
                        else:
                            print(f'Image in pod \'{pod_name}\' in namespace \'{namespace}\' is up to date.')
                    else:
                        print(f'Registry {domain} is not supported')
                else:
                    print('It is not in containername-list.')

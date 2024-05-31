from kubernetes.client import ApiException

from app.singleton import Singleton
from kubernetes import client, config
import datetime


@Singleton
class KubeClient:

    def __init__(self):
        self.targets = []
        config.load_incluster_config()
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()



    # Where app_name is daemonset/statefulset/deployment name
    # Can of course contain multiple pods for each app
    def pods_for_app_name(self, app_name, namespace):
        label_selector = f'app.kubernetes.io/name={app_name}'
        pods = self.core_api.list_namespaced_pod(label_selector=label_selector, namespace=namespace).items
        return pods

    def gather_all_apps_with_annotation(self):
        self.targets.clear()
        self._gather_daemonsets_with_annotation()
        self._gather_statefulset_with_annotation()
        self._gather_deployments_with_annotation()

    def _gather_daemonsets_with_annotation(self):
        self.targets.extend(self._resources_with_annotation(self.apps_api.list_daemon_set_for_all_namespaces))
        print(f'Found targets in total: {self.targets}')

    def _gather_statefulset_with_annotation(self):
        self.targets.extend(self._resources_with_annotation(self.apps_api.list_stateful_set_for_all_namespaces))
        print(f'Found targets in total: {self.targets}')

    def _gather_deployments_with_annotation(self):
        self.targets.extend(self._resources_with_annotation(self.apps_api.list_deployment_for_all_namespaces))
        print(f'Found targets in total: {self.targets}')

    def _resources_with_annotation(self, resource_list_method):
        resources_with_annotation = []
        for resource in resource_list_method().items:
            annotations = resource.metadata.annotations
            contains_annotation = 'image.pod.updater' in annotations if annotations else False
            if annotations and contains_annotation:
                name_and_container_names = {
                    'name': resource.metadata.name,
                    'namespace': resource.metadata.namespace,
                    'containers': annotations['image.pod.updater'],
                    'additional': annotations.get('image.pod.updater.additional', '')
                }
                ## additional:
                ## Any additional restarts can be defined here. For example,
                ## in cases where a website gets redeployed,
                ## the corresponding cache in front of it needs to be redeployed.
                ## NamespaceA=shopware-stage;NamespaceB=varnish-stage

                resources_with_annotation.append(name_and_container_names)
        return resources_with_annotation

    def gathered_apps_result(self):
        result = {
            'targets': self.targets
        }

        return result

    def redeploy_pod(self, pod_name, namespace):
        now = datetime.datetime.utcnow()
        now = str(now.isoformat("T") + "Z")
        body = {
            'spec': {
                'template': {
                    'metadata': {
                        'annotations': {
                            'kubectl.kubernetes.io/restartedAt': now
                        }
                    }
                }
            }
        }

        try:
            return str(self.core_api.patch_namespaced_pod(name=pod_name, namespace=namespace, body=body, pretty='true'))
        except ApiException as e:
            print(f'Exception when calling patch_namespaced_pod with name={pod_name}, namespace={namespace}: {e}')
            return str(e)

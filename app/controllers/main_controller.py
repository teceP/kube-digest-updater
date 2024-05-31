import nest_asyncio

from flask import Blueprint, render_template, jsonify, current_app
from ..models.found_res import FoundRes
from datetime import datetime
from urllib.parse import urlparse

from ..services.kub_client import KubeClient
from ..services.registry_service import RegistryService
from ..services.resource_service import ResourceService

main = Blueprint('main', __name__)
resource_service = ResourceService.instance()
registry_service = RegistryService.instance()
kub_client = KubeClient.instance()

@main.route('/')
def index():
    task_interval_seconds = current_app.config['TASK_INTERVAL_SECONDS']
    print(f'Task Interval Seconds from Config: {task_interval_seconds}')
    return render_template('index.html')


@main.route('/list')
def get_list():
    return jsonify([p.to_dict() for p in resource_service.resources])


@main.route('/add_item')
def add_item():
    new_item = FoundRes(name='Test', namespace='Monitoring', image='docker.io/...', latest_checked=None,
                        current_digest=None, time_added=datetime.utcnow().isoformat())
    resource_service.resources.append(new_item)
    return jsonify({"status": "success", "new_item": new_item.to_dict()})


@main.route('/updatelist')
def list_pod_for_all_namespaces():
    resource_service.fetch_annotated_resources(current_app)
    return jsonify([p.to_dict() for p in resource_service.resources])


@main.route('/hc')
async def check_harbor():
    digest = ''

    for found_res in resource_service.resources:
        print('For found res in resources...')
        print(f'image_domain: {found_res.image_domain}')
        harbor_domain = urlparse(registry_service.harbor_client.url).netloc
        print(f'harbor url: {harbor_domain}')

        if found_res.image_domain == harbor_domain:
            print('Found found_res.image_domain in harbor client url')
            artifacts = registry_service.harbor_client.get_artifact(
                project_name=found_res.image_project_name,
                repository_name=found_res.image_repository_name,
                reference=found_res.image_reference)

            print(f'Artifacts: {artifacts.digest}')
            digest = str(artifacts.digest).split(":")[1]
            found_res.latest_digest = digest
            print(f'FoundRes: {found_res.to_dict()}')

    return digest

@main.route('/redeploy')
def redeploy_pod():
    namespace = 'monitoring'
    deployment = 'grafana-image-renderer'
    return KubeClient.instance().redeploy_pod(namespace=namespace, deployment=deployment)

@main.route('/gather')
def gather_apps():
    kub_client.gather_all_apps_with_annotation()

    return jsonify(kub_client.gathered_apps_result())

@main.route('/pods')
def gather_pods():
    pods = kub_client.pods_for_app_name(app_name='grafana-image-renderer', namespace='monitoring')
    result = [p.to_dict() for p in pods]

    return jsonify(result)


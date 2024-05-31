class FoundRes:
    def __init__(self, name, namespace, image_domain, image_project_name, image_repository_name, image_reference,
                 time_added,
                 latest_checked, current_digest, latest_digest=''):
        self.name = name
        self.namespace = namespace
        self.image_domain = image_domain
        self.image_project_name = image_project_name
        self.image_repository_name = image_repository_name
        self.image_reference = image_reference
        self.time_added = time_added
        self.latest_checked = latest_checked
        self.current_digest = current_digest
        self.latest_digest = latest_digest

    def to_dict(self):
        return {
            'name': self.name,
            'namespace': self.namespace,
            'image_domain': self.image_domain,
            'image_project_name': self.image_project_name,
            'image_repository_name': self.image_repository_name,
            'image_reference': self.image_reference,
            'time_added': self.time_added,
            'latest_checked': self.latest_checked,
            'current_digest': self.current_digest,
            'latest_digest': self.latest_digest
        }

    def __str__(self):
        return f'name: {self.name}, namespace: {self.namespace}, image_domain: {self.image_domain}, image_project_name: {self.image_project_name}, image_repository_name: {self.image_repository_name}, image_reference: {self.image_reference}, time_added: {self.time_added}, current_digest: {self.current_digest}, latest_digest: {self.latest_digest}'

class Helper:

    @staticmethod
    def get_domain_from_image_id(image_id: str) -> str:
        return image_id.split('/')[0]

    @staticmethod
    def get_project_from_image_id(image_id: str) -> str:
        return image_id.split('/')[1]

    @staticmethod
    def get_repository_from_image_id(image_id: str) -> str:
        return image_id.split('/')[2].split("@")[0]

    @staticmethod
    def get_sha_from_image_id(image_id: str) -> str:
        return image_id.split('@')[1]

    @staticmethod
    def get_tag_from_image(image: str) -> str:
        return image.split(':')[1]


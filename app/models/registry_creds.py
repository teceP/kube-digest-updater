class RegistryCreds:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'url': self.url,
            'username': self.username,
            'password': self.password
        }

class LoginType:
    def __init__(self, client_id, client_secret, grant_type, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.username = username
        self.password = password

    def prepare(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "password": self.password,
            "username": self.username,
        }
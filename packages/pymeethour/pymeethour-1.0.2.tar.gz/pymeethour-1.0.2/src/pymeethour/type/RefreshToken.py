class RefreshToken:
    def __init__(self, client_id:str, client_secret: str, refresh_token:str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.grant_type = "refresh_token"

    def prepare(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token
        }

from httpx import URL


class Session:
    access_token: str
    base_url: URL

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def get_access_token(self):
        return self.access_token

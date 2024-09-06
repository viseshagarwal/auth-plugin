import requests
from .base_auth import BaseAuth


class OAuth2Auth(BaseAuth):
    def __init__(self, client_id, client_secret, redirect_uri, auth_url, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url

    def get_authorization_url(self):
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"

    def get_access_token(self, code):
        response = requests.post(
            self.token_url,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        return response.json().get("access_token")

    def authenticate(self, token):
        raise NotImplementedError(
            "You need to implement the authenticate method to handle OAuth2-specific logic."
        )

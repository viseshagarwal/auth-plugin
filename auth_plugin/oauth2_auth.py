import requests
import logging
from requests.exceptions import RequestException
from .base_auth import BaseAuth


class OAuth2Auth(BaseAuth):
    def __init__(self, client_id, client_secret, redirect_uri, auth_url, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url

    def get_authorization_url(self):
        try:
            auth_url = f"{self.auth_url}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"
            logging.info("Authorization URL generated successfully")
            return auth_url
        except Exception as e:
            logging.error(f"Error generating authorization URL: {str(e)}")
            raise RuntimeError("Failed to generate authorization URL")

    def get_access_token(self, code):
        try:
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
            response.raise_for_status()
            token = response.json().get("access_token")
            logging.info("Access token received successfully")
            return token
        except RequestException as e:
            logging.error(f"Error getting access token: {str(e)}")
            raise RuntimeError("Failed to obtain access token")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise RuntimeError("An unexpected error occurred during token retrieval")

    def authenticate(self, token):
        raise NotImplementedError(
            "You need to implement the authenticate method to handle OAuth2-specific logic."
        )

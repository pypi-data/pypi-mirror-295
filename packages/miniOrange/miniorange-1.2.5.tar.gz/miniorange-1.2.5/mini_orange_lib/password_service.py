from typing import Dict
import requests
from urllib.parse import urlencode
import logging
from mini_orange_lib.exceptions import TokenRequestError
from mini_orange_lib.auth_service import AuthorizationFlow

class PasswordFlow(AuthorizationFlow):
    """Handles Resource Owner Password Credentials Grant flow."""

    def build_auth_url(self) -> Dict:
        """Password flow does not require an authorization URL."""
        return {}

    def request_token_password(self, username: str, password: str) -> Dict:
        """Requests the token using resource owner password credentials."""
        base_url = self.config.base_url
        client_id = self.config.credentials.client_id
        client_secret = self.config.credentials.client_secret

        if not username or not password:
            raise ValueError("Username and password must be provided")

        params = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        }
        post_url = f"{base_url}/moas/rest/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(post_url, data=urlencode(params), headers=headers)
            response.raise_for_status()
            data = response.json()
            logging.debug(f"Token endpoint response: {data}")
            return data
        except requests.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            raise TokenRequestError(f"Token request failed: {str(e)}")

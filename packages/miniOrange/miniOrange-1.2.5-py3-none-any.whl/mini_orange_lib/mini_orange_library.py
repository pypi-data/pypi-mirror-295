import logging
import requests
from mini_orange_lib import PasswordFlow, TokenResponseHandler, JWTManager, Config
from mini_orange_lib.auth_service import AuthCodeFlow, PKCEFlow, ImplicitFlow

class MiniOrangeLibrary:
    def __init__(self, config: Config):
        """Initializes the MiniOrangeLibrary with the provided configuration."""
        if not isinstance(config, Config):
            raise TypeError("Expected config to be an instance of Config")
        self.config = config
        self.token_response_handler = TokenResponseHandler(config)
        self.jwt_manager = JWTManager(config.public_key, config.credentials.client_id)
        self.password_flow = PasswordFlow(config)

    def start_authentication(self, grant_type: str) -> str:
        """Starts the authentication process based on the grant type."""
        auth_flow = self._get_auth_flow(grant_type)
        return auth_flow.build_auth_url()

    def _get_auth_flow(self, grant_type: str):
        """Returns the appropriate authorization flow based on the grant type."""
        if grant_type == 'auth_code':
            return AuthCodeFlow(self.config)
        elif grant_type == 'auth_pkce':
            return PKCEFlow(self.config)
        elif grant_type == 'implicit':
            return ImplicitFlow(self.config)
        else:
            raise ValueError(f"Unsupported grant type: {grant_type}")

    def handle_auth_response(self, uri: str, code_verifier: str = None) -> dict:
        """Handles the authentication response and extracts tokens."""
        try:

            return self.token_response_handler.handle_authorization_response(uri,  code_verifier)
        except Exception as e:
            logging.error(f"Error handling authentication response: {e}")
            return {"status": "failure", "message": str(e)}

    def request_token_password(self, username: str, password: str) -> dict:
        """Requests an access token using resource owner password credentials."""
        try:
            return self.password_flow.request_token_password(username, password)
        except Exception as e:
            logging.error(f"Error requesting token with password: {e}")
            return {"status": "failure", "message": str(e)}

    def fetch_user_info(self, access_token: str) -> dict:
        """Fetches user information using the provided access token."""
        user_info_url = f"{self.config.base_url}/moas/rest/oauth/getuserinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            response = requests.get(user_info_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request error fetching user info: {e}")
            return {"status": "failure", "message": str(e)}

    def decode_jwt(self, token: str) -> dict:
        """Decodes a JWT and returns the payload."""
        try:
            return self.jwt_manager.decode_jwt(token)
        except Exception as e:
            logging.error(f"Error decoding JWT: {e}")
            return {"status": "failure", "message": str(e)}


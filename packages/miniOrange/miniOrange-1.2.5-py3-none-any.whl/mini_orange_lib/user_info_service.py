# mini_orange_lib/user_info_service.py
import logging

import requests
from mini_orange_lib.config import Config
from mini_orange_lib.exceptions import AuthorizationError

class UserInfoService:
    def __init__(self, config: Config):
        if not isinstance(config, Config):
            raise TypeError("Expected config to be an instance of Config")
        self.config = config

    def fetch_user_info(self, access_token: str) -> dict:
        """Fetches user information using the access token."""
        if not access_token:
            raise ValueError("Access token must be provided")

        user_info_url = f"{self.config.base_url}/moas/rest/oauth/getuserinfo"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            logging.debug( f"Sending request to {user_info_url} with headers: {headers}" )
            response = requests.get( user_info_url  , headers=headers )
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logging.debug( f"User info response: {data}" )
            return data
        except requests.HTTPError as http_err:
            logging.error( f"HTTP error occurred: {http_err}" )
            raise AuthorizationError( f"HTTP error occurred: {http_err}" )
        except requests.RequestException as req_err:
            logging.error( f"Request error: {req_err}" )
            raise AuthorizationError( f"Request error: {req_err}" )
        except ValueError as json_err:
            logging.error( f"Error parsing JSON response: {json_err}" )
            raise AuthorizationError( f"Error parsing JSON response: {json_err}" )
        except Exception as e:
            logging.error( f"Unexpected error: {e}" )
            raise AuthorizationError( f"Unexpected error: {e}" )

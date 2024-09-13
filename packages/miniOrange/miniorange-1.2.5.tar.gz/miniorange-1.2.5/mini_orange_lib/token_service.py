import requests
import logging
from urllib.parse import urlencode , urlparse , parse_qs

from flask import session

from mini_orange_lib.config import Config
from mini_orange_lib.exceptions import TokenRequestError , InvalidConfigurationError , AuthorizationError


class TokenResponseHandler:
    def __init__(self , config: Config):
        if not isinstance( config , Config ):
            raise TypeError( "Expected config to be an instance of Config" )
        self.config = config

    def handle_authorization_response(self , uri: str , code_verifier: str = None) -> dict:
        """Handles the authorization response based on the grant type."""
        if not all( [self.config.credentials.client_id , self.config.base_url , self.config.redirect_url] ):
            raise InvalidConfigurationError(
                parameter_name='client_id/client_secret/redirect_url' ,
                message="Client ID, Client Secret, or Redirect URL is not set"
            )

        # Parse the URI to handle query and fragment parts
        parsed_uri = urlparse( uri )
        logging.debug( f"Parsed URI: {parsed_uri}" )
        if parsed_uri.path == "/callback":
            query_params = parse_qs( parsed_uri.query )
            code = query_params.get( "code" , [None] )[0]
            state = query_params.get( "state" , [None] )[0]
            id_token = query_params.get( "id_token" , [None] )[0]
            logging.debug( f"Authorization code: {code}, State: {state}" )
            if state != session.get( 'state' ):
                logging.debug( f"State:{state},State_Session:{self.state}" )
                raise AuthorizationError( message="State is not matching" )
            if code:
                return self._request_token( code , code_verifier )
            if id_token:
                return {"id_token": id_token}
        else:
            raise AuthorizationError( message="Invalid callback URL" )

    def _request_token(self , code: str , code_verifier: str = None) -> dict:
        """Requests a token using the provided authorization code."""
        code_verifier = session.get( 'code_verifier' )
        logging.debug( f"Requesting token with code: {code} and code_verifier: {code_verifier}" )

        base_url = self.config.base_url
        redirect_url = self.config.redirect_url
        client_id = self.config.credentials.client_id
        client_secret = self.config.credentials.client_secret

        params = {
            'grant_type': 'authorization_code' ,
            'client_id': client_id ,
            'client_secret': client_secret ,
            'code': code ,
            'redirect_uri': redirect_url
        }
        if code_verifier:
            params['code_verifier'] = code_verifier

        post_url = f"{base_url}/moas/rest/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            logging.debug( f"Sending POST request to URL: {post_url} with params: {params}" )
            response = requests.post( post_url , data=urlencode( params ) , headers=headers )
            response.raise_for_status()
            try:
                data = response.json()
                logging.debug( f"Token endpoint response: {data}" )
                return data
            except ValueError:
                logging.error( "Failed to decode JSON response" )
                raise TokenRequestError( "Invalid JSON response from token endpoint" )
        except requests.RequestException as e:
            logging.error( f"Request error: {str( e )}" )
            raise TokenRequestError( f"Token request failed: {str( e )}" )

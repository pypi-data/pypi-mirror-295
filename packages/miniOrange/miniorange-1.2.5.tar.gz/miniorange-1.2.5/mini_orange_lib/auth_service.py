# mini_orange_lib/auth_service.py
import secrets
from flask import session
from mini_orange_lib.utils import generate_pkce_pair
from mini_orange_lib.token_service import TokenResponseHandler
class AuthorizationFlow:
    """Base class for authorization flows."""
    def __init__(self , config):
        self.config = config
        self.state = None

    def generate_state(self):
        self.state = secrets.token_urlsafe( 16 )
        session['state'] = self.state
        return self.state

    def build_auth_url(self):
        raise NotImplementedError( "Subclasses should implement this!" )

    def handle_authorization_response(self , uri):
        raise NotImplementedError( "Subclasses should implement this!" )
class AuthCodeFlow( AuthorizationFlow ):
    """Handles Authorization Code Grant flow."""
    def build_auth_url(self) -> str:
        """Builds the URL for the authorization code flow."""
        base_url = self.config.base_url
        client_id = self.config.credentials.client_id
        redirect_url = self.config.redirect_url
        state = self.generate_state()   # Function to generate a unique state

        auth_url = (
            f"{base_url}/moas/idp/openidsso?"
            f"&client_id={client_id}&"
            f"&redirect_uri={redirect_url}&"
            f"scope=openid&"
            f"response_type=code&"
            f"&state={state}"
        )
        return auth_url

    def handle_authorization_response(self , uri):
        """Handles the authorization response and extracts tokens."""
        return TokenResponseHandler( self.config ).handle_authorization_response( uri )
class PKCEFlow( AuthorizationFlow ):
    """Handles PKCE Grant flow."""

    def build_auth_url(self):
        """Builds the URL for the PKCE flow."""
        code_verifier , code_challenge = generate_pkce_pair()
        session['code_verifier'] = code_verifier
        state = self.generate_state()
        base_url = self.config.base_url
        redirect_url = self.config.redirect_url
        client_id = self.config.credentials.client_id

        auth_url = (
            f"{base_url}/moas/idp/openidsso?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_url}&"
            f"scope=openid&"
            f"response_type=code&"
            f"state={state}&"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=S256"
        )
        return auth_url

    def handle_authorization_response(self , uri):
        """Handles the authorization response and extracts tokens with code_verifier."""
        code_verifier = session.get( 'code_verifier' )
        return TokenResponseHandler( self.config ).handle_authorization_response( uri , code_verifier )
class ImplicitFlow( AuthorizationFlow ):
    """Handles Implicit Grant flow."""

    def build_auth_url(self):
        """Builds the URL for the implicit flow."""
        state = self.generate_state()
        base_url = self.config.base_url
        redirect_url = self.config.redirect_url
        client_id = self.config.credentials.client_id

        auth_url = (
            f"{base_url}/moas/idp/openidsso?"
            f"response_type=token&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_url}&"
            f"scope=openid&"
            f"state={state}"
        )
        return auth_url

    def handle_authorization_response(self , uri):
        """Implicit flow usually handles response client-side."""
        raise NotImplementedError( "Implicit flow response handling is typically done client-side" )

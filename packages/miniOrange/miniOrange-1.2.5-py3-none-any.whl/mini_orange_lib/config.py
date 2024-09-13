class _ClientCredentials:
    """Private class to manage client credentials."""

    def __init__(self, client_id: str, client_secret: str):
        self.__client_id = client_id
        self.__client_secret = client_secret

    @property
    def client_id(self) -> str:
        """Returns the client ID."""
        return self.__client_id

    @property
    def client_secret(self) -> str:
        """Returns the client secret."""
        return self.__client_secret

class Config:
    """Configuration class for OAuth flows and JWT management."""

    def __init__(self, client_id: str, client_secret: str, base_url: str, redirect_url: str, public_key: str, grant_type: str = None):
        self.__credentials = _ClientCredentials(client_id, client_secret)
        self.__base_url = base_url
        self.__redirect_url = redirect_url
        self.__public_key = public_key
        self.__grant_type = grant_type

    @property
    def credentials(self) -> _ClientCredentials:
        """Returns the client credentials."""
        return self.__credentials

    @property
    def base_url(self) -> str:
        """Returns the base URL."""
        return self.__base_url

    @property
    def redirect_url(self) -> str:
        """Returns the redirect URL."""
        return self.__redirect_url

    @property
    def public_key(self) -> str:
        """Returns the public key."""
        return self.__public_key

    @property
    def grant_type(self) -> str:
        """Returns the grant type."""
        return self.__grant_type

    def get(self, key: str) -> str:
        """Returns the value for the specified key."""
        key_map = {
            'client_id': self.__credentials.client_id,
            'client_secret': self.__credentials.client_secret,
            'base_url': self.__base_url,
            'redirect_url': self.__redirect_url,
            'public_key': self.__public_key,
            'grant_type': self.__grant_type
        }
        if key in key_map:
            return key_map[key]
        else:
            raise KeyError(f"Invalid configuration key: '{key}'")

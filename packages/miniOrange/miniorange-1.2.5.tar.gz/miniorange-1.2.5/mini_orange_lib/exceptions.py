class AuthorizationError( Exception ):
    """Exception raised for errors in authorization."""

    def __init__(self , message: str = "An error occurred during authorization"):
        super().__init__( message )


class TokenRequestError( Exception ):
    """Exception raised for errors in token requests."""

    def __init__(self , message: str = "An error occurred during token request"):
        super().__init__( message )


class InvalidConfigurationError( Exception ):
    """Exception raised for invalid configuration."""

    def __init__(self , parameter_name: str , message: str):
        """
        Initializes the exception with the parameter name and error message.

        Args:
            parameter_name (str): The name of the parameter that caused the error.
            message (str): The error message.
        """
        super().__init__( message )
        self.parameter_name = parameter_name

    def __str__(self):
        return f"{self.parameter_name}: {super().__str__()}"


class JwtExpiredSignatureError( Exception ):
    """Exception raised when the JWT token has expired."""

    def __init__(self , message: str = "JWT token has expired"):
        super().__init__( message )


class JwtInvalidTokenError( Exception ):
    """Exception raised for invalid JWT tokens."""

    def __init__(self , message: str = "Invalid JWT token"):
        super().__init__( message )

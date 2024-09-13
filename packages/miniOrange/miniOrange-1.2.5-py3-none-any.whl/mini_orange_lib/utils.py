import base64
import hashlib
import logging
import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def generate_pkce_pair() -> tuple[str, str]:
    """
    Generates a code verifier and code challenge pair for PKCE.

    :return: Tuple of (code_verifier, code_challenge)
    """
    try:
        # Generate a random code verifier
        code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
        logging.debug(f"Generated code verifier: {code_verifier}")

        # Generate the code challenge using SHA256
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).rstrip(b'=').decode('utf-8')
        logging.debug(f"Generated code challenge: {code_challenge}")

        return code_verifier, code_challenge

    except Exception as e:
        logging.error(f"Error generating PKCE pair: {e}")
        raise

def load_public_key(pem_data: str):
    """
    Loads a public key from PEM-encoded data.

    :param pem_data: PEM-encoded public key as a string.
    :return: A public key object.
    :raises ValueError: If the PEM data is invalid or cannot be parsed.
    """
    try:
        # Convert the PEM data to bytes
        pem_bytes = pem_data.encode('utf-8')
        logging.debug(f"Loading public key from PEM data")

        # Load the public key from PEM data
        public_key = load_pem_public_key(pem_bytes, backend=default_backend())
        logging.debug("Public key successfully loaded")

        return public_key

    except ValueError as e:
        logging.error(f"Error loading public key: {e}")
        raise ValueError(f"Failed to load public key: {e}")
    except Exception as e:
        logging.error(f"Unexpected error loading public key: {e}")
        raise

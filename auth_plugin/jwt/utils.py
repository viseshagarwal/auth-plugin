from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from typing import Tuple
from .exceptions import JWTError


def generate_rsa_keys(key_size: int = 2048) -> Tuple[bytes, bytes]:
    """Generate RSA public/private key pair

    Args:
        key_size: Size of the RSA key in bits

    Returns:
        Tuple containing private and public keys in PEM format
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )

        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem_private, pem_public
    except Exception as e:
        raise JWTError(f"RSA key generation failed: {str(e)}")

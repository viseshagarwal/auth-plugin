import jwt
import datetime
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class JWTAuth:
    def __init__(
        self,
        secret_key,
        algorithm="HS256",
        private_key=None,
        public_key=None,
        token_expiration=3600,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiration = token_expiration

        if algorithm.startswith("RS"):
            self.private_key = private_key
            self.public_key = public_key
        else:
            self.private_key = None
            self.public_key = None

    def generate_token(self, payload):
        try:
            payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=self.token_expiration
            )

            if self.algorithm.startswith("HS"):
                token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            elif self.algorithm.startswith("RS"):
                token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
            else:
                raise ValueError(f"Unsupported algorithm: {self.algorithm}")

            return token
        except Exception as e:
            raise RuntimeError(f"Error generating token: {str(e)}")

    def decode_token(self, token):
        try:
            if self.algorithm.startswith("HS"):
                decoded = jwt.decode(
                    token, self.secret_key, algorithms=[self.algorithm]
                )
            elif self.algorithm.startswith("RS"):
                decoded = jwt.decode(
                    token, self.public_key, algorithms=[self.algorithm]
                )
            else:
                raise ValueError(f"Unsupported algorithm: {self.algorithm}")

            return decoded
        except ExpiredSignatureError:
            raise RuntimeError("Token has expired")
        except InvalidTokenError:
            raise RuntimeError("Invalid token")
        except DecodeError:
            raise RuntimeError("Error decoding token")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

    @staticmethod
    def generate_rsa_keys():
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048, backend=default_backend()
            )
            public_key = private_key.public_key()

            pem_private_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )

            pem_public_key = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            return pem_private_key, pem_public_key
        except Exception as e:
            raise RuntimeError(f"Error generating RSA keys: {str(e)}")

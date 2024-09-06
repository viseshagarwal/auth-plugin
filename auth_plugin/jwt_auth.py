import jwt
import datetime
from .base_auth import BaseAuth


class JWTAuth(BaseAuth):
    def __init__(self, secret_key, algorithm="HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_token(self, user_id, expires_in=3600):
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

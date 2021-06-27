import datetime
import typing as tp

import jwt


class JWT:
    JWT_SECRET = "secret"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_IN = 3  # minutes

    def generate_token(self, payload: dict) -> str:
        payload.update(
            {"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.JWT_EXPIRE_IN)}
        )
        jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
        return jwt_token

    def get_payload(self, token: str) -> tp.Optional[dict]:
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError as e:
            return None


security_token = JWT()

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def hash_string(self, string: str):
        return self.pwd_context.hash(string)

    def verity(self, plain: str, hashed: str):
        return self.pwd_context.verify(plain, hashed)


security_crypto = Crypto()

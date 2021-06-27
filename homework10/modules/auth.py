import modules.db_utils as db_utils
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from modules.db import User
from modules.error import unable_validate_token_exception
from modules.security import security_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authorization")


async def get_auth_user(token: str = Depends(oauth2_scheme), request: Request = None) -> User:
    user_data = security_token.get_payload(token)
    if user_data is None or "id" not in user_data:
        raise unable_validate_token_exception

    user_id = user_data["id"]
    user = db_utils.get_user(user_id)
    if user is None:
        raise unable_validate_token_exception

    return user

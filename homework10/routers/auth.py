import modules.db_utils as db_utils
from fastapi import APIRouter
from modules.error import already_exists_exception, wrong_auth_data_exception
from modules.security import security_crypto, security_token
from pydantic import BaseModel

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class Credentials(BaseModel):
    login: str
    password: str


@router.post("/authorization", response_model=Token)
async def login_for_token(form_data: Credentials):
    user = db_utils.find_user(form_data.login)
    if not user:
        raise wrong_auth_data_exception

    hashed_password = user.password
    if not security_crypto.verity(form_data.password, hashed_password):
        raise wrong_auth_data_exception

    token = security_token.generate_token({"id": user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registration", response_model=Token)
async def register_and_login(form_data: Credentials):
    user = db_utils.create_user(form_data.login, security_crypto.hash_string(form_data.password))
    if not user:
        raise already_exists_exception

    token = security_token.generate_token({"id": user.id})
    return {"access_token": token, "token_type": "bearer"}

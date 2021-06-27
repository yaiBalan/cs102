import typing as tp

import modules.db_utils as db_utils
from fastapi import APIRouter, Depends
from modules.auth import User, get_auth_user
from modules.error import invalid_note_exception, invalid_params_exception
from pydantic import BaseModel


class APIResult(BaseModel):
    data: tp.Any = None


class DataString(BaseModel):
    data: str


class DataShare(BaseModel):
    share: bool


router = APIRouter(tags=["notes"])


@router.get("/notes", response_model=APIResult)
async def read_users(user: User = Depends(get_auth_user)) -> APIResult:
    return APIResult(data=db_utils.get_notes(user))


single_router = APIRouter(prefix="/note", tags=["note"])


@single_router.get("/{note_id}", response_model=APIResult)
async def get_note(user: User = Depends(get_auth_user), note_id: int = -1) -> APIResult:
    note = db_utils.get_shared_note(user, note_id)
    if not note:
        raise invalid_note_exception
    return APIResult(data=note.as_dict())


@single_router.post("/")
async def create_note(
    user: User = Depends(get_auth_user), request_body: DataString = None
) -> APIResult:
    assert request_body is not None
    data = request_body.data
    created_note = db_utils.create_note(user, data)
    return APIResult(data=created_note.as_dict() if created_note else False)


@single_router.post("/{note_id}/share")
async def share_note(
    user: User = Depends(get_auth_user), note_id: int = -1, request_body: DataShare = None
) -> APIResult:
    assert request_body is not None
    share = request_body.share
    return APIResult(data=db_utils.share_note(user, note_id, share))


@single_router.put("/{note_id}")
async def update_note(
    user: User = Depends(get_auth_user),
    note_id: int = -1,
    request_body: DataString = None,
) -> APIResult:
    assert request_body is not None
    data = request_body.data
    return APIResult(data=db_utils.update_note(user, note_id, data))


@single_router.delete("/{note_id}")
async def delete_note(user: User = Depends(get_auth_user), note_id: int = -1) -> APIResult:
    if note_id is None:
        raise invalid_params_exception
    if db_utils.delete_note(user, note_id):
        return APIResult(data=True)
    else:
        raise invalid_note_exception


router.include_router(single_router)

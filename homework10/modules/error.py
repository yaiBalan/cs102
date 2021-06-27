from fastapi import HTTPException, status

unable_validate_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

wrong_auth_data_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

already_exists_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="This user is already registered",
    headers={"WWW-Authenticate": "Bearer"},
)

# Notes

invalid_params_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request",
)

invalid_note_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Note doesn't exist or you don't have permission to check it",
)

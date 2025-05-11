from fastapi import Request, HTTPException, status, Depends
from jose import JWTError, jwt

from app.core.config import config
from app.domains.auth.exceptions import *
from app.domains.user.exceptions import UserNotExists


def authorize_user(request: Request) -> str:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer"):
        raise TokenNotFound()

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
        print(payload)
        user_id = payload.get("sub")
        if user_id is None:
            raise UserNotExists()
        return user_id
    except JWTError:
        raise TokenNotFound()
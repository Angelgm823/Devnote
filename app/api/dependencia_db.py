from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.models.users import User
from app.core.security import decode_token

from app.core.db import get_session
from app.repositories.user_repository import UserRepository

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


# dependencia para base de datos
def get_db() -> Session:
    return next(get_session())


DBSESSION = Annotated[Session, Depends(get_db)]



def get_current_user(token: Annotated[str, Depends(oauth2)], db: DBSESSION) -> User:
    credencials_exc = HTTPException(status_code=401, detail="Etiqueta no encontrada",
                                    headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise credencials_exc

    repository = UserRepository(db)
    user = repository.get_user_by_id(user_id)

    if not user:
        raise credencials_exc
    return user

CURRENT_USER = Annotated[User, Depends(get_current_user)]
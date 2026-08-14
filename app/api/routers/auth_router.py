from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.api.dependencia_db import DBSESSION
from app.models.users import UserRead, UserCreate
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def refister(payload: UserCreate, db: DBSESSION):
    service = AuthService(UserRepository(db))
    return service.register(payload)


@router.post("/login")
def login(email: str, password: str, db: DBSESSION):
    service = AuthService(UserRepository(db))
    token = service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
def token(db: DBSESSION, form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    password = form.password
    service = AuthService(UserRepository(db))
    token = service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}

from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
from app.models.users import User, UserCreate
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, payload: UserCreate) -> User:
        if self.repository.get_by_email(payload.email):
            raise HTTPException(status_code=400, detail="El correo ya existe")

        user = User(email=payload.email, tag_name=payload.tag_name,
                    hashed_password=hash_password(payload.password[:72]))

        return self.repository.create(user)

    def login(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        token = create_access_token({"sub": str(user.id)})
        return token

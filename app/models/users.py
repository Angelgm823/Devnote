from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):  # clase heredando sqlmodel
    id: int = Field(default=None, primary_key=True)  # llave primaria
    email: str = Field(index=None, unique=True)
    tag_name: str = Field(default="")
    hashed_password: str
    active: bool = Field(default=True)


class UserCreate(SQLModel):
    email: str
    tag_name: str
    password: str


class UserRead(SQLModel):
    email: str
    tag_name: str
    hashed_password: str

    model_config = {"from_attributes": True}  # como modelo de un sql

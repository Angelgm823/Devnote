from typing import Iterator

from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True,
                       connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})

def init_db() -> None:
    pass
    if settings.ENVIRONTMENT == "DEV":
        SQLModel.metadata.create_all(engine)
    # SQLModel.metadata.create_all(engine) # dev desarrollo

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
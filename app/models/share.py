from enum import Enum

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class ShareRol(str, Enum):
    READ = "read"
    WRITE = "write"


class NoteShare(SQLModel):
    __tablename__ = "note_share"
    __table_args__ = (UniqueConstraint("note_id", "user_id", name="uq_note_user"))

    id: int = Field(default=None, primary_key=True)
    note_id: int = Field(foreign_key="note.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: ShareRol = Field(default=ShareRol.READ)


class LabelShare(SQLModel, table=True):
    __tablename__ = "label_share"
    __table_args__ = (UniqueConstraint("label_id", "user_id", name="uq_label_user"))

    id: int = Field(default=None, primary_key=True)
    label_id: int = Field(foreign_key="label.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: ShareRol = Field(default=ShareRol.READ)

class ShareRequest(SQLModel):
    target_user_id: int = Field(gt=0)
    role: ShareRol = ShareRol.READ
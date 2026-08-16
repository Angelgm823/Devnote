from fastapi import APIRouter, status

from app.models.label import LabelRead, LabelCreate
from app.services.label_service import LabelService
from app.api.dependencia_db import DBSESSION, CURRENT_USER

router = APIRouter(prefix="/label", tags=["Label"])


@router.get("/", response_model=list[LabelRead])
def get_label(db: DBSESSION, user: CURRENT_USER):
    return LabelService(db).list(user.id)


@router.post("/", response_model=LabelRead, status_code=status.HTTP_201_CREATED)
def create_label(payload: LabelCreate, db: DBSESSION, user: CURRENT_USER):
    return LabelService(db).create(user.id, payload)


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(label_id: int, db: DBSESSION, user: CURRENT_USER):
    LabelService(db).delete(user.id, label_id)

    return None

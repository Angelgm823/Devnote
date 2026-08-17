from fastapi import HTTPException
from sqlmodel import Session

from app.models.label import Label, LabelCreate

from app.repositories.label_repository import LabelRepository
from app.repositories.share_repository import ShareRepository


class LabelService:
    def __init__(self, db: Session):
        self.repository = LabelRepository(db)
        self.shares = ShareRepository(db)

    def list(self, owner_id: int) -> list[Label]:
        owned = self.repository.list_by_user(owner_id)

        shared_ids = self.shares.list_label_ids_shared_with_user(owner_id)
        shared = self.repository.list_by_ids(shared_ids)

        labels = {label.id: label for label in owned}
        for label in shared:
            labels.setdefault(label.id, label)

        return sorted(labels.values(), key=lambda label: label.name)

    def create(self, owner_id: int, payload: LabelCreate) -> Label:
        if self.repository.get_by_name(owner_id, payload.name):
            raise HTTPException(status_code=400, detail="La etiqueta ya existe")

        return self.repository.create(owner_id, payload.name)

    def delete(self, owner_id: int, label_id: int) -> None:
        label = self.repository.get(label_id)

        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="La etiqueta no existe o no está autorizado")

        self.repository.delete(label)

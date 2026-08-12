from fastapi import HTTPException
from sqlmodel import Session

from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository
from app.models.share import ShareRol


class ShareService:
    def __init__(self, db: Session):
        self.shares = ShareRepository(db)
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)

    # compartir la nota
    def share_note(self, owner_id: int, note_id: int, target_user_id: int, role: ShareRol):
        note = self.notes.get(note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="Nota no encontrada o autorización invalida")

        share = self.shares.upsert_note_share(note_id, target_user_id, role.value if hasattr(role, "value") else role)
        return share

    # descompatir la nota
    def unsahre_note(self, owner_id: int, note_id: int, target_user_id: int):
        note = self.notes.get(note_id)
        if not note or note.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="Nota no encontrada o autorización invalida")

        self.shares.remove_note_share(note_id, target_user_id)

    # compartir etiqueta
    def sahre_label(self, owner_id: int, label_id: int, target_user_id: int, role: ShareRol):
        label = self.labels.get(label_id)

        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="Etiqueta no encontrada")

        label = self.shares.upsert_label_share(label_id, target_user_id, role.value if hasattr(role, "value") else role)
        return label

    # descompartir etiqueta
    def unshare_label(self, owner_id: int, label_id: int, target_user_id: int):
        label = self.labels.get(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="Etiqueta no encontrada o sin autorizacion")

        self.shares.remove_label_share(label_id, target_user_id)

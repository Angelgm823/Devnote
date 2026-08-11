from fastapi import HTTPException
from sqlmodel import Session

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRol
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)
        self.shares = ShareRepository(db)

    # permisos

    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shares.has_note_share(note_id=note.id, user_id=user_id):
            return True

        label_ids = self.labels.list_label_ids_for_note(note.id)
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id)

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shares.has_note_share(note_id=note.id, user_id=user_id, role=ShareRol.WRITE):
            return True

        label_ids = self.labels.list_label_ids_for_note(note.id)
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id, role=ShareRol.WRITE)

    def list_visible(self, user_id: int) -> list[Note]:
        # notas propias
        owned = self.notes.list_owned(user_id)

        # notas compartidas
        direct_ids = self.shares.list_note_ids_shared_direcly(user_id)

        # notas compartidas por label
        shared_label_ids = self.shares.list_label_ids_shared_with_user(user_id)
        ids_by_label = self.labels.list_note_ids_by_label_ids(shared_label_ids)

        ids = list({*direct_ids, *ids_by_label})
        shared = self.notes.list_by_ids(ids=ids)

        ids_combinate = {note.id: note for note in owned}

        for note in shared:
            ids_combinate.setdefault(note.id, note)

        return sorted(ids_combinate.values(), key=lambda note: note.id, reversed=True)

    def create(self, owner_id: int, payload: NoteCreate) -> Note:
        note = self.notes.create(Note(owner_id=owner_id, **payload.model_dump(exclude={"labels_ids"})))

        if payload.labels_ids:
            self._set_labels(owner_id, note.id, payload.labels_ids)

        return note

    def update(self, user_id: int, note_id: int, payload: NoteUpdate) -> Note:
        note = self.notes.get(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada")

        if not self.user_can_edit(user_id, note):
            raise HTTPException(status_code=404, detail="Usuario no tiene permisos para editar")

        updates = payload.model_dump(exclude_none=True)
        label_ids = updates.pop("label_ids", None)

        for key, values in updates.items():
            setattr(note, key, values)

        note = self.notes.update(note)
        if label_ids is not None:
            if note.owner_id != user_id:
                raise HTTPException(status_code=404, detail="No existe o está autorizado")
            self._set_labels(user_id, note.id, label_ids)
        return note

    def delete(self, user_id: int, note_id: int) -> None:
        note = self.notes.get(note_id)
        if not note or note.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Nota no encontrada")

        self.notes.delete(note)

    # helper
    def _set_labels(self, owner_id: int, note_id: int, labels_ids: list[int]) -> None:
        valid_ids = self.labels.list_ids_for_owner_subset(owner_id, labels_ids or [])

        self.notes.replace_label(owner_id, note_id, valid_ids)

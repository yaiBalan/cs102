import typing as tp

from modules.db import Note, User
from peewee import DatabaseError, IntegrityError


def get_user(user_id: tp.Any) -> tp.Optional[User]:
    user = User.get_or_none(User.id == user_id)
    return user


def find_user(login: str) -> tp.Optional[User]:
    user = User.get_or_none(User.login == login)
    return user


def create_user(login: str, hashed_password: str) -> tp.Optional[User]:
    try:
        user = User(login=login, password=hashed_password)
        user.save()
        return user
    except IntegrityError:
        return None
    except DatabaseError as e:
        print("Unknown database error:", e)
        return None


# ---


def create_note(user: User, data: str) -> tp.Optional[Note]:
    try:
        note = Note(user=user, data=data)
        note.save()
        return note
    except IntegrityError:
        return None
    except DatabaseError as e:
        print("Unknown database error:", e)
        return None


# --


def get_notes(user: User) -> tp.List[Note]:
    return [note.as_dict() for note in user.notes]


def get_note(user: User, note_id: int) -> tp.Optional[Note]:
    """
    Returns selected Note of specified User or None
    """
    note_select = user.notes.where(Note.id == note_id)
    if len(note_select) == 0:
        return None
    return note_select[0]


def get_shared_note(user: User, note_id: int) -> tp.Optional[Note]:
    """
    Returns selected Note if it is shared or owned by the user
    """
    note = Note.get_or_none(Note.id == note_id)
    if note is None or not (note.user == user or note.shared):
        return None
    return note


# ---


def share_note(user: User, note_id: int, shared: bool) -> bool:
    """
    Sets "shared" status of selected note if possible and returns True. Otherwise returns False
    """
    note = get_note(user, note_id)
    if not note:
        return False

    note.shared = shared
    note.save()
    return True


def update_note(user: User, note_id: int, data: str) -> bool:
    """
    Updates note and returns True. Returns False in case note wasn't found
    """
    note = get_shared_note(user, note_id)
    if not note:
        return False
    raw_update_note(note, data)
    return True


def raw_update_note(note: Note, data: str):
    note.data = data
    note.save()


# ---


def delete_note(user: User, note_id: int) -> bool:
    note = get_note(user, note_id)
    if not note:
        return False
    return raw_delete_note(note)


def raw_delete_note(note: Note) -> bool:
    """
    Deletes specified note and returns True if the number of rows deleted is greater than zero
    """
    return note.delete_instance() > 0

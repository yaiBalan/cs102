from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    TextField,
)

db = SqliteDatabase("db.db")


# ---


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    login = CharField(unique=True)
    password = CharField()


class Note(BaseModel):
    user = ForeignKeyField(User, backref="notes")
    data = TextField()
    shared = BooleanField(default=False)

    def as_dict(self):
        return {"id": self.id, "data": self.data, "shared": self.shared}


# ---

db.connect()
db.create_tables([User, Note])
db.close()

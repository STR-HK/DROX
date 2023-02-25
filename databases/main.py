from datetime import datetime
from editDB import addColumn
from querybuilder import TextDatabase
import os

db = TextDatabase()
db.connect("path.sqlite")

db.create_table_if_not_exists(
    table_name="match",
    fields={
        "id": "TEXT",
        "path": "TEXT",
    },
)
db.create_table_if_not_exists(
    table_name="playlist",
    fields={
        "id": "INTEGER",
        "title": "TEXT",
        "description": "TEXT",
        "thumbnail": "TEXT",
    },
)


def registe_file(id, path):
    db.insert(
        table_name="match", values={"id": id, "path": path, "time": datetime.utcnow()}
    )
    db.save()


# def add_playlist(id, )


def create_id():
    return int(datetime.timestamp(datetime.now()))


def after_cw_playlist_terminate():
    db.save()


class cw_playlist:
    def __init__(self, id=None) -> None:
        if id == None:
            self.id = create_id()
            self.create_data()
        else:
            self.id = id

    def init_data(self):
        db.select(
            table_name="playlist",
            field_names="*",
            condition=f"WHERE id = '{self.id}'",
        )

    def create_data(self):
        db.insert(
            table_name="playlist",
            values={
                "id": self.id,
                "title": "",
                "description": "",
                "thumbnail": "",
            },
        )
        after_cw_playlist_terminate()


py = cw_playlist()
print(py.id)

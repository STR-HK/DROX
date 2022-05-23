from datetime import datetime
from querybuilder import TextDatabase
import os

# db = TextDatabase()
# db.connect("data.sqlite")

# db.create_table_if_not_exists(
#     table_name="playlist",
#     fields={"title": "TEXT", "count": "INTEGER", "id": "TEXT", "time": "DATETIME"},
# )

# db.insert(
#     table_name="playlist",
#     values={"title": "test", "count": 200, "id": "JhlBA6", "time": datetime.utcnow()},
# )

# db.save()


dlmana = TextDatabase()
dlmana.connect("path.sqlite")

dlmana.create_table_if_not_exists(
    table_name="match",
    fields={"id": "TEXT", "path": "TEXT", "time": "DATETIME"},
)


def init_dl_folder():
    if not os.path.isdir("./downloads"):
        os.mkdir("./downloads")


init_dl_folder()


def get_new_dl_path() -> str:
    dl_path = "./downloads/{}/".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(dl_path)
    return dl_path


def registe_file(id, path):
    dlmana.insert(
        table_name="match", values={"id": id, "path": path, "time": datetime.utcnow()}
    )
    dlmana.save()


def get_path_by_id(id: str) -> str or None:
    paths = dlmana.select(
        table_name="match",
        field_names="path",
        condition="id = '{}'".format(id),
    )
    if paths:
        return paths[0][0]
    else:
        return None


def id_exists(id: str) -> bool:
    if dlmana.select(
        table_name="match",
        field_names="path",
        condition="id = '{}'".format(id),
    ):
        return True
    else:
        return False


def fix_title(title: str) -> str:
    ascii = {
        "<": "＜",
        ">": "＞",
        ":": "：",
        '"': "＂",
        "/": "／",
        "\\": "＼",
        "|": "｜",
        "?": "？",
        "*": "＊",
    }
    for key, value in ascii.items():
        title = title.replace(key, value)

    return title


# registe_file("JhlBA6", get_new_dl_path() + "test.mp4")
get_path_by_id("JhlBA6")

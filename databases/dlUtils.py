import os


def dl_init():
    if not os.path.isdir("./downloads"):
        os.mkdir("./downloads")


def get_dl_new_path() -> str:
    dl_path = "./downloads/{}/".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(dl_path)
    return dl_path


def get_dl_path_by_id(id: str) -> str or None:
    paths = db.select(
        table_name="match",
        field_names="path",
        condition="id = '{}'".format(id),
    )
    if paths:
        return paths[0][0]
    else:
        return None


def get_dl_id_exists(id: str) -> bool:
    if db.select(
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

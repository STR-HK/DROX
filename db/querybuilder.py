import sqlite3


class TextDatabase:
    def __init__(self) -> None:
        pass

    def connect(self, location: str) -> None:
        self.connect = sqlite3.connect(location, check_same_thread=False)

        self.connect.row_factory = sqlite3.Row

        self.cursor = self.connect.cursor()

        self.say = True

    def save(self) -> None:
        self.connect.commit()

    def execute(self, query: str, params: list = None) -> list or None:
        try:
            response = (
                self.cursor.execute(query)
                if params is None
                else self.cursor.execute(query, params)
            )
        except Exception as e:
            print(query, ":", e)
            return

        fetchall = response.fetchall()

        if self.say:
            print(f"Execute : {query} & {params} -> {fetchall}")
        return fetchall

    def select(
        self,
        table_name: str,
        field_names: list or str,
        condition: str = None,
        order: str = None,
    ) -> list:
        select_query = (
            "SELECT {field_names} FROM {table_name} {where} {order_by}".format(
                field_names=", ".join(field_names)
                if isinstance(field_names, list)
                else field_names,
                table_name=table_name,
                where="{condition}".format(
                    condition=f"WHERE {condition}" if condition else ""
                ),
                order_by="".format(order=f"ORDER BY {order}" if order else ""),
            )
        )

        return self.execute(select_query)

    def create_table_if_not_exists(self, table_name: str, fields: dict) -> None:
        create_table_if_not_exists_query = (
            "CREATE TABLE IF NOT EXISTS {table_name}({fields})".format(
                table_name=table_name,
                fields=", ".join(
                    "{} {}".format(field_name, field_type)
                    for field_name, field_type in fields.items()
                ),
            )
        )

        self.execute(create_table_if_not_exists_query)

    def update(self, table_name: str, values: dict, condition: dict = None) -> list:
        update_query = "UPDATE {table_name} SET {values} {where}".format(
            table_name=table_name,
            values=", ".join([" = ".join([field_name, "?"]) for field_name in values]),
            where="{condition}".format(
                condition=f"WHERE {condition}" if condition else ""
            ),
        )
        update_params = list(values.values())

        self.execute(update_query, update_params)

    def insert(self, table_name: str, values: dict) -> list:
        insert_query = (
            "INSERT INTO {table_name}({field_names}) VALUES({values})".format(
                table_name=table_name,
                field_names=", ".join(values.keys()),
                values=", ".join(["?" for _ in range(len(values))]),
            )
        )
        insert_params = list(values.values())

        self.execute(insert_query, insert_params)

    def delete(self, table_name: str, condition: str) -> list:
        delete_query = "DELETE FROM {table_name} WHERE {condition}".format(
            table_name=table_name, condition=condition
        )

        self.execute(delete_query)

    def drop_table_if_exists(self, table_name: str) -> None:
        drop_table_if_exists_query = "DROP TABLE IF EXISTS {table_name}".format(
            table_name=table_name
        )

        self.execute(drop_table_if_exists_query)


# db = TextDatabase()
# db.connect('./database/auth.db')
# db.create_table_if_not_exists(table_name='bull_table', fields=['a','b','c'])
# db.insert(table_name='auth', values={'token':'gamma'})
# db.update(table_name='bull_table', values={'a':'????????? ?????? ???'}, condition="a = '????????? ???'")
# db.delete(table_name='bull_table', condition="a = '????????? ?????? ???'")
# db.save()

from querybuilder import TextDatabase


def addColumn(db: TextDatabase, table, column, type_of):
    rows = db.select(
        table_name=table,
        field_names="*",
    )

    first_row = dict(rows[0])
    column_data = dict()
    for key, value in first_row.items():
        if type(value) == str:
            column_data[key] = "TEXT"
        elif type(value) == int:
            column_data[key] = "INTEGER"
        elif type(value) == float:
            column_data[key] = "REAL"
        else:
            column_data[key] = "BLOB"

    column_data[column] = type_of

    db.drop_table_if_exists(table_name=table)

    db.create_table_if_not_exists(
        table_name=table,
        fields=column_data,
    )

    for row in rows:
        db.insert(
            table_name=table,
            values=dict(row),
        )

    db.save()

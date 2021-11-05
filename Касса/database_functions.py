from CONSTANTS import *


def DRAW_DATABASE(self, QTableWidgetItem):
    result = CUR.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()
    self.tableWidget.setRowCount(len(result))
    self.tableWidget.setColumnCount(len(result[0]))
    self.titles = [description[0] for description in CUR.description]
    for i, elem in enumerate(result):
        for j, val in enumerate(elem):
            self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
    self.modified = {}


def SELECT(table_columns, table, required_columns, columns, comparison_signs='='):
    if comparison_signs == '=':
        comparison_signs = ['='] * len(required_columns)
    execute = f"""SELECT {', '.join(table_columns)} FROM {table} WHERE """
    execute += ' AND '.join([f"{required_columns[i]} {comparison_signs[i]} ?" for i in range(len(required_columns))])
    return CUR.execute(execute, columns).fetchall()


def UPDATE(table, replaceable_columns, columns1, required_columns, columns2, comparison_signs='='):
    if comparison_signs:
        comparison_signs = ['='] * len(required_columns)
    execute = f"UPDATE {table} SET "
    execute += ' AND '.join([f"{replaceable_columns[i]}={columns1[i]}"
                             for i in range(len(replaceable_columns))]) + ' WHERE '
    execute += ' AND '.join([f"{required_columns[i]} {comparison_signs[i]} ?" for i in range(len(required_columns))])
    CUR.execute(execute, columns2).fetchall()


def INSERT(table, field_names):
    CUR.execute(f'INSERT INTO {table}{tuple(field_names)} VALUES{tuple(field_names)}')
    CON.commit()


def DELETE(table, required_columns, columns, comparison_signs='='):
    if comparison_signs:
        comparison_signs = ['='] * len(required_columns)
    e = f'DELETE from {table} where '
    e += ', '.join([f'{required_columns[i]}{comparison_signs[i]}?' for i in range(len(required_columns))])
    CUR.execute(e, columns).fetchall()
    CON.commit()

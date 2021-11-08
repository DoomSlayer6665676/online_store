from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import QtCore
from database_functions import *
from PyQt5 import uic


class table(QWidget):
    closeWidget = QtCore.pyqtSignal()

    def __init__(self):
        super(table, self).__init__()
        uic.loadUi('./design/table.ui', self)
        self.modified = {}
        self.titles = None
        self.setupUi()

    def setupUi(self):
        DRAW_DATABASE(self, QTableWidgetItem)

    def closeEvent(self, event):
        self.closeWidget.emit()


class terminal(QWidget):
    def __init__(self):
        super(terminal, self).__init__()
        uic.loadUi('./design/terminal.ui', self)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_3.clicked.connect(self.update)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.modified = {}
        self.titles = None
        self.window_open = True
        self.setupUi()

    def add(self):
        INSERT(TABLE_NAME, TABLE_COLUMNS[1:])

    def delete(self):
        DELETE(TABLE_NAME, (TABLE_COLUMNS[0],), (self.spinBox.value(),))

    def update(self):
        self.save_results()
        self.setupUi()

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()
        self.modified['id'] = item.row() + 1
        if self.window_open:
            self.save_results()

    def setupUi(self):
        self.window_open = False
        DRAW_DATABASE(self, QTableWidgetItem)
        self.window_open = True

    def save_results(self):
        if self.modified:
            que = "UPDATE Список_продуктов SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            CUR.execute(que, (self.modified.get('id'),))
            CON.commit()
            self.modified.clear()

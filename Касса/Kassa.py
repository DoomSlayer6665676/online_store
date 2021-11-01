# -*- coding: utf-8 -*-
import sys
import sqlite3

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QTableWidgetItem, QFileDialog, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Kassa.ui', self)
        self.openWidget = False
        self.con = sqlite3.connect("Склад.db")
        self.cur = self.con.cursor()
        self.comm = "/clearочисткатерминала/del_outputочисткафайлаoutput/del_inputочисткафайла/list" \
                    "списоквещейнаскладеIDDQD"
        self.pushButton.clicked.connect(self.cheque)
        self.action_9.triggered.connect(self.exit)
        self.action_4.triggered.connect(self.command)
        self.action_5.triggered.connect(self.input_create)
        self.action_6.triggered.connect(self.output_create)
        self.action_10.triggered.connect(self.tabli)
        self.action_8.triggered.connect(self.terminal)
        self.a = list()
        self.output = 'output.txt'
        self.input = 'input.txt'

    def terminal(self):
        self.termin = terminal()
        self.termin.show()

    def output_create(self):
        self.output = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', 'output.txt',
            'файл (*.txt);;Все файлы (*)')[0]
        f = open(self.output, 'w')
        print(f.write(self.textBrowser.toPlainText() + '\n' + self.textBrowser_2.toPlainText()))
        f.close()

    def tabli(self):
        self.tab = tabl()
        self.openWidget = True
        self.tab.show()
        self.tab.closeWidget.connect(self.funk)

    def funk(self):
        self.openWidget = False

    def clear(self):
        self.textBrowser.setText(' ')
        self.textBrowser_2.setText(' ')

    def del_output(self):
        file = open(self.output, 'w')
        file.close()

    def del_input(self):
        file = open(self.input, 'w')
        file.close()

    def list(self):
        self.tabli()

    def IDDQD(self):
        self.IDD = Doom()
        self.IDD.show()

    def cheque(self):
        self.summ = 0
        self.a = list(map(lambda x: x.split(),
                          self.textEdit.toPlainText().split(', ')))
        for i in range(len(self.a)):
            if self.a[i][0] in self.comm:
                if '/clear' in self.a[i][0]:
                    self.clear()
                if '/del_output' in self.a[i][0]:
                    self.del_output()
                if '/del_input' in self.a[i][0]:
                    self.del_input()
                if '/list' in self.a[i][0]:
                    self.list()
                if 'IDDQD' in self.a[i][0]:
                    self.IDDQD()
                return
            result = self.cur.execute("SELECT Предмет FROM Список_продуктов WHERE Предмет=?",
                                      (self.a[i][0],)).fetchall()
            if not result:
                self.textBrowser.setText('Нет такого предмета')
                return
            result = self.cur.execute("SELECT * FROM Список_продуктов WHERE Предмет=? AND Количество>=?",
                                      (self.a[i][0], self.a[i][1])).fetchall()
            if not result:
                self.textBrowser.setText('Нет такого количества')
                return
        for i in range(len(self.a)):
            result = self.cur.execute("SELECT * FROM Список_продуктов WHERE Предмет=? AND Количество>=?",
                                      (self.a[i][0], self.a[i][1])).fetchall()
            self.summ += result[0][-1] * int(self.a[i][1])
            self.a[i].append(str(result[0][-1]))
            self.cur.execute("UPDATE Список_продуктов SET Количество=? WHERE Предмет=?",
                             (result[0][-2] - int(self.a[i][1]), self.a[i][0])).fetchall()
            self.con.commit()
            if self.openWidget:
                self.tab.setupUi()
        elements = list(map(lambda x: ' '.join(x), self.a))
        self.conclusion(elements)

    def conclusion(self, a):
        b = '\n' + '_' * len(max(a)) + '\n' + '–' * len(max(a)) + '\n'
        self.textBrowser.setText(b.join(a) + '\n' + '_' * len(max(a))
                                 + '\n' + '–' * len(max(a)) + '\n')
        self.textBrowser_2.setText('ИТОГ:' + str(self.summ))
        data = self.textBrowser_2.toPlainText()
        HTML = ""
        for i in data:
            color = "#{:06x}".format(000000)
            HTML += "<font color='{}' size = {} >{}</font>".format(
                color, 8, i)
        self.textBrowser_2.setHtml(HTML)

    def exit(self):
        sys.exit(app.exec_())

    def command(self):
        msg = QMessageBox()
        msg.setWindowTitle("Комманды")
        msg.setText("/clear - очистка терминала\n/del output - очистка файла output\n/del input - очистка файла "
                    "input\n/list - список вещей на складе\n/??? - яйцо")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def input_create(self):
        self.input = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', 'input.txt',
            'файл (*.txt);;Все файлы (*)')[0]
        inp = open(self.input, mode='rt')
        a = list(map(lambda x: ' '.join(x), map(lambda x: x.split(), inp.readlines())))
        inp.close()
        self.textEdit.clear()
        self.textEdit.setText(', '.join(a))


class tabl(QWidget):
    closeWidget = QtCore.pyqtSignal()

    def __init__(self):
        super(tabl, self).__init__()
        uic.loadUi('tabl.ui', self)
        self.con = sqlite3.connect("Склад.db")
        self.modified = {}
        self.titles = None
        self.setupUi()

    def setupUi(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM Список_продуктов").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def closeEvent(self, event):
        self.closeWidget.emit()


class terminal(QWidget):
    def __init__(self):
        super(terminal, self).__init__()
        uic.loadUi('terminal.ui', self)
        self.con = sqlite3.connect("Склад.db")
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_3.clicked.connect(self.update)
        self.modified = {}
        self.titles = None
        self.setupUi()

    def update(self):
        self.save_results()
        self.setupUi()

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()
        self.modified['id'] = item.row() + 1
        if self.tru:
            self.save_results()

    def setupUi(self):
        self.tru = False
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM Список_продуктов").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
        self.tru = True

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE Список_продуктов SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.modified.get('id'),))
            self.con.commit()
            self.modified.clear()


class Doom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 1024, 576)
        self.setWindowTitle('666')
        self.pixmap = QPixmap('High_resolution_wallpaper_background_ID_77700322238-1024x576.jpg')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(1024, 576)
        self.image.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

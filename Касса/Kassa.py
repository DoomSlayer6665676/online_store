# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from DOOM import Doom
from PyQt5 import QtCore, QtMultimedia
from database import *


class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('./design/box_office.ui', self)
        self.openWidget = False
        self.pushButton.clicked.connect(self.cheque)
        self.action_9.triggered.connect(self.exit)
        self.action_4.triggered.connect(self.command)
        self.action_5.triggered.connect(self.input_create)
        self.action_6.triggered.connect(self.output_create)
        self.action_10.triggered.connect(self.show_table)
        self.action_8.triggered.connect(self.terminal)
        self.columns = list()
        self.output = './txt_and_jpg/output.txt'
        self.input = './txt_and_jpg/input.txt'
        self.ter = terminal()
        self.tab = table()
        self.IDD = Doom()
        self.sum = 0
        self.command = []
        self.player = QtMultimedia.QMediaPlayer()
        media = QtCore.QUrl.fromLocalFile(LOCATION_OF_MP3_box_office)
        content = QtMultimedia.QMediaContent(media)
        self.player.setMedia(content)

    def terminal(self):
        self.ter.show()

    def output_create(self):
        self.output = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', 'output.txt',
            'файл (*.txt);;Все файлы (*)')[0]
        try:
            f = open(self.output, 'w')
            print(f.write(self.textBrowser.toPlainText() + '\n' + self.textBrowser_2.toPlainText()))
            f.close()
        except FileNotFoundError:
            print('файл не найден')

    def show_table(self):
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
        self.IDD.show()
        self.IDD.player.play()

    def database(self):
        CUR.execute(' '.join(self.command))
        print(self.command)
        CON.commit()

    def cheque(self):
        self.columns = list(map(lambda x: x.split(),
                                self.textEdit.toPlainText().split(', ')))
        for i in range(len(self.columns)):
            if self.columns[i][0] in (COMMANDS + 'IDDQD'):
                if '/clear' in self.columns[i][0]:
                    self.clear()
                if '/del_output' in self.columns[i][0]:
                    self.del_output()
                if '/del_input' in self.columns[i][0]:
                    self.del_input()
                if '/list' in self.columns[i][0]:
                    self.list()
                if 'IDDQD' in self.columns[i][0]:
                    self.IDDQD()
                if '/database' in self.columns[i][0]:
                    self.command = self.columns[i][1:]
                    self.database()
                return
            result = SELECT((TABLE_COLUMNS[1],), TABLE_NAME,
                            (TABLE_COLUMNS[1],), (self.columns[i][0],))
            if not result:
                self.textBrowser.setText(MISSING_ELEMENT)
                return
            try:
                result = SELECT("*", TABLE_NAME, TABLE_COLUMNS[1:3],
                                (self.columns[i][0], int(self.columns[i][1])), comparison_signs=('=', '>='))
            except IndexError:
                self.columns[i].append('1')
            if not result:
                self.textBrowser.setText(LACK_OF_QUANTITY)
                return
            print(self.columns)
        for i in range(len(self.columns)):
            result = SELECT("*", TABLE_NAME, TABLE_COLUMNS[1:3],
                            (self.columns[i][0], int(self.columns[i][1])), comparison_signs=('=', '>='))
            self.sum += result[0][-1] * int(self.columns[i][1])
            self.columns[i].append(str(result[0][-1]))
            UPDATE(TABLE_NAME, [TABLE_COLUMNS[2]], [result[0][-2] - int(self.columns[i][1])],
                   [TABLE_COLUMNS[1]], [self.columns[i][0]])
            CON.commit()
            self.tab.setupUi()
        elements = list(map(lambda x: ' '.join(x), self.columns))
        self.conclusion(elements)
        self.player.play()

    def conclusion(self, a):
        b = '\n' + '_' * len(max(a)) + '\n' + '–' * len(max(a)) + '\n'
        self.textBrowser.setText(b.join(a) + '\n' + '_' * len(max(a))
                                 + '\n' + '–' * len(max(a)) + '\n')
        self.textBrowser_2.setText('ИТОГ:' + str(self.sum))
        data = self.textBrowser_2.toPlainText()
        HTML = ""
        for i in data:
            color = "#{:06x}".format(000000)
            HTML += "<font color='{}' size = {} >{}</font>".format(
                color, 8, i)
        self.textBrowser_2.setHtml(HTML)
        self.sum = 0

    @staticmethod
    def exit():
        sys.exit(app.exec_())

    @staticmethod
    def command():
        msg = QMessageBox()
        msg.setWindowTitle("Комманды")
        msg.setText(COMMANDS)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def input_create(self):
        self.input = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', 'input.txt',
            'файл (*.txt);;Все файлы (*)')[0]
        try:
            inp = open(self.input, mode='rt')
            a = list(map(lambda x: ' '.join(x), map(lambda x: x.split(), inp.readlines())))
            inp.close()
            self.textEdit.clear()
            self.textEdit.setText(', '.join(a))
        except FileNotFoundError:
            print('файл не найден')
        except UnboundLocalError:
            print('файл не найден')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

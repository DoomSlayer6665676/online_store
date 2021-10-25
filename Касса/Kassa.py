# -*- coding: utf-8 -*-
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class SpisokKommand(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('list.ui', self)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Kassa.ui', self)
        self.pushButton.clicked.connect(self.cheque)
        self.action_9.triggered.connect(self.exit)
        self.action_4.triggered.connect(self.command)
        self.action_5.triggered.connect(self.input)

    def cheque(self):
        a = self.textEdit.toPlainText().split(', ')
        a = list(map(lambda x: x.split(), a))
        a = list(map(lambda x: ' '.join(x), a))
        b = '\n' + '_'*len(max(a)) + '\n' + '–'*len(max(a)) + '\n'
        self.textBrowser.setText(b.join(a))

    def conclusion(self, a):
        b = '\n' + '_' * len(max(a)) + '\n' + '–' * len(max(a)) + '\n'
        self.textBrowser.setText(b.join(a))

    def exit(self):
        sys.exit(app.exec_())

    def command(self):
        msg = QMessageBox()
        msg.setWindowTitle("Комманды")
        msg.setText("/clear - очистка терминала\n/del output - очистка файла output\n/del input - очистка файла "
                    "input\n/list - список вещей на складе\n/??? - яйцо")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def input(self):
        inp = open('input.txt', mode='rt')
        a = list(map(lambda x: ' '.join(x), map(lambda x: x.split(), inp.readlines())))
        b = '\n' + '_' * len(max(a)) + '\n' + '–' * len(max(a)) + '\n'
        self.textBrowser.setText(b.join(a))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

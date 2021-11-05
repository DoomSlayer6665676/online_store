from CONSTANTS import IMAGE_NAME, LOCATION_OF_MP3_DOOM
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtMultimedia


class Doom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(IMAGE_NAME)
        self.image = QLabel(self)
        self.player = QtMultimedia.QMediaPlayer()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 1024, 576)
        self.setWindowTitle('666')
        self.image.move(0, 0)
        self.image.resize(1024, 576)
        self.image.setPixmap(self.pixmap)

        media = QtCore.QUrl.fromLocalFile(LOCATION_OF_MP3_DOOM)
        content = QtMultimedia.QMediaContent(media)
        self.player.setMedia(content)

    def closeEvent(self, event):
        self.player.stop()

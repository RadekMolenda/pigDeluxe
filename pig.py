import sys
from PySide.QtCore import *
from PySide.QtGui import *

from PySide.phonon import Phonon

import time

app = QApplication(sys.argv)

message = QTime.currentTime()

pigR = QPixmap("./pigR.png")
pigL = QPixmap("./pigL.png")

mediaObject = None

class Pig(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        self.setStyleSheet("background: transparent")
        self.setPixmap(pigR)
        self.setWindowFlags(Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    def moveRight(self):
        self.setPixmap(pigR)
        self.move(self.pos() + QPoint(1, 0))

    def moveLeft(self):
        self.setPixmap(pigL)
        self.move(self.pos() + QPoint(-1, 0))

    def snort(self):
        QSound.play("pig.wav")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            app.quit()
        elif e.key() == Qt.Key_Right:
            mediaObject.play()
            self.moveRight()
        elif e.key() == Qt.Key_Left:
            mediaObject.play()
            self.moveLeft()
        elif e.key() == Qt.Key_Return:
            mediaObject.play()

pig = Pig()
audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, pig)
mediaObject = Phonon.MediaObject(pig)
mediaSource = Phonon.MediaSource("./pig.wav")
Phonon.createPath(mediaObject, audioOutput)

mediaObject.enqueue(mediaSource)

pig.show()

sys.exit(app.exec_())



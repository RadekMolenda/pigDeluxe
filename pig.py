import sys
import random
from PySide.QtCore import *
from PySide.QtGui import *

from PySide.phonon import Phonon

import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--width', '-x', type=int, default=50, help='pig width')
parser.add_argument('--height', '-y', type=int, default=50, help='pig height')
args = parser.parse_args()

app = QApplication(sys.argv)

message = QTime.currentTime()

pigR = QPixmap("./pigR.png")
pigL = QPixmap("./pigL.png")

class Pig(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        self.setStyleSheet("background: transparent")
        self.setPixmap(pigR)
        self.setWindowFlags(Qt.SplashScreen)
        self.setScaledContents(True)
        self.setFixedWidth(args.width)
        self.setFixedHeight(args.height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        self.voice = Snorter(self)

    def moveRight(self):
        self.setPixmap(pigR)
        self.move(self.pos() + QPoint(1, 0))

    def moveLeft(self):
        self.setPixmap(pigL)
        self.move(self.pos() + QPoint(-1, 0))

    def snort(self):
        self.voice.snort()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            app.quit()
        elif e.key() == Qt.Key_Right:
            self.snort()
            self.moveRight()
        elif e.key() == Qt.Key_Left:
            self.snort()
            self.moveLeft()
        elif e.key() == Qt.Key_Return:
            self.snort()

class Snorter():
    def __init__(self, pig):
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, pig)
        self.mediaObject = Phonon.MediaObject(pig)
        self.mediaSources = [Phonon.MediaSource("./pig1.mp3"), Phonon.MediaSource("./pig2.mp3")]
        Phonon.createPath(self.mediaObject, self.audioOutput)

    def snort(self):
        self.mediaObject.setCurrentSource(random.choice(self.mediaSources))
        self.mediaObject.play()

pig = Pig()

pig.show()

sys.exit(app.exec_())



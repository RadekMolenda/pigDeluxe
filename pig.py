import sys
import random
from PySide.QtCore import *
from PySide.QtGui import *

from PySide.phonon import Phonon
from itertools import cycle

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
pigR2 = QPixmap("./pigR2.png")
pigL2 = QPixmap("./pigL2.png")
pigRight = [pigR, pigR2]
pigLeft = [pigL, pigL2]

class PigMove():
    def __init__(self, positions):
        self.positions = positions
        self.current = 0

    def move(self):
        self.current = (1 + self.current) % len(self.positions)
        return self.positions[self.current]

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
        self.autoMode = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.randomMove)
        self.rightMove = PigMove(pigRight)
        self.leftMove = PigMove(pigLeft)

    def moveRight(self):
        self.snort()
        self.setPixmap(self.rightMove.move())
        self.move(self.pos() + QPoint(1, 0))

    def moveLeft(self):
        self.snort()
        self.setPixmap(self.leftMove.move())
        self.move(self.pos() + QPoint(-1, 0))

    def randomMove(self):
        action = random.choice([self.moveRight, self.moveLeft])
        action()

    def snort(self):
        self.voice.snort()

    def toggleAutomode(self):
        self.autoMode = not self.autoMode
        if self.autoMode:
            self.timer.start(1000)
        else:
            self.timer.stop()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            app.quit()
        elif e.key() == Qt.Key_Right:
            self.moveRight()
        elif e.key() == Qt.Key_Left:
            self.moveLeft()
        elif e.key() == Qt.Key_Return:
            self.snort()
        elif e.key() == Qt.Key_A:
            self.toggleAutomode()

class Snorter():
    MEDIA_FILES = ['./pig1.mp3', './pig2.mp3']

    def __init__(self, pig):
        self.mediaObjects = []
        for mediaFile in self.MEDIA_FILES:
            source = Phonon.MediaSource(mediaFile)
            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, pig)
            mediaObject = Phonon.MediaObject(pig)
            mediaObject.setCurrentSource(source)
            Phonon.createPath(mediaObject, audioOutput)
            self.mediaObjects.append(mediaObject)

    def snort(self):
        mediaObject = random.choice(self.mediaObjects)
        if mediaObject.state() == Phonon.StoppedState:
            mediaObject.play()

pig = Pig()

pig.show()

sys.exit(app.exec_())



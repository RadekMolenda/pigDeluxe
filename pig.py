#!/usr/bin/env python3

import sys
import random
from PySide.QtCore import *
from PySide.QtGui import *

from PySide.phonon import Phonon
from itertools import cycle

import time
import argparse
import psutil


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

class PigTarget():
    def __init__(self, pig):
        self.pig = pig
        self.position = None

    def reached(self):
        return self.pig.pos() == self.position

    def pickPosition(self):
        pos = self.pig.pos()
        geo = app.desktop().screenGeometry(pos)
        new = random.randint(geo.left(), geo.right())
        self.position = QPoint(new, pos.y())

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
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        self.setScaledContents(True)
        self.setFixedWidth(args.width)
        self.setFixedHeight(args.height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        self.voice = Snorter(self)
        self.autoMode = True
        self.timer = QTimer(self)
        self.movingRight = True
        self.movingLeft = False
        self.timer.timeout.connect(self.pigMove)
        self.rightMove = PigMove(pigRight)
        self.leftMove = PigMove(pigLeft)
        self.target = PigTarget(self)
        self.timer.start(1000)

    def moveRight(self):
        self.snort()
        self.setPixmap(self.rightMove.move())
        self.move(self.pos() + QPoint(1, 0))
        self.movingRight = True
        self.movingLeft = False

    def moveLeft(self):
        self.snort()
        self.setPixmap(self.leftMove.move())
        self.move(self.pos() + QPoint(-1, 0))
        self.movingLeft = True
        self.movingRight = False

    def pigMove(self):
        if self.target.reached() or self.target.position is None:
            self.target.pickPosition()
        else:
            self.moveToTarget()

    def moveToTarget(self):
        targetPos = self.target.position
        pigPos = self.pos()
        if pigPos.x() < targetPos.x():
            self.moveRight()
        else:
            self.moveLeft()

    def snort(self):
        self.voice.snort()

    def toggleAutomode(self):
        self.autoMode = not self.autoMode
        if self.autoMode and not self.timer.isActive():
            self.timer.start(1000)
        elif self.timer.isActive():
            self.timer.stop()

    def changeSpeed(self):
        interval = int(1 / psutil.cpu_times_percent(percpu=False).system * 5000)
        if interval < 500:
            self.voice.panic()
        else:
            self.voice.calmDown()

        if self.timer.isActive():
            self.timer.setInterval(interval)

    def mousePressEvent(self, e):
        self.dragOffset = e.pos()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self.dragOffset)

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
    transform = lambda aList: list(map(lambda x: Phonon.MediaSource(x), aList))
    MEDIA_FILES = transform(['./pig1.mp3', './pig2.mp3'])
    PANIC_MEDIA_FILES = transform(['./pig1_panic.mp3', './pig2_panic.mp3'])

    def __init__(self, pig):
        audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, pig)
        self.mediaObject = Phonon.MediaObject(pig)
        Phonon.createPath(self.mediaObject, audioOutput)
        self.calmDown()

    def snort(self):
        if self.mediaObject.state() == Phonon.StoppedState:
            random.shuffle(self.mediaFiles)
            self.mediaObject.enqueue(self.mediaFiles[0])
            self.mediaObject.play()

    def panic(self):
        self.mediaFiles = self.PANIC_MEDIA_FILES

    def calmDown(self):
        self.mediaFiles = self.MEDIA_FILES


pig = Pig()
pig.show()
timer = QTimer()
timer.timeout.connect(pig.changeSpeed)
timer.start(2000)

sys.exit(app.exec_())

#!/usr/bin/env python3

import sys
import random
from PySide.QtCore import *
from PySide.QtGui import *

from PySide.phonon import Phonon
from itertools import cycle
from pig_gravity import pigGravity, pigDrag

import time
import argparse
import psutil


parser = argparse.ArgumentParser()
parser.add_argument('--width', '-x', type=int, default=50, help='pig width')
parser.add_argument('--height', '-y', type=int, default=50, help='pig height')
args = parser.parse_args()

app = QApplication(sys.argv)

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

class PigAnimate():
    def __init__(self):
        self.rightFrames = cycle([QPixmap("./pigR.png"), QPixmap("./pigR2.png")])
        self.leftFrames = cycle([QPixmap("./pigL.png"), QPixmap("./pigL2.png")])

    def moveRight(self):
        return next(self.rightFrames)

    def moveLeft(self):
        return next(self.leftFrames)

class PigAutoMode():
    def __init__(self, pig, enabled=True):
        self.timer = QTimer(pig)
        self.enabled = enabled
        self.timer.timeout.connect(pig.pigMove)
        self.timer.start(1000)

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled and not self.timer.isActive():
            self.timer.start(1000)
        elif self.timer.isActive():
            self.timer.stop()

    def hookKeyPress(self, event):
        self.toggle()

class PigForce:
    def __init__(self, rx, ry):
        self.rx = rx
        self.ry = ry
        self.pigDrag = pigDrag([self.rx, self.ry])
        self.pigGravity = pigGravity([self.rx, self.ry])
    def affect(self, vector):
        x, y = vector
        self.rx, self.ry = self.pigDrag(self.rx, self.ry)
        self.rx, self.ry = self.pigGravity(self.rx, self.ry)
        return [x + self.rx, y - self.ry]

class PigJump:
    def __init__(self, pig):
        self.fps = 60.0
        self.timer = QTimer(pig)
        self.pig = pig
        self.start = pig.pos()
        self.force = PigForce((random.random() - 0.5) * 10, random.random() * 40)
        self.nextPoint = [self.start.x(), self.start.y()]
        self.stopRy = - self.force.ry + (random.random() * 0.5) * 2

    def movement(self, vector):
        return self.force.affect(self.nextPoint)

    def interval(self):
        return int(1000 / self.fps)

    def projectLocation(self):
        return list(map(lambda x: int(x), self.nextPoint))

    def move(self):
        self.nextPoint = self.movement(self.nextPoint)
        self.pig.move(QPoint(*self.projectLocation()))
        if self.force.ry <= self.stopRy:
            self.timer.stop()

    def jump(self):
        if not self.timer.isActive():
            self.timer.timeout.connect(lambda: self.move())
            self.timer.start(self.interval())


class PigCpuGuard:
    def __init__(self, timer):
        self.timer = timer

    def changeSpeed(self):
        interval = int(1 / (psutil.cpu_times_percent(percpu=False).system + 1) * 5000)

        if self.timer.isActive():
            self.timer.setInterval(interval)


class Pig(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        self.voice = Snorter(self)
        self.autoMode = PigAutoMode(self)
        self.animation = PigAnimate()
        self.target = PigTarget(self)
        self.__setup()

    def setup(self):
        self.setStyleSheet("background: transparent")
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        self.setScaledContents(True)
        self.setFixedWidth(args.width)
        self.setFixedHeight(args.height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    __setup = setup

    def checkTimer(self):
        if self.autoMode.timer.interval() < 500:
            self.voice.panic()
        else:
            self.voice.calmDown()

    def moveRight(self):
        self.snort()
        self.setPixmap(self.animation.moveRight())
        self.move(self.pos() + QPoint(1, 0))

    def moveLeft(self):
        self.snort()
        self.setPixmap(self.animation.moveLeft())
        self.move(self.pos() + QPoint(-1, 0))

    def pigMove(self):
        if self.target.reached() or self.target.position is None:
            self.target.pickPosition()
        else:
            self.moveToTarget()

    def jump(self):
        PigJump(self).jump()

    def moveToTarget(self):
        targetPos = self.target.position
        pigPos = self.pos()
        if pigPos.x() < targetPos.x():
            self.moveRight()
        else:
            self.moveLeft()

    def snort(self):
        self.voice.snort()

    def mousePressEvent(self, e):
        self.dragOffset = e.pos()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self.dragOffset)

    def mouseReleaseEvent(self, e):
        self.target.pickPosition()

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
            self.autoMode.hookKeyPress(e)
        elif e.key() == Qt.Key_J:
            self.jump()

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

if __name__ == '__main__':
    pig = Pig()
    pig.show()
    timer = QTimer()
    guard = PigCpuGuard(pig.autoMode.timer)
    timer.timeout.connect(pig.checkTimer)
    timer.timeout.connect(guard.changeSpeed)
    timer.start(2000)

    sys.exit(app.exec_())

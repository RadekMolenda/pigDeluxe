from PySide.QtGui import QPixmap
from PySide.QtCore import Qt
from itertools import cycle

class PigSkin:
    def __init__(self, frame):
        self.frame = frame
        self.rightFrames = cycle([QPixmap("./pigR.png"), QPixmap("./pigR2.png")])
        self.leftFrames = cycle([QPixmap("./pigL.png"), QPixmap("./pigL2.png")])
        self.current = next(self.rightFrames)

    def nextSkin(self):
        pass

    def handleKeyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.current = next(self.leftFrames)
        elif event.key() ==Qt.Key_Right:
            self.current = next(self.rightFrames)
        self.frame.setPixmap(self.current)

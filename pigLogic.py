from PySide.QtGui import QPixmap
from PySide.QtCore import Qt
from pigSkin import PigSkin

class Pig:
    def __init__(self, frame):
        self.frame = frame
        self.skin = PigSkin(frame)

    def trap(self):
        self.frame.setPixmap(self.skin.current)

    def handleKeyPressEvent(self, event):
        self.skin.handleKeyPressEvent(event)

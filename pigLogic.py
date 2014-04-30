from PySide.QtGui import QPixmap
from pigPicture import PigPicture
class Pig:
    def __init__(self, frame):
        self.picture = PigPicture(frame)

    def handleKeyPressEvent(self, event):
        self.picture.handleKeyPressEvent(event)

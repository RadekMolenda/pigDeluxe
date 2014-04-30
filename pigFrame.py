from PySide.QtGui import QLabel
from PySide.QtCore import Qt

class PigFrame(QLabel):
    def __init__(self, app, args):
        QLabel.__init__(self)
        self.app = app
        self.pig = None
        self.args = args
        self.__setup()

    def setup(self):
        self.setStyleSheet("background: transparent")
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        self.setScaledContents(True)
        self.setFixedWidth(self.args.width)
        self.setFixedHeight(self.args.height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    __setup = setup

    def trap(self, pig):
        self.pig = pig
        self.pig.trap()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.app.quit()
        self.pig.handleKeyPressEvent(e)

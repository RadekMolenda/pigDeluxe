import sys
from PySide.QtGui import QApplication
from pigFrame import PigFrame
from pigLogic import Pig
import argparse

class PigRunner:
    def __init__(self):
        self.__parseArgs()

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--width', '-x', type=int, default=50, help='pig width')
        parser.add_argument('--height', '-y', type=int, default=50, help='pig height')
        self.args = parser.parse_args()

    __parseArgs = parseArgs

    def run(self):
        app = QApplication(sys.argv)
        frame = PigFrame(app, self.args)
        frame.trap(Pig(frame))
        frame.show()
        sys.exit(app.exec_())

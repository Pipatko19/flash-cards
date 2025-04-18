from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
import sys

from flashcards.settings.settings import Settings
from flashcards.dashboard.landing_screen import LandingScreen

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('FlashCards')
        self.setGeometry(qtc.QRect(0, 0, 756, 538)) #size not really important
        self.setCentralWidget(LandingScreen(self))
        self.show()
    def switch_to_settings(self, id=None):
        """Switch the central widget to settings"""
        self.setCentralWidget(Settings(self, id))
    def switch_to_landing_screen(self):
        """Switch the central widget to landing screen"""
        self.setCentralWidget(LandingScreen(self))




if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    
    #style
    with open('style.qss', 'r') as f:
        _style = f.read()
    app.setStyleSheet(_style)
    
    mw = MainWindow()
    sys.exit(app.exec())


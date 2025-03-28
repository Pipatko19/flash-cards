from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
import sys

from flashcards.main_settings import Settings

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('FlashCards')
        self.setGeometry(qtc.QRect(0, 0, 756, 538)) #size not really important
        self.setCentralWidget(Settings())
        self.show()
        


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    
    #style
    with open('style.qss', 'r') as f:
        _style = f.read()
    app.setStyleSheet(_style)
    
    mw = MainWindow()
    sys.exit(app.exec())


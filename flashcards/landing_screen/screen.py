from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

class LandingScreen(qtw.QWidget):
    def __init__(self):
        """Landing screen for the application"""
        super().__init__()
        self.setWindowTitle('FlashCards')
        self.setGeometry(qtc.QRect(0, 0, 756, 538))
        self._init_widgets()
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.title = qtw.QLabel('FlashCards')
        self.title.setObjectName('title')
        
        self.cards = qtw.QTableWidget()
        self.cards.setObjectName('cards')
        
        self.add_button = qtw.QPushButton('Add Card')
        self.add_button.setObjectName('add_button')

    def _init_layouts(self):
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.title, 0, qtc.Qt.AlignTop)
        layout.addWidget(self.cards, 1)
        layout.addWidget(self.add_button, 0, qtc.Qt.AlignBottom)


if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    
    #style
    with open('style.qss', 'r') as f:
        _style = f.read()
    app.setStyleSheet(_style)
    
    mw = LandingScreen()
    mw.show()
    sys.exit(app.exec())
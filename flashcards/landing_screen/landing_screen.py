from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

print('cwd', os.getcwd())
print('-', *sys.path, '-', sep='\n')

from flashcards.storage import load_sets, FILENAME

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
        
        self.cards = qtw.QTableWidget(1, 5)
        self.populate_table()
        self.cards.setObjectName('sets')
        self.cards.setHorizontalHeaderLabels(['Title', 'Card count', 'Description', 'Tags', 'Open'])
        self.cards.setRowHeight(0, 50)
        self.cards.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.add_button = qtw.QPushButton('Add Card')
        self.add_button.setObjectName('add_button')

    def _init_layouts(self):
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        #layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.title, 0, Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.cards, 1)
        layout.addWidget(self.add_button, 0, qtc.Qt.AlignBottom)

    def populate_table(self):
        """Populate the table from a file"""
        sets = load_sets(FILENAME)
        self.cards.setRowCount(len(sets))
        for row, set in enumerate(sets):
            for col, item in enumerate(set):
                self.cards.setItem(row, col, qtw.QTableWidgetItem(item))
                
            edit_button = qtw.QPushButton('Edit')
            self.cards.setCellWidget(row, 4, edit_button)
    

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
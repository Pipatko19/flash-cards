from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

from functools import partial
import sys
import os

from flashcards.widgets import ButtonGroup
from flashcards.storage import load_sets, FILENAME, remove_set

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class LandingScreen(qtw.QWidget):
    def __init__(self, mw, *args):
        """Landing screen for the application"""
        super().__init__(*args)

        self.mw = mw
        
        self._init_widgets()
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.lblTitle = qtw.QLabel('FlashCards')
        self.lblTitle.setObjectName('lblTitle')
        
        self.tblCards = qtw.QTableWidget(0, 5)

        self.tblCards.setObjectName('sets')
        self.tblCards.setHorizontalHeaderLabels(['title', 'Card count', 'Description', 'Tags', 'Open'])
        self.tblCards.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.tblCards.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.populate_table()
        self.btnAdd = qtw.QPushButton('Add Card')
        self.btnAdd.setObjectName('add_button')
    
        self.btnAdd.pressed.connect(self.add_row)

    def _init_layouts(self):
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        #layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.lblTitle, 0, Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.tblCards, 1)
        layout.addWidget(self.btnAdd, 0, qtc.Qt.AlignBottom)

    def populate_table(self):
        """Populate the table from a file"""
        for card_set in load_sets(FILENAME):
            *values, id = card_set
            self.add_row(id, *values)
    
    def switch(self):
        """Switch the central widget"""
        id = self.sender().property('id')
        self.mw.switch_to_settings(id)

    def remove_row(self):
        """Remove a row from the table and the file"""
        id = self.sender().property('id')
        for row in range(self.tblCards.rowCount()):
            item = self.tblCards.cellWidget(row, 4)
            if item and item.property('id') == id:
                result = qtw.QMessageBox.warning(
                    self, 
                    'Delete set', 
                    'Are you sure you want to delete this set?', 
                    qtw.QMessageBox.Yes | qtw.QMessageBox.No
                )
                if result == qtw.QMessageBox.Yes:
                    self.tblCards.removeRow(row)
                    remove_set(FILENAME, id)
                break
        

    def add_row(self, id=None, *values):
        """Add a row to the table"""
        last_idx = self.tblCards.rowCount()
        self.tblCards.insertRow(last_idx)
        self.tblCards.setRowHeight(last_idx, 75)
        for col, item in enumerate(values):
            item = qtw.QTableWidgetItem(item)
            item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
            self.tblCards.setItem(last_idx, col, item)
        
        edit_buttons = ButtonGroup(['delete', 'edit', 'play'], set_name=False)
        edit_buttons.setProperty('id', id)
        edit_buttons.edit.setIcon(qtg.QIcon('assets/pencil.svg'))
        edit_buttons.delete.setIcon(qtg.QIcon('assets/trash.svg'))
        edit_buttons.play.setIcon(qtg.QIcon('assets/play.svg'))
        edit_buttons.edit.pressed.connect(self.switch)
        edit_buttons.delete.pressed.connect(self.remove_row)

        self.tblCards.setCellWidget(last_idx, 4, edit_buttons)

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
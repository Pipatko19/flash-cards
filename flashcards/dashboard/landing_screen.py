from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

import sys

from flashcards.widgets import ButtonGroup
from flashcards.storage import load_sets, FILENAME, remove_set

class LandingScreen(qtw.QWidget):
    def __init__(self, mw, *args):
        """Landing screen for the application"""
        super().__init__(*args)

        self.mw = mw
        
        self._init_widgets()
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.lbl_title = qtw.QLabel('FlashCards')
        self.lbl_title.setObjectName('lblTitle')
        
        self.tbl_cards = qtw.QTableWidget(0, 5)

        self.tbl_cards.setObjectName('sets')
        self.tbl_cards.setHorizontalHeaderLabels(['title', 'Card count', 'Description', 'Tags', 'Open'])
        self.tbl_cards.setSelectionMode(qtw.QAbstractItemView.SelectionMode.NoSelection)
        self.tbl_cards.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.Stretch)
        
        self.populate_table()
        
        self.btn_add = qtw.QPushButton('Add Card')
        self.btn_add.setObjectName('add_button')
    
        self.btn_add.pressed.connect(self.add_row)

    def _init_layouts(self):
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(self.lbl_title, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.tbl_cards, 1)
        layout.addWidget(self.btn_add, 0, Qt.AlignmentFlag.AlignBottom)

    def populate_table(self):
        """Populate the table from a file"""
        for card_set in load_sets(FILENAME):
            *values, id = card_set
            self.add_row(id, *values)
    
    @qtc.Slot()
    def switch(self):
        """Switch the central widget"""
        id = self.sender().property('id')
        self.mw.switch_to_settings(id)
    
    @qtc.Slot()
    def play(self):
        id = self.sender().property('id')
        self.mw.switch_to_flashcards(id)

    def remove_row(self):
        """Remove a row from the table and the file"""
        id = self.sender().property('id')
        for row in range(self.tbl_cards.rowCount()):
            item = self.tbl_cards.cellWidget(row, 4)
            if item and item.property('id') == id:
                result = qtw.QMessageBox.warning(
                    self, 
                    'Delete set', 
                    'Are you sure you want to delete this set?', 
                    qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No
                )
                if result == qtw.QMessageBox.StandardButton.Yes:
                    self.tbl_cards.removeRow(row)
                    remove_set(FILENAME, id)
                break
        

    def add_row(self, id=None, *values):
        """Add a row to the table"""
        last_idx = self.tbl_cards.rowCount()
        self.tbl_cards.insertRow(last_idx)
        self.tbl_cards.setRowHeight(last_idx, 75)
        for col, item in enumerate(values):
            item = qtw.QTableWidgetItem(item)
            item.setFlags(item.flags() & ~qtc.Qt.ItemFlag.ItemIsEditable)
            self.tbl_cards.setItem(last_idx, col, item)
        
        edit_buttons = ButtonGroup(['delete', 'edit', 'play'], set_name=False)
        edit_buttons.setProperty('id', id)
        edit_buttons.edit.setIcon(qtg.QIcon('assets/icons/pencil.svg'))
        edit_buttons.delete.setIcon(qtg.QIcon('assets/icons/trash.svg'))
        edit_buttons.play.setIcon(qtg.QIcon('assets/icons/play.svg'))
        edit_buttons.edit.pressed.connect(self.switch)
        edit_buttons.delete.pressed.connect(self.remove_row)
        edit_buttons.play.pressed.connect(self.play)

        self.tbl_cards.setCellWidget(last_idx, 4, edit_buttons)

if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    
    #style
    with open('style.qss', 'r') as f:
        _style = f.read()
    app.setStyleSheet(_style)
    
    mw = LandingScreen('')
    mw.show()
    sys.exit(app.exec())
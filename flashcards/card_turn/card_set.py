from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

class FlashCards(qtw.QWidget):
    def __init__(self, mw, id=None):
        """UI for playing the flashcards"""
        super().__init__()
        self.mw = mw

        self._init_widgets()
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.card_select_label = qtw.QLabel('0/0') 
        
        self.card_face = qtw.QLabel()
        self.previous_card_button = qtw.QPushButton()
        self.next_card_button = qtw.QPushButton()
        
        self.
        
        
        self.tags = qtw.QLineEdit()
        self.description = qtw.QTextEdit()
        self.json_button = qtw.QPushButton('Import from CSV')
        self.saving_buttons = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Save | qtw.QDialogButtonBox.Cancel)
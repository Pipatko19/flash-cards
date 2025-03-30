from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from flashcards.cards import CardWidget, NamedField, ScrollableGroupBox

class Settings(qtw.QWidget):
    def __init__(self):
        """UI for creating and changing cards"""
        super().__init__()
        self._init_widgets()

        self.tags.field.setPlaceholderText('Comma separated')
        self.description.field.setPlaceholderText('Optional')
        
        self.csv_button.setObjectName('csv_button')
        self.confirm_button.setObjectName('confirm_button')

        #resize options
        self.title.setMinimumSize(300, self.title.sizeHint().height())
        self.tags.setMinimumSize(300, self.tags.sizeHint().height())
        self.title.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        self.tags.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.title = NamedField('Title', qtw.QLineEdit())
        self.tags = NamedField('Tags', qtw.QLineEdit())

        self.csv_button = qtw.QPushButton('Import from CSV')
        self.confirm_button = qtw.QPushButton('Confirm')
        self.description = NamedField('Description', qtw.QTextEdit())
        self.cards = ScrollableGroupBox()
        
    def _init_layouts(self):
        """Setting widgets to the main layout"""
        main_layout = qtw.QGridLayout()
        self.setLayout(main_layout)
        
        main_layout.setColumnMinimumWidth(1, 100)
        main_layout.setColumnStretch(0, 2)
        main_layout.setColumnStretch(1, 1)
        main_layout.setColumnStretch(2, 2)
        main_layout.setRowStretch(0, 0)
        main_layout.setRowStretch(1, 0)
                
        main_layout.addWidget(self.title, 0, 0)
        main_layout.addWidget(self.tags, 1, 0)
        main_layout.addWidget(self.description, 0, 2, 2, 1)
        main_layout.addWidget(self.csv_button, 2, 0, qtc.Qt.AlignLeft)
        main_layout.addWidget(self.confirm_button, 2, 2, qtc.Qt.AlignRight)
        main_layout.addWidget(self.cards, 3, 0, 1, 3)
        
        

            
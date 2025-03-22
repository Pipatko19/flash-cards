from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

class Settings(qtw.QWidget):
    def __init__(self):
        super().__init__()
        main_layout = qtw.QGridLayout()
        self.setLayout(main_layout)
        self.title = NamedField('Title', qtw.QLineEdit())
        self.tags = NamedField('Tags', qtw.QLineEdit())
        self.tags.field.setPlaceholderText('Comma separated')
        
        self.csv_button = qtw.QPushButton('Import from CSV')
        self.confirm_button = qtw.QPushButton('Confirm')
        
        self.description = NamedField('Description', qtw.QTextEdit())
        self.description.field.setPlaceholderText('Optional')
        
        self.cards = Scrollable_GroupBox()
        
        main_layout.addWidget(self.title, 0, 0)
        main_layout.addWidget(self.tags, 1, 0)
        main_layout.addWidget(self.description, 0, 1, 2, 1)
        main_layout.addWidget(self.csv_button, 2, 0)
        main_layout.addWidget(self.confirm_button, 2, 1)
        main_layout.addWidget(self.cards, 3, 0, 1, 2)
        
        
class NamedField(qtw.QWidget):
    def __init__(self, name, field):
        super().__init__()
        layout = qtw.QVBoxLayout()
        self.field = field
        self.setLayout(layout)
        layout.addWidget(qtw.QLabel(name))
        layout.addWidget(field)

class Scrollable_GroupBox(qtw.QWidget):
    def __init__(self):
        super().__init__()
        

        self._outer_container = qtw.QGroupBox()
        self._outer_container.setTitle('Item count:')
        self._outer_container.setLayout(qtw.QVBoxLayout())
        self.scrolls = qtw.QScrollArea()
        self.scrolls.setWidgetResizable(True)
        self._inner_container = qtw.QGroupBox()
        self.main_layout = qtw.QVBoxLayout()
        
        self.setLayout(qtw.QVBoxLayout())
        self._outer_container.layout().addWidget(self.scrolls)
        self.scrolls.setWidget(self._inner_container)
        self.layout().addWidget(self._outer_container)
        self._inner_container.setLayout(self.main_layout)
        
        for i in range(5):
            self.main_layout.addWidget(Card())
            


class Card(qtw.QWidget):
    def __init__(self, front_text='', back_text='', parent=None):
        super().__init__(parent)
        layout = qtw.QFormLayout()
        self.setLayout(layout)
        
        front_input = qtw.QLineEdit()
        front_input.setPlaceholderText(front_text)
        back_input = qtw.QLineEdit()
        back_input.setPlaceholderText(back_text)
        
        layout.addRow(front_input, back_input)
        
        # front_input.textChanged.connect(lambda text: print(text))
        # back_input.textChanged.connect(lambda text: print(text))
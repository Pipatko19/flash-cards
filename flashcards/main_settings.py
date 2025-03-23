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

        self.title.setMinimumSize(300, self.title.sizeHint().height())
        self.tags.setMinimumSize(300, self.tags.sizeHint().height())
        self.tags.field.setPlaceholderText('Comma separated')
        
        self.title.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        self.tags.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        
        self.csv_button = qtw.QPushButton('Import from CSV')
        self.confirm_button = qtw.QPushButton('Confirm')
        self.csv_button.setMinimumSize(self.csv_button.sizeHint() + qtc.QSize(10, 0))
        self.confirm_button.setMinimumSize(self.confirm_button.sizeHint() + qtc.QSize(10, 0))
        
        self.csv_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        self.confirm_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        
        self.description = NamedField('Description', qtw.QTextEdit())
        self.description.field.setPlaceholderText('Optional')
        
        self.cards = Scrollable_GroupBox()

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

        
        
class NamedField(qtw.QWidget):
    def __init__(self, name, field):
        super().__init__()
        layout = qtw.QVBoxLayout()
        self.field = field
        self.setLayout(layout)
        layout.addWidget(qtw.QLabel(name))
        layout.addWidget(field, 1)

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
        
        for i in range(4):
            self.main_layout.addWidget(Card())
            


class Card(qtw.QWidget):
    
    def __init__(self, front_text='front', back_text='back', parent=None):
        super().__init__(parent)
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        
        margin = qtc.QMargins(20, 20, 20, 20)
        
        front_input = qtw.QTextEdit()
        front_input.setPlaceholderText(front_text)

        back_input = qtw.QTextEdit()
        back_input.setPlaceholderText(back_text)

        
        layout.addWidget(front_input, 1)
        layout.setContentsMargins(margin)
        layout.setSpacing(40)
        layout.addWidget(back_input, 1)
        
        # front_input.textChanged.connect(lambda text: print(text))
        # back_input.textChanged.connect(lambda text: print(text))
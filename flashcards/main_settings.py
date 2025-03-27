from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from flashcards.cards import CardWidget

class Settings(qtw.QWidget):
    def __init__(self):
        """UI for creating and changing cards"""
        super().__init__()
        self._init_widgets()

        self.tags.field.setPlaceholderText('Comma separated')
        self.description.field.setPlaceholderText('Optional')

        #resize options
        self.title.setMinimumSize(300, self.title.sizeHint().height())
        self.tags.setMinimumSize(300, self.tags.sizeHint().height())
        self.title.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        self.tags.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        
        self.csv_button.setMinimumSize(self.csv_button.sizeHint() + qtc.QSize(10, 0))
        self.confirm_button.setMinimumSize(self.confirm_button.sizeHint() + qtc.QSize(10, 0))
        
        self.csv_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        self.confirm_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.title = NamedField('Title', qtw.QLineEdit())
        self.tags = NamedField('Tags', qtw.QLineEdit())

        self.csv_button = qtw.QPushButton('Import from CSV')
        self.confirm_button = qtw.QPushButton('Confirm')
        self.description = NamedField('Description', qtw.QTextEdit())
        self.cards = Scrollable_GroupBox()
        
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
        
        
class NamedField(qtw.QWidget):
    def __init__(self, name, field):
        """Wraps a widget with a title

        Args:
            name (str): title of the widget
            field (QWidget): the widget that gets wrapped
        """
        super().__init__()
        layout = qtw.QVBoxLayout()
        self.field = field
        self.setLayout(layout)
        layout.addWidget(qtw.QLabel(name))
        layout.addWidget(field, 1)

class Scrollable_GroupBox(qtw.QWidget):
    def __init__(self):
        """The container for card creation. 
        GroupBox(for title) -> ScrollArea(scroll functionality) -> GroupBox(holding) -> Cards
        """
        super().__init__()
        
        #init
        self.outer_container = qtw.QGroupBox()
        self.outer_container.setTitle('Card count:')
        self.outer_container.setObjectName('card_container')
        self.outer_container.setLayout(qtw.QVBoxLayout())
        
        self._scrolls = qtw.QScrollArea()
        self._scrolls.setWidgetResizable(True)

        self._inner_container = qtw.QGroupBox()
        self.main_layout = qtw.QVBoxLayout()
        
        #connecting
        self.setLayout(qtw.QVBoxLayout())
        self.outer_container.layout().addWidget(self._scrolls)
        self._scrolls.setWidget(self._inner_container)
        self.layout().addWidget(self.outer_container)
        self._inner_container.setLayout(self.main_layout)

        
        for i in range(3):
            self.main_layout.addWidget(CardWidget())
            
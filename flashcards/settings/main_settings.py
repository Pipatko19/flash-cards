from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from flashcards.settings.cards import ScrollableGroupBox
from flashcards.storage import save_to_file, load_from_file, FILENAME
from flashcards.widgets import NamedField, TightenedButtons

class Settings(qtw.QWidget):
    def __init__(self, mw, id=None):
        """UI for creating and changing cards"""
        super().__init__()
        self.mw = mw
        
        self._init_widgets()

        self.tags.field.setPlaceholderText('Comma separated')
        self.description.field.setPlaceholderText('Optional')
        
        self.json_button.setObjectName('json_button')
        
        self.saving_buttons.save.pressed.connect(self.save_settings)
        self.saving_buttons.cancel.pressed.connect(self.cancel)
        self.json_button.pressed.connect(self.load_from_json)

        #resize options
        self.title.setMinimumSize(300, self.title.sizeHint().height())
        self.tags.setMinimumSize(300, self.tags.sizeHint().height())
        self.title.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        self.tags.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        
        self.load_from_json(id)
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.title = NamedField('Title', qtw.QLineEdit())
        self.tags = NamedField('Tags', qtw.QLineEdit())

        self.json_button = qtw.QPushButton('Import from CSV')
        self.saving_buttons = TightenedButtons(['cancel', 'save'])
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
        main_layout.addWidget(self.json_button, 2, 0, qtc.Qt.AlignLeft)
        main_layout.addWidget(self.saving_buttons, 2, 2, qtc.Qt.AlignRight)
        main_layout.addWidget(self.cards, 3, 0, 1, 3)
        
    def save_settings(self):
        """Save settings to a file"""
        name = self.title.field.text()
        description = self.description.field.toPlainText()
        tags = self.tags.field.text()
        flashcards = self.cards.model.flashcards
        save_to_file(FILENAME, title=name, description=description, tags=tags, flashcards=flashcards, id=self.id)
        self.mw.switch_widget()

    
    def cancel(self):
        """Cancel changes"""
        self.mw.switch_widget()
    def load_from_json(self, id):
        """Load settings from a JSON file"""
        print(id)
        if id is None:
            self.cards.add_card()
            self.id = None
            print('hi')
            return 
        data = load_from_file(FILENAME, id)
        self.id = data['id']
        self.title.field.setText(data['title'])
        self.description.field.setPlainText(data['description'])
        self.tags.field.setText(data['tags'])
        
        # Load flashFs into the model
        self.cards.populate(data['flashcards'])

        

            
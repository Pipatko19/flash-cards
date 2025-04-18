from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from flashcards.settings.cards import ScrollableGroupBox
from flashcards.storage import save_to_file, get_set_by_id, FILENAME
from flashcards.widgets import NamedField, ButtonGroup

class Settings(qtw.QWidget):
    def __init__(self, mw, id=None):
        """UI for creating and changing cards"""
        super().__init__()
        self.mw = mw
        
        self._init_widgets()

        #resize options
        self.txtTitle.setMinimumSize(300, self.txtTitle.sizeHint().height())
        self.txtTags.setMinimumSize(300, self.txtTags.sizeHint().height())
        self.txtTitle.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        self.txtTags.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        
        self.load_from_json(id)
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.txtTitle = NamedField('Title', qtw.QLineEdit())
        self.txtTags = NamedField('Tags', qtw.QLineEdit())
        self.txtTags.field.setPlaceholderText('Comma separated')
        
        self.txtDescription = NamedField('Description', qtw.QTextEdit())
        self.txtDescription.field.setPlaceholderText('Optional')

        self.btnJson = qtw.QPushButton('Import from CSV')
        self.btnSave = ButtonGroup(['cancel', 'save'])

        self.btnJson.setObjectName('json_button')
        self.btnJson.pressed.connect(self.load_from_json)
        self.btnSave.save.pressed.connect(self.save_settings)
        self.btnSave.cancel.pressed.connect(self.cancel)

        
        self.grpCards = ScrollableGroupBox()
        
        
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
                
        main_layout.addWidget(self.txtTitle, 0, 0)
        main_layout.addWidget(self.txtTags, 1, 0)
        main_layout.addWidget(self.txtDescription, 0, 2, 2, 1)
        main_layout.addWidget(self.btnJson, 2, 0, qtc.Qt.AlignLeft)
        main_layout.addWidget(self.btnSave, 2, 2, qtc.Qt.AlignRight)
        main_layout.addWidget(self.grpCards, 3, 0, 1, 3)
        
    def save_settings(self):
        """Save settings to a file"""
        name = self.txtTitle.field.text()
        description = self.txtDescription.field.toPlainText()
        tags = self.txtTags.field.text()
        flashcards = self.grpCards.model.flashcards
        save_to_file(FILENAME, title=name, description=description, tags=tags, flashcards=flashcards, id=self.id)
        self.mw.switch_to_landing_screen()

    
    def cancel(self):
        """Cancel changes"""
        self.mw.switch_to_landing_screen()
    def load_from_json(self, id):
        """Load settings from a JSON file"""
        if id is None:
            self.grpCards.add_card()
            self.id = None
            return 
        data = get_set_by_id(FILENAME, id)
        self.id = data['id']
        self.txtTitle.field.setText(data['title'])
        self.txtDescription.field.setPlainText(data['description'])
        self.txtTags.field.setText(data['tags'])
        
        # Load flashFs into the model
        self.grpCards.populate(data['flashcards'])

        

            
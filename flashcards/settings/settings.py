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
        self.setObjectName('settings')
        
        self._init_widgets()

        #resize options
        self.txt_title.setMinimumSize(300, self.txt_title.sizeHint().height())
        self.txt_tags.setMinimumSize(300, self.txt_tags.sizeHint().height())
        self.txt_title.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        self.txt_tags.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        
        self.load_from_json(id)
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.txt_title = NamedField('Title', qtw.QLineEdit())
        self.txt_tags = NamedField('Tags', qtw.QLineEdit())
        self.txt_tags.field.setPlaceholderText('Comma separated')

        self.txt_description = NamedField('Description', qtw.QTextEdit())
        self.txt_description.field.setPlaceholderText('Optional')

        self.btn_json = qtw.QPushButton('Import from CSV')
        self.btn_save = ButtonGroup(['cancel', 'save'])

        self.btn_json.setObjectName('json_button')
        self.btn_json.pressed.connect(self.load_from_json)
        self.btn_save.save.pressed.connect(self.save_settings)
        self.btn_save.cancel.pressed.connect(self.cancel)

        
        self.grp_cards = ScrollableGroupBox()
        
        
    def _init_layouts(self):
        """Setting widgets to the main layout"""
        main_layout = qtw.QGridLayout()
        self.setLayout(main_layout)
        
        main_layout.setColumnMinimumWidth(1, 100)
        main_layout.setColumnStretch(0, 2)
        main_layout.setColumnStretch(2, 2)
        main_layout.setRowStretch(0, 0)
        main_layout.setRowStretch(1, 0)
                
        main_layout.addWidget(self.txt_title, 0, 0)
        main_layout.addWidget(self.txt_tags, 1, 0)
        main_layout.addWidget(self.txt_description, 0, 2, 2, 1)
        main_layout.addWidget(self.btn_json, 2, 0, qtc.Qt.AlignLeft)
        main_layout.addWidget(self.btn_save, 2, 2, qtc.Qt.AlignRight)
        main_layout.addWidget(self.grp_cards, 3, 0, 1, 3)
        
    def save_settings(self):
        """Save settings to a file"""
        name = self.txt_title.field.text()
        description = self.txt_description.field.toPlainText()
        tags = self.txt_tags.field.text()
        flashcards = self.grp_cards.model.flashcards
        save_to_file(FILENAME, title=name, description=description, tags=tags, flashcards=flashcards, id=self.id)
        self.mw.switch_to_landing_screen()

    
    def cancel(self):
        """Cancel changes"""
        self.mw.switch_to_landing_screen()
    def load_from_json(self, id):
        """Load settings from a JSON file"""
        if id is None:
            self.grp_cards.add_card()
            self.id = None
            return 
        data = get_set_by_id(FILENAME, id)
        self.id = data['id']
        self.txt_title.field.setText(data['title'])
        self.txt_description.field.setPlainText(data['description'])
        self.txt_tags.field.setText(data['tags'])
        
        # Load flashcards into the model
        self.grp_cards.populate(data['flashcards'])

        

            
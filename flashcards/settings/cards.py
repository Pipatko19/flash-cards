from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QMargins
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from functools import partial
from flashcards.card_model import FlashCardsModel

from flashcards.widgets import ShadowedWidget

class CardWidget(QWidget):
    frontChangedSignal = qtc.Signal(str)
    backChangedSignal = qtc.Signal(str)
    
    def __init__(self, front_text='Front', back_text='Back', parent=None):
        """Represents a card with a front and a back side"""
        super().__init__(parent)
        
        
        # Main layout
        layout = QHBoxLayout(self)
        margin = QMargins(20, 20, 20, 20)

        # Create QTextEdit widgets
        self.front_input = QTextEdit()
        self.front_input.setObjectName('card')
        self.front_input.setPlaceholderText(front_text)
        self.front_input.setMinimumHeight(150)
        
        self.back_input = QTextEdit()
        self.back_input.setObjectName('card')
        self.back_input.setPlaceholderText(back_text)
        self.back_input.setMinimumHeight(150)


        # Create ShadowedWidget containers for both front and back
        front_input_widget = ShadowedWidget(self.front_input)
        back_input_widget = ShadowedWidget(self.back_input)

        self.front_input.textChanged.connect(self._emit_front_text_changed)
        self.back_input.textChanged.connect(self._emit_back_text_changed)

        # Add ShadowedWidgets to the main layout
        layout.addWidget(front_input_widget, 1)
        layout.addWidget(back_input_widget, 1)
        
        # Adjust margins and spacing
        layout.setContentsMargins(margin)
        layout.setSpacing(40)
        
    def _emit_front_text_changed(self):
        self.frontChangedSignal.emit(self.front_input.toPlainText())
    def _emit_back_text_changed(self):
        self.backChangedSignal.emit(self.back_input.toPlainText())
    @property
    def empty(self):
        return self.front_input.toPlainText() == '' and self.back_input.toPlainText() == ''
    


class ScrollableGroupBox(qtw.QWidget):
    def __init__(self):
        """The container for card creation. 
        GroupBox(for title) -> ScrollArea(scroll functionality) -> GroupBox(holding) -> Cards
        """
        super().__init__()
        
        self.model = FlashCardsModel(self)
        
        #init
        
        self._outer_container = qtw.QGroupBox()
        self._outer_container.setTitle('Card count:')
        self._outer_container.setObjectName('card_container')
        self._outer_container.setLayout(qtw.QVBoxLayout())
        
        self._scrolls = qtw.QScrollArea()
        self._scrolls.setWidgetResizable(True)

        self._inner_container = qtw.QGroupBox()
        self.main_layout = qtw.QVBoxLayout()
        
        #connecting
        self.setLayout(qtw.QVBoxLayout())
        self._outer_container.layout().addWidget(self._scrolls)
        self._scrolls.setWidget(self._inner_container)
        self.layout().addWidget(self._outer_container)
        self._inner_container.setLayout(self.main_layout)
            
        self.textedits: list[CardWidget] = []
                
    def add_card(self):
        """Create and configure a new card"""
        card = CardWidget()
        self.main_layout.addWidget(card)
        self.model.insertRow(self.model.rowCount())
        idx = len(self.textedits)
        modeled_idx = self.model.index(idx)
        card.frontChangedSignal.connect(
            partial(self.on_change, modeled_idx, FlashCardsModel.QUESTION_ROLE) # text from signal
        )
        card.backChangedSignal.connect(
            partial(self.on_change, modeled_idx, FlashCardsModel.ANSWER_ROLE)
        )
        self.textedits.append(card)

    def remove_card(self):
        """Remove the last card"""
        last_textedit = self.textedits.pop()
        self.layout().removeWidget(last_textedit)
        last_textedit.deleteLater()
        self.model.removeRow(self.model.rowCount())

    def on_change(self, idx, role, value):
        """Update the model when the text in the card changes"""
        self.model.setData(idx, value, role)
        idx_num = idx.row()
        cur_card = self.textedits[idx_num]
        card_count = len(self.textedits)
        
        if idx_num == card_count - 1:
            self.add_card()
            
        elif idx_num == card_count - 2 and cur_card.empty:
            self.remove_card()
        self._outer_container.setTitle(f'Card count: {len(self.textedits)}')
            
    def populate(self, data: list[dict[str, str]]):
        """Populate the card with data"""
        print('-----data-----', *data, '--------------', sep='\n')
        for row in range(len(data)):
            self.add_card()
        self.model.overwrite_data(data)
        for idx, card in enumerate(self.textedits):
            if idx >= len(data):
                break
            card.blockSignals(True)
            card.front_input.setPlainText(data[idx]['question'])
            card.back_input.setPlainText(data[idx]['answer'])
            card.blockSignals(False)
        self._outer_container.setTitle(f'Card count: {len(self.textedits)}')

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Tab:
    #         print('heloo')
    #         focused_card = QApplication.focusWidget()
    #         if focused_card in self.textedits:
    #             print('fuck yeah')
    #             cur_idx = self.textedits.index(focused_card)
    #             self.textedits[cur_idx + 1].setFocus()
    #     else:
    #         return super().keyPressEvent(event)
    
if __name__ == "__main__":
    app = QApplication([])
    widget = CardWidget()
    widget.show()
    app.exec()

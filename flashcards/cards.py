from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QMargins
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from flashcards.card_model import FlashCardsModel

class ShadowedWidget(QWidget):
    def __init__(self, widget, parent=None):
        """Adds a shadow to the widget"""
        super().__init__(parent)
        
        # Apply the shadow effect to this widget
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(0, 3)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(Qt.gray)
        
        widget.setGraphicsEffect(shadow_effect)
        
        # Set the layout for the widget
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(widget)

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
        
        self.back_input = QTextEdit()
        self.back_input.setObjectName('card')
        self.back_input.setPlaceholderText(back_text)

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

class ScrollableGroupBox(qtw.QWidget):
    def __init__(self):
        """The container for card creation. 
        GroupBox(for title) -> ScrollArea(scroll functionality) -> GroupBox(holding) -> Cards
        """
        super().__init__()
        
        self.model = FlashCardsModel()
        
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
            
        self.idx = 0
        
        for _ in range(3): self.add_card()
        
    def add_card(self):
        card = CardWidget()
        self.main_layout.addWidget(card)
        self.model.add_Flashcard()
        modeled_idx = self.model.index(self.idx)
        card.frontChangedSignal.connect(
            lambda value, idx=modeled_idx, role=FlashCardsModel.QUESTION_ROLE: self.set_to_model(value, idx, role)
        )
        card.backChangedSignal.connect(
            lambda value, idx=modeled_idx, role=FlashCardsModel.ANSWER_ROLE: self.set_to_model(value, idx, role)
        )
        self.idx += 1
    
    def pop_card(self):
        
    
    def set_to_model(self, value, idx, role):
        self.model.setData(idx, value, role)
    
if __name__ == "__main__":
    app = QApplication([])
    widget = CardWidget()
    widget.show()
    app.exec()

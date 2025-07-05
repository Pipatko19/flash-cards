from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

from dataclasses import dataclass

@dataclass
class Card:
    front: str
    back: str
    def __repr__(self):
        return f"Card({self.front} -> {self.back})"

class CardData:
    def __init__(self, cards: list[dict]):
        self.cards = [Card(c["question"], c["answer"]) for c in cards]
        
        self.count = len(self.cards)
        self.cur_idx = 0

    def __repr__(self) -> str:
        txt = f"{self.__class__.__name__}\n"
        for i in range(self.count):
            txt += repr(self.cards[i])
        return txt
    @property
    def cur_front(self):
        """Return the current front"""
        return self.cards[self.cur_idx].front
    @property
    def cur_back(self):
        """Return the current back"""
        return self.cards[self.cur_idx].back
    
    def next(self) -> bool:
        """Go to the next card"""
        if self.cur_idx < self.count - 1:
            self.cur_idx += 1
            return True
        return False

    def prev(self) -> bool:
        """Go to the previous card"""
        if self.cur_idx > 0:
            self.cur_idx -= 1
            return True
        return False

class CardContainer(qtw.QWidget):
    def __init__(self, data: list[dict], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = CardData(data)
        
        self._init_widgets()
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.lbl_card = qtw.QLabel(self.data.cur_front, self)
        self.lbl_card.setObjectName('card')
        self.lbl_card.setMinimumSize(500, 350)
        self.lbl_card.setSizePolicy(qtw.QSizePolicy.Policy.Preferred, qtw.QSizePolicy.Policy.Expanding)
        self.lbl_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_card.setWordWrap(True)
        
        self.progress = qtw.QProgressBar(self)
        self.progress.setRange(0, self.data.count)
        self.progress.setValue(1)
        self.progress.setFormat("Card %v/%m")

    def _init_layouts(self):
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.lbl_card, 1)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress, 0)
    
    @qtc.Slot()
    def prev(self):
        """Go to the previous card"""
        success = self.data.prev()
        if success:
            self.lbl_card.setText(self.data.cur_front)
            self.progress.setValue(self.data.cur_idx + 1)
            return True
        return False
    
    @qtc.Slot()
    def next(self):
        """Go to the next card"""
        success = self.data.next()
        if success:
            self.lbl_card.setText(self.data.cur_front)
            self.progress.setValue(self.data.cur_idx + 1)
            return True
        return False
    
    @qtc.Slot()
    def flip(self):
        """Flip the card"""
        if self.lbl_card.text() == self.data.cur_front:
            self.lbl_card.setText(self.data.cur_back)
        else:
            self.lbl_card.setText(self.data.cur_front)
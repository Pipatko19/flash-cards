from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

import sys

from flashcards.widgets import ButtonGroup, ShadowedWidget
from flashcards.storage import get_set_by_id, FILENAME
from flashcards.card_set.card import CardContainer

def svg_to_pixmap(svg_path, size):
    """Convert SVG to QPixmap"""
    svg_renderer = QSvgRenderer(svg_path)
    pixmap = qtg.QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = qtg.QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    return pixmap



class FlashCards(qtw.QLabel): #it is not QWidget because of QSS formatting, as it doesn't work with QWidget
    def __init__(self, mw, id: int | None = None):
        """UI for playing the flashcards"""
        super().__init__()
        self.setObjectName('flashcards')
        self.mw = mw
        self.id = id

        self.cur_idx = 0

        self._init_widgets()
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        if self.id is None:
            data = {'title': 'Flashcards', 'flashcards': []}
        else:
            data = get_set_by_id(FILENAME, self.id)
        self.lbl_title = qtw.QLabel(data['title'])
        self.lbl_title.setObjectName('flash-title')
        self.lbl_select = qtw.QLabel('0/0') 
        
        self.card = CardContainer(data['flashcards'])
        self.shadowed = ShadowedWidget(self.card)
        
        def nav_button(icon_path: str):
            """Create a navigation button with an icon"""
            btn = qtw.QPushButton()
            btn.setObjectName('move')
            btn.setMinimumHeight(200)
            btn.setIcon(qtg.QIcon(icon_path))
            btn.setIconSize(qtc.QSize(60, 200))
            return btn

        self.btn_previous = nav_button('assets/icons/double_arrow_left.svg')
        self.btn_next = nav_button('assets/icons/double_arrow_right.svg')

        
        self.buttons = ButtonGroup(['know', 'flip', 'dont know'])
        
        self.buttons.flip.pressed.connect(self.card.flip)
        self.btn_previous.pressed.connect(self.card.prev)
        self.btn_next.pressed.connect(self.card.next)
        
    def _init_layouts(self):
        """Setting widgets to the main layout"""
        layout = qtw.QGridLayout()
        self.setLayout(layout)
        
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 0)
        spacer = qtw.QSpacerItem(20, 30, qtw.QSizePolicy.Policy.Minimum, qtw.QSizePolicy.Policy.Preferred)
        layout.addItem(spacer, 2, 0, 1, 3)
        
        layout.addWidget(self.lbl_title, 0, 0, 1, 0)
        layout.addWidget(self.lbl_select, 0, 1, Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.btn_previous, 1, 0)
        layout.addWidget(self.shadowed, 1, 1)
        layout.addWidget(self.btn_next, 1, 2)

        layout.addWidget(self.buttons, 3, 1)
        
if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    
    #style
    with open('style.qss', 'r') as f:
        _style = f.read()
    app.setStyleSheet(_style)
    
    mw = FlashCards(None, 0)
    #mw.setGeometry(qtc.QRect(0, 0, 756, 538))
    mw.show()
    sys.exit(app.exec())
        
        
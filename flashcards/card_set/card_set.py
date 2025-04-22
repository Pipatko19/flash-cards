from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flashcards.widgets import ButtonGroup, ShadowedWidget

def svg_to_pixmap(svg_path, size):
    """Convert SVG to QPixmap"""
    svg_renderer = QSvgRenderer(svg_path)
    pixmap = qtg.QPixmap(size)
    pixmap.fill(Qt.transparent)
    painter = qtg.QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    return pixmap



class FlashCards(qtw.QLabel): #it is not QWidget because of QSS formatting, as it doesn't work with QWidget
    def __init__(self, mw, id=None):
        """UI for playing the flashcards"""
        super().__init__()
        self.setGeometry(qtc.QRect(0, 0, 828, 478))
        self.setObjectName('flashcards')
        self.mw = mw

        self._init_widgets()
        
        self._init_layouts()

    def _init_widgets(self):
        """Widget creation"""
        self.lbl_title = qtw.QLabel('Placeholder')
        self.lbl_select = qtw.QLabel('0/0') 
        
        self.lbl_card = qtw.QLabel('Placeholder', self)
        self.lbl_card.setObjectName('card')
        self.lbl_card.setMinimumSize(500, 350)
        self.lbl_card.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Expanding)
        self.lbl_card.setAlignment(Qt.AlignCenter)
        self.lbl_card.setWordWrap(True)
        self.shadowed = ShadowedWidget(self.lbl_card)

        self.btn_previous = qtw.QPushButton()
        self.btn_previous.setObjectName('move')

        self.btn_previous.setMinimumHeight(200)
        self.btn_previous.setIcon(qtg.QIcon('assets/icons/double_arrow_left.svg'))
        self.btn_previous.setIconSize(qtc.QSize(60, 200)) #only width matters, idk why
        
        self.btn_next = qtw.QPushButton()
        self.btn_next.setObjectName('move')
        self.btn_next.setMinimumHeight(200)
        self.btn_next.setIcon(qtg.QIcon('assets/icons/double_arrow_right.svg'))
        self.btn_next.setIconSize(qtc.QSize(60, 200))
        
        self.buttons = ButtonGroup(['know', 'flip', 'dont know'])
    def _init_layouts(self):
        """Setting widgets to the main layout"""
        layout = qtw.QGridLayout()
        self.setLayout(layout)
        
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 0)
        spacer = qtw.QSpacerItem(20, 30, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Preferred)
        layout.addItem(spacer, 2, 0, 1, 3)
        
        layout.addWidget(self.lbl_title, 0, 0)
        layout.addWidget(self.lbl_select, 0, 1, Qt.AlignCenter)

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
    
    mw = FlashCards(None)
    #mw.setGeometry(qtc.QRect(0, 0, 756, 538))
    mw.show()
    sys.exit(app.exec())
        
        
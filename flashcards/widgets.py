
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

from typing import Collection, Generic, TypeVar

T = TypeVar('T', bound = qtw.QWidget)

class NamedField(qtw.QWidget, Generic[T]):
    def __init__(self, name: str, field: T):
        """Wraps a widget with a title

        Args:
            name (str): title of the widget
            field (QWidget): the widget that gets wrapped
        """
        super().__init__()
        layout = qtw.QVBoxLayout(self)
        self.field = field
        layout.addWidget(qtw.QLabel(name))
        layout.addWidget(field, 1)
        
class ShadowedWidget(qtw.QWidget):
    BLUR_RADIUS = 20
    COLOR = Qt.GlobalColor.gray
    
    def __init__(self, widget, parent=None, offset=(0, 0)):
        """Adds a shadow to the widget
        
        Args:
            widget (QWidget): the widget that gets wrapped
        """
        super().__init__(parent)
        
        # Apply the shadow effect to this widget
        shadow_effect = qtw.QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(*offset)
        shadow_effect.setBlurRadius(self.BLUR_RADIUS)
        shadow_effect.setColor(self.COLOR)
        
        widget.setGraphicsEffect(shadow_effect)
        
        # Set the layout for the widget
        layout = qtw.QHBoxLayout(self)
        layout.addWidget(widget)

class ButtonGroup(qtw.QWidget):
    def __init__(self, button_names: Collection[str], set_name=True):
        super().__init__()
        self.buttons = dict()
        self.set_name = set_name

        layout = qtw.QHBoxLayout()
        self.setLayout(layout)

        for name in button_names:
           self.add_button(name)

        
    def __getattribute__(self, name):
        if name == 'buttons':
            return super().__getattribute__('buttons')
        buttons = super().__getattribute__('buttons')
        if name in buttons:
            return buttons[name]
        return super().__getattribute__(name)

    def add_button(self, name):
        """Creates a new button"""
        if self.set_name:
            button = qtw.QPushButton(name, parent=self)
        else:
            button = qtw.QPushButton(parent=self)
        self.buttons[name] = button
        button.setObjectName(name)
        self.layout().addWidget(button)
        
    def setProperty(self, name, value):
        result = super().setProperty(name, value)
        for button in self.buttons.values():
            button.setProperty(name, value)
        return result
    
if __name__ == '__main__':
    app = qtw.QApplication([])
    but = ButtonGroup(['one', 'two', 'three'])
    but.add_button('new')
    print(but.buttons)

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

from typing import Collection

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
        
class ShadowedWidget(qtw.QWidget):
    def __init__(self, widget, parent=None):
        """Adds a shadow to the widget"""
        super().__init__(parent)
        
        # Apply the shadow effect to this widget
        shadow_effect = qtw.QGraphicsDropShadowEffect(self)
        shadow_effect.setOffset(0, 3)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(Qt.gray)
        
        widget.setGraphicsEffect(shadow_effect)
        
        # Set the layout for the widget
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(widget)

class ButtonGroup(qtw.QWidget):
    def __init__(self, button_names: Collection[str], set_name=True):
        super().__init__()
        self.buttons = dict()

        layout = qtw.QHBoxLayout()
        self.setLayout(layout)

        for name in button_names:
           self.add_button(name, set_name)

        
    def __getattribute__(self, name):
        if name == 'buttons':
            return super().__getattribute__('buttons')
        buttons = super().__getattribute__('buttons')
        if name in buttons:
            return buttons[name]
        return super().__getattribute__(name)

    def add_button(self, name, set_name=True):
        """Adds a button to the layout"""
        if set_name:
            button = qtw.QPushButton(name)
        else:
            button = qtw.QPushButton()
        self.buttons[name] = button
        button.setObjectName(name)
        self.layout().addWidget(button)
        
    def setProperty(self, name, value):
        super().setProperty(name, value)
        for button in self.buttons.values():
            button.setProperty(name, value)
if __name__ == '__main__':
    app = qtw.QApplication([])
    but = ButtonGroup(['one', 'two', 'three'])
    but.add_button('new')
    print(but.buttons)
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QMargins

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
    def __init__(self, front_text='Front', back_text='Back', parent=None):
        """Represents a card with a front and a back side"""
        super().__init__(parent)
        
        # Main layout
        layout = QHBoxLayout(self)
        
        margin = QMargins(20, 20, 20, 20)

        # Create QTextEdit widgets
        front_input = QTextEdit()
        front_input.setObjectName('card')
        front_input.setPlaceholderText(front_text)
        
        back_input = QTextEdit()
        back_input.setObjectName('card')
        back_input.setPlaceholderText(back_text)

        # Create ShadowedWidget containers for both front and back
        self.front_input_widget = ShadowedWidget(front_input)
        self.back_input_widget = ShadowedWidget(back_input)

        # Add ShadowedWidgets to the main layout
        layout.addWidget(self.front_input_widget, 1)
        layout.addWidget(self.back_input_widget, 1)
        
        # Adjust margins and spacing
        layout.setContentsMargins(margin)
        layout.setSpacing(40)

if __name__ == "__main__":
    app = QApplication([])
    widget = CardWidget()
    widget.show()
    app.exec()

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtGui import QPalette, QColor
import sys



class Style:
    def __init__(self, app: qtw.QApplication):
        self.app = app
        self._force_dark = None
    
    
    @property
    def dark_mode(self):
        if self._force_dark is not None:
            return self._force_dark
        if "--light" in sys.argv:
            return False
        elif "--dark" in sys.argv:
            return True
        return qtw.QApplication.styleHints().colorScheme() == qtc.Qt.ColorScheme.Dark
    
    def apply_generic_colors(self):
        """Changes generic colors"""
        self.app.setStyle('Fusion')
        palette = QPalette()
        if self.dark_mode:
            palette.setColor(QPalette.Base, QColor('#2B2B2B'))
            palette.setColor(QPalette.Text, QColor('#FFFFFF'))
            palette.setColor(QPalette.Window, QColor('#121212'))
            palette.setColor(QPalette.WindowText, QColor('#FFFFFF'))
            palette.setColor(QPalette.Button, QColor('#333333'))
            palette.setColor(QPalette.ButtonText, QColor('#FFFFFF'))
            palette.setColor(QPalette.PlaceholderText, QColor('#A0A0A0'))

        else:
            palette.setColor(QPalette.Base, QColor('#e9e9e9'))
            palette.setColor(QPalette.Text, QColor('#000000'))
            palette.setColor(QPalette.Window, QColor('#D4F3FF'))
            palette.setColor(QPalette.WindowText, QColor('#000000'))
            palette.setColor(QPalette.Button, QColor('#dcdcdc'))
            palette.setColor(QPalette.ButtonText, QColor('000000'))
            palette.setColor(QPalette.PlaceholderText, QColor('#858585'))
        self.app.setPalette(palette)
        
    def set_simple_colors(self, widget: qtw.QWidget, light_bg, light_fg, dark_bg, dark_fg):
        palette = QPalette()
        if self.dark_mode:
            palette.setColor(QPalette.Base, dark_bg)
            palette.setColor(QPalette.Text, dark_fg)
            palette.setColor(QPalette.Window, dark_bg)
            palette.setColor(QPalette.WindowText, dark_fg)
            palette.setColor(QPalette.Button, dark_bg)
            palette.setColor(QPalette.ButtonText, dark_fg)
        else:
            palette.setColor(QPalette.Base, light_bg)
            palette.setColor(QPalette.Text, light_fg)
            palette.setColor(QPalette.Window, light_bg)
            palette.setColor(QPalette.WindowText, light_fg)
            palette.setColor(QPalette.Button, light_bg)
            palette.setColor(QPalette.ButtonText, light_fg)
        widget.setPalette(palette)
    
    def toggle_theme(self):
        """Switch between dark and light mode"""
        self._force_dark = not self.dark_mode
        self.apply_generic_colors(self.app)
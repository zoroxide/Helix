"""
Output Console Widget
Displays program output, errors, and execution results with interactive input support
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal
from .themes import ThemeManager


class OutputConsole(QTextEdit):
    """Output console for displaying program results and errors with input capability"""
    
    input_submitted = pyqtSignal(str)  # Signal when user submits input
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager or ThemeManager()
        self.setReadOnly(False)  # Allow typing for interactive input
        self.input_start_pos = 0
        self.accepting_input = False
        font = QFont("Consolas", 10)
        self.setFont(font)
        
        theme = self.theme_manager.get_current_theme()
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme.ui['console_bg'].name()};
                color: {theme.ui['console_fg'].name()};
                border: none;
            }}
        """)
        
    def append_output(self, text, color="#CCCCCC"):
        """Append colored text to console"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.setTextColor(QColor(color))
        self.insertPlainText(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        self.input_start_pos = self.textCursor().position()
        
    def clear_output(self):
        """Clear console output"""
        self.clear()
        self.input_start_pos = 0
        
    def enable_input(self):
        """Enable input mode for interactive programs"""
        self.accepting_input = True
        self.input_start_pos = self.textCursor().position()
        
    def disable_input(self):
        """Disable input mode"""
        self.accepting_input = False
        
    def keyPressEvent(self, event):
        """Handle key press for input"""
        cursor = self.textCursor()
        
        # If not accepting input, prevent editing old content
        if not self.accepting_input and cursor.position() < self.input_start_pos:
            if event.key() not in (Qt.Key_Left, Qt.Key_Up, Qt.Key_Down, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                event.accept()
                return
        
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.accepting_input:
                # Get input text
                cursor.setPosition(self.input_start_pos)
                cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
                input_text = cursor.selectedText()
                
                # Move to end and add newline
                cursor.movePosition(QTextCursor.End)
                self.setTextCursor(cursor)
                self.insertPlainText('\n')
                
                # Emit signal with input
                self.input_submitted.emit(input_text + '\n')
                self.input_start_pos = self.textCursor().position()
                event.accept()
                return
        
        # Allow normal text editing
        super().keyPressEvent(event)

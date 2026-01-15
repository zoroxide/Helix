"""
Terminal Widget
Interactive terminal for running commands - type directly in the terminal!
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtCore import QProcess, Qt, QTimer
from .themes import ThemeManager


class TerminalWidget(QTextEdit):
    """Interactive terminal widget with direct input"""
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager or ThemeManager()
        self.process = None
        self.command_history = []
        self.history_index = -1
        self.prompt = "PS> "
        self.command_start_pos = 0
        self.init_ui()
        self.start_shell()
        
    def init_ui(self):
        """Initialize the terminal UI"""
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
        
        # Not read-only - allow typing directly
        self.setReadOnly(False)
        
    def start_shell(self):
        """Start a shell process"""
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        
        # Start PowerShell on Windows, bash on Unix
        import sys
        if sys.platform == 'win32':
            self.process.start('powershell.exe', ['-NoLogo', '-NoExit'])
        else:
            self.process.start('/bin/bash')
            
        self.append_text("Terminal started. Type commands directly below.\n", "#4EC9B0")
        self.show_prompt()
        
    def show_prompt(self):
        """Show command prompt"""
        self.append_text(self.prompt, "#569CD6")
        self.command_start_pos = self.textCursor().position()
        
    def append_text(self, text, color="#CCCCCC"):
        """Append colored text"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.setTextColor(QColor(color))
        self.insertPlainText(text)
        self.setTextColor(QColor("#CCCCCC"))
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
    def execute_command(self):
        """Execute the entered command"""
        command = self.input.text().strip()
        if not command:
            return
            
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Display command
        self.append_output(f"PS> {command}\n", "#569CD6")
        
        # Execute command
        if self.process and self.process.state() == QProcess.Running:
            self.process.write((command + '\n').encode())
        
        self.input.clear()
        
    def handle_stdout(self):
        """Handle standard output"""
        if self.process:
            data = self.process.readAllStandardOutput()
            text = bytes(data).decode('utf-8', errors='ignore')
            if text.strip():
                # Filter out PowerShell prompts to avoid duplication
                import re
                # Remove PS prompts like "PS C:\path>" or "PS D:\path>"
                text = re.sub(r'PS [A-Z]:[^>]*>\s*', '', text)
                if text.strip():
                    self.append_text(text, "#CCCCCC")
            
    def handle_stderr(self):
        """Handle standard error"""
        if self.process:
            data = self.process.readAllStandardError()
            text = bytes(data).decode('utf-8', errors='ignore')
            if text.strip():
                self.append_text(text, "#F48771")
            
    def process_finished(self):
        """Handle process finish"""
        self.append_text("\nProcess terminated. Restarting...\n", "#FFA500")
        self.start_shell()
        
    def keyPressEvent(self, event):
        """Handle key press events"""
        cursor = self.textCursor()
        
        # Prevent editing before the command prompt
        if cursor.position() < self.command_start_pos:
            if event.key() not in (Qt.Key_Left, Qt.Key_Up, Qt.Key_Down, Qt.Key_Right):
                cursor.setPosition(self.command_start_pos)
                self.setTextCursor(cursor)
        
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Execute command
            self.execute_command()
            event.accept()
            
        elif event.key() == Qt.Key_Backspace:
            # Prevent backspace before prompt
            if cursor.position() <= self.command_start_pos:
                event.accept()
                return
            super().keyPressEvent(event)
            
        elif event.key() == Qt.Key_Left:
            # Prevent moving left before prompt
            if cursor.position() <= self.command_start_pos:
                event.accept()
                return
            super().keyPressEvent(event)
            
        elif event.key() == Qt.Key_Home:
            # Move to start of command (after prompt)
            cursor.setPosition(self.command_start_pos)
            self.setTextCursor(cursor)
            event.accept()
            
        elif event.key() == Qt.Key_Up:
            # Previous command in history
            if self.command_history and self.history_index > 0:
                self.history_index -= 1
                self.replace_current_command(self.command_history[self.history_index])
            event.accept()
            
        elif event.key() == Qt.Key_Down:
            # Next command in history
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.replace_current_command(self.command_history[self.history_index])
            elif self.history_index >= len(self.command_history) - 1:
                self.history_index = len(self.command_history)
                self.replace_current_command("")
            event.accept()
            
        else:
            # Normal typing
            super().keyPressEvent(event)
            
    def replace_current_command(self, text):
        """Replace current command with text"""
        cursor = self.textCursor()
        cursor.setPosition(self.command_start_pos)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.insertPlainText(text)
        
    def get_current_command(self):
        """Get the current command text"""
        cursor = self.textCursor()
        cursor.setPosition(self.command_start_pos)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        return cursor.selectedText()
        
    def execute_command(self):
        """Execute the current command"""
        command = self.get_current_command().strip()
        
        if command:
            # Add to history
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            # Move cursor to end and add newline
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            self.insertPlainText('\n')
            
            # Execute command
            if self.process and self.process.state() == QProcess.Running:
                # Special commands
                if command.lower() == 'clear' or command.lower() == 'cls':
                    self.clear()
                    self.append_text("Terminal cleared.\n", "#4EC9B0")
                    self.show_prompt()
                    return
                    
                self.process.write((command + '\n').encode())
                
                # Wait for output, then show new prompt
                QTimer.singleShot(200, self.show_prompt)
        else:
            # Empty command, just show new prompt
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            self.insertPlainText('\n')
            self.show_prompt()
        
    def append_output(self, text, color="#CCCCCC"):
        """Append text to output"""
        self.output.setTextColor(QColor(color))
        self.output.insertPlainText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
        
    def clear_terminal(self):
        """Clear terminal output"""
        self.clear()
        self.append_text("Terminal cleared.\n", "#4EC9B0")
        self.show_prompt()
        
    def cleanup(self):
        """Cleanup terminal process"""
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()

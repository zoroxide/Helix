"""
Helix - Main IDE Window
Contains the main application window with all UI components
"""

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QSplitter, QAction, QFileDialog, 
                             QMessageBox, QTabWidget, QStatusBar, QLabel, QToolBar)
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QKeySequence

from .code_editor import CodeEditor
from .output_console import OutputConsole
from .file_explorer import FileExplorer
from .terminal_widget import TerminalWidget
from .themes import ThemeManager


class PythonIDE(QMainWindow):
    """Main IDE window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.process = None
        self.theme_manager = ThemeManager()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Helix - Untitled")
        self.setGeometry(100, 100, 1400, 900)
        
        # Status bar - CREATE THIS FIRST before calling new_file()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.status_label)
        
        # Central widget with tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1E1E1E;
            }
            QTabBar::tab {
                background-color: #2D2D30;
                color: #CCCCCC;
                padding: 8px 20px;
                margin-right: 2px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background-color: #3E3E42;
            }
        """)
        
        # Create first editor tab
        self.new_file()
        
        # Output console
        self.output_console = OutputConsole(theme_manager=self.theme_manager)
        self.output_console.input_submitted.connect(self.handle_console_input)
        
        # Terminal widget
        self.terminal_widget = TerminalWidget(theme_manager=self.theme_manager)
        
        # Create tab widget for output and terminal
        self.bottom_tabs = QTabWidget()
        self.bottom_tabs.addTab(self.output_console, "Output")
        self.bottom_tabs.addTab(self.terminal_widget, "Terminal")
        self.bottom_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1E1E1E;
            }
            QTabBar::tab {
                background-color: #2D2D30;
                color: #CCCCCC;
                padding: 8px 20px;
                margin-right: 2px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background-color: #3E3E42;
            }
        """)
        
        # Create splitter for editor and output/terminal
        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.vertical_splitter.addWidget(self.tabs)
        self.vertical_splitter.addWidget(self.bottom_tabs)
        self.vertical_splitter.setSizes([600, 200])
        
        # File explorer
        self.file_explorer = FileExplorer(theme_manager=self.theme_manager)
        self.file_explorer.file_opened.connect(self.open_file)
        
        # Main horizontal splitter
        self.horizontal_splitter = QSplitter(Qt.Horizontal)
        self.horizontal_splitter.addWidget(self.file_explorer)
        self.horizontal_splitter.addWidget(self.vertical_splitter)
        self.horizontal_splitter.setSizes([250, 1150])
        
        self.setCentralWidget(self.horizontal_splitter)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QMenuBar {
                background-color: #2D2D30;
                color: #CCCCCC;
                border-bottom: 1px solid #3E3E42;
            }
            QMenuBar::item:selected {
                background-color: #3E3E42;
            }
            QMenu {
                background-color: #252526;
                color: #CCCCCC;
                border: 1px solid #3E3E42;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
            QToolBar {
                background-color: #2D2D30;
                border: none;
                spacing: 3px;
                padding: 4px;
            }
            QToolButton {
                background-color: #2D2D30;
                color: #CCCCCC;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #3E3E42;
            }
            QStatusBar {
                background-color: #007ACC;
                color: #FFFFFF;
            }
            QSplitter::handle {
                background-color: #2D2D30;
            }
        """)
        
        self.show()
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New File", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        open_action = QAction("Open File...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(lambda: self.open_file())
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("Open Folder...", self)
        open_folder_action.setShortcut("Ctrl+K")
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(lambda: self.get_current_editor().undo())
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(lambda: self.get_current_editor().redo())
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(lambda: self.get_current_editor().cut())
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(lambda: self.get_current_editor().copy())
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(lambda: self.get_current_editor().paste())
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(lambda: self.get_current_editor().selectAll())
        edit_menu.addAction(select_all_action)
        
        # Run menu
        run_menu = menubar.addMenu("Run")
        
        run_action = QAction("Run Python File", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)
        
        stop_action = QAction("Stop Execution", self)
        stop_action.setShortcut("Shift+F5")
        stop_action.triggered.connect(self.stop_execution)
        run_menu.addAction(stop_action)
        
        run_menu.addSeparator()
        
        clear_output_action = QAction("Clear Output", self)
        clear_output_action.triggered.connect(self.output_console.clear_output)
        run_menu.addAction(clear_output_action)
        
        # Theme menu
        theme_menu = menubar.addMenu("Theme")
        
        for theme_name in self.theme_manager.get_theme_names():
            theme_action = QAction(theme_name, self)
            theme_action.triggered.connect(lambda checked, name=theme_name: self.change_theme(name))
            theme_menu.addAction(theme_action)
        
    def create_toolbar(self):
        """Create toolbar with icons"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(toolbar.iconSize())
        self.addToolBar(toolbar)
        
        # New file
        new_btn = QAction("📄 New", self)
        new_btn.triggered.connect(self.new_file)
        toolbar.addAction(new_btn)
        
        # Open file
        open_btn = QAction("📂 Open", self)
        open_btn.triggered.connect(lambda: self.open_file())
        toolbar.addAction(open_btn)
        
        # Save file
        save_btn = QAction("💾 Save", self)
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)
        
        toolbar.addSeparator()
        
        # Run button
        run_btn = QAction("▶️ Run (F5)", self)
        run_btn.triggered.connect(self.run_code)
        toolbar.addAction(run_btn)
        
        # Stop button
        stop_btn = QAction("⏹️ Stop", self)
        stop_btn.triggered.connect(self.stop_execution)
        toolbar.addAction(stop_btn)
        
        toolbar.addSeparator()
        
        # Clear output
        clear_btn = QAction("🗑️ Clear Output", self)
        clear_btn.triggered.connect(self.output_console.clear_output)
        toolbar.addAction(clear_btn)
        
    def get_current_editor(self):
        """Get the current active editor"""
        return self.tabs.currentWidget()
        
    def new_file(self):
        """Create a new file tab"""
        editor = CodeEditor(theme_manager=self.theme_manager)
        editor.filename = None
        index = self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentIndex(index)
        self.status_label.setText("New file created")
        
    def open_file(self, filename=None):
        """Open a file"""
        if filename is None or filename is False:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "Python Files (*.py);;All Files (*.*)"
            )
            
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check if file is already open
                for i in range(self.tabs.count()):
                    editor = self.tabs.widget(i)
                    if editor.filename == filename:
                        self.tabs.setCurrentIndex(i)
                        self.status_label.setText(f"Already open: {filename}")
                        return
                
                # Create new tab
                editor = CodeEditor(theme_manager=self.theme_manager)
                editor.setText(content)
                editor.filename = filename
                
                tab_name = os.path.basename(filename)
                index = self.tabs.addTab(editor, tab_name)
                self.tabs.setCurrentIndex(index)
                
                self.current_file = filename
                self.setWindowTitle(f"Helix - {filename}")
                self.status_label.setText(f"Opened: {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")
                
    def save_file(self):
        """Save current file"""
        editor = self.get_current_editor()
        if editor.filename:
            try:
                with open(editor.filename, 'w', encoding='utf-8') as f:
                    f.write(editor.text())
                self.status_label.setText(f"Saved: {editor.filename}")
                
                # Update tab name (remove * if it was modified)
                index = self.tabs.currentIndex()
                tab_name = os.path.basename(editor.filename)
                self.tabs.setTabText(index, tab_name)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_file_as()
            
    def save_file_as(self):
        """Save file with new name"""
        editor = self.get_current_editor()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Python Files (*.py);;All Files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(editor.text())
                    
                editor.filename = filename
                self.current_file = filename
                
                tab_name = os.path.basename(filename)
                index = self.tabs.currentIndex()
                self.tabs.setTabText(index, tab_name)
                
                self.setWindowTitle(f"Helix - {filename}")
                self.status_label.setText(f"Saved as: {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
                
    def open_folder(self):
        """Open folder in file explorer"""
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder:
            self.file_explorer.set_root_path(folder)
            self.status_label.setText(f"Opened folder: {folder}")
            
    def close_tab(self, index):
        """Close a tab"""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            # Keep at least one tab
            editor = self.tabs.widget(0)
            editor.clear()
            editor.filename = None
            self.tabs.setTabText(0, "Untitled")
            
    def run_code(self):
        """Run the current Python file"""
        editor = self.get_current_editor()
        
        # Save file first if it has a filename
        if editor.filename:
            self.save_file()
            file_to_run = editor.filename
        else:
            # Save to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(editor.text())
                file_to_run = f.name
        
        # Clear output
        self.output_console.clear_output()
        self.output_console.append_output(f"▶️ Running: {file_to_run}\n" + "="*60 + "\n", "#4EC9B0")
        
        # Create process
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        
        # Start process
        python_executable = sys.executable
        self.process.start(python_executable, [file_to_run])
        
        # Enable input in output console for interactive programs
        self.output_console.enable_input()
        
        self.status_label.setText("Running...")
        
    def handle_console_input(self, text):
        """Handle input from output console"""
        if self.process and self.process.state() == QProcess.Running:
            self.process.write(text.encode())
        
    def handle_stdout(self):
        """Handle standard output from process"""
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf-8", errors="ignore")
        self.output_console.append_output(stdout, "#CCCCCC")
        
    def handle_stderr(self):
        """Handle standard error from process"""
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf-8", errors="ignore")
        self.output_console.append_output(stderr, "#F48771")
        
    def process_finished(self, exit_code, exit_status):
        """Handle process completion"""
        self.output_console.disable_input()
        self.output_console.append_output(f"\n{'='*60}", "#4EC9B0")
        if exit_code == 0:
            self.output_console.append_output(f"✅ Process finished successfully (Exit code: {exit_code})", "#4EC9B0")
            self.status_label.setText("Execution completed successfully")
        else:
            self.output_console.append_output(f"❌ Process exited with code: {exit_code}", "#F48771")
            self.status_label.setText(f"Execution failed (Exit code: {exit_code})")
            
    def stop_execution(self):
        """Stop the running process"""
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.output_console.append_output("\n⏹️ Execution stopped by user", "#FFA500")
            self.status_label.setText("Execution stopped")
        else:
            self.status_label.setText("No process running")
    
    def change_theme(self, theme_name):
        """Change the IDE theme"""
        self.theme_manager.set_theme(theme_name)
        theme = self.theme_manager.get_current_theme()
        
        # Apply theme to all editor tabs
        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            if isinstance(editor, CodeEditor):
                editor.theme_manager = self.theme_manager
                editor.apply_theme(theme)
        
        # Apply theme to output console
        self.output_console.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme.ui['console_bg'].name()};
                color: {theme.ui['console_fg'].name()};
                border: none;
            }}
        """)
        
        # Apply theme to file explorer
        self.file_explorer.tree_view.setStyleSheet(f"""
            QTreeView {{
                background-color: {theme.ui['explorer_bg'].name()};
                color: {theme.ui['explorer_fg'].name()};
                border: none;
                outline: none;
            }}
            QTreeView::item:hover {{
                background-color: {theme.ui['explorer_hover'].name()};
            }}
            QTreeView::item:selected {{
                background-color: {theme.ui['explorer_selected'].name()};
            }}
        """)
        
        # Apply theme to tabs
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {theme.ui['tab_selected_bg'].name()};
            }}
            QTabBar::tab {{
                background-color: {theme.ui['tab_bg'].name()};
                color: {theme.ui['tab_fg'].name()};
                padding: 8px 20px;
                margin-right: 2px;
                border: none;
            }}
            QTabBar::tab:selected {{
                background-color: {theme.ui['tab_selected_bg'].name()};
                color: {theme.ui['tab_selected_fg'].name()};
            }}
            QTabBar::tab:hover {{
                background-color: {theme.ui['tab_hover'].name()};
            }}
        """)
        
        # Apply theme to bottom tabs (output/terminal)
        self.bottom_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {theme.ui['tab_selected_bg'].name()};
            }}
            QTabBar::tab {{
                background-color: {theme.ui['tab_bg'].name()};
                color: {theme.ui['tab_fg'].name()};
                padding: 8px 20px;
                margin-right: 2px;
                border: none;
            }}
            QTabBar::tab:selected {{
                background-color: {theme.ui['tab_selected_bg'].name()};
                color: {theme.ui['tab_selected_fg'].name()};
            }}
            QTabBar::tab:hover {{
                background-color: {theme.ui['tab_hover'].name()};
            }}
        """)
        
        # Apply theme to main window
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme.ui['main_bg'].name()};
            }}
            QMenuBar {{
                background-color: {theme.ui['menubar_bg'].name()};
                color: {theme.ui['menubar_fg'].name()};
                border-bottom: 1px solid {theme.ui['splitter'].name()};
            }}
            QMenuBar::item:selected {{
                background-color: {theme.ui['tab_hover'].name()};
            }}
            QMenu {{
                background-color: {theme.ui['menu_bg'].name()};
                color: {theme.ui['menubar_fg'].name()};
                border: 1px solid {theme.ui['splitter'].name()};
            }}
            QMenu::item:selected {{
                background-color: {theme.ui['menu_hover'].name()};
            }}
            QToolBar {{
                background-color: {theme.ui['toolbar_bg'].name()};
                border: none;
                spacing: 3px;
                padding: 4px;
            }}
            QToolButton {{
                background-color: {theme.ui['toolbar_bg'].name()};
                color: {theme.ui['menubar_fg'].name()};
                border: none;
                padding: 5px;
                border-radius: 3px;
            }}
            QToolButton:hover {{
                background-color: {theme.ui['tab_hover'].name()};
            }}
            QStatusBar {{
                background-color: {theme.ui['statusbar_bg'].name()};
                color: {theme.ui['statusbar_fg'].name()};
            }}
            QSplitter::handle {{
                background-color: {theme.ui['splitter'].name()};
            }}
        """)
        
        self.status_label.setText(f"Theme changed to: {theme_name}")
            
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self, "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.process and self.process.state() == QProcess.Running:
                self.process.kill()
            # Cleanup terminal
            if hasattr(self, 'terminal_widget'):
                self.terminal_widget.cleanup()
            event.accept()
        else:
            event.ignore()

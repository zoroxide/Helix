"""
File Explorer Widget
Tree view for browsing and opening files
"""

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel
from PyQt5.QtCore import pyqtSignal, QDir, Qt
from .themes import ThemeManager


class FileExplorer(QWidget):
    """File explorer tree view"""
    
    file_opened = pyqtSignal(str)
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager or ThemeManager()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the file explorer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tree view
        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        
        # Sort directories first, then files
        self.model.sort(0, Qt.AscendingOrder)
        
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.AscendingOrder)
        self.tree_view.setColumnWidth(0, 200)
        
        # Enable sorting with directories first
        self.tree_view.model().sort(0, Qt.AscendingOrder)
        
        # Hide extra columns
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)
        
        # Styling with theme
        theme = self.theme_manager.get_current_theme()
        self.tree_view.setStyleSheet(f"""
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
        
        # Double-click to open file
        self.tree_view.doubleClicked.connect(self.on_double_click)
        
        layout.addWidget(self.tree_view)
        
    def on_double_click(self, index):
        """Handle file double-click"""
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.file_opened.emit(file_path)
            
    def set_root_path(self, path):
        """Set the root path for file explorer"""
        self.model.setRootPath(path)
        self.tree_view.setRootIndex(self.model.index(path))

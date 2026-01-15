"""
Theme Manager
Handles different color themes for the IDE
"""

from PyQt5.QtGui import QColor


class Theme:
    """Base theme class"""
    
    def __init__(self, name):
        self.name = name
        self.editor = {}
        self.syntax = {}
        self.ui = {}
        
        
class DarkTheme(Theme):
    """VS Code Dark Theme (Black Editor)"""
    
    def __init__(self):
        super().__init__("Dark (Black)")
        
        # Editor colors (Black background)
        self.editor = {
            'background': QColor("#000000"),  # Pure black
            'foreground': QColor("#D4D4D4"),
            'line_numbers_bg': QColor("#0A0A0A"),
            'line_numbers_fg': QColor("#858585"),
            'current_line': QColor("#1A1A1A"),
            'caret': QColor("#FFFFFF"),
            'selection_bg': QColor("#264F78"),
            'selection_fg': QColor("#FFFFFF"),
            'matched_brace_bg': QColor("#3C3C3C"),
            'matched_brace_fg': QColor("#FFD700"),
            'edge_line': QColor("#2A2A2A"),
            'indent_guide_bg': QColor("#1A1A1A"),
            'indent_guide_fg': QColor("#404040"),
            'fold_margin': QColor("#000000"),
        }
        
        # Syntax highlighting
        self.syntax = {
            'default': QColor("#D4D4D4"),
            'keyword': QColor("#569CD6"),
            'string': QColor("#CE9178"),
            'comment': QColor("#6A9955"),
            'class': QColor("#4EC9B0"),
            'function': QColor("#DCDCAA"),
            'number': QColor("#B5CEA8"),
            'operator': QColor("#D4D4D4"),
        }
        
        # UI colors
        self.ui = {
            'main_bg': QColor("#1E1E1E"),
            'menubar_bg': QColor("#2D2D30"),
            'menubar_fg': QColor("#CCCCCC"),
            'menu_bg': QColor("#252526"),
            'menu_hover': QColor("#094771"),
            'toolbar_bg': QColor("#2D2D30"),
            'statusbar_bg': QColor("#007ACC"),
            'statusbar_fg': QColor("#FFFFFF"),
            'tab_bg': QColor("#2D2D30"),
            'tab_fg': QColor("#CCCCCC"),
            'tab_selected_bg': QColor("#1E1E1E"),
            'tab_selected_fg': QColor("#FFFFFF"),
            'tab_hover': QColor("#3E3E42"),
            'explorer_bg': QColor("#252526"),
            'explorer_fg': QColor("#CCCCCC"),
            'explorer_hover': QColor("#2A2D2E"),
            'explorer_selected': QColor("#094771"),
            'console_bg': QColor("#1E1E1E"),
            'console_fg': QColor("#CCCCCC"),
            'splitter': QColor("#2D2D30"),
        }


class LightTheme(Theme):
    """VS Code Light Theme"""
    
    def __init__(self):
        super().__init__("Light")
        
        # Editor colors
        self.editor = {
            'background': QColor("#FFFFFF"),
            'foreground': QColor("#000000"),
            'line_numbers_bg': QColor("#F5F5F5"),
            'line_numbers_fg': QColor("#237893"),
            'current_line': QColor("#F0F0F0"),
            'caret': QColor("#000000"),
            'selection_bg': QColor("#ADD6FF"),
            'selection_fg': QColor("#000000"),
            'matched_brace_bg': QColor("#D3D3D3"),
            'matched_brace_fg': QColor("#0000FF"),
            'edge_line': QColor("#E0E0E0"),
            'indent_guide_bg': QColor("#F5F5F5"),
            'indent_guide_fg': QColor("#D3D3D3"),
            'fold_margin': QColor("#FFFFFF"),
        }
        
        # Syntax highlighting
        self.syntax = {
            'default': QColor("#000000"),
            'keyword': QColor("#0000FF"),
            'string': QColor("#A31515"),
            'comment': QColor("#008000"),
            'class': QColor("#267F99"),
            'function': QColor("#795E26"),
            'number': QColor("#098658"),
            'operator': QColor("#000000"),
        }
        
        # UI colors
        self.ui = {
            'main_bg': QColor("#F3F3F3"),
            'menubar_bg': QColor("#F3F3F3"),
            'menubar_fg': QColor("#000000"),
            'menu_bg': QColor("#FFFFFF"),
            'menu_hover': QColor("#0078D7"),
            'toolbar_bg': QColor("#F3F3F3"),
            'statusbar_bg': QColor("#007ACC"),
            'statusbar_fg': QColor("#FFFFFF"),
            'tab_bg': QColor("#ECECEC"),
            'tab_fg': QColor("#000000"),
            'tab_selected_bg': QColor("#FFFFFF"),
            'tab_selected_fg': QColor("#000000"),
            'tab_hover': QColor("#E0E0E0"),
            'explorer_bg': QColor("#F3F3F3"),
            'explorer_fg': QColor("#000000"),
            'explorer_hover': QColor("#E8E8E8"),
            'explorer_selected': QColor("#0078D7"),
            'console_bg': QColor("#FFFFFF"),
            'console_fg': QColor("#000000"),
            'splitter': QColor("#CCCCCC"),
        }


class MonokaiTheme(Theme):
    """Monokai Pro Theme"""
    
    def __init__(self):
        super().__init__("Monokai")
        
        # Editor colors
        self.editor = {
            'background': QColor("#2D2A2E"),
            'foreground': QColor("#FCFCFA"),
            'line_numbers_bg': QColor("#221F22"),
            'line_numbers_fg': QColor("#5B595C"),
            'current_line': QColor("#3E3B3F"),
            'caret': QColor("#FCFCFA"),
            'selection_bg': QColor("#5B595C"),
            'selection_fg': QColor("#FCFCFA"),
            'matched_brace_bg': QColor("#5B595C"),
            'matched_brace_fg': QColor("#FFD866"),
            'edge_line': QColor("#403E41"),
            'indent_guide_bg': QColor("#2D2A2E"),
            'indent_guide_fg': QColor("#5B595C"),
            'fold_margin': QColor("#2D2A2E"),
        }
        
        # Syntax highlighting
        self.syntax = {
            'default': QColor("#FCFCFA"),
            'keyword': QColor("#FF6188"),
            'string': QColor("#FFD866"),
            'comment': QColor("#727072"),
            'class': QColor("#78DCE8"),
            'function': QColor("#A9DC76"),
            'number': QColor("#AB9DF2"),
            'operator': QColor("#FF6188"),
        }
        
        # UI colors
        self.ui = {
            'main_bg': QColor("#221F22"),
            'menubar_bg': QColor("#2D2A2E"),
            'menubar_fg': QColor("#FCFCFA"),
            'menu_bg': QColor("#2D2A2E"),
            'menu_hover': QColor("#5B595C"),
            'toolbar_bg': QColor("#2D2A2E"),
            'statusbar_bg': QColor("#FF6188"),
            'statusbar_fg': QColor("#FCFCFA"),
            'tab_bg': QColor("#221F22"),
            'tab_fg': QColor("#939293"),
            'tab_selected_bg': QColor("#2D2A2E"),
            'tab_selected_fg': QColor("#FCFCFA"),
            'tab_hover': QColor("#3E3B3F"),
            'explorer_bg': QColor("#221F22"),
            'explorer_fg': QColor("#FCFCFA"),
            'explorer_hover': QColor("#3E3B3F"),
            'explorer_selected': QColor("#5B595C"),
            'console_bg': QColor("#2D2A2E"),
            'console_fg': QColor("#FCFCFA"),
            'splitter': QColor("#403E41"),
        }


class DraculaTheme(Theme):
    """Dracula Theme"""
    
    def __init__(self):
        super().__init__("Dracula")
        
        # Editor colors
        self.editor = {
            'background': QColor("#282A36"),
            'foreground': QColor("#F8F8F2"),
            'line_numbers_bg': QColor("#1E1F29"),
            'line_numbers_fg': QColor("#6272A4"),
            'current_line': QColor("#44475A"),
            'caret': QColor("#F8F8F2"),
            'selection_bg': QColor("#44475A"),
            'selection_fg': QColor("#F8F8F2"),
            'matched_brace_bg': QColor("#6272A4"),
            'matched_brace_fg': QColor("#FFB86C"),
            'edge_line': QColor("#44475A"),
            'indent_guide_bg': QColor("#282A36"),
            'indent_guide_fg': QColor("#44475A"),
            'fold_margin': QColor("#282A36"),
        }
        
        # Syntax highlighting
        self.syntax = {
            'default': QColor("#F8F8F2"),
            'keyword': QColor("#FF79C6"),
            'string': QColor("#F1FA8C"),
            'comment': QColor("#6272A4"),
            'class': QColor("#8BE9FD"),
            'function': QColor("#50FA7B"),
            'number': QColor("#BD93F9"),
            'operator': QColor("#FF79C6"),
        }
        
        # UI colors
        self.ui = {
            'main_bg': QColor("#1E1F29"),
            'menubar_bg': QColor("#282A36"),
            'menubar_fg': QColor("#F8F8F2"),
            'menu_bg': QColor("#282A36"),
            'menu_hover': QColor("#44475A"),
            'toolbar_bg': QColor("#282A36"),
            'statusbar_bg': QColor("#BD93F9"),
            'statusbar_fg': QColor("#282A36"),
            'tab_bg': QColor("#1E1F29"),
            'tab_fg': QColor("#6272A4"),
            'tab_selected_bg': QColor("#282A36"),
            'tab_selected_fg': QColor("#F8F8F2"),
            'tab_hover': QColor("#44475A"),
            'explorer_bg': QColor("#1E1F29"),
            'explorer_fg': QColor("#F8F8F2"),
            'explorer_hover': QColor("#44475A"),
            'explorer_selected': QColor("#6272A4"),
            'console_bg': QColor("#282A36"),
            'console_fg': QColor("#F8F8F2"),
            'splitter': QColor("#44475A"),
        }


class ThemeManager:
    """Manages all available themes"""
    
    def __init__(self):
        self.themes = {
            'Dark (Black)': DarkTheme(),
            'Light': LightTheme(),
            'Monokai': MonokaiTheme(),
            'Dracula': DraculaTheme(),
        }
        self.current_theme = self.themes['Dark (Black)']
        
    def get_theme(self, name):
        """Get theme by name"""
        return self.themes.get(name, self.current_theme)
        
    def set_theme(self, name):
        """Set current theme"""
        if name in self.themes:
            self.current_theme = self.themes[name]
            return True
        return False
        
    def get_theme_names(self):
        """Get list of all theme names"""
        return list(self.themes.keys())
        
    def get_current_theme(self):
        """Get current active theme"""
        return self.current_theme

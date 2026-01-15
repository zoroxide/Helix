"""
Code Editor Widget
Advanced code editor with syntax highlighting, line numbers, and Monaco-like appearance
"""

from PyQt5.QtGui import QFont, QColor
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from .themes import ThemeManager


class CodeEditor(QsciScintilla):
    """Advanced code editor with syntax highlighting and line numbers"""
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.filename = None
        self.theme_manager = theme_manager or ThemeManager()
        self.setup_editor()
        
    def setup_editor(self):
        """Configure editor appearance and behavior"""
        theme = self.theme_manager.get_current_theme()
        
        # Font settings
        font = QFont("Consolas", 11)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setMarginsFont(font)
        
        # Background and foreground colors FIRST (before lexer)
        self.setPaper(theme.editor['background'])
        self.setColor(theme.editor['foreground'])
        
        # Python lexer for syntax highlighting
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(font)
        
        # Set default colors for ALL lexer styles
        self.lexer.setDefaultColor(theme.syntax['default'])
        self.lexer.setDefaultPaper(theme.editor['background'])
        
        # Set paper (background) color for ALL possible styles (0-127)
        for i in range(128):
            self.lexer.setPaper(theme.editor['background'], i)
            self.lexer.setFont(font, i)
        
        # Apply theme colors to specific Python syntax elements
        self.lexer.setColor(theme.syntax['default'], QsciLexerPython.Default)
        self.lexer.setColor(theme.syntax['keyword'], QsciLexerPython.Keyword)
        self.lexer.setColor(theme.syntax['string'], QsciLexerPython.DoubleQuotedString)
        self.lexer.setColor(theme.syntax['string'], QsciLexerPython.SingleQuotedString)
        self.lexer.setColor(theme.syntax['string'], QsciLexerPython.TripleDoubleQuotedString)
        self.lexer.setColor(theme.syntax['string'], QsciLexerPython.TripleSingleQuotedString)
        self.lexer.setColor(theme.syntax['comment'], QsciLexerPython.Comment)
        self.lexer.setColor(theme.syntax['comment'], QsciLexerPython.CommentBlock)
        self.lexer.setColor(theme.syntax['class'], QsciLexerPython.ClassName)
        self.lexer.setColor(theme.syntax['function'], QsciLexerPython.FunctionMethodName)
        self.lexer.setColor(theme.syntax['function'], QsciLexerPython.Decorator)
        self.lexer.setColor(theme.syntax['number'], QsciLexerPython.Number)
        self.lexer.setColor(theme.syntax['operator'], QsciLexerPython.Operator)
        self.lexer.setColor(theme.syntax['default'], QsciLexerPython.Identifier)
        self.lexer.setColor(theme.syntax['string'], QsciLexerPython.UnclosedString)
        self.lexer.setColor(theme.syntax['keyword'], QsciLexerPython.HighlightedIdentifier)
        
        # Set the lexer
        self.setLexer(self.lexer)
        
        # Line numbers margin
        fontmetrics = self.fontMetrics()
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(theme.editor['line_numbers_bg'])
        self.setMarginsForegroundColor(theme.editor['line_numbers_fg'])
        
        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(theme.editor['matched_brace_bg'])
        self.setMatchedBraceForegroundColor(theme.editor['matched_brace_fg'])
        
        # Current line highlighting
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(theme.editor['current_line'])
        self.setCaretForegroundColor(theme.editor['caret'])
        
        # Indentation
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setIndentationGuidesBackgroundColor(theme.editor['indent_guide_bg'])
        self.setIndentationGuidesForegroundColor(theme.editor['indent_guide_fg'])
        
        # Auto-completion
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(True)
        
        # Edge line (80 characters)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(theme.editor['edge_line'])
        
        # Background and foreground colors (set again after lexer)
        self.setPaper(theme.editor['background'])
        self.setColor(theme.editor['foreground'])
        
        # Ensure caret (cursor) is visible
        self.SendScintilla(QsciScintilla.SCI_SETCARETFORE, theme.editor['caret'].rgb())
        
        # Selection colors
        self.setSelectionBackgroundColor(theme.editor['selection_bg'])
        self.setSelectionForegroundColor(theme.editor['selection_fg'])
        
        # Whitespace visibility
        self.setWhitespaceVisibility(QsciScintilla.WsInvisible)
        
        # Folding
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setFoldMarginColors(theme.editor['fold_margin'], theme.editor['fold_margin'])
        
    def apply_theme(self, theme):
        """Apply a new theme to the editor"""
        # Save current content and cursor position
        content = self.text()
        line, col = self.getCursorPosition()
        
        # Reapply editor setup with new theme
        self.setup_editor()
        
        # Restore content and cursor
        self.setText(content)
        self.setCursorPosition(line, col)

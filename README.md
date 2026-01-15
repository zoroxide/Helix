# Helix - A Modern Python IDE

A feature-rich Python IDE built with PyQt5, featuring Monaco-like syntax highlighting and a modern VS Code-inspired interface.
<img width="1919" height="1055" alt="image" src="https://github.com/user-attachments/assets/d923f5fa-1809-4c34-8430-69644cce44f7" />



## Features

- **Monaco-Style Code Editor** - Beautiful syntax highlighting with QScintilla
- **File Explorer** - Tree view for easy file navigation
- **File Operations** - New, Open, Save, Save As with full support
- **Run Python Code** - Execute scripts directly with F5
- **Output Console** - Real-time output display with color-coded messages
- **Dark Theme** - VS Code-inspired dark theme
- **Multi-Tab Editor** - Work on multiple files simultaneously
- **Line Numbers** - Clear line numbering for code navigation
- **Syntax Highlighting** - Python-specific highlighting
- **Auto-Completion** - Smart code completion
- **Indentation Guides** - Visual guides for code structure
- **Brace Matching** - Highlight matching brackets
- **Keyboard Shortcuts** - Standard shortcuts (Ctrl+N, Ctrl+S, F5, etc.)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the IDE:
```bash
python main.py
```

## Project Structure

```
helix/
├── main.py                 # Entry point
├── ui/
│   ├── __init__.py        # UI package
│   ├── main_window.py     # Main IDE window
│   ├── code_editor.py     # Code editor widget
│   ├── output_console.py  # Output console widget
│   └── file_explorer.py   # File explorer widget
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

### Keyboard Shortcuts

- `Ctrl+N` - New file
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `Ctrl+Shift+S` - Save as
- `F5` - Run Python file
- `Shift+F5` - Stop execution
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+X` - Cut
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste

## Features Breakdown

### Code Editor
- Powered by QScintilla for professional code editing
- Python syntax highlighting with Monaco-like colors
- Auto-indentation and smart tab handling
- Line numbers and current line highlighting
- Code folding support
- 80-character edge line guide

### File Explorer
- Browse project files in a tree view
- Double-click to open Python files
- Folder navigation support

### Output Console
- Color-coded output (normal, error, success)
- Real-time process output display
- Clear output functionality

### Theme
- Dark theme inspired by VS Code
- Consistent color scheme across all components
- Professional and easy on the eyes

## Technical Details

- **GUI Framework**: PyQt5
- **Editor Component**: QScintilla
- **Language**: Python 3.x
- **Process Execution**: QProcess for running Python scripts

---

Built with ❤️ using Python and PyQt5

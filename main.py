"""
A Modern Code Editor for Python Development

Entry point for the application

Authors: Loay Mohamed
License: MIT
Date: 2024-06
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui import PythonIDE


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Helix")
    
    # Set application style
    app.setStyle("Fusion")
    
    ide = PythonIDE()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

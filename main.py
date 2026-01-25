#!/usr/bin/env python3
"""
Main entry point for the Stamp Collection Manager application.
"""
import sys
from PySide6.QtWidgets import QApplication

from controller import StampController


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Stamp Collection Manager")
    app.setOrganizationName("StampCollector")
    app.setApplicationVersion("1.0.0")
    
    # Create and run controller
    controller = StampController()
    controller.run()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

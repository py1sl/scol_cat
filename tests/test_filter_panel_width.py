"""
Test for filter panel width fix.
Verifies that the filter panel has adequate width for country names.
"""
import pytest
from PySide6.QtWidgets import QApplication, QGroupBox
from view import MainWindow


@pytest.fixture
def app():
    """Fixture for QApplication."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit the app, it might be used by other tests


@pytest.fixture
def main_window(app):
    """Fixture for MainWindow."""
    window = MainWindow()
    return window


def test_filter_panel_has_adequate_width(main_window):
    """Test that filter panel has adequate width (at least 400px)."""
    # Find the filter panel widget
    filter_panel = None
    for child in main_window.findChildren(QGroupBox):
        if child.title() == "Filters":
            filter_panel = child
            break
    
    assert filter_panel is not None, "Filter panel should exist"
    
    # Check that maximum width is at least 400px (doubled from original 200px)
    max_width = filter_panel.maximumWidth()
    assert max_width >= 400, f"Filter panel maximum width should be at least 400px, got {max_width}px"


def test_filter_panel_width_is_doubled(main_window):
    """Test that filter panel width is exactly 400px (double the original 200px)."""
    # Find the filter panel widget
    filter_panel = None
    for child in main_window.findChildren(QGroupBox):
        if child.title() == "Filters":
            filter_panel = child
            break
    
    assert filter_panel is not None, "Filter panel should exist"
    
    # Check that maximum width is exactly 400px
    max_width = filter_panel.maximumWidth()
    assert max_width == 400, f"Filter panel maximum width should be 400px (doubled from 200px), got {max_width}px"

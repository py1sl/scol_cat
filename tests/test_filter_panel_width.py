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


@pytest.fixture
def filter_panel(main_window):
    """Fixture to get the filter panel from the main window."""
    for child in main_window.findChildren(QGroupBox):
        if child.title() == "Filters":
            return child
    return None


def test_filter_panel_exists(filter_panel):
    """Test that filter panel exists in the main window."""
    assert filter_panel is not None, "Filter panel should exist"


def test_filter_panel_width_is_doubled(filter_panel):
    """Test that filter panel width is 400px (double the original 200px)."""
    # Check that maximum width is exactly 400px (doubled from 200px)
    max_width = filter_panel.maximumWidth()
    assert max_width == 400, f"Filter panel maximum width should be 400px (doubled from 200px), got {max_width}px"

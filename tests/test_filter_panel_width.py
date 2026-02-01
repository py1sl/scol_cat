"""
Test for filter panel width fix.
Verifies that the filter panel has adequate width for country names.
"""
import pytest
import os


def test_filter_panel_width_is_doubled():
    """Test that filter panel width is 400px (double the original 200px)."""
    # Since we can't actually import due to Qt dependencies in CI, we'll verify
    # the code structure by reading the file
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check that the filter panel maximum width is set to 400
    assert 'filter_panel.setMaximumWidth(400)' in content, \
        "Filter panel maximum width should be set to 400px (doubled from 200px)"


def test_filter_panel_exists():
    """Test that filter panel is created in the main window."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for filter panel creation
    assert 'filter_panel = QGroupBox("Filters")' in content, \
        "Filter panel should be created as a QGroupBox"
    assert 'filter_panel.setMaximumWidth' in content, \
        "Filter panel should have maximum width constraint"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

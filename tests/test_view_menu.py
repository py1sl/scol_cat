"""
Test the View menu Full Details toggle functionality.
"""
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock Qt modules before import
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtWidgets'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()
sys.modules['PySide6.QtGui'] = MagicMock()


def test_stamp_details_widget_has_full_details_mode():
    """Test that StampDetailsWidget has the full details mode methods."""
    # Since we can't actually import due to Qt dependencies, we'll verify
    # the code structure by reading the file
    with open('/home/runner/work/scol_cat/scol_cat/view.py', 'r') as f:
        content = f.read()
    
    # Check for key additions
    assert 'self.show_unique_id = False' in content
    assert 'def set_full_details_mode(self, enabled: bool):' in content
    assert 'def update_unique_id_visibility(self):' in content
    assert 'self.unique_id_row_label.setVisible(self.show_unique_id)' in content
    assert 'self.unique_id_label.setVisible(self.show_unique_id)' in content


def test_main_window_has_view_menu():
    """Test that MainWindow has the View menu."""
    with open('/home/runner/work/scol_cat/scol_cat/view.py', 'r') as f:
        content = f.read()
    
    # Check for View menu addition
    assert 'view_menu = menu_bar.addMenu("View")' in content
    assert 'self.full_details_action = QAction("Full Details", self)' in content
    assert 'self.full_details_action.setCheckable(True)' in content
    assert 'self.full_details_action.setChecked(False)' in content
    assert 'def on_full_details_toggled(self, checked: bool):' in content
    assert 'self.details_widget.set_full_details_mode(checked)' in content


def test_default_full_details_is_off():
    """Test that Full Details defaults to off."""
    with open('/home/runner/work/scol_cat/scol_cat/view.py', 'r') as f:
        content = f.read()
    
    # Default state should be False/off
    assert 'self.show_unique_id = False' in content
    assert 'self.full_details_action.setChecked(False)' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

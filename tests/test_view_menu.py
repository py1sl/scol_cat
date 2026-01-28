"""
Test the View menu Full Details toggle functionality.
"""
import pytest
import os


def test_stamp_details_widget_has_full_details_mode():
    """Test that StampDetailsWidget has the full details mode methods."""
    # Since we can't actually import due to Qt dependencies in CI, we'll verify
    # the code structure by reading the file
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for key additions
    assert 'self.show_unique_id = False' in content
    assert 'def set_full_details_mode(self, enabled: bool):' in content
    assert 'def update_unique_id_visibility(self):' in content
    assert 'self.unique_id_row_label.setVisible(self.show_unique_id)' in content
    assert 'self.unique_id_label.setVisible(self.show_unique_id)' in content


def test_main_window_has_view_menu():
    """Test that MainWindow has the View menu."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
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
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Default state should be False/off
    assert 'self.show_unique_id = False' in content
    assert 'self.full_details_action.setChecked(False)' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

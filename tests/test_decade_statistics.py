"""
Test the integration of decade statistics feature.
"""
import pytest
import os


def test_decade_statistics_dialog_exists():
    """Test that DecadeStatisticsDialog class exists in view.py."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for the DecadeStatisticsDialog class
    assert 'class DecadeStatisticsDialog(QDialog):' in content
    assert 'def __init__(self, parent=None, decade_stats: dict = None):' in content
    assert 'self.decade_stats = decade_stats or {}' in content


def test_decade_statistics_dialog_has_table():
    """Test that DecadeStatisticsDialog has table setup."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for table implementation
    assert 'table_label = QLabel("Stamps by Decade:")' in content
    assert 'self.table.setColumnCount(2)' in content
    assert 'self.table.setHorizontalHeaderLabels(["Decade", "Number of Stamps"])' in content


def test_decade_statistics_dialog_has_chart():
    """Test that DecadeStatisticsDialog has bar chart implementation."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for chart implementation
    assert 'chart_label = QLabel("Bar Chart:")' in content
    assert 'self.figure = Figure(figsize=(8, 4))' in content
    assert 'self.canvas = FigureCanvas(self.figure)' in content
    assert 'ax.bar(decades, counts' in content
    assert "ax.set_xlabel('Decade')" in content
    assert "ax.set_ylabel('Number of Stamps')" in content
    assert "ax.set_title('Stamps by Decade')" in content


def test_main_window_has_decade_statistics_signal():
    """Test that MainWindow has decade_statistics_requested signal."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for signal definition
    assert 'decade_statistics_requested = Signal()' in content


def test_main_window_has_decade_statistics_menu():
    """Test that MainWindow has Stamps by Decade menu item."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for menu item
    assert 'stamps_by_decade_action = QAction("Stamps by Decade", self)' in content
    assert 'stamps_by_decade_action.triggered.connect(self.decade_statistics_requested.emit)' in content
    assert 'statistics_menu.addAction(stamps_by_decade_action)' in content


def test_controller_imports_decade_statistics_dialog():
    """Test that Controller imports DecadeStatisticsDialog."""
    controller_file_path = os.path.join(os.path.dirname(__file__), '..', 'controller.py')
    with open(controller_file_path, 'r') as f:
        content = f.read()
    
    # Check for import
    assert 'DecadeStatisticsDialog' in content


def test_controller_connects_decade_statistics_signal():
    """Test that Controller connects the decade_statistics_requested signal."""
    controller_file_path = os.path.join(os.path.dirname(__file__), '..', 'controller.py')
    with open(controller_file_path, 'r') as f:
        content = f.read()
    
    # Check for signal connection
    assert 'self.view.decade_statistics_requested.connect(self.show_decade_statistics)' in content


def test_controller_has_show_decade_statistics_method():
    """Test that Controller has show_decade_statistics method."""
    controller_file_path = os.path.join(os.path.dirname(__file__), '..', 'controller.py')
    with open(controller_file_path, 'r') as f:
        content = f.read()
    
    # Check for method implementation
    assert 'def show_decade_statistics(self):' in content
    assert 'decade_stats = self.database.get_decade_statistics()' in content
    assert 'dialog = DecadeStatisticsDialog(self.view, decade_stats)' in content
    assert 'dialog.exec()' in content


def test_matplotlib_added_to_requirements():
    """Test that matplotlib is added to requirements.txt."""
    requirements_file_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    with open(requirements_file_path, 'r') as f:
        content = f.read()
    
    # Check for matplotlib
    assert 'matplotlib' in content


def test_matplotlib_imports_in_view():
    """Test that matplotlib is imported in view.py."""
    view_file_path = os.path.join(os.path.dirname(__file__), '..', 'view.py')
    with open(view_file_path, 'r') as f:
        content = f.read()
    
    # Check for matplotlib imports (using QtAgg backend for Qt5/Qt6 compatibility)
    assert 'import matplotlib' in content
    assert 'from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas' in content
    assert 'from matplotlib.figure import Figure' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

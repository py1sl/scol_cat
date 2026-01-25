"""
View layer for the stamp collection application.
Implements the GUI using PySide6.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QMessageBox, QDialog, QFormLayout, QListWidgetItem, QScrollArea,
    QSplitter, QGroupBox, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QAction
from typing import Optional, List
import os

from model import Stamp


class StampDialog(QDialog):
    """Dialog for adding or editing a stamp entry."""
    
    def __init__(self, parent=None, stamp: Optional[Stamp] = None):
        super().__init__(parent)
        self.stamp = stamp
        self.image_path = stamp.image_path if stamp else ""
        self.setup_ui()
        
        if stamp:
            self.load_stamp_data(stamp)
    
    def setup_ui(self):
        """Set up the dialog UI."""
        self.setWindowTitle("Add Stamp" if not self.stamp else "Edit Stamp")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Form layout for stamp fields
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        form_layout.addRow("Name:", self.name_edit)
        
        self.country_edit = QLineEdit()
        form_layout.addRow("Country:", self.country_edit)
        
        # Image selection
        image_layout = QHBoxLayout()
        self.image_label = QLabel("No image selected")
        self.image_label.setMinimumHeight(30)
        image_button = QPushButton("Browse...")
        image_button.clicked.connect(self.browse_image)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(image_button)
        form_layout.addRow("Image:", image_layout)
        
        self.dates_edit = QLineEdit()
        form_layout.addRow("Dates:", self.dates_edit)
        
        self.collection_number_edit = QLineEdit()
        form_layout.addRow("Collection Number:", self.collection_number_edit)
        
        self.catalogue_ids_edit = QLineEdit()
        form_layout.addRow("Catalogue IDs:", self.catalogue_ids_edit)
        
        self.comments_edit = QTextEdit()
        self.comments_edit.setMaximumHeight(100)
        form_layout.addRow("Comments:", self.comments_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def browse_image(self):
        """Open file dialog to select an image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Stamp Image",
            "",
            "Image Files (*.jpg *.jpeg *.png *.bmp)"
        )
        if file_path:
            self.image_path = file_path
            self.image_label.setText(os.path.basename(file_path))
    
    def load_stamp_data(self, stamp: Stamp):
        """Load stamp data into the form."""
        self.name_edit.setText(stamp.name)
        self.country_edit.setText(stamp.country)
        self.dates_edit.setText(stamp.dates)
        self.collection_number_edit.setText(stamp.collection_number)
        self.catalogue_ids_edit.setText(stamp.catalogue_ids)
        self.comments_edit.setPlainText(stamp.comments)
        
        if stamp.image_path:
            self.image_path = stamp.image_path
            self.image_label.setText(os.path.basename(stamp.image_path))
    
    def get_stamp_data(self) -> Stamp:
        """Get stamp data from the form."""
        if self.stamp:
            # Editing existing stamp
            stamp = Stamp(unique_id=self.stamp.unique_id)
        else:
            # Creating new stamp
            stamp = Stamp()
        
        stamp.name = self.name_edit.text()
        stamp.country = self.country_edit.text()
        stamp.image_path = self.image_path
        stamp.dates = self.dates_edit.text()
        stamp.collection_number = self.collection_number_edit.text()
        stamp.catalogue_ids = self.catalogue_ids_edit.text()
        stamp.comments = self.comments_edit.toPlainText()
        
        return stamp


class StampDetailsWidget(QWidget):
    """Widget to display detailed information about a stamp."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the details widget UI."""
        layout = QVBoxLayout()
        
        # Create a scroll area for the details
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMaximumHeight(300)
        self.image_label.setScaledContents(False)
        self.content_layout.addWidget(self.image_label)
        
        # Details group
        details_group = QGroupBox("Stamp Details")
        details_layout = QFormLayout()
        
        self.name_label = QLabel()
        details_layout.addRow("Name:", self.name_label)
        
        self.country_label = QLabel()
        details_layout.addRow("Country:", self.country_label)
        
        self.dates_label = QLabel()
        details_layout.addRow("Dates:", self.dates_label)
        
        self.collection_number_label = QLabel()
        details_layout.addRow("Collection Number:", self.collection_number_label)
        
        self.catalogue_ids_label = QLabel()
        details_layout.addRow("Catalogue IDs:", self.catalogue_ids_label)
        
        self.unique_id_label = QLabel()
        details_layout.addRow("Unique ID:", self.unique_id_label)
        
        self.comments_label = QLabel()
        self.comments_label.setWordWrap(True)
        details_layout.addRow("Comments:", self.comments_label)
        
        details_group.setLayout(details_layout)
        self.content_layout.addWidget(details_group)
        
        self.content_layout.addStretch()
        content_widget.setLayout(self.content_layout)
        scroll.setWidget(content_widget)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
        
        # Initially show a message
        self.clear()
    
    def display_stamp(self, stamp: Stamp):
        """Display stamp information."""
        self.name_label.setText(stamp.name or "N/A")
        self.country_label.setText(stamp.country or "N/A")
        self.dates_label.setText(stamp.dates or "N/A")
        self.collection_number_label.setText(stamp.collection_number or "N/A")
        self.catalogue_ids_label.setText(stamp.catalogue_ids or "N/A")
        self.unique_id_label.setText(stamp.unique_id)
        self.comments_label.setText(stamp.comments or "N/A")
        
        # Load and display image
        if stamp.image_path and os.path.exists(stamp.image_path):
            pixmap = QPixmap(stamp.image_path)
            if not pixmap.isNull():
                # Scale image to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    400, 300,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("Unable to load image")
        else:
            self.image_label.setText("No image available")
    
    def clear(self):
        """Clear the details display."""
        self.name_label.setText("")
        self.country_label.setText("")
        self.dates_label.setText("")
        self.collection_number_label.setText("")
        self.catalogue_ids_label.setText("")
        self.unique_id_label.setText("")
        self.comments_label.setText("")
        self.image_label.clear()
        self.image_label.setText("Select a stamp to view details")


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    stamp_selected = Signal(str)  # Emits unique_id
    add_stamp_requested = Signal()
    edit_stamp_requested = Signal(str)  # Emits unique_id
    delete_stamp_requested = Signal(str)  # Emits unique_id
    load_database_requested = Signal()
    save_database_requested = Signal()
    new_database_requested = Signal()
    country_filter_changed = Signal(str)  # Emits selected country
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main window UI."""
        self.setWindowTitle("Stamp Collection Manager")
        self.setMinimumSize(900, 600)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create splitter for list and details
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - List of stamps
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Filter section
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Country:")
        self.country_filter = QComboBox()
        self.country_filter.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.country_filter, 1)
        left_layout.addLayout(filter_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Stamp")
        add_button.clicked.connect(self.add_stamp_requested.emit)
        edit_button = QPushButton("Edit Stamp")
        edit_button.clicked.connect(self.on_edit_clicked)
        delete_button = QPushButton("Delete Stamp")
        delete_button.clicked.connect(self.on_delete_clicked)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        left_layout.addLayout(button_layout)
        
        # List widget
        self.stamp_list = QListWidget()
        self.stamp_list.itemSelectionChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.stamp_list)
        
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        
        # Right panel - Stamp details
        self.details_widget = StampDetailsWidget()
        splitter.addWidget(self.details_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 600])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        new_action = QAction("New Database", self)
        new_action.triggered.connect(self.new_database_requested.emit)
        file_menu.addAction(new_action)
        
        load_action = QAction("Load Database", self)
        load_action.triggered.connect(self.load_database_requested.emit)
        file_menu.addAction(load_action)
        
        save_action = QAction("Save Database", self)
        save_action.triggered.connect(self.save_database_requested.emit)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def on_selection_changed(self):
        """Handle stamp selection change."""
        selected_items = self.stamp_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            unique_id = item.data(Qt.UserRole)
            self.stamp_selected.emit(unique_id)
    
    def on_edit_clicked(self):
        """Handle edit button click."""
        selected_items = self.stamp_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            unique_id = item.data(Qt.UserRole)
            self.edit_stamp_requested.emit(unique_id)
    
    def on_delete_clicked(self):
        """Handle delete button click."""
        selected_items = self.stamp_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            unique_id = item.data(Qt.UserRole)
            
            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                "Are you sure you want to delete this stamp?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_stamp_requested.emit(unique_id)
    
    def update_stamp_list(self, stamps: List[Stamp]):
        """Update the list of stamps."""
        self.stamp_list.clear()
        for stamp in stamps:
            display_text = f"{stamp.name} ({stamp.country})" if stamp.country else stamp.name
            if not display_text:
                display_text = f"Stamp {stamp.unique_id[:8]}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, stamp.unique_id)
            self.stamp_list.addItem(item)
    
    def update_country_filter(self, countries: List[str]):
        """Update the country filter dropdown with available countries."""
        current_selection = self.country_filter.currentText()
        self.country_filter.clear()
        
        # Add "All Countries" as first option
        self.country_filter.addItem("All Countries")
        
        # Add unique countries
        for country in sorted(countries):
            if country:  # Only add non-empty countries
                self.country_filter.addItem(country)
        
        # Restore previous selection if it still exists
        index = self.country_filter.findText(current_selection)
        if index >= 0:
            self.country_filter.setCurrentIndex(index)
    
    def on_filter_changed(self, country: str):
        """Handle country filter change."""
        self.country_filter_changed.emit(country)
    
    def show_stamp_details(self, stamp: Stamp):
        """Show stamp details in the details panel."""
        self.details_widget.display_stamp(stamp)
    
    def clear_stamp_details(self):
        """Clear the stamp details panel."""
        self.details_widget.clear()
    
    def set_status_message(self, message: str):
        """Set status bar message."""
        self.statusBar().showMessage(message)

"""
Controller layer for the stamp collection application.
Coordinates between Model and View following MVC pattern.
"""
from PySide6.QtWidgets import QFileDialog, QMessageBox
from typing import Optional, List

from model import StampDatabase, Stamp
from view import MainWindow, StampDialog, StatisticsDialog


class StampController:
    """Controller that manages interactions between Model and View."""
    
    def __init__(self):
        self.database = StampDatabase()
        self.view = MainWindow()
        self.current_filter = "All Countries"
        
        # Connect signals from view to controller methods
        self.view.load_database_requested.connect(self.load_database)
        self.view.save_database_requested.connect(self.save_database)
        self.view.new_database_requested.connect(self.new_database)
        self.view.add_stamp_requested.connect(self.add_stamp)
        self.view.edit_stamp_requested.connect(self.edit_stamp)
        self.view.delete_stamp_requested.connect(self.delete_stamp)
        self.view.stamp_selected.connect(self.show_stamp_details)
        self.view.country_filter_changed.connect(self.on_country_filter_changed)
        self.view.statistics_requested.connect(self.show_statistics)
    
    def run(self):
        """Start the application."""
        self.view.show()
    
    def load_database(self):
        """Load a database from a JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Load Database",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            if self.database.is_modified():
                reply = QMessageBox.question(
                    self.view,
                    "Unsaved Changes",
                    "You have unsaved changes. Do you want to save before loading?",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                
                if reply == QMessageBox.Cancel:
                    return
                elif reply == QMessageBox.Yes:
                    if not self.save_database():
                        return
            
            if self.database.load(file_path):
                self.refresh_view()
                self.view.set_status_message(f"Loaded database: {file_path}")
                QMessageBox.information(
                    self.view,
                    "Success",
                    f"Database loaded successfully.\nTotal stamps: {len(self.database.stamps)}"
                )
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    "Failed to load database."
                )
    
    def save_database(self) -> bool:
        """
        Save the current database.
        
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.database.file_path:
            # No file path set, prompt for one
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Save Database",
                "stamps.json",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if not file_path:
                return False
            
            if self.database.save(file_path):
                self.view.set_status_message(f"Saved database: {file_path}")
                QMessageBox.information(
                    self.view,
                    "Success",
                    "Database saved successfully."
                )
                return True
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    "Failed to save database."
                )
                return False
        else:
            # Save to existing file path
            if self.database.save():
                self.view.set_status_message(f"Saved database: {self.database.file_path}")
                return True
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    "Failed to save database."
                )
                return False
    
    def new_database(self):
        """Create a new database."""
        if self.database.is_modified():
            reply = QMessageBox.question(
                self.view,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new database?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Cancel:
                return
            elif reply == QMessageBox.Yes:
                if not self.save_database():
                    return
        
        self.database.clear()
        self.refresh_view()
        self.view.set_status_message("New database created")
    
    def add_stamp(self):
        """Add a new stamp to the collection."""
        dialog = StampDialog(self.view)
        
        if dialog.exec():
            stamp = dialog.get_stamp_data()
            self.database.add_stamp(stamp)
            self.refresh_view()
            self.view.set_status_message("Stamp added successfully")
    
    def edit_stamp(self, unique_id: str):
        """
        Edit an existing stamp.
        
        Args:
            unique_id: ID of the stamp to edit
        """
        stamp = self.database.get_stamp(unique_id)
        if not stamp:
            QMessageBox.warning(
                self.view,
                "Error",
                "Stamp not found."
            )
            return
        
        dialog = StampDialog(self.view, stamp)
        
        if dialog.exec():
            updated_stamp = dialog.get_stamp_data()
            if self.database.update_stamp(unique_id, updated_stamp):
                self.refresh_view()
                self.view.set_status_message("Stamp updated successfully")
                # Re-select the updated stamp
                self.show_stamp_details(unique_id)
            else:
                QMessageBox.warning(
                    self.view,
                    "Error",
                    "Failed to update stamp."
                )
    
    def delete_stamp(self, unique_id: str):
        """
        Delete a stamp from the collection.
        
        Args:
            unique_id: ID of the stamp to delete
        """
        if self.database.delete_stamp(unique_id):
            self.refresh_view()
            self.view.clear_stamp_details()
            self.view.set_status_message("Stamp deleted successfully")
        else:
            QMessageBox.warning(
                self.view,
                "Error",
                "Failed to delete stamp."
            )
    
    def show_stamp_details(self, unique_id: str):
        """
        Display details of a selected stamp.
        
        Args:
            unique_id: ID of the stamp to display
        """
        stamp = self.database.get_stamp(unique_id)
        if stamp:
            self.view.show_stamp_details(stamp)
    
    def refresh_view(self):
        """Refresh the view with current database state."""
        stamps = self.database.get_all_stamps()
        
        # Update country filter options
        # Extract non-empty country values
        countries = set(
            stamp.country for stamp in stamps 
            if stamp.country is not None and stamp.country.strip()
        )
        self.view.update_country_filter(list(countries))
        
        # Apply current filter
        filtered_stamps = self.get_filtered_stamps()
        self.view.update_stamp_list(filtered_stamps)
        
        # Update window title to show database status
        title = "Stamp Collection Manager"
        if self.database.file_path:
            title += f" - {self.database.file_path}"
        if self.database.is_modified():
            title += " *"
        self.view.setWindowTitle(title)
    
    def get_filtered_stamps(self) -> List[Stamp]:
        """
        Get stamps filtered by current country filter.
        
        Returns:
            List of stamps matching the current country filter.
            Returns all stamps if filter is "All Countries".
        """
        stamps = self.database.get_all_stamps()
        
        if self.current_filter == "All Countries":
            return stamps
        
        # Filter stamps by country, handling None values
        return [
            stamp for stamp in stamps 
            if stamp.country is not None and stamp.country == self.current_filter
        ]
    
    def on_country_filter_changed(self, country: str):
        """Handle country filter change."""
        self.current_filter = country
        filtered_stamps = self.get_filtered_stamps()
        self.view.update_stamp_list(filtered_stamps)
        
        # Update status message
        if country == "All Countries":
            self.view.set_status_message(f"Showing all stamps ({len(filtered_stamps)} total)")
        else:
            self.view.set_status_message(f"Filtered by {country} ({len(filtered_stamps)} stamps)")
    
    def show_statistics(self):
        """Display statistics dialog."""
        country_stats = self.database.get_country_statistics()
        total_count = self.database.get_total_count()
        
        dialog = StatisticsDialog(self.view, country_stats, total_count)
        dialog.exec()

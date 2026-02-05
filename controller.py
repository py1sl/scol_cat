"""
Controller layer for the stamp collection application.
Coordinates between Model and View following MVC pattern.
"""
from PySide6.QtWidgets import QFileDialog, QMessageBox
from typing import Optional, List

from model import StampDatabase, Stamp, parse_date_field, get_decade_from_year, parse_decade_string
from view import MainWindow, StampDialog, StatisticsDialog, DecadeStatisticsDialog


class StampController:
    """Controller that manages interactions between Model and View."""
    
    def __init__(self):
        self.database = StampDatabase()
        self.view = MainWindow()
        self.current_filter = "All Countries"
        self.current_decade_filter = "All Decades"
        self.current_search_text = ""
        
        # Connect signals from view to controller methods
        self.view.load_database_requested.connect(self.load_database)
        self.view.save_database_requested.connect(self.save_database)
        self.view.new_database_requested.connect(self.new_database)
        self.view.add_stamp_requested.connect(self.add_stamp)
        self.view.edit_stamp_requested.connect(self.edit_stamp)
        self.view.delete_stamp_requested.connect(self.delete_stamp)
        self.view.stamp_selected.connect(self.show_stamp_details)
        self.view.country_filter_changed.connect(self.on_country_filter_changed)
        self.view.decade_filter_changed.connect(self.on_decade_filter_changed)
        self.view.search_text_changed.connect(self.on_search_text_changed)
        self.view.statistics_requested.connect(self.show_statistics)
        self.view.decade_statistics_requested.connect(self.show_decade_statistics)
    
    def run(self):
        """Start the application."""
        self.view.show()
    
    def validate_stamp_data(self, name: str, image_path: str, exclude_id: Optional[str] = None) -> Optional[str]:
        """
        Validate stamp data for uniqueness.
        
        Args:
            name: Stamp name to validate
            image_path: Image path to validate
            exclude_id: Optional ID to exclude from validation (for editing)
            
        Returns:
            Error message if validation fails, None if validation passes
        """
        # Check if name is already in use
        if name and self.database.is_name_in_use(name, exclude_id):
            return f"The name '{name}' is already in use by another stamp.\nPlease choose a different name."
        
        # Check if image path is already in use
        if image_path and self.database.is_image_path_in_use(image_path, exclude_id):
            import os
            return f"The image path '{os.path.basename(image_path)}' is already in use by another stamp.\nPlease choose a different image."
        
        return None
    
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
        dialog = StampDialog(self.view, validation_callback=self.validate_stamp_data)
        
        if dialog.exec():
            stamp = dialog.get_stamp_data()
            self.database.add_stamp(stamp)
            # Auto-save the database after adding a stamp
            if self.database.file_path:
                self.database.save()
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
        
        dialog = StampDialog(self.view, stamp, validation_callback=self.validate_stamp_data)
        
        if dialog.exec():
            updated_stamp = dialog.get_stamp_data()
            if self.database.update_stamp(unique_id, updated_stamp):
                # Auto-save the database after updating a stamp
                if self.database.file_path:
                    self.database.save()
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
        
        # Update decade filter options
        decade_stats = self.database.get_decade_statistics()
        decades = list(decade_stats.keys())
        self.view.update_decade_filter(decades)
        
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
        Get stamps filtered by current search text, country, and decade filters.
        
        Returns:
            List of stamps matching the current filters.
        """
        # Apply search filter first
        if self.current_search_text and self.current_search_text.strip():
            stamps = self.database.search_stamps(self.current_search_text)
        else:
            stamps = self.database.get_all_stamps()
        
        # Apply country filter
        if self.current_filter != "All Countries":
            stamps = [
                stamp for stamp in stamps 
                if stamp.country is not None and stamp.country == self.current_filter
            ]
        
        # Apply decade filter
        if self.current_decade_filter != "All Decades":
            filtered_by_decade = []
            filter_decade = parse_decade_string(self.current_decade_filter)
            
            for stamp in stamps:
                year = parse_date_field(stamp.dates)
                
                if filter_decade is None:
                    # "Unknown" filter - include stamps with unparseable dates
                    if year is None:
                        filtered_by_decade.append(stamp)
                else:
                    # Numeric decade filter
                    if year is not None:
                        stamp_decade = get_decade_from_year(year)
                        if stamp_decade == filter_decade:
                            filtered_by_decade.append(stamp)
            
            stamps = filtered_by_decade
        
        return stamps
    
    def on_country_filter_changed(self, country: str):
        """Handle country filter change."""
        self.current_filter = country
        self.update_filtered_view()
    
    def on_decade_filter_changed(self, decade: str):
        """Handle decade filter change."""
        self.current_decade_filter = decade
        self.update_filtered_view()
    
    def on_search_text_changed(self, text: str):
        """Handle search text change."""
        self.current_search_text = text
        self.update_filtered_view()
    
    def update_filtered_view(self):
        """Update the view with current filters applied."""
        filtered_stamps = self.get_filtered_stamps()
        self.view.update_stamp_list(filtered_stamps)
        
        # Update status message
        filters = []
        if self.current_search_text and self.current_search_text.strip():
            filters.append(f'search: "{self.current_search_text.strip()}"')
        if self.current_filter != "All Countries":
            filters.append(self.current_filter)
        if self.current_decade_filter != "All Decades":
            filters.append(self.current_decade_filter)
        
        if filters:
            filter_text = ", ".join(filters)
            self.view.set_status_message(f"Filtered by {filter_text} ({len(filtered_stamps)} stamps)")
        else:
            self.view.set_status_message(f"Showing all stamps ({len(filtered_stamps)} total)")
    
    def show_statistics(self):
        """Display statistics dialog."""
        country_stats = self.database.get_country_statistics()
        total_count = self.database.get_total_count()
        
        dialog = StatisticsDialog(self.view, country_stats, total_count)
        dialog.exec()
    
    def show_decade_statistics(self):
        """Display decade statistics dialog."""
        decade_stats = self.database.get_decade_statistics()
        
        dialog = DecadeStatisticsDialog(self.view, decade_stats)
        dialog.exec()

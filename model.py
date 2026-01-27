"""
Model layer for the stamp collection application.
Handles data management and persistence using JSON.
"""
import json
import os
import re
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union
from datetime import datetime
import uuid


def parse_date_field(date_str: str) -> Optional[int]:
    """
    Parse a date field and return a representative year.
    
    Handles:
    - Single year: "1840" -> 1840
    - Year range with dash: "1840-1850" -> 1845 (mid-year)
    - Year range with 'to': "1840 to 1850" -> 1845 (mid-year)
    - Circa dates: "circa 1840" -> 1840
    
    Args:
        date_str: The date string to parse
        
    Returns:
        The representative year, or None if parsing fails
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    # Clean up the string
    date_str = date_str.strip()
    if not date_str:
        return None
    
    # Handle circa dates - remove "circa", "c.", "ca." (case insensitive)
    circa_pattern = r'^(circa|c\.|ca\.)\s*'
    date_str = re.sub(circa_pattern, '', date_str, flags=re.IGNORECASE).strip()
    
    # Try to match year range with dash (e.g., "1840-1850")
    range_dash_pattern = r'^(\d{4})\s*-\s*(\d{4})$'
    match = re.match(range_dash_pattern, date_str)
    if match:
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        # Return mid-year
        return (start_year + end_year) // 2
    
    # Try to match year range with 'to' (e.g., "1840 to 1850")
    range_to_pattern = r'^(\d{4})\s+to\s+(\d{4})$'
    match = re.match(range_to_pattern, date_str, flags=re.IGNORECASE)
    if match:
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        # Return mid-year
        return (start_year + end_year) // 2
    
    # Try to match single year (e.g., "1840")
    single_year_pattern = r'^(\d{4})$'
    match = re.match(single_year_pattern, date_str)
    if match:
        return int(match.group(1))
    
    # Could not parse
    return None


def get_decade_from_year(year: int) -> int:
    """
    Get the decade for a given year.
    
    Args:
        year: The year
        
    Returns:
        The decade (e.g., 1840 for year 1845)
    """
    return (year // 10) * 10


@dataclass
class Stamp:
    """Represents a single stamp entry in the collection."""
    unique_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    country: str = ""
    image_path: str = ""
    dates: str = ""
    comments: str = ""
    catalogue_ids: str = ""
    collection_number: str = ""
    
    def to_dict(self) -> dict:
        """Convert stamp to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Stamp':
        """Create stamp from dictionary."""
        return cls(**data)


class StampDatabase:
    """Manages the stamp collection database using JSON."""
    
    def __init__(self):
        self.stamps: List[Stamp] = []
        self.file_path: Optional[str] = None
        self._modified = False
    
    def load(self, file_path: str) -> bool:
        """
        Load database from JSON file.
        
        Args:
            file_path: Path to the JSON database file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                # Create empty database if file doesn't exist
                self.stamps = []
                self.file_path = file_path
                self._modified = False
                return True
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.stamps = [Stamp.from_dict(stamp_data) for stamp_data in data.get('stamps', [])]
                self.file_path = file_path
                self._modified = False
                return True
        except Exception as e:
            print(f"Error loading database: {e}")
            return False
    
    def save(self, file_path: Optional[str] = None) -> bool:
        """
        Save database to JSON file.
        
        Args:
            file_path: Path to save to (uses current file_path if None)
            
        Returns:
            True if successful, False otherwise
        """
        save_path = file_path or self.file_path
        if not save_path:
            return False
        
        try:
            data = {
                'stamps': [stamp.to_dict() for stamp in self.stamps],
                'metadata': {
                    'version': '1.0',
                    'last_modified': datetime.now().isoformat()
                }
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.file_path = save_path
            self._modified = False
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def add_stamp(self, stamp: Stamp) -> None:
        """Add a new stamp to the collection."""
        self.stamps.append(stamp)
        self._modified = True
    
    def update_stamp(self, unique_id: str, updated_stamp: Stamp) -> bool:
        """
        Update an existing stamp.
        
        Args:
            unique_id: ID of the stamp to update
            updated_stamp: Updated stamp data
            
        Returns:
            True if stamp was found and updated, False otherwise
        """
        for i, stamp in enumerate(self.stamps):
            if stamp.unique_id == unique_id:
                # Preserve the original unique_id
                updated_stamp.unique_id = unique_id
                self.stamps[i] = updated_stamp
                self._modified = True
                return True
        return False
    
    def delete_stamp(self, unique_id: str) -> bool:
        """
        Delete a stamp from the collection.
        
        Args:
            unique_id: ID of the stamp to delete
            
        Returns:
            True if stamp was found and deleted, False otherwise
        """
        for i, stamp in enumerate(self.stamps):
            if stamp.unique_id == unique_id:
                del self.stamps[i]
                self._modified = True
                return True
        return False
    
    def get_stamp(self, unique_id: str) -> Optional[Stamp]:
        """
        Get a stamp by its unique ID.
        
        Args:
            unique_id: ID of the stamp to retrieve
            
        Returns:
            Stamp if found, None otherwise
        """
        for stamp in self.stamps:
            if stamp.unique_id == unique_id:
                return stamp
        return None
    
    def get_all_stamps(self) -> List[Stamp]:
        """Get all stamps in the collection."""
        return self.stamps.copy()
    
    def is_modified(self) -> bool:
        """Check if the database has unsaved changes."""
        return self._modified
    
    def clear(self) -> None:
        """Clear all stamps from the database."""
        self.stamps = []
        self.file_path = None
        self._modified = False
    
    def get_country_statistics(self) -> dict:
        """
        Get statistics on stamp counts by country.
        
        Returns:
            Dictionary mapping country names to their stamp counts.
        """
        country_counts = {}
        for stamp in self.stamps:
            country = stamp.country if stamp.country and stamp.country.strip() else "Unknown"
            country_counts[country] = country_counts.get(country, 0) + 1
        return country_counts
    
    def get_total_count(self) -> int:
        """
        Get total number of stamps in the database.
        
        Returns:
            Total stamp count.
        """
        return len(self.stamps)
    
    def get_decade_statistics(self) -> dict:
        """
        Get statistics on stamp counts by decade.
        
        parses the dates field of each stamp and groups stamps by decade.
        For year ranges, the mid-year is used to determine the decade.
        
        Returns:
            Dictionary mapping decade (e.g., "1840s") to their stamp counts.
            Stamps with unparseable dates are grouped under "Unknown".
        """
        decade_counts = {}
        for stamp in self.stamps:
            year = parse_date_field(stamp.dates)
            if year is not None:
                decade = get_decade_from_year(year)
                decade_label = f"{decade}s"
                decade_counts[decade_label] = decade_counts.get(decade_label, 0) + 1
            else:
                decade_counts["Unknown"] = decade_counts.get("Unknown", 0) + 1
        return decade_counts

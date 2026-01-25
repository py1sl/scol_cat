"""
Model layer for the stamp collection application.
Handles data management and persistence using JSON.
"""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime
import uuid


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

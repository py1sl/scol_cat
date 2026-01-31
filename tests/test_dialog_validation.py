"""Integration tests for stamp validation in the dialog."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from model import Stamp, StampDatabase


class TestDialogValidation:
    """Test validation logic that would be in the dialog."""
    
    @pytest.fixture
    def database(self):
        """Create a database with test stamps."""
        db = StampDatabase()
        db.add_stamp(Stamp(unique_id="s1", name="Stamp A", image_path="/images/a.jpg"))
        db.add_stamp(Stamp(unique_id="s2", name="Stamp B", image_path="/images/b.jpg"))
        return db
    
    def test_adding_new_stamp_with_unique_values(self, database):
        """Test adding a stamp with unique name and image path."""
        name = "New Stamp"
        image_path = "/images/new.jpg"
        
        # Both should be available
        assert not database.is_name_in_use(name)
        assert not database.is_image_path_in_use(image_path)
        
        # Adding should succeed
        new_stamp = Stamp(name=name, image_path=image_path)
        database.add_stamp(new_stamp)
        assert len(database.stamps) == 3
    
    def test_adding_new_stamp_with_duplicate_name(self, database):
        """Test validation when adding a stamp with duplicate name."""
        name = "Stamp A"  # Already exists
        image_path = "/images/new.jpg"  # Unique
        
        # Name is in use
        assert database.is_name_in_use(name)
        assert not database.is_image_path_in_use(image_path)
        
        # In the dialog, this would show a warning and not proceed
        # But the model allows it (validation is in the dialog)
    
    def test_adding_new_stamp_with_duplicate_image_path(self, database):
        """Test validation when adding a stamp with duplicate image path."""
        name = "New Stamp"  # Unique
        image_path = "/images/a.jpg"  # Already exists
        
        # Image path is in use
        assert not database.is_name_in_use(name)
        assert database.is_image_path_in_use(image_path)
    
    def test_editing_stamp_keeping_same_values(self, database):
        """Test editing a stamp without changing name or image path."""
        stamp = database.get_stamp("s1")
        name = stamp.name  # "Stamp A"
        image_path = stamp.image_path  # "/images/a.jpg"
        
        # When excluding the current stamp, should not detect as duplicate
        assert not database.is_name_in_use(name, exclude_id="s1")
        assert not database.is_image_path_in_use(image_path, exclude_id="s1")
    
    def test_editing_stamp_changing_to_duplicate_name(self, database):
        """Test editing a stamp to use another stamp's name."""
        # Editing s1 to use s2's name
        assert database.is_name_in_use("Stamp B", exclude_id="s1")
    
    def test_editing_stamp_changing_to_duplicate_image_path(self, database):
        """Test editing a stamp to use another stamp's image path."""
        # Editing s1 to use s2's image path
        assert database.is_image_path_in_use("/images/b.jpg", exclude_id="s1")
    
    def test_editing_stamp_changing_to_unique_values(self, database):
        """Test editing a stamp to use unique values."""
        # Editing s1 to use new unique values
        assert not database.is_name_in_use("New Name", exclude_id="s1")
        assert not database.is_image_path_in_use("/images/new.jpg", exclude_id="s1")
    
    def test_empty_name_not_considered_duplicate(self, database):
        """Test that empty names are not considered duplicates."""
        db = StampDatabase()
        db.add_stamp(Stamp(name="", image_path="/a.jpg"))
        db.add_stamp(Stamp(name="", image_path="/b.jpg"))
        
        # Empty names should not be flagged as duplicates
        assert not db.is_name_in_use("")
        assert not db.is_name_in_use("   ")
    
    def test_empty_image_path_not_considered_duplicate(self, database):
        """Test that empty image paths are not considered duplicates."""
        db = StampDatabase()
        db.add_stamp(Stamp(name="A", image_path=""))
        db.add_stamp(Stamp(name="B", image_path=""))
        
        # Empty paths should not be flagged as duplicates
        assert not db.is_image_path_in_use("")
        assert not db.is_image_path_in_use("   ")

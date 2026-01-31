"""Unit tests for stamp name and image path validation."""
import pytest
from model import Stamp, StampDatabase


class TestStampValidation:
    """Tests for stamp duplicate validation."""
    
    @pytest.fixture
    def database(self):
        """Create a database with some stamps for testing."""
        db = StampDatabase()
        db.add_stamp(Stamp(unique_id="s1", name="Penny Black", image_path="/path/to/penny_black.jpg"))
        db.add_stamp(Stamp(unique_id="s2", name="Blue Mauritius", image_path="/path/to/blue_mauritius.jpg"))
        db.add_stamp(Stamp(unique_id="s3", name="Inverted Jenny", image_path="/path/to/inverted_jenny.jpg"))
        return db
    
    def test_is_name_in_use_duplicate(self, database):
        """Test that is_name_in_use returns True for existing name."""
        assert database.is_name_in_use("Penny Black") is True
        assert database.is_name_in_use("Blue Mauritius") is True
    
    def test_is_name_in_use_new_name(self, database):
        """Test that is_name_in_use returns False for new name."""
        assert database.is_name_in_use("New Stamp Name") is False
        assert database.is_name_in_use("Another Stamp") is False
    
    def test_is_name_in_use_empty_name(self, database):
        """Test that is_name_in_use returns False for empty name."""
        assert database.is_name_in_use("") is False
        assert database.is_name_in_use("   ") is False
    
    def test_is_name_in_use_exclude_self(self, database):
        """Test that is_name_in_use excludes the current stamp when editing."""
        # When editing "s1", the name "Penny Black" should not be flagged as duplicate
        assert database.is_name_in_use("Penny Black", exclude_id="s1") is False
        # But it should still detect other stamps with the same name
        assert database.is_name_in_use("Blue Mauritius", exclude_id="s1") is True
    
    def test_is_image_path_in_use_duplicate(self, database):
        """Test that is_image_path_in_use returns True for existing path."""
        assert database.is_image_path_in_use("/path/to/penny_black.jpg") is True
        assert database.is_image_path_in_use("/path/to/blue_mauritius.jpg") is True
    
    def test_is_image_path_in_use_new_path(self, database):
        """Test that is_image_path_in_use returns False for new path."""
        assert database.is_image_path_in_use("/path/to/new_stamp.jpg") is False
        assert database.is_image_path_in_use("/different/path/image.jpg") is False
    
    def test_is_image_path_in_use_empty_path(self, database):
        """Test that is_image_path_in_use returns False for empty path."""
        assert database.is_image_path_in_use("") is False
        assert database.is_image_path_in_use("   ") is False
    
    def test_is_image_path_in_use_exclude_self(self, database):
        """Test that is_image_path_in_use excludes the current stamp when editing."""
        # When editing "s1", the path "/path/to/penny_black.jpg" should not be flagged
        assert database.is_image_path_in_use("/path/to/penny_black.jpg", exclude_id="s1") is False
        # But it should still detect other stamps with the same path
        assert database.is_image_path_in_use("/path/to/blue_mauritius.jpg", exclude_id="s1") is True
    
    def test_validation_case_sensitive(self, database):
        """Test that validation is case-sensitive."""
        # Different case should not be considered duplicate
        assert database.is_name_in_use("penny black") is False
        assert database.is_name_in_use("PENNY BLACK") is False
    
    def test_validation_with_whitespace(self, database):
        """Test that validation handles whitespace correctly."""
        # Names with extra whitespace should be treated as different
        assert database.is_name_in_use(" Penny Black") is False
        assert database.is_name_in_use("Penny Black ") is False
    
    def test_multiple_stamps_same_name_different_ids(self):
        """Test detection when multiple stamps have the same name."""
        db = StampDatabase()
        db.add_stamp(Stamp(unique_id="s1", name="Test", image_path="/a.jpg"))
        db.add_stamp(Stamp(unique_id="s2", name="Test", image_path="/b.jpg"))
        
        # Should detect duplicate regardless of which one we're checking
        assert db.is_name_in_use("Test") is True
        # When editing s1, should still detect s2 has the same name
        assert db.is_name_in_use("Test", exclude_id="s1") is True
        # When editing s2, should still detect s1 has the same name
        assert db.is_name_in_use("Test", exclude_id="s2") is True
    
    def test_add_stamp_with_duplicate_name(self, database):
        """Test adding a stamp with a duplicate name (should be allowed by model)."""
        # The model allows duplicates, validation happens in the dialog
        new_stamp = Stamp(name="Penny Black", image_path="/new/path.jpg")
        database.add_stamp(new_stamp)
        
        # Both stamps exist
        assert len([s for s in database.stamps if s.name == "Penny Black"]) == 2
    
    def test_update_stamp_keep_same_name(self, database):
        """Test that updating a stamp with its own name should work."""
        stamp = database.get_stamp("s1")
        assert stamp.name == "Penny Black"
        
        # Should be able to keep the same name when editing
        assert database.is_name_in_use("Penny Black", exclude_id="s1") is False

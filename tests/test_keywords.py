"""Unit tests for keywords field in Stamp model."""
import pytest
from model import Stamp, StampDatabase
import tempfile
import os


class TestKeywordsField:
    """Tests for keywords field in Stamp."""
    
    def test_stamp_has_keywords_field(self):
        """Test that Stamp has a keywords field with default empty string."""
        stamp = Stamp()
        assert hasattr(stamp, 'keywords')
        assert stamp.keywords == ""
    
    def test_stamp_creation_with_keywords(self):
        """Test creating a stamp with keywords."""
        stamp = Stamp(
            name="Test Stamp",
            country="Test Country",
            keywords="airmail, vintage, rare"
        )
        assert stamp.keywords == "airmail, vintage, rare"
    
    def test_stamp_to_dict_includes_keywords(self):
        """Test that to_dict includes keywords field."""
        stamp = Stamp(
            name="Test Stamp",
            keywords="test, sample, demo"
        )
        stamp_dict = stamp.to_dict()
        assert "keywords" in stamp_dict
        assert stamp_dict["keywords"] == "test, sample, demo"
    
    def test_stamp_from_dict_includes_keywords(self):
        """Test that from_dict properly loads keywords field."""
        stamp_dict = {
            "unique_id": "test-123",
            "name": "Test Stamp",
            "country": "Test Country",
            "image_path": "/test/path.jpg",
            "dates": "2020",
            "comments": "Test comments",
            "catalogue_ids": "CAT123",
            "collection_number": "001",
            "keywords": "historical, important"
        }
        stamp = Stamp.from_dict(stamp_dict)
        assert stamp.keywords == "historical, important"
    
    def test_stamp_from_dict_without_keywords(self):
        """Test that from_dict handles missing keywords field (backwards compatibility)."""
        stamp_dict = {
            "unique_id": "test-123",
            "name": "Test Stamp",
            "country": "Test Country",
            "image_path": "/test/path.jpg",
            "dates": "2020",
            "comments": "Test comments",
            "catalogue_ids": "CAT123",
            "collection_number": "001"
        }
        # This should not raise an error, keywords should default to empty string
        stamp = Stamp.from_dict(stamp_dict)
        assert stamp.keywords == ""
    
    def test_keywords_persistence_in_database(self):
        """Test that keywords are persisted when saving to and loading from database."""
        # Create a database with a stamp that has keywords
        db = StampDatabase()
        stamp1 = Stamp(
            name="Penny Black",
            country="United Kingdom",
            keywords="first, adhesive, postage"
        )
        stamp2 = Stamp(
            name="Blue Mauritius",
            country="Mauritius",
            keywords="rare, valuable, blue"
        )
        db.add_stamp(stamp1)
        db.add_stamp(stamp2)
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            db.save(temp_file)
            
            # Load from the file into a new database
            new_db = StampDatabase()
            new_db.load(temp_file)
            
            # Verify keywords are preserved
            loaded_stamps = new_db.get_all_stamps()
            assert len(loaded_stamps) == 2
            
            penny_black = next(s for s in loaded_stamps if s.name == "Penny Black")
            assert penny_black.keywords == "first, adhesive, postage"
            
            blue_mauritius = next(s for s in loaded_stamps if s.name == "Blue Mauritius")
            assert blue_mauritius.keywords == "rare, valuable, blue"
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_update_stamp_keywords(self):
        """Test updating a stamp's keywords."""
        db = StampDatabase()
        stamp = Stamp(
            unique_id="test-123",
            name="Test Stamp",
            keywords="old, keywords"
        )
        db.add_stamp(stamp)
        
        # Update the keywords
        stamp.keywords = "new, updated, keywords"
        db.update_stamp(stamp.unique_id, stamp)
        
        # Verify the update
        updated_stamp = db.get_stamp("test-123")
        assert updated_stamp.keywords == "new, updated, keywords"
    
    def test_empty_keywords(self):
        """Test that empty keywords work correctly."""
        stamp = Stamp(name="Test", keywords="")
        assert stamp.keywords == ""
        
        db = StampDatabase()
        db.add_stamp(stamp)
        retrieved = db.get_stamp(stamp.unique_id)
        assert retrieved.keywords == ""
    
    def test_keywords_with_special_characters(self):
        """Test that keywords with special characters are handled correctly."""
        stamp = Stamp(
            name="Test",
            keywords="vintage, 1940's, World War II, rare & valuable"
        )
        
        db = StampDatabase()
        db.add_stamp(stamp)
        
        # Save and load
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            db.save(temp_file)
            new_db = StampDatabase()
            new_db.load(temp_file)
            
            loaded_stamp = new_db.get_stamp(stamp.unique_id)
            assert loaded_stamp.keywords == "vintage, 1940's, World War II, rare & valuable"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

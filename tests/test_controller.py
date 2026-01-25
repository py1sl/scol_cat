"""Unit tests for the controller module - business logic only."""
import pytest
import os
from unittest.mock import Mock, MagicMock, patch
from model import Stamp, StampDatabase


class TestControllerBusinessLogic:
    """Tests for the controller business logic without Qt dependencies."""
    
    @pytest.fixture
    def sample_stamps(self):
        """Create sample stamps for testing."""
        return [
            Stamp(unique_id="s1", name="Stamp1", country="USA"),
            Stamp(unique_id="s2", name="Stamp2", country="UK"),
            Stamp(unique_id="s3", name="Stamp3", country="USA"),
        ]
    
    def test_filter_all_countries(self, sample_stamps):
        """Test filtering with 'All Countries' returns all stamps."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        # Simulate get_filtered_stamps logic
        filter_value = "All Countries"
        if filter_value == "All Countries":
            filtered = db.get_all_stamps()
        else:
            filtered = [s for s in db.get_all_stamps() if s.country == filter_value]
        
        assert len(filtered) == 3
    
    def test_filter_specific_country(self, sample_stamps):
        """Test filtering by specific country."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        # Simulate get_filtered_stamps logic for USA
        filter_value = "USA"
        filtered = [s for s in db.get_all_stamps() if s.country == filter_value]
        
        assert len(filtered) == 2
        assert all(s.country == "USA" for s in filtered)
    
    def test_filter_with_none_country(self):
        """Test filtering handles None country values."""
        db = StampDatabase()
        db.add_stamp(Stamp(name="S1", country="USA"))
        db.add_stamp(Stamp(name="S2", country=None))
        db.add_stamp(Stamp(name="S3", country=""))
        
        # Simulate filtering logic that handles None
        filter_value = "USA"
        filtered = [
            s for s in db.get_all_stamps() 
            if s.country is not None and s.country == filter_value
        ]
        
        assert len(filtered) == 1
        assert filtered[0].name == "S1"
    
    def test_extract_unique_countries(self, sample_stamps):
        """Test extracting unique country values."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        db.add_stamp(Stamp(name="S4", country=""))
        db.add_stamp(Stamp(name="S5", country=None))
        
        # Simulate country extraction logic
        countries = set(
            stamp.country for stamp in db.get_all_stamps()
            if stamp.country is not None and stamp.country.strip()
        )
        
        assert countries == {"USA", "UK"}
    
    def test_database_modified_after_operations(self):
        """Test database modification tracking."""
        db = StampDatabase()
        
        assert not db.is_modified()
        
        stamp = Stamp(name="Test")
        db.add_stamp(stamp)
        assert db.is_modified()
        
        db._modified = False  # Simulate after save
        db.update_stamp(stamp.unique_id, stamp)
        assert db.is_modified()
        
        db._modified = False
        db.delete_stamp(stamp.unique_id)
        assert db.is_modified()


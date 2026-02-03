"""Unit tests for search functionality."""
import pytest
from model import Stamp, StampDatabase


class TestSearchStamps:
    """Tests for search functionality in the StampDatabase."""
    
    @pytest.fixture
    def sample_stamps(self):
        """Create sample stamps with various text fields for testing."""
        return [
            Stamp(
                unique_id="s1",
                name="Penny Black",
                country="United Kingdom",
                dates="1840",
                keywords="first, adhesive, postage",
                comments="The world's first adhesive postage stamp"
            ),
            Stamp(
                unique_id="s2",
                name="Blue Mauritius",
                country="Mauritius",
                dates="1847",
                keywords="rare, valuable, blue",
                comments="One of the rarest stamps in the world"
            ),
            Stamp(
                unique_id="s3",
                name="Inverted Jenny",
                country="USA",
                dates="1918",
                collection_number="001",
                keywords="aviation, error, famous",
                comments="Famous for its inverted airplane print"
            ),
            Stamp(
                unique_id="s4",
                name="Red Penny",
                country="United Kingdom",
                dates="1841",
                catalogue_ids="SG8",
                comments="Red variant"
            ),
            Stamp(
                unique_id="s5",
                name="Canadian Maple",
                country="Canada",
                dates="1851",
                keywords="nature, maple",
                comments="Features the iconic maple leaf"
            ),
        ]
    
    def test_search_by_name_case_insensitive(self, sample_stamps):
        """Test searching by name (case insensitive)."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        # Search for "penny" (case insensitive)
        results = db.search_stamps("penny")
        assert len(results) == 2
        assert all(stamp.unique_id in ["s1", "s4"] for stamp in results)
        
        # Search for "PENNY" (uppercase)
        results = db.search_stamps("PENNY")
        assert len(results) == 2
        
        # Search for "PeNnY" (mixed case)
        results = db.search_stamps("PeNnY")
        assert len(results) == 2
    
    def test_search_by_country(self, sample_stamps):
        """Test searching by country name."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("united kingdom")
        assert len(results) == 2
        assert all(stamp.unique_id in ["s1", "s4"] for stamp in results)
        
        results = db.search_stamps("mauritius")
        assert len(results) == 1
        assert results[0].unique_id == "s2"
    
    def test_search_by_keywords(self, sample_stamps):
        """Test searching by keywords field."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("rare")
        assert len(results) == 1
        assert results[0].unique_id == "s2"
        
        results = db.search_stamps("famous")
        assert len(results) == 1
        assert results[0].unique_id == "s3"
    
    def test_search_by_comments(self, sample_stamps):
        """Test searching in comments field."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("world")
        assert len(results) == 2
        assert all(stamp.unique_id in ["s1", "s2"] for stamp in results)
        
        results = db.search_stamps("airplane")
        assert len(results) == 1
        assert results[0].unique_id == "s3"
    
    def test_search_by_dates(self, sample_stamps):
        """Test searching in dates field."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("1840")
        assert len(results) == 1
        assert results[0].unique_id == "s1"
    
    def test_search_by_collection_number(self, sample_stamps):
        """Test searching by collection number."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("001")
        assert len(results) == 1
        assert results[0].unique_id == "s3"
    
    def test_search_by_catalogue_ids(self, sample_stamps):
        """Test searching by catalogue IDs."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("SG8")
        assert len(results) == 1
        assert results[0].unique_id == "s4"
    
    def test_search_empty_string_returns_all(self, sample_stamps):
        """Test that empty search returns all stamps."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("")
        assert len(results) == 5
        
        results = db.search_stamps("   ")
        assert len(results) == 5
    
    def test_search_no_matches(self, sample_stamps):
        """Test searching for text that doesn't match anything."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("zzzzzz")
        assert len(results) == 0
        
        results = db.search_stamps("nonexistent")
        assert len(results) == 0
    
    def test_search_partial_match(self, sample_stamps):
        """Test that partial matches work."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        # "black" should match "Penny Black"
        results = db.search_stamps("black")
        assert len(results) == 1
        assert results[0].unique_id == "s1"
        
        # "avi" should match "aviation" in keywords
        results = db.search_stamps("avi")
        assert len(results) == 1
        assert results[0].unique_id == "s3"
    
    def test_search_with_whitespace(self, sample_stamps):
        """Test search with leading/trailing whitespace."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        results = db.search_stamps("  penny  ")
        assert len(results) == 2
    
    def test_search_case_insensitive_all_fields(self, sample_stamps):
        """Test case insensitivity works across all fields."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        # Test uppercase search across different fields
        results_upper = db.search_stamps("RARE")
        results_lower = db.search_stamps("rare")
        assert len(results_upper) == len(results_lower)
        
        results_upper = db.search_stamps("UNITED KINGDOM")
        results_lower = db.search_stamps("united kingdom")
        assert len(results_upper) == len(results_lower)
    
    def test_search_empty_database(self):
        """Test searching in an empty database."""
        db = StampDatabase()
        results = db.search_stamps("anything")
        assert len(results) == 0
    
    def test_search_returns_stamp_once(self, sample_stamps):
        """Test that a stamp is returned only once even if search matches multiple fields."""
        db = StampDatabase()
        # Create a stamp with "blue" in multiple fields
        stamp = Stamp(
            unique_id="s1",
            name="Blue Stamp",
            country="Blue Country",
            keywords="blue, sky",
            comments="A blue colored stamp"
        )
        db.add_stamp(stamp)
        
        results = db.search_stamps("blue")
        assert len(results) == 1
        assert results[0].unique_id == "s1"
    
    def test_search_special_characters(self):
        """Test searching with special characters."""
        db = StampDatabase()
        stamp = Stamp(
            name="Test & Sample",
            comments="Special chars: @#$%"
        )
        db.add_stamp(stamp)
        
        results = db.search_stamps("&")
        assert len(results) == 1
        
        results = db.search_stamps("@")
        assert len(results) == 1
    
    def test_search_numeric_strings(self, sample_stamps):
        """Test searching for numeric strings."""
        db = StampDatabase()
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        # Search for years
        results = db.search_stamps("1918")
        assert len(results) == 1
        assert results[0].unique_id == "s3"

"""Unit tests for filtering functionality including country and decade filters."""
import pytest
from model import Stamp, StampDatabase


class TestDecadeFiltering:
    """Tests for decade filtering logic."""
    
    @pytest.fixture
    def sample_stamps_with_dates(self):
        """Create sample stamps with various dates for testing."""
        return [
            Stamp(unique_id="s1", name="Stamp1", country="USA", dates="1840"),
            Stamp(unique_id="s2", name="Stamp2", country="UK", dates="1845"),
            Stamp(unique_id="s3", name="Stamp3", country="USA", dates="1850-1860"),
            Stamp(unique_id="s4", name="Stamp4", country="Canada", dates="1860"),
            Stamp(unique_id="s5", name="Stamp5", country="France", dates="unknown"),
            Stamp(unique_id="s6", name="Stamp6", country="Germany", dates="circa 1870"),
        ]
    
    def test_filter_by_decade_1840s(self, sample_stamps_with_dates):
        """Test filtering by 1840s decade."""
        from model import parse_date_field, get_decade_from_year
        
        db = StampDatabase()
        for stamp in sample_stamps_with_dates:
            db.add_stamp(stamp)
        
        # Filter for 1840s
        filter_decade = 1840
        filtered = []
        for stamp in db.get_all_stamps():
            year = parse_date_field(stamp.dates)
            if year is not None:
                stamp_decade = get_decade_from_year(year)
                if stamp_decade == filter_decade:
                    filtered.append(stamp)
        
        assert len(filtered) == 2
        assert all(stamp.unique_id in ["s1", "s2"] for stamp in filtered)
    
    def test_filter_by_decade_1850s(self, sample_stamps_with_dates):
        """Test filtering by 1850s decade - includes range that spans into 1850s."""
        from model import parse_date_field, get_decade_from_year
        
        db = StampDatabase()
        for stamp in sample_stamps_with_dates:
            db.add_stamp(stamp)
        
        # Filter for 1850s (stamp with range "1850-1860" should match as midpoint is 1855)
        filter_decade = 1850
        filtered = []
        for stamp in db.get_all_stamps():
            year = parse_date_field(stamp.dates)
            if year is not None:
                stamp_decade = get_decade_from_year(year)
                if stamp_decade == filter_decade:
                    filtered.append(stamp)
        
        assert len(filtered) == 1
        assert filtered[0].unique_id == "s3"
    
    def test_filter_by_decade_unknown(self, sample_stamps_with_dates):
        """Test filtering for stamps with unknown/unparseable dates."""
        from model import parse_date_field
        
        db = StampDatabase()
        for stamp in sample_stamps_with_dates:
            db.add_stamp(stamp)
        
        # Filter for Unknown
        filtered = []
        for stamp in db.get_all_stamps():
            year = parse_date_field(stamp.dates)
            if year is None:
                filtered.append(stamp)
        
        assert len(filtered) == 1
        assert filtered[0].unique_id == "s5"
    
    def test_filter_by_decade_with_circa(self, sample_stamps_with_dates):
        """Test that circa dates are properly filtered."""
        from model import parse_date_field, get_decade_from_year
        
        db = StampDatabase()
        for stamp in sample_stamps_with_dates:
            db.add_stamp(stamp)
        
        # Filter for 1870s
        filter_decade = 1870
        filtered = []
        for stamp in db.get_all_stamps():
            year = parse_date_field(stamp.dates)
            if year is not None:
                stamp_decade = get_decade_from_year(year)
                if stamp_decade == filter_decade:
                    filtered.append(stamp)
        
        assert len(filtered) == 1
        assert filtered[0].unique_id == "s6"
    
    def test_combined_country_and_decade_filter(self, sample_stamps_with_dates):
        """Test combining country and decade filters."""
        from model import parse_date_field, get_decade_from_year
        
        db = StampDatabase()
        for stamp in sample_stamps_with_dates:
            db.add_stamp(stamp)
        
        # Filter for USA and 1840s
        country_filter = "USA"
        decade_filter = 1840
        
        filtered = []
        for stamp in db.get_all_stamps():
            # Apply country filter
            if stamp.country != country_filter:
                continue
            # Apply decade filter
            year = parse_date_field(stamp.dates)
            if year is not None:
                stamp_decade = get_decade_from_year(year)
                if stamp_decade == decade_filter:
                    filtered.append(stamp)
        
        assert len(filtered) == 1
        assert filtered[0].unique_id == "s1"
    
    def test_decade_filter_with_empty_dates(self):
        """Test that stamps with empty dates are treated as Unknown."""
        from model import parse_date_field
        
        db = StampDatabase()
        db.add_stamp(Stamp(name="S1", country="USA", dates=""))
        db.add_stamp(Stamp(name="S2", country="USA", dates="1840"))
        
        # Empty dates should be parsed as None (Unknown)
        filtered = []
        for stamp in db.get_all_stamps():
            year = parse_date_field(stamp.dates)
            if year is None:
                filtered.append(stamp)
        
        assert len(filtered) == 1
        assert filtered[0].name == "S1"


class TestFilterViewIntegration:
    """Tests for filter view updates."""
    
    def test_decade_statistics_provides_filter_options(self):
        """Test that decade statistics can be used to populate filter options."""
        db = StampDatabase()
        db.add_stamp(Stamp(name="S1", dates="1840"))
        db.add_stamp(Stamp(name="S2", dates="1850"))
        db.add_stamp(Stamp(name="S3", dates="1860"))
        db.add_stamp(Stamp(name="S4", dates="unknown"))
        
        decade_stats = db.get_decade_statistics()
        decades = list(decade_stats.keys())
        
        # Should have 3 decades plus Unknown
        assert len(decades) == 4
        assert "1840s" in decades
        assert "1850s" in decades
        assert "1860s" in decades
        assert "Unknown" in decades
    
    def test_empty_database_has_no_decades(self):
        """Test that empty database returns empty decade statistics."""
        db = StampDatabase()
        decade_stats = db.get_decade_statistics()
        
        assert len(decade_stats) == 0

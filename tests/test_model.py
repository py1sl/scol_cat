"""Unit tests for the model module."""
import json
import os
import tempfile
import pytest
from model import Stamp, StampDatabase, parse_date_field, get_decade_from_year, parse_decade_string


class TestDateParsing:
    """Tests for date parsing functions."""
    
    def test_parse_single_year(self):
        """Test parsing a single year."""
        assert parse_date_field("1840") == 1840
        assert parse_date_field("1999") == 1999
        assert parse_date_field("2024") == 2024
    
    def test_parse_year_range_with_dash(self):
        """Test parsing year ranges with dash."""
        assert parse_date_field("1840-1850") == 1845
        assert parse_date_field("1990-2000") == 1995
        assert parse_date_field("2010-2020") == 2015
        # Test with spaces
        assert parse_date_field("1840 - 1850") == 1845
        assert parse_date_field("1840- 1850") == 1845
        assert parse_date_field("1840 -1850") == 1845
    
    def test_parse_year_range_with_to(self):
        """Test parsing year ranges with 'to'."""
        assert parse_date_field("1840 to 1850") == 1845
        assert parse_date_field("1990 to 2000") == 1995
        # Test case insensitivity
        assert parse_date_field("1840 TO 1850") == 1845
        assert parse_date_field("1840 To 1850") == 1845
    
    def test_parse_circa_dates(self):
        """Test parsing circa dates."""
        assert parse_date_field("circa 1840") == 1840
        assert parse_date_field("c. 1840") == 1840
        assert parse_date_field("ca. 1840") == 1840
        # Test case insensitivity
        assert parse_date_field("CIRCA 1840") == 1840
        assert parse_date_field("Circa 1840") == 1840
        assert parse_date_field("C. 1840") == 1840
    
    def test_parse_invalid_dates(self):
        """Test parsing invalid or unparseable dates."""
        assert parse_date_field("") is None
        assert parse_date_field("   ") is None
        assert parse_date_field("invalid") is None
        assert parse_date_field("12345") is None
        assert parse_date_field("abc-def") is None
        assert parse_date_field(None) is None
    
    def test_parse_edge_cases(self):
        """Test edge cases for date parsing."""
        # Leading/trailing whitespace
        assert parse_date_field("  1840  ") == 1840
        assert parse_date_field("  1840-1850  ") == 1845
        assert parse_date_field("  circa 1840  ") == 1840
    
    def test_get_decade_from_year(self):
        """Test getting decade from year."""
        assert get_decade_from_year(1840) == 1840
        assert get_decade_from_year(1845) == 1840
        assert get_decade_from_year(1849) == 1840
        assert get_decade_from_year(1850) == 1850
        assert get_decade_from_year(1999) == 1990
        assert get_decade_from_year(2000) == 2000
        assert get_decade_from_year(2024) == 2020
    
    def test_parse_decade_string(self):
        """Test parsing decade strings."""
        assert parse_decade_string("1840s") == 1840
        assert parse_decade_string("1850s") == 1850
        assert parse_decade_string("1990s") == 1990
        assert parse_decade_string("2020s") == 2020
        
        # Without 's' suffix
        assert parse_decade_string("1840") == 1840
        
        # Unknown should return None
        assert parse_decade_string("Unknown") is None
        
        # Invalid strings should return None
        assert parse_decade_string("invalid") is None
        assert parse_decade_string("") is None


class TestStamp:
    """Tests for the Stamp dataclass."""
    
    def test_stamp_creation_with_defaults(self):
        """Test creating a stamp with default values."""
        stamp = Stamp()
        assert stamp.unique_id != ""  # Should have auto-generated UUID
        assert stamp.name == ""
        assert stamp.country == ""
        assert stamp.image_path == ""
        assert stamp.dates == ""
        assert stamp.comments == ""
        assert stamp.catalogue_ids == ""
        assert stamp.collection_number == ""
    
    def test_stamp_creation_with_values(self):
        """Test creating a stamp with specific values."""
        stamp = Stamp(
            unique_id="test-123",
            name="Penny Black",
            country="United Kingdom",
            dates="1840",
            collection_number="001"
        )
        assert stamp.unique_id == "test-123"
        assert stamp.name == "Penny Black"
        assert stamp.country == "United Kingdom"
        assert stamp.dates == "1840"
        assert stamp.collection_number == "001"
    
    def test_stamp_to_dict(self):
        """Test converting stamp to dictionary."""
        stamp = Stamp(
            unique_id="test-456",
            name="Test Stamp",
            country="Test Country"
        )
        stamp_dict = stamp.to_dict()
        
        assert isinstance(stamp_dict, dict)
        assert stamp_dict['unique_id'] == "test-456"
        assert stamp_dict['name'] == "Test Stamp"
        assert stamp_dict['country'] == "Test Country"
        assert 'image_path' in stamp_dict
        assert 'dates' in stamp_dict
    
    def test_stamp_from_dict(self):
        """Test creating stamp from dictionary."""
        data = {
            'unique_id': 'from-dict-001',
            'name': 'Dict Stamp',
            'country': 'Dict Country',
            'image_path': '/path/to/image.jpg',
            'dates': '2024',
            'comments': 'Test comments',
            'catalogue_ids': 'SG:123',
            'collection_number': '042'
        }
        stamp = Stamp.from_dict(data)
        
        assert stamp.unique_id == 'from-dict-001'
        assert stamp.name == 'Dict Stamp'
        assert stamp.country == 'Dict Country'
        assert stamp.image_path == '/path/to/image.jpg'
        assert stamp.dates == '2024'
        assert stamp.comments == 'Test comments'
        assert stamp.catalogue_ids == 'SG:123'
        assert stamp.collection_number == '042'
    
    def test_unique_id_auto_generation(self):
        """Test that unique IDs are automatically generated and unique."""
        stamp1 = Stamp()
        stamp2 = Stamp()
        
        assert stamp1.unique_id != ""
        assert stamp2.unique_id != ""
        assert stamp1.unique_id != stamp2.unique_id


class TestStampDatabase:
    """Tests for the StampDatabase class."""
    
    @pytest.fixture
    def db(self):
        """Create a fresh database for each test."""
        return StampDatabase()
    
    @pytest.fixture
    def temp_json_file(self):
        """Create a temporary JSON file for testing."""
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)
    
    @pytest.fixture
    def sample_stamps(self):
        """Create sample stamps for testing."""
        return [
            Stamp(
                unique_id="stamp-001",
                name="Penny Black",
                country="United Kingdom",
                dates="1840"
            ),
            Stamp(
                unique_id="stamp-002",
                name="Blue Mauritius",
                country="Mauritius",
                dates="1847"
            )
        ]
    
    def test_database_initialization(self, db):
        """Test database is initialized empty."""
        assert len(db.stamps) == 0
        assert db.file_path is None
        assert not db.is_modified()
    
    def test_add_stamp(self, db):
        """Test adding a stamp to the database."""
        stamp = Stamp(name="Test Stamp", country="Test Country")
        db.add_stamp(stamp)
        
        assert len(db.stamps) == 1
        assert db.stamps[0].name == "Test Stamp"
        assert db.is_modified()
    
    def test_add_multiple_stamps(self, db, sample_stamps):
        """Test adding multiple stamps."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        assert len(db.stamps) == 2
        assert db.stamps[0].name == "Penny Black"
        assert db.stamps[1].name == "Blue Mauritius"
    
    def test_get_stamp(self, db, sample_stamps):
        """Test retrieving a stamp by ID."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        stamp = db.get_stamp("stamp-001")
        assert stamp is not None
        assert stamp.name == "Penny Black"
        
        stamp = db.get_stamp("stamp-002")
        assert stamp is not None
        assert stamp.name == "Blue Mauritius"
    
    def test_get_stamp_not_found(self, db):
        """Test retrieving a non-existent stamp."""
        stamp = db.get_stamp("non-existent")
        assert stamp is None
    
    def test_get_all_stamps(self, db, sample_stamps):
        """Test getting all stamps."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        all_stamps = db.get_all_stamps()
        assert len(all_stamps) == 2
        assert all_stamps[0].name == "Penny Black"
        assert all_stamps[1].name == "Blue Mauritius"
        
        # Verify it returns a copy, not the original list
        all_stamps.clear()
        assert len(db.stamps) == 2
    
    def test_update_stamp(self, db, sample_stamps):
        """Test updating an existing stamp."""
        db.add_stamp(sample_stamps[0])
        
        updated_stamp = Stamp(
            unique_id="different-id",  # This should be overwritten
            name="Updated Penny Black",
            country="UK",
            dates="1840-1841"
        )
        
        result = db.update_stamp("stamp-001", updated_stamp)
        
        assert result is True
        assert db.stamps[0].unique_id == "stamp-001"  # ID preserved
        assert db.stamps[0].name == "Updated Penny Black"
        assert db.stamps[0].country == "UK"
        assert db.is_modified()
    
    def test_update_stamp_not_found(self, db):
        """Test updating a non-existent stamp."""
        stamp = Stamp(name="Test")
        result = db.update_stamp("non-existent", stamp)
        assert result is False
    
    def test_delete_stamp(self, db, sample_stamps):
        """Test deleting a stamp."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        result = db.delete_stamp("stamp-001")
        
        assert result is True
        assert len(db.stamps) == 1
        assert db.stamps[0].unique_id == "stamp-002"
        assert db.is_modified()
    
    def test_delete_stamp_not_found(self, db):
        """Test deleting a non-existent stamp."""
        result = db.delete_stamp("non-existent")
        assert result is False
    
    def test_clear(self, db, sample_stamps):
        """Test clearing the database."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        db.file_path = "test.json"
        db.clear()
        
        assert len(db.stamps) == 0
        assert db.file_path is None
        assert not db.is_modified()
    
    def test_save_new_file(self, db, temp_json_file, sample_stamps):
        """Test saving database to a new file."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        
        result = db.save(temp_json_file)
        
        assert result is True
        assert db.file_path == temp_json_file
        assert not db.is_modified()
        assert os.path.exists(temp_json_file)
        
        # Verify file contents
        with open(temp_json_file, 'r') as f:
            data = json.load(f)
        
        assert 'stamps' in data
        assert 'metadata' in data
        assert len(data['stamps']) == 2
        assert data['stamps'][0]['name'] == "Penny Black"
    
    def test_save_without_file_path(self, db):
        """Test saving without a file path returns False."""
        db.add_stamp(Stamp(name="Test"))
        result = db.save()
        assert result is False
    
    def test_save_existing_file(self, db, temp_json_file, sample_stamps):
        """Test saving to existing file path."""
        db.add_stamp(sample_stamps[0])
        db.save(temp_json_file)
        
        # Add another stamp and save
        db.add_stamp(sample_stamps[1])
        result = db.save()
        
        assert result is True
        assert not db.is_modified()
        
        # Verify updated contents
        with open(temp_json_file, 'r') as f:
            data = json.load(f)
        assert len(data['stamps']) == 2
    
    def test_load_non_existent_file(self, db, tmp_path):
        """Test loading a non-existent file creates empty database."""
        non_existent_path = tmp_path / "test_nonexistent_file.json"
        
        result = db.load(str(non_existent_path))
        
        assert result is True
        assert len(db.stamps) == 0
        assert db.file_path == str(non_existent_path)
        assert not db.is_modified()
    
    def test_load_existing_file(self, db, temp_json_file, sample_stamps):
        """Test loading an existing database file."""
        # First save some stamps
        db1 = StampDatabase()
        for stamp in sample_stamps:
            db1.add_stamp(stamp)
        db1.save(temp_json_file)
        
        # Load into new database
        db2 = StampDatabase()
        result = db2.load(temp_json_file)
        
        assert result is True
        assert len(db2.stamps) == 2
        assert db2.stamps[0].name == "Penny Black"
        assert db2.stamps[1].name == "Blue Mauritius"
        assert db2.file_path == temp_json_file
        assert not db2.is_modified()
    
    def test_load_invalid_json(self, db, temp_json_file):
        """Test loading an invalid JSON file."""
        # Write invalid JSON
        with open(temp_json_file, 'w') as f:
            f.write("invalid json {{{")
        
        result = db.load(temp_json_file)
        assert result is False
    
    def test_is_modified_flag(self, db, sample_stamps):
        """Test the modified flag is properly managed."""
        assert not db.is_modified()
        
        db.add_stamp(sample_stamps[0])
        assert db.is_modified()
        
        # Clear should reset modified flag
        db.clear()
        assert not db.is_modified()
        
        db.add_stamp(sample_stamps[0])
        db.add_stamp(sample_stamps[1])
        assert db.is_modified()
        
        db.update_stamp("stamp-001", sample_stamps[0])
        assert db.is_modified()
        
        db.delete_stamp("stamp-001")
        assert db.is_modified()
    
    def test_save_preserves_metadata(self, db, temp_json_file, sample_stamps):
        """Test that saving includes metadata."""
        for stamp in sample_stamps:
            db.add_stamp(stamp)
        db.save(temp_json_file)
        
        with open(temp_json_file, 'r') as f:
            data = json.load(f)
        
        assert 'metadata' in data
        assert 'version' in data['metadata']
        assert 'last_modified' in data['metadata']
        assert data['metadata']['version'] == '1.0'
    
    def test_get_country_statistics_empty(self, db):
        """Test getting country statistics from empty database."""
        stats = db.get_country_statistics()
        assert stats == {}
    
    def test_get_country_statistics(self, db):
        """Test getting country statistics."""
        stamps = [
            Stamp(name="Stamp 1", country="United Kingdom"),
            Stamp(name="Stamp 2", country="United Kingdom"),
            Stamp(name="Stamp 3", country="France"),
            Stamp(name="Stamp 4", country="Germany"),
            Stamp(name="Stamp 5", country="France"),
        ]
        for stamp in stamps:
            db.add_stamp(stamp)
        
        stats = db.get_country_statistics()
        
        assert len(stats) == 3
        assert stats["United Kingdom"] == 2
        assert stats["France"] == 2
        assert stats["Germany"] == 1
    
    def test_get_country_statistics_with_empty_country(self, db):
        """Test country statistics with empty country names."""
        stamps = [
            Stamp(name="Stamp 1", country="France"),
            Stamp(name="Stamp 2", country=""),
            Stamp(name="Stamp 3", country="   "),
            Stamp(name="Stamp 4", country="France"),
        ]
        for stamp in stamps:
            db.add_stamp(stamp)
        
        stats = db.get_country_statistics()
        
        assert stats["France"] == 2
        assert stats["Unknown"] == 2
    
    def test_get_total_count(self, db, sample_stamps):
        """Test getting total stamp count."""
        assert db.get_total_count() == 0
        
        db.add_stamp(sample_stamps[0])
        assert db.get_total_count() == 1
        
        db.add_stamp(sample_stamps[1])
        assert db.get_total_count() == 2
        
        db.delete_stamp("stamp-001")
        assert db.get_total_count() == 1
    
    def test_get_decade_statistics_empty(self, db):
        """Test getting decade statistics from empty database."""
        stats = db.get_decade_statistics()
        assert stats == {}
    
    def test_get_decade_statistics(self, db):
        """Test getting decade statistics."""
        stamps = [
            Stamp(name="Stamp 1", dates="1840"),
            Stamp(name="Stamp 2", dates="1845"),
            Stamp(name="Stamp 3", dates="1850"),
            Stamp(name="Stamp 4", dates="1990-2000"),  # Mid-year 1995
            Stamp(name="Stamp 5", dates="circa 1845"),
            Stamp(name="Stamp 6", dates="2020 to 2024"),  # Mid-year 2022
        ]
        for stamp in stamps:
            db.add_stamp(stamp)
        
        stats = db.get_decade_statistics()
        
        assert stats["1840s"] == 3  # 1840, 1845, circa 1845
        assert stats["1850s"] == 1  # 1850
        assert stats["1990s"] == 1  # 1995 (mid-year of 1990-2000)
        assert stats["2020s"] == 1  # 2022 (mid-year of 2020-2024)
    
    def test_get_decade_statistics_with_invalid_dates(self, db):
        """Test decade statistics with invalid or unparseable dates."""
        stamps = [
            Stamp(name="Stamp 1", dates="1840"),
            Stamp(name="Stamp 2", dates=""),
            Stamp(name="Stamp 3", dates="invalid date"),
            Stamp(name="Stamp 4", dates="1845"),
        ]
        for stamp in stamps:
            db.add_stamp(stamp)
        
        stats = db.get_decade_statistics()
        
        assert stats["1840s"] == 2
        assert stats["Unknown"] == 2
    
    def test_get_decade_statistics_various_formats(self, db):
        """Test decade statistics with various date formats."""
        stamps = [
            Stamp(name="Single year", dates="1920"),
            Stamp(name="Range with dash", dates="1920-1930"),  # 1925
            Stamp(name="Range with to", dates="1920 to 1930"),  # 1925
            Stamp(name="Circa", dates="circa 1922"),
            Stamp(name="Another single", dates="1925"),
        ]
        for stamp in stamps:
            db.add_stamp(stamp)
        
        stats = db.get_decade_statistics()
        
        # All should be in 1920s
        assert stats["1920s"] == 5
        assert len(stats) == 1  # Only one decade

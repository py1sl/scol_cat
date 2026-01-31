"""Unit tests for data loading functions."""
import os
import json
import tempfile
import pytest
import pandas as pd
from model import load_country_names, load_british_empire_commonwealth


class TestCountryNamesLoading:
    """Tests for loading country names data."""
    
    def test_load_country_names_default_path(self):
        """Test loading country names from default path."""
        df = load_country_names()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert 'current_name' in df.columns
        assert 'previous_name' in df.columns
        assert 'year_range' in df.columns
    
    def test_load_country_names_content(self):
        """Test that loaded country names have expected content."""
        df = load_country_names()
        # Check that we have some expected entries
        assert len(df) > 0
        # Check that Germany-related entries exist
        germany_entries = df[df['current_name'] == 'Germany']
        assert len(germany_entries) > 0
        # Verify at least one Germany entry has expected previous names
        previous_names = germany_entries['previous_name'].tolist()
        assert any('German' in name or 'Prussia' in name for name in previous_names)
    
    def test_load_country_names_custom_path(self):
        """Test loading country names from custom path."""
        # Create a temporary file with test data
        test_data = [
            {
                "current_name": "Test Country A",
                "previous_name": "Old Country A",
                "year_range": "1900-1950"
            },
            {
                "current_name": "Test Country B",
                "previous_name": "Old Country B",
                "year_range": "1840-1900"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(test_data, f)
            temp_path = f.name
        
        try:
            df = load_country_names(temp_path)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert df.iloc[0]['current_name'] == 'Test Country A'
            assert df.iloc[1]['current_name'] == 'Test Country B'
        finally:
            os.unlink(temp_path)
    
    def test_load_country_names_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_country_names('/nonexistent/path/to/file.json')
    
    def test_load_country_names_invalid_json(self):
        """Test that JSONDecodeError is raised for invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write("{ invalid json content }")
            temp_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                load_country_names(temp_path)
        finally:
            os.unlink(temp_path)


class TestBritishEmpireCommonwealthLoading:
    """Tests for loading British Empire and Commonwealth countries."""
    
    def test_load_british_empire_commonwealth_default_path(self):
        """Test loading British Empire/Commonwealth list from default path."""
        countries = load_british_empire_commonwealth()
        assert isinstance(countries, list)
        assert len(countries) > 0
        assert all(isinstance(country, str) for country in countries)
    
    def test_load_british_empire_commonwealth_content(self):
        """Test that loaded list has expected content."""
        countries = load_british_empire_commonwealth()
        # Check for some expected Commonwealth countries
        assert 'United Kingdom' in countries
        assert 'Canada' in countries
        assert 'Australia' in countries
        assert 'India' in countries
        assert 'New Zealand' in countries
    
    def test_load_british_empire_commonwealth_custom_path(self):
        """Test loading British Empire/Commonwealth list from custom path."""
        # Create a temporary file with test data
        test_data = ['Country A', 'Country B', 'Country C']
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(test_data, f)
            temp_path = f.name
        
        try:
            countries = load_british_empire_commonwealth(temp_path)
            assert isinstance(countries, list)
            assert len(countries) == 3
            assert countries == test_data
        finally:
            os.unlink(temp_path)
    
    def test_load_british_empire_commonwealth_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_british_empire_commonwealth('/nonexistent/path/to/file.json')
    
    def test_load_british_empire_commonwealth_invalid_json(self):
        """Test that JSONDecodeError is raised for invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write("{ invalid json content }")
            temp_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                load_british_empire_commonwealth(temp_path)
        finally:
            os.unlink(temp_path)

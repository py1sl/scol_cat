# Data Loading Functions

The `model.py` module provides functions to load historical country data and British Empire/Commonwealth information.

## Functions

### `load_country_names(file_path=None)`

Loads country name history data from a JSON file into a pandas DataFrame.

**Parameters:**
- `file_path` (str, optional): Path to the country_names.json file. If None, uses the default path `data/country_names.json`.

**Returns:**
- `pd.DataFrame`: A DataFrame with columns:
  - `current_name`: Current name of the country
  - `previous_name`: Historical name of the country
  - `year_range`: Year range when the previous name was in use (e.g., "1840-1947")

**Example:**
```python
from model import load_country_names

# Load using default path
df = load_country_names()
print(df.head())

# Load from custom path
df = load_country_names('/path/to/custom/country_names.json')
```

### `load_british_empire_commonwealth(file_path=None)`

Loads the list of British Empire and Commonwealth countries from a JSON file.

**Parameters:**
- `file_path` (str, optional): Path to the british_empire_commonwealth.json file. If None, uses the default path `data/british_empire_commonwealth.json`.

**Returns:**
- `list`: A list of country names (strings)

**Example:**
```python
from model import load_british_empire_commonwealth

# Load using default path
countries = load_british_empire_commonwealth()
print(f"Number of countries: {len(countries)}")
print(countries[:5])  # First 5 countries

# Load from custom path
countries = load_british_empire_commonwealth('/path/to/custom/countries.json')
```

## Data Files

### `data/country_names.json`

Contains historical country name changes going back to 1840. Each entry includes:
- Current country name
- Previous name
- Year range when the previous name was used

Example entry:
```json
{
  "current_name": "Germany",
  "previous_name": "West Germany",
  "year_range": "1949-1990"
}
```

### `data/british_empire_commonwealth.json`

Contains a list of countries that are or were part of the British Empire and Commonwealth.

Example:
```json
[
  "United Kingdom",
  "Canada",
  "Australia",
  "India",
  ...
]
```

## Use Cases

These functions can be used for:

1. **Historical stamp cataloging**: Match historical country names to current names
2. **Commonwealth filtering**: Identify stamps from British Empire/Commonwealth countries
3. **Data analysis**: Analyze stamp collections by historical and modern country boundaries
4. **Reference lookup**: Quickly find what a country was called in different time periods

## Example: Finding Historical Names

```python
from model import load_country_names

# Load data
df = load_country_names()

# Find all historical names for Germany
germany_history = df[df['current_name'] == 'Germany']
print(germany_history)

# Find what countries existed before 1900
df_parsed = df.copy()
df_parsed['start_year'] = df_parsed['year_range'].str.split('-').str[0].astype(int)
pre_1900 = df_parsed[df_parsed['start_year'] < 1900]
print(pre_1900)
```

## Example: Checking if a Country is in the Commonwealth

```python
from model import load_british_empire_commonwealth

countries = load_british_empire_commonwealth()

def is_commonwealth(country_name):
    return country_name in countries

print(is_commonwealth("Canada"))  # True
print(is_commonwealth("France"))  # False
```

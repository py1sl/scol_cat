# scol_cat - Stamp Collection Manager

A digital record of stamp collection with a PySide6 GUI interface.

## Features

- **Load and Save Database**: Manage your stamp collection using JSON files
- **View Entries**: Browse through your stamp collection with an intuitive list view
- **Filter by Country**: Filter the stamp list by country of origin
- **Add New Entries**: Add new stamps with detailed information
- **Edit Entries**: Update existing stamp information
- **Delete Entries**: Remove stamps from your collection
- **Image Support**: Attach JPEG/PNG images to each stamp

## Stamp Entry Fields

Each stamp entry includes:
- **Image**: JPEG/PNG image of the stamp
- **Name**: Name or description of the stamp
- **Country**: Country of origin
- **Dates**: Issue dates or period
- **Collection Number**: Your personal collection number
- **Catalogue IDs**: ID numbers from other stamp catalogues
- **Comments**: Additional notes or comments
- **Unique ID**: Automatically generated unique identifier

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/py1sl/scol_cat.git
   cd scol_cat
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Getting Started

1. **Create a New Database**: File → New Database
2. **Load Existing Database**: File → Load Database (select a .json file)
   - Try loading the included `example_stamps.json` to see sample data
3. **Filter Stamps**: Use the "Filter by Country" dropdown to view stamps from a specific country
4. **Add a Stamp**: Click "Add Stamp" button and fill in the details
5. **View Stamp Details**: Click on a stamp in the list to view full details
6. **Edit a Stamp**: Select a stamp and click "Edit Stamp"
7. **Delete a Stamp**: Select a stamp and click "Delete Stamp"
8. **Save Your Work**: File → Save Database

## Database Format

The application uses JSON format for data storage, which is suitable for collections of up to a few thousand entries. The database file contains:
- List of stamp entries with all their details
- Metadata including version and last modification time

## Architecture

The application follows the **Model-View-Controller (MVC)** pattern:
- **Model** (`model.py`): Data management and persistence
- **View** (`view.py`): PySide6 GUI components
- **Controller** (`controller.py`): Business logic and coordination

## Documentation

Additional documentation is available in the [`docs/`](docs/) folder:
- [Data Loading Functions](docs/DATA_LOADING.md) - Information about loading country data
- [Testing Guide](docs/TESTING.md) - How to run tests and view coverage
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md) - Details about recent feature implementations

## Screenshots

**Main Window (Empty)**
![Main Window](https://github.com/user-attachments/assets/6ea24e5d-0f93-4f02-94e5-42f4d0ace2da)

**Main Window (With Sample Data)**
![With Data](https://github.com/user-attachments/assets/736882d9-ccd9-4a07-987d-d3d6941dd257)

**Add/Edit Dialog**
![Edit Dialog](https://github.com/user-attachments/assets/229986e7-a4c2-4351-b790-01adc203ef24)

## License

This is a hobby project.

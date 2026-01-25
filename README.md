# scol_cat - Stamp Collection Manager

A digital record of stamp collection with a PySide6 GUI interface.

## Features

- **Load and Save Database**: Manage your stamp collection using JSON files
- **View Entries**: Browse through your stamp collection with an intuitive list view
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
3. **Add a Stamp**: Click "Add Stamp" button and fill in the details
4. **View Stamp Details**: Click on a stamp in the list to view full details
5. **Edit a Stamp**: Select a stamp and click "Edit Stamp"
6. **Delete a Stamp**: Select a stamp and click "Delete Stamp"
7. **Save Your Work**: File → Save Database

## Database Format

The application uses JSON format for data storage, which is suitable for collections of up to a few thousand entries. The database file contains:
- List of stamp entries with all their details
- Metadata including version and last modification time

## Architecture

The application follows the **Model-View-Controller (MVC)** pattern:
- **Model** (`model.py`): Data management and persistence
- **View** (`view.py`): PySide6 GUI components
- **Controller** (`controller.py`): Business logic and coordination

## License

This is a hobby project.

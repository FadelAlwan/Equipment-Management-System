# IT Equipment Manager

A desktop application to track and manage company IT assets.
Built as an internship project.

## Features
- Add, edit, and delete equipment records
- Search and filter across all fields
- Track device status, department, and assigned user
- Dashboard with live statistics
- Export data to Excel with formatting
- Dark modern UI

## Technologies
- Python 3.10+
- CustomTkinter (GUI)
- SQLite (Database)
- Pandas + OpenPyXL (Excel Export)

## Installation

### Option A — Run the .exe (Windows)
1. Download `IT Equipment Manager.exe` from [Releases]
2. Run it — no installation needed
3. `equipment.db` is created automatically next to the .exe

### Option B — Run from source
```bash
git clone https://github.com/FadelAlwan/Equipment-Management-System
cd Equipment-Management-System
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Project Structure
it-asset-manager/

├── main.py              # Entry point
├── theme.py             # Color theme
├── database/
│   ├── db_setup.py      # Database creation
│   └── db_manager.py    # CRUD operations
├── gui/
│   ├── main_window.py   # Main window
│   ├── add_asset_form.py
│   └── edit_asset_form.py
└── utils/

## Screenshots

## License
MIT License
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
1. Download **IT Equipment Manager.exe** from [Releases](../../releases).
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

## Screenshots

## Limitations

- **Windows only** — the application is built with CustomTkinter which is
  optimized for Windows. Mac and Linux are not officially supported.
- **Single user** — the database is a local SQLite file, so it is designed for one
  person at a time. There is no multi-user or network sync support.
- **No authentication** — there is no login system or user roles. Anyone with access
  to the machine can use the app.
- **No automatic backups** — the `equipment.db` file must be backed up manually.
  If the file is deleted, all data is lost.
- **No internet connection** — the app works fully offline. There is no cloud sync
  or remote access.
- **Excel export only** — data can be exported to `.xlsx` but not PDF or CSV.

## Future Improvements

- [ ] **Login system** — username and password with Admin and Viewer roles
- [ ] **Audit log** — track who added, edited, or deleted a record and when
- [ ] **Multi-user support** — migrate from SQLite to PostgreSQL for shared access
  over a network
- [ ] **Web version** — rebuild using Flask or Django so the system can be accessed
  from any browser
- [ ] **Email alerts** — notify IT staff when a device warranty is about to expire
- [ ] **PDF export** — generate a formatted PDF report in addition to Excel
- [ ] **Dark/Light theme toggle** — let the user switch between themes from settings
- [ ] **Bulk import** — import equipment records from an existing Excel file
- [ ] **Asset history** — track changes made to each equipment record over time
- [ ] **Mac and Linux support** — test and fix compatibility across platforms

## License
MIT License

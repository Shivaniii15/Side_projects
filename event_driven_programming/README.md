# File Monitor & Dashboard

A Python automation tool that watches a folder for new files, automatically renames and moves them, logs every action to a SQLite database, and sends desktop notifications — plus a Streamlit dashboard to visualize the activity.

## What it does

**`file_monitor.py`**
1. Watches a folder (`Downloads/incoming` by default) using `watchdog`
2. When a new `.pdf` or `.csv` file appears, it:
   - Renames it with a timestamp prefix (e.g. `09-04-26_14-30-22_report.pdf`)
   - Moves it to a destination folder (e.g. a OneDrive folder)
   - Logs the original name, new name, file type, destination, and timestamp to a SQLite database
   - Sends a desktop notification confirming the file was processed
3. Runs continuously in the background until stopped (Ctrl+C)

**`dashboard.py`**
- A Streamlit web dashboard that reads from the same SQLite database
- Shows total files processed, breakdown by file type (PDF vs CSV), a recent-files table, and a bar chart of file type counts

## How the two pieces connect

Both scripts point at the same database file (`file_monitor_log.db`, stored in the user's home folder). `file_monitor.py` **writes** to it every time a file is processed; `dashboard.py` only **reads** from it to display activity — they can run independently, and the dashboard will simply reflect whatever the monitor has logged so far.

## Database schema

**`file_log`** — one row per file processed

| column | type | description |
|---|---|---|
| id | INTEGER PRIMARY KEY | auto-incrementing row id |
| original_name | TEXT | filename as it was first detected |
| new_name | TEXT | filename after timestamp prefix was added |
| file_type | TEXT | file extension (`.pdf`, `.csv`) |
| moved_to | TEXT | full destination path |
| processed_at | TEXT | timestamp the file was processed |

## Setup

```
pip install watchdog plyer streamlit pandas
```

Update these constants at the top of `file_monitor.py` if needed:
- `WATCH_FOLDER` — the folder to monitor for new files
- `DESTINATION_FOLDER` — where processed files get moved to
- `WATCHED_EXTENSIONS` — which file types to react to (default: `.pdf`, `.csv`)

## Running it

**Start the file monitor** (run this first, leave it running in the background):
```
python file_monitor.py
```
Press `Ctrl+C` to stop it gracefully.

**View logged activity as plain text** (optional, without the dashboard):
```python
from file_monitor import print_log
print_log()
```

**Launch the dashboard**:
```
streamlit run dashboard.py
```
This opens a browser tab showing live stats from the database.

## Logging

All monitor activity (files detected, moved, errors, database writes) is logged to `file_monitor.log` in the working directory, and mirrored to the terminal.

## Notes

- Only files with extensions listed in `WATCHED_EXTENSIONS` are processed — everything else is silently ignored (logged at DEBUG level)
- If a file fails to move (e.g. permissions issue), it is **not** logged to the database or notified — the error is recorded in the log file instead, so the database only ever reflects successfully processed files
- `WATCH_FOLDER` and `DESTINATION_FOLDER` are created automatically on first run if they don't already exist
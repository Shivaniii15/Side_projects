"""

FILE MONITOR — A Python Script to Watch a Folder and Move Files
Author: Vaani :)

How it works:
1. it uses the watchdog library to monitor a specific folder for new files.
2. When a new file with a specified extension (e.g. .pdf, .csv) is detected, it:
   - Renames the file to include a timestamp (e.g. 09-04-26_14-30-22_report.pdf)
    - Moves it to a destination folder (e.g. inside OneDrive AUT)
    - Logs the original name, new name, file type, destination path, and timestamp to a SQLite database.
    - Sends a desktop notification to inform the user that a file was processed.

4 systems involved:    
- watch folder
- process file
- database log
- notification 

"""

import time
import shutil
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer

# FileSystemEventHandler is a base class we will inherit from to create our custom event handler
# It will call the code when a new file is created
from watchdog.events import FileSystemEventHandler

# Desktop notification 
from plyer import notification

#------------------------------------------------------
# Basic configuration 
#------------------------------------------------------
# Where to watch for files
WATCH_FOLDER = Path.home() / "Downloads" / "incoming"

# Where to move files after processing.
DESTINATION_FOLDER = Path.home() /  "OneDrive - AUT University" / "ProcessedFiles"

# extensions to watch for (it's case sensitive)
WATCHED_EXTENSIONS = {".pdf", ".csv"}

# Where to store the SQLite database that logs every processed file.
DB_PATH = Path.home() / "file_monitor_log.db"

# We use logging (python's built in) instead of print() for better control
logging.basicConfig(
    level=logging.INFO,                          # Show INFO and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # Timestamp + level + message
    handlers=[
        logging.FileHandler("file_monitor.log"),  # Write to a .log file
        logging.StreamHandler()                   # Also print to the terminal
    ]
)
logger = logging.getLogger(__name__)


#------------------------------------------------------
#  Database setup 
#------------------------------------------------------

def init_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS file_log (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                original_name TEXT    NOT NULL,
                new_name      TEXT    NOT NULL,
                file_type     TEXT    NOT NULL,
                moved_to      TEXT    NOT NULL,
                processed_at  TEXT    NOT NULL
            )
        """)
        conn.commit()
    logger.info(f"Database ready at: {DB_PATH}")


def log_to_database(original_name: str, new_name: str, file_type: str, moved_to: str):
    processed_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # ? is used as placeholders
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO file_log (original_name, new_name, file_type, moved_to, processed_at)
            
            VALUES (?, ?, ?, ?, ?)
        """, (original_name, new_name, file_type, moved_to, processed_at))
        conn.commit()

    logger.info(f"Logged to DB: {original_name} -> {new_name}")


# --------------------------------------------------------
#  File process
# --------------------------------------------------------

# build new filename only generates a new name
def build_new_filename(original_path: Path) -> str:
    
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    return f"{timestamp}_{original_path.stem}{original_path.suffix}"


def send_desktop_notification(filename: str, destination: str):
    
    notification.notify(
        title="File Monitor",
        message=f"Processed: {filename}\n -> {destination}",
        app_name="File Monitor",
        timeout=10  # Notification disappears after 10 seconds
    )


def process_file(file_path: Path):
    time.sleep(1) #buffer

    # double-check the file still exists
    if not file_path.exists():
        logger.warning(f"File disappeared before processing: {file_path.name}")
        return

    # calling the rename function 
    new_name = build_new_filename(file_path)

    # moving the file
    destination_path = DESTINATION_FOLDER / new_name

    try:
        # SH-Util.move actually renames the file.
        # also moves it to the destination folder.
        shutil.move(str(file_path), str(destination_path))
        logger.info(f"Moved: {file_path.name}  ->  {destination_path}")

    except Exception as e:
        logger.error(f"Failed to move {file_path.name}: {e}")
        return  # don't log to DB or notify if the move failed

    # DB logging
    log_to_database(
        original_name=file_path.name,
        new_name=new_name,
        file_type=file_path.suffix.lower(),
        moved_to=str(destination_path)
    )

    # notification
    send_desktop_notification(new_name, str(DESTINATION_FOLDER))


# --------------------------------------------------------
#  Watchdog 
# --------------------------------------------------------

class FileHandler(FileSystemEventHandler):

    def on_created(self, event):
        
        # ignore folder creation events, we only care about files
        if event.is_directory:
            return

        # converting raw string into path object (easier)
        file_path = Path(event.src_path)

        # only process files with the extensions we care about
        if file_path.suffix.lower() not in WATCHED_EXTENSIONS:
            logger.debug(f"Ignored (unsupported type): {file_path.name}")
            return

        logger.info(f"New file detected: {file_path.name}")
        process_file(file_path)


# --------------------------------------------------------
#  Starting the watcher
# --------------------------------------------------------

def main():
   
    # Create the folders if they don't already exist.
    WATCH_FOLDER.mkdir(parents=True, exist_ok=True)
    DESTINATION_FOLDER.mkdir(parents=True, exist_ok=True)

    # initialise the database (creates the table if needed)
    init_database()

    logger.info("=" * 50)
    logger.info("  FILE MONITOR STARTED")
    logger.info(f"  Watching:     {WATCH_FOLDER}")
    logger.info(f"  Destination:  {DESTINATION_FOLDER}")
    logger.info(f"  Watching for: {WATCHED_EXTENSIONS}")
    logger.info("  Press Ctrl+C to stop.")
    logger.info("=" * 50)

    # - Observer() is the actual watcher
    event_handler = FileHandler()
    observer = Observer()

    # .schedule() tells the observer WHAT to watch (event_handler),
    # WHERE to watch (WATCH_FOLDER), and whether to include subfolders (recursive=False)
    observer.schedule(event_handler, str(WATCH_FOLDER), recursive=False)

    # start the observer in a background thread
    observer.start()

    try:
        # Keep the main thread alive in a loop so the background observer keeps running.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # Ctrl+C pressed — gracefully stop the observer
        logger.info("Stopping file monitor...")
        observer.stop()

    # .join() waits for the observer thread to fully finish before exiting
    observer.join()
    logger.info("File monitor stopped.")


def print_log():
    with sqlite3.connect(DB_PATH) as conn: #opens SQlite database
        # get data from file_log table, sort by proccesed time (DESC)
        rows = conn.execute("SELECT * FROM file_log ORDER BY processed_at DESC").fetchall()

    if not rows:
        print("No files logged yet.")
        return

    print(f"\n{'ID':<5} {'Original':<30} {'New Name':<45} {'Type':<6} {'Processed At'}")
    print("-" * 100)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<45} {row[3]:<6} {row[5]}")

if __name__ == "__main__":
    main()
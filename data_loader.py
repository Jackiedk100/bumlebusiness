# Import datetime to verify timestamp format
from datetime import datetime
# Import Path to build the log file path relative to this file
from pathlib import Path
# Import shlex to preserve quoted messages with spacing
import shlex


# Path to the log file, relative to this file (works no matter where the program is started from)
LOG_FILE_PATH = Path(__file__).parent / "data" / "cyber_security_log_sample.txt"


# Create function to load raw log file.
def load_logs():
    # Try added for file loading
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
            return file.readlines()
    # Except added for handling missing file
    except FileNotFoundError:
        print(f"File not found: {LOG_FILE_PATH}")
    # Except added for missing read permission
    except PermissionError:
        print(f"No permission to read file: {LOG_FILE_PATH}")
    # Except added for files that are not valid UTF-8 text
    except UnicodeDecodeError:
        print(f"File could not be decoded as UTF-8: {LOG_FILE_PATH}")
    # Except added for any other file error (e.g. path is a directory)
    except OSError as error:
        print(f"Could not read file {LOG_FILE_PATH}: {error}")
    return None


def parse_log(log_line, line_number):
    # Try added for lines with unbalanced quotes (e.g. msg="text without closing quote)
    try:
        parts = shlex.split(log_line)
    except ValueError:
        print(f"Invalid quotation at line {line_number}: {log_line.strip()}")
        return None

    # If no indexes are present in parts
    if not parts:
        print("Empty log entry")
        return None
    # Verify timestamp formnat is correct
    try:
        datetime.strptime(parts[0], "%Y-%m-%dT%H:%M:%S")
        # Except error and print invalid timestamp and line number
    except ValueError:
        print(f"Invalid timestamp at line {line_number}: {parts[0]}")
        return None


    # Empty dictionary for parsed log entry
    log_entry = {}
    # create separate timestamp entry, as it does not follow same key to value principle
    log_entry["timestamp"] = parts[0]

    # Divide log entries into key=value pair
    for part in parts[1:]:
        # Check for = from parts [1]
        if "=" in part:
            key, value = part.split("=", 1)
            log_entry[key] = value
            # else report key-value error and line number and part of log that is wrong
        else:
            print(f"Invalid key-value pair at line {line_number}: {part}")
            return None
    return log_entry

# Parse all log lines and return a list of dictionaries (one per valid entry)
def parse_logs(lines):
    parsed_logs = []
    # Enumerate lines starting from 1
    for line_number, line in enumerate(lines, start=1):
        parsed_entry = parse_log(line, line_number)
        # If parsed data is good
        if parsed_entry is not None:
            parsed_logs.append(parsed_entry)
        # Else print log line number that fails
        else:
            print(f"Invalid log entry at line {line_number}")
    return parsed_logs

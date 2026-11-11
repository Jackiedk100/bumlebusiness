# Import datetime til timestamp verificering
from datetime import datetime
# Import shlex to preserve quoted messages with spacing
import shlex


# Import pandas to structure log data in a table (DataFrame)
import pandas as pd



# create function to load raw log file.

def load_logs():
    # Try added for file loading
    try:
        with open("data/cyber_security_log_sample.txt", "r", encoding="utf-8") as file:
            return file.readlines()
        # Except added for handling missing file
    except FileNotFoundError:
        print("File not found")
        return None
def parse_log(log_line, line_number):
    parts = shlex.split(log_line)


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

# Verify successful log file loading and parsing
if __name__ == "__main__":
    logs = load_logs()
    # if logs cannot be found
    if logs is None:
        print("No logs found")
    else:
        # Parse each log entry and store dictionaries in parsed_logs
        parsed_logs = []
        # Enumerate lines starting from 1
        for line_number, line in enumerate(logs, start=1):
            parsed_entry = parse_log(line, line_number)
            # If parsed data is good
            if parsed_entry is not None:
                parsed_logs.append(parsed_entry)
            # Else print log line number that fails
            else:
                print(f"Invalid log entry at line {line_number}")


        #Convert list of dictionaries into a DataFrame (rows = log entries, columns = fields)
        df = pd.DataFrame(parsed_logs)
        #Display first 10 rows to verify the table structure
        print(df.head(10))

        print("Parsed entries:", len(parsed_logs))
        # Number of lines loaded from log
        print("Total lines loaded:", len(logs))
        # Verify no lines are empty
        print("Non-empty lines:", sum(1 for line in logs if line.strip()))
        # Verify first line can be loaded from log
        print("First line:", logs[0])
        # Verify last line can be loaded from log
        print("Last line:", logs[-1])
        # Sanity check for each line is a new log entry.
        print("Log entries:", sum (1 for line in logs if line [:4].isdigit()))



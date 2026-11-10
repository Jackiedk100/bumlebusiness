# Import shlex to preserve quoted messages with spacing
import shlex
# Import pandas to structure log data in a table (DataFrame)
import pandas as pd

# create function to load raw log file.

def load_logs():
    with open("data/cyber_security_log_sample.txt", "r", encoding="utf-8") as file:
        return file.readlines()
def parse_log(log_line):
    parts = shlex.split(log_line)

    # Empty dictionary for parsed log entry
    log_entry = {}
    # create separate timestamp entry, as it does not follow same key to value principle
    log_entry["timestamp"] = parts[0]

    # Divide log entries into key=value pair
    for part in parts[1:]:
        key, value = part.split("=", 1)
        log_entry[key] = value
    return log_entry

# Verify successful log file loading and parsing
if __name__ == "__main__":
    logs = load_logs()
    # Parse each log entry and store dictionaries in parsed_logs
    parsed_logs = [parse_log(line) for line in logs]

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




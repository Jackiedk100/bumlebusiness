# Import shlex to help separate msg from logfile
import shlex

# create function to load logs and define log path

def load_logs():
    with open("data/cyber_security_log_sample.txt", "r", encoding="utf-8") as file:
        return file.readlines()
def parse_log(log_line):
    parts = shlex.split(log_line)

    # Empty dictionary for divided log entries
    log_entry = {}
    # create separate timestamp entry as it is not divided by =
    log_entry["timestamp"] = parts[0]

    # Divide log entries into key & value pair after =
    for part in parts[1:]:
        key, value = part.split("=", 1)
        log_entry[key] = value
    return log_entry

# Verify log file was loaded
if __name__ == "__main__":
    logs = load_logs()
    # Parse every line for each line in the log and store it in parsed_logs
    parsed_logs = [parse_log(line) for line in logs]
    print("Parsed entries:", len(parsed_logs))
    # Number of lines loaded from log
    print("Total lines loaded:", len(logs))
    # Verify no lines are empty
    print("Non-empty lines:", sum(1 for line in logs if line.strip()))
    # Verify first line can be loaded from log
    print("First line:", logs[0])
    # Verify last line can be loaded from log
    print("Last line:", logs[-1])
    # Sanity check to make sure 541 lines are actually complete lines not divided by checking
    # for 4 digits (year)
    print("Log entries:", sum (1 for line in logs if line [:4].isdigit()))




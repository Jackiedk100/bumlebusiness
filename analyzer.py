# Import table_view to reuse the shared log table
import table_view as tv
import pandas as pd

# Columns that can be searched, linked to the menu choices
SEARCH_COLUMNS = {
    "1": "src_ip",
    "2": "user",
    "3": "event"
}

# Return log entries where level is one of the given levels (WARN, ALERT)
def filter_by_level(df, levels):
    return df[df["level"].isin(levels)]

# Return log entries that failed or were blocked
def filter_failed_events(df):
    return df[df["status"].isin(["FAILED", "BLOCKED"])]

# Return log entries where status is one of the given statuses (OK, FAILED, BLOCKED)
def filter_by_status(df, statuses):
    return df[df["status"].isin(statuses)]

# Return log entries between start and end. None means no limit
def filter_by_time_range(df, start=None, end=None):
    if start is not None:
        df = df[df["timestamp"] >= start]
    if end is not None:
        df = df[df["timestamp"] <= end]
    return df

# Ask for a date and time. Blank input gives None (no limit)
def ask_for_time(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            return None
        try:
            return pd.to_datetime(text)
        except ValueError:
            print("Invalid date. Use for example 2026-03-01 08:30")

# Return log entries where one column matches the search value
def search_logs(df, column, keyword):

    # Chek that the column exists, so a typo can't crash the program
    if column not in df.columns:
        print(f"Unknown column: {column}")
        return df.iloc[0:0]
    return df[df[column].astype(str).str.contains(keyword, case=False, regex=False, na=False)]

# Return log entries where IP, user or event matches the search value
def search_all(df, keyword):
    mask = pd.Series(False, index=df.index)
    for column in SEARCH_COLUMNS.values():
        mask |= df[column].astype(str).str.contains(keyword, case=False, regex=False, na=False)
    return df[mask]

# Find IPs with many failed logins within a few minutes (brute force)
def find_brute_force(df, min_attempts=5, window_minutes=5):
    try:
        failed = df[df["event"] == "LOGIN_FAILED"]
        suspects = []

        # Check one IP at a time
        for ip in failed["src_ip"].unique():
            attempts = failed[failed["src_ip"] == ip]

            # Start a time window at each attempt and count the attempts inside it
            most_attempts = 0
            for start_time in attempts["timestamp"]:
                end_time = start_time + pd.Timedelta(minutes=window_minutes)
                in_window = attempts[(attempts["timestamp"] >= start_time) & (attempts["timestamp"] <= end_time)]
                most_attempts = max(most_attempts, len(in_window))

            if most_attempts >= min_attempts:
                suspects.append({
                    "src_ip": ip,
                    "max_attempts": most_attempts,
                    "first_seen": attempts["timestamp"].min(),
                    "last_seen": attempts["timestamp"].max(),
                    "users": ", ".join(sorted(attempts["user"].unique())),
                })
        return pd.DataFrame(suspects)
    # Except added so a missing column does not crash the program
    except Exception as error:
        print(f"Could not search for brute force: {error}")
        return pd.DataFrame()

# Return every failed login from the suspected IPs, sorted by time
def get_suspect_attempts(df, suspects):
    failed = df[df["event"] == "LOGIN_FAILED"]
    return failed[failed["src_ip"].isin(suspects["src_ip"])].sort_values("timestamp")

# Printing the search menu with the 4 options
def print_search_menu():
    print("\n===== Search logs =====")
    print("1: Search by IP")
    print("2: Search by User")
    print("3: Search by Event")
    print("4: Search in all 3")
    print("0: Back")

# Show the search menu, ask for a value and print the maching log entries
def search_menu(df):
    while True:
        print_search_menu()
        choice = input("Enter your choice: ").strip()

        #Leave the search menu
        if choice == "0":
            break

        # Wrong chioce
        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice. Please try again.")
            continue

        # Ask for the value to search for. strip() removes spaces before and after
        value = input("Enter search value: ").strip()

        # Search in all 3 columns
        if choice == "4":
            results = search_all(df, value)

        # Search in the one column linked to the menu choice IP or user
        else:
            results = search_logs(df, SEARCH_COLUMNS[choice], value)

        # Print the result or a message if isn't found
        if results.empty:
            print(f"No logs entries found for {value}.")
        else:
            print(f"Found {len(results)} logs entries:")
            tv.show_table(results, rows=len(results))

# Printing the filter menu
def print_filter_menu():
    print("\n===== Filter logs =====")
    print("1: Failed or blocked events")
    print("2: Level WARN or ALERT")
    print("3: By status (OK, FAILED, BLOCKED)")
    print("4: By time range")
    print("0: Back")

# Show the filter menu, apply the chosen filter and print the matching log entries
def filter_menu(df):
    while True:
        print_filter_menu()
        choice = input("Enter your choice: ").strip()

        # Leave the filter menu
        if choice == "0":
            break

        if choice == "1":
            results = filter_failed_events(df)
        elif choice == "2":
            results = filter_by_level(df, ["WARN", "ALERT"])
        elif choice == "3":
            status = input("Enter status (OK, FAILED or BLOCKED): ").strip().upper()
            if status not in ("OK", "FAILED", "BLOCKED"):
                print("Invalid status. Please try again.")
                continue
            results = filter_by_status(df, [status])
        elif choice == "4":
            start = ask_for_time("Start, e.g. 2026-03-01 08:00 (blank = from the beginning): ")
            end = ask_for_time("End, e.g. 2026-03-01 23:59 (blank = to the end): ")
            results = filter_by_time_range(df, start, end)
        else:
            print("Invalid choice. Please try again.")
            continue

        # Print the result or a message if nothing is found
        if results.empty:
            print("No log entries match the filter.")
        else:
            print(f"Found {len(results)} log entries:")
            tv.show_table(results, rows=len(results))













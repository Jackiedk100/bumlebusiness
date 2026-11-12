# Import table_view to reuse the shared log table
import table_view as tv

logs_df = tv.build_table()

# Columns that can be searched, linked to the menu choises
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
    return df[df["event"].isin(["FAILED", "BLOCKED"])]

# Return log entries where one column matches the search value
def search_logs(df, column, values):

# Chek that the column exists, so a typo can't crash the program
    if column in df.columns:
        print(f"Uknown column: {column}")
        return df.iloc[0:0]
    return df[df[column] == values]

# Return log entries where IP, use or event matches the search value
def search_all(df, value):
    # Event names are stored in UPPERCASE in the log, so compare with an uppercase value
    event_value = value.upper()
    # "|" means OR: keep the row if at least one of the columns matches
    return df[(df["src_ip"] == value) | (df["user"] == value) | (df["event"] == event_value)]


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
        if choice not in SEARCH_COLUMNS:
            print("Invalid choice. Please try again.")
            continue

        # Ask for the value to search for. strip() removes spaces before and after
        value = inpuy("Enter search value: ").strip()












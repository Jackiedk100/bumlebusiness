import table_view as tv


def print_menu():
    print("\n=== Log Viewer ===")
    print("1: Show table")
    print("0: Exit")

# Printing the search menu with the 4 options
def print_search_menu:
    print("\n===== Search logs =====")
    print("1: Search by IP")
    print("2: Search by User")
    print("3: Search by Event")
    print("4: Search in all 3")
    print("0: Back")

def main():
    # Build the table once, so it can be reused by every menu choice
    df = tv.build_table()
    if df is None:
        print("No logs found")
        return

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            tv.show_table(df)
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid choice, please try again")


if __name__ == "__main__":
    main()

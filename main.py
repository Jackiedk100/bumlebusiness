import table_view as tv


def print_menu():
    print("\n=== Log Viewer ===")
    print("1: Show table")
    print("0: Exit")


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

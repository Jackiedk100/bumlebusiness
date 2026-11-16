import table_view as tv
import analyzer as al
import visualization as vs


def print_menu():
    print("\n=== Log Viewer ===")
    print("1: Show table")
    print("2: Scatter plot - log levels per IP")
    print("3: Bar chart - status per source IP")
    print("4: Line chart - activity over time")
    print("5: Scatter plot - IP activity vs. failed share")
    print("6: Search in log")
    print("7: Detect brute force")
    print("8: Filter log")
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
            # Let the user choose between the first and the latest 20 log entries
            view = input("Show (f)irst or (l)atest 20 entries? [f/l]: ").strip().lower()
            if view == "l":
                tv.show_latest(df)
            else:
                tv.show_table(df)
        elif choice == "2":
            vs.plot_scatter_levels_per_ip(df)
        elif choice == "3":
            vs.plot_status_per_ip(df)
        elif choice == "4":
            vs.plot_activity_over_time(df)
        elif choice == "5":
            vs.plot_scatter_ip_activity(df)
        elif choice == "6":
            al.search_menu(df)
        elif choice == "7":
            suspects = al.find_brute_force(df)
            if suspects.empty:
                print("No brute force activity found")
            else:
                print("\nSuspected IPs:")
                tv.show_table(suspects, rows=len(suspects))

                # Show every single failed login from the suspected IPs
                attempts = al.get_suspect_attempts(df, suspects)
                print(f"\nAll {len(attempts)} suspected login attempts:")
                tv.show_table(attempts, rows=len(attempts))

                vs.plot_brute_force(df, suspects)
        elif choice == "8":
            al.filter_menu(df)
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid choice, please try again")


if __name__ == "__main__":
    main()

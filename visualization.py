# this file is for visualization of the data

# importing matplotlib
import matplotlib.pyplot as plt

# US5: Scatter plot - source IP vs number of INFO, WARN and ALERT entries
# Each level gets its own dot and color, so IPs with few INFO but many WARN/ALERT stand out
def plot_scatter_levels_per_ip(df):
    try:
        # Count entries per IP and level
        # Each level gets its own column
        levels_per_ip = df.groupby(["src_ip", "level"]).size().unstack(fill_value=0)
        # Sort IPs by number of INFO entries
        # IPs with no normal activity end up to the left
        levels_per_ip = levels_per_ip.sort_values("INFO")

        # One dot per level per IP each level with its own color
        level_colors = {"INFO": "tab:green", "WARN": "tab:orange", "ALERT": "tab:red"}
        for level, color in level_colors.items():
            # Skip a level if it does not exist
            if level in levels_per_ip.columns:
                plt.scatter(levels_per_ip.index, levels_per_ip[level], label=level, color=color)

        plt.title("Log levels per source IP")
        plt.xlabel("Source IP")
        plt.ylabel("Number of log entries")
        # Rotate IP labels so they dont overlap
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Level")
        plt.tight_layout()
        plt.show()
    # Except added so the program doesnt crash if a column is missing or data is bad
    except Exception as error:
        print(f"Could not draw scatter plot: {error}")


# US5: Scatter plot - one dot per source IP
# x = total number of log entries from the IP
# y = percentage of entries that failed or were blocked
def plot_scatter_ip_activity(df):
    try:
        # Group by IP: count all entries, and entries where the status is failed or blocked
        ip_stats = df.groupby("src_ip").agg(
            total=("status", "size"),
            failed=("status", lambda status: (status != "OK").sum()),
        )
        # Calculate the percentage of failed and blocked entries per IP
        ip_stats["failed_pct"] = ip_stats["failed"] / ip_stats["total"] * 100

        # Split IPs into normal and suspicious 
        suspicious = ip_stats[ip_stats["failed_pct"] > 50]
        normal = ip_stats[ip_stats["failed_pct"] <= 50]

        plt.scatter(normal["total"], normal["failed_pct"], label="Normal", color="tab:blue")
        plt.scatter(suspicious["total"], suspicious["failed_pct"], label="Suspicious (> 50 %)", color="tab:red")

        # Write the IP address next to each suspicious dot
        for ip, row in suspicious.iterrows():
            plt.annotate(ip, (row["total"], row["failed_pct"]), xytext=(5, 5), textcoords="offset points")

        plt.title("Source IPs: activity vs. share of failed/blocked")
        plt.xlabel("Number of log entries from IP")
        plt.ylabel("Failed or blocked (%)")
        plt.legend()
        plt.tight_layout()
        plt.show()
    # Except added so a missing column or bad data does not crash the program
    except Exception as error:
        print(f"Could not draw scatter plot: {error}")


# US6: Stacked bar chart - number of ok/failed/blocked per source IP
def plot_status_per_ip(df):
    try:
        # Count entries per IP and status
        # Turn each status into its own column
        status_per_ip = df.groupby(["src_ip", "status"]).size().unstack(fill_value=0)
        status_per_ip.plot(kind="bar", stacked=True)

        plt.title("Status per source IP")
        plt.xlabel("Source IP")
        plt.ylabel("Number of log entries")
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Status")
        plt.tight_layout()
        plt.show()
    except Exception as error:
        print(f"Could not draw bar chart: {error}")

# US6: Line chart - number of log entries per hour, one line per level
def plot_activity_over_time(df):
    try:
        # Round timestamps down to the hour and count entries per hour and level
        entries_per_hour = df.groupby([df["timestamp"].dt.floor("h"), "level"]).size().unstack(fill_value=0)
        entries_per_hour.plot(marker="o")

        plt.title("Log entries per hour by level")
        plt.xlabel("Time")
        plt.ylabel("Number of log entries")
        plt.legend(title="Level")
        plt.tight_layout()
        plt.show()
    except Exception as error:
        print(f"Could not draw line chart: {error}")

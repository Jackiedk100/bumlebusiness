# log path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# create function to load logs

def load_logs():
    file_path = BASE_DIR / "data" / "cyber_security_log_sample.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        logs = file.readlines()
    return logs



if __name__ == "__main__":
    logs = load_logs()
    print(logs[:5])
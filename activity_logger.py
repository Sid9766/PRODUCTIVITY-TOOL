import win32gui
import win32process
import psutil
import time
import json
from datetime import datetime

LOG_FILE = "activity_log.jsonl"

def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        window_title = win32gui.GetWindowText(hwnd)
        app_name = process.name()
        return {
            "timestamp": datetime.now().isoformat(),
            "app": app_name,
            "title": window_title
        }
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "app": "Unknown",
            "title": f"Error: {str(e)}"
        }

def log_activity():
    last_app = None
    print("🟢 ContextPilot Activity Logger started. Press Ctrl+C to stop.\n")
    while True:
        info = get_active_window_info()
        if info["app"] != last_app:  # Log only when app changes
            print(f"[{info['timestamp']}] {info['app']} - {info['title']}")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(info) + "\n")
            last_app = info["app"]
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    log_activity()

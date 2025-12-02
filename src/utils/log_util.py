import os
from datetime import datetime

# Global log file path (set when workflow starts)
_LOG_FILE = None


def set_log_file(log_file: str):
    """Sets the global log file used for all logging."""
    global _LOG_FILE
    _LOG_FILE = log_file


def init_log(log_dir: str, prefix: str = "log") -> str:
    """
    Creates a log file and registers it as the global log destination.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{prefix}.txt")
    with open(log_file, "w") as f:
        f.write(f"=== Log started at {datetime.now()} ===\n")

    set_log_file(log_file)
    return log_file


def log(message: str):
    """Writes message to the global log file."""
    if not _LOG_FILE:
        raise RuntimeError("Log file not initialized. Call init_log() first.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(_LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

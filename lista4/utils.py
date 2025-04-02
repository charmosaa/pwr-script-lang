# utils.py
import os
import json
import datetime
import subprocess

def get_converted_dir():
    return os.environ.get("CONVERTED_DIR", os.path.join(os.getcwd(), "converted"))

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M")

def get_full_path(path):
    return os.path.abspath(os.path.expanduser(path))

def log_conversion(history_file, original_file, output_format, output_file, program_used):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "original_file": original_file,
        "output_format": output_format,
        "output_file": output_file,
        "program_used": program_used  
    }
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass
    history.append(entry)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

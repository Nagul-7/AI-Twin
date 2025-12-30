# tools.py

import os
import json

PROJECT_DIR = "."


def list_files():
    files = []
    for root, dirs, filenames in os.walk(PROJECT_DIR):
        for f in filenames:
            if not f.startswith("."):
                files.append(os.path.join(root, f))
    return files


def read_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


def clear_memory():
    with open("memory.json", "w") as f:
        f.write("""{
  "profile": {},
  "interests": [],
  "skills": [],
  "preferences": {}
}""")
    return "Memory cleared"

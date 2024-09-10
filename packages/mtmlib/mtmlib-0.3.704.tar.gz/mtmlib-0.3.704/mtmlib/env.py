import os
import platform
import sys
from pathlib import Path


def in_jupyter_notebook():
    return "JPY_PARENT_PID" in os.environ


def is_in_docker():
    return Path("/.dockerenv").exists()

def is_ubuntu():
    if platform.system() != "Linux":
        return False
    try:
        with open("/etc/os-release") as f:  # noqa: PTH123
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"').lower() == "ubuntu"
    except FileNotFoundError:
        return False
    return False

def init_env():
    sys.path.insert(0, str(Path("./mtmlib").absolute()))
    sys.path.insert(0, str(Path("./mtmtrain").absolute()))

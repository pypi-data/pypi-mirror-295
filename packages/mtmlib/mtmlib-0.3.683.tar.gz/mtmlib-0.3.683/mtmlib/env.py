import os
import sys
from pathlib import Path


def in_jupyter_notebook():
    return "JPY_PARENT_PID" in os.environ


def is_in_docker():
    return Path("/.dockerenv").exists()


def init_env():
    sys.path.insert(0, str(Path("./mtmlib").absolute()))
    sys.path.insert(0, str(Path("./mtmtrain").absolute()))

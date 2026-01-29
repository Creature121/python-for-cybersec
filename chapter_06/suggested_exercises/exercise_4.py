from watchfiles import watch, Change
from pathlib import Path
import subprocess

file = Path("../terminated.txt")
# print(file.exists())
for changes in watch(file):
    for change_type, path in changes:
        if Path(path) == file and change_type == Change.modified:
            with open(file) as f:
                last_line = f.readlines()[-1]
            if "Process terminated" in last_line:
                subprocess.run(file)

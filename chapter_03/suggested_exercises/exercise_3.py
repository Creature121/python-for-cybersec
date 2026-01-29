import os
import subprocess
from pathlib import Path
import shlex
from itertools import accumulate
import psutil


def CheckValidTask(creator, task):
    allowlist = ["Microsoft", "Mozilla", "Adobe Systems Incorporated"]
    extensions = [".exe", ".py", ".dll"]
    trusted = [creator for x in allowlist if creator.startswith(x)]
    executable = [task for ext in extensions if ext in task]

    if executable:
        exe = task.split(" ")[0]
        variables = os.path.expandvars(exe).lower()
        if variables.startswith(r"c:\\windows\\system32") or variables.startswith(
            r"c:\windows\system32"
        ):
            return True
        else:
            return trusted
    else:
        return True


output = str(
    subprocess.check_output("schtasks /query /v /fo csv /nh", shell=True)
).split("\\r\\n")

results = [o.split(",") for o in output]

for intermediate in results:
    result = [x.strip('"') for x in intermediate]
    if len(result) > 8:
        name = result[1]
        creator = result[7]
        task = result[8]
        if not CheckValidTask(creator, task):
            # print(f"{name}, {creator}, {task}")
            exe_path = next(
                (
                    Path(os.path.expandvars(s))
                    for s in accumulate(
                        shlex.split(task, posix=False), lambda a, b: f"{a} {b}"
                    )
                    if s.lower().endswith(".exe")
                ),
                None,
            )
            print("========================================")
            print(exe_path)
            try:
                print(f"Size {exe_path.stat().st_size}")  # ty:ignore[possibly-missing-attribute]
                print(
                    "Currently Running"
                    if any(
                        process.info["exe"] and Path(process.info["exe"]) == exe_path
                        for process in psutil.process_iter(["exe"])
                    )
                    else "Not Running."
                )
            except FileNotFoundError:
                print("The executable no longer exists.")
            print("========================================")

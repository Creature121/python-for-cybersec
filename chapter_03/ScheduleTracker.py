import os
import pathlib
import subprocess


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
            print(f"{name}, {creator}, {task}")

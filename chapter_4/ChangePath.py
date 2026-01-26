import os
import winreg


def readPathValue(reg_hive, reg_path):
    reg = winreg.ConnectRegistry(None, reg_hive)
    key = winreg.OpenKey(reg, reg_path, access=winreg.KEY_READ)
    index = 0

    while True:
        val = winreg.EnumValue(key, index)
        if val[0] == "Path":
            return val[1]
        index += 1


def editPathValue(reg_hive, reg_path, target_dir):
    path = readPathValue(reg_hive, reg_path)

    if target_dir in path:
        return

    new_path = f"{target_dir};{path}"
    reg = winreg.ConnectRegistry(None, reg_hive)
    key = winreg.OpenKey(reg, reg_path, access=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)


# Modify user path
reg_hive = winreg.HKEY_CURRENT_USER
reg_path = "Environment"
target_dir = os.getcwd()
# editPathValue(reg_hive, reg_path, target_dir)

# Modify System PATH
# reg_hive = winreg.HKEY_LOCAL_MACHINE
# reg_path = "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
editPathValue(reg_hive, reg_path, target_dir)

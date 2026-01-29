# import filetime
import winfiletime
import winreg
from datetime import datetime, timedelta

delta = timedelta(weeks=2)
# time_comparison = filetime.from_datetime(datetime.now() - delta)
time_comparison = winfiletime.from_datetime(datetime.now() - delta)


def checkTimeDelta(time):
    if time_comparison < time:
        return True
    else:
        return False


def checkPath(hive, hive_name, reg_path):
    try:
        key = winreg.OpenKey(hive, reg_path, access=winreg.KEY_READ)
        result = winreg.QueryInfoKey(key)

        if checkTimeDelta(result[2]):
            print(f"Path at {hive_name}\\{reg_path} has potentially been modified.")
            val = winreg.QueryValueEx(key, "Path")[0]
            for v in val.split(";"):
                print(f"\t{v}")
    except Exception as _e:
        return


def checkPaths():
    checkPath(
        winreg.HKEY_LOCAL_MACHINE,
        "HKLM",
        "System\CurrentControlSet\Control\Session Manager\Environment",
    )
    checkPath(winreg.HKEY_CURRENT_USER, "HKCU", "Environment")

    try:
        number_of_users = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
        for i in range(number_of_users):
            user_key = winreg.EnumKey(winreg.HKEY_USERS, i)
            reg_path = f"{user_key}\\Environment"
            checkPath(winreg.HKEY_USERS, "HKU", reg_path)
    except Exception as _e:
        return


checkPaths()

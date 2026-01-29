import win32con
from win32api import GetLogicalDriveStrings  # ty:ignore[unresolved-import]
from win32file import GetDriveType  # ty:ignore[unresolved-import]
import os.path
import psutil


def GetRemovableDrives():
    driveStrings = GetLogicalDriveStrings()
    drives = [item for item in driveStrings.split("\x00") if item]
    return [
        drive for drive in drives if GetDriveType(drive) is win32con.DRIVE_REMOVABLE
    ]


def CheckAutoRun(drive):
    filename = f"{drive}Autorun.inf"
    if os.path.isfile(filename):
        print(f"Autorun file at {filename}")
        with open(filename, "r") as f:
            for line in f:
                if line.startswith("Open"):
                    index = line.index("=")
                    return line[index + 1 :].rstrip()
    else:
        return None


def DetectAutorunProcess(executable):
    for process in psutil.process_iter():
        if executable == process.name():
            print(f"Autorun file running with PID {process.pid}")


for drive in GetRemovableDrives():
    executable = CheckAutoRun(drive)
    if executable:
        DetectAutorunProcess(executable)

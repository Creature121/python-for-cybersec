import winreg
import psutil
import subprocess
from pathlib import Path

# av_list = ["MBAM", "WinDefend"]
av_list = ["FakeAV"]  # So that I don't disable my actual AV

reg_hive = winreg.HKEY_LOCAL_MACHINE
reg_path = "SYSTEM\CurrentControlSet\Services"

try:
    key = winreg.OpenKey(reg_hive, reg_path, 0, access=winreg.KEY_READ)
    num_keys = winreg.QueryInfoKey(key)[0]

    for i in range(num_keys):
        sub_key = winreg.EnumKey(key, i)

        for name in av_list:
            if name in sub_key:
                sub_path = f"{reg_path}\\{sub_key}"
                try:
                    sub_sub_key = winreg.OpenKey(
                        reg_hive, sub_path, 0, access=winreg.KEY_ALL_ACCESS
                    )
                except OSError as e:
                    if e.errno == 5:
                        print("Failed to get write access...")
                    print(e)

                num_vals = winreg.QueryInfoKey(sub_sub_key)[1]
                run_check = False

                for j in range(num_vals):
                    val = winreg.EnumValue(sub_sub_key, j)
                    if val[0] == "Start" and val[1] == 4:
                        print(f"Service {sub_key} has been disabled.")

                        print("Attempting to re-enable autostart...")
                        try:
                            winreg.SetValueEx(
                                sub_sub_key, "Start", 0, winreg.REG_DWORD, 0x02
                            )
                            print(f"Successfully enabled Service {sub_key}.")
                        except Exception as e:
                            print("Failed to set Start value.")
                            print(e)

                        run_check = True

                    if run_check and val[0] == "ImagePath":
                        print(f"Checking if Service {sub_key} is still running...")
                        exe_path = Path(val[1].strip('"'))
                        # This logic is still wonky, need to work on it some more.
                        for process in psutil.process_iter(["exe"]):
                            try:
                                process_exe = process.info["exe"]
                                if "note" in str(process_exe):
                                    print(process_exe)
                                if process_exe and Path(process_exe) == exe_path:
                                    print(f"Service {sub_key} is still running.")
                                    run_check = False
                                    break
                            except Exception as e:
                                print(e)
                                continue
                        else:
                            print(
                                f"Service {sub_key} is not running. Attempting to start it..."
                            )
                            try:
                                # print(exe_path.exists())
                                subprocess.Popen([exe_path])
                                print(f"Successfully started Service {sub_key}.")
                            except OSError as e:
                                print(f"Failed to run Service {sub_key}.")
                                print(e)


except Exception as e:
    print(e)

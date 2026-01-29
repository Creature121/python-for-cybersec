import winreg

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

                for j in range(num_vals):
                    val = winreg.EnumValue(sub_sub_key, j)
                    if val[0] == "Start" and val[1] == 4:
                        print(f"Service {sub_key} has been disabled.")
                        try:
                            winreg.SetValueEx(
                                sub_sub_key, "Start", 0, winreg.REG_DWORD, 0x02
                            )
                            print(f"Successfully enabled Service {sub_key}.")
                        except Exception as e:
                            print("Failed to set Start value...")
                            print(e)
except Exception as e:
    print(e)

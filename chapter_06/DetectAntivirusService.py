import winreg

av_list = ["MBAM", "WinDefend"]  # Added WinDefend as I use Windows Defender

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
                sub_sub_key = winreg.OpenKey(
                    reg_hive, sub_path, 0, access=winreg.KEY_READ
                )
                num_vals = winreg.QueryInfoKey(sub_sub_key)[1]

                for j in range(num_vals):
                    val = winreg.EnumValue(sub_sub_key, j)
                    if val[0] == "Start" and val[1] == 2:
                        print(f"Service {sub_key} set to run automatically.")
except Exception as e:
    print(e)

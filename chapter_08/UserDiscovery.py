# from icecream import ic
import os
import wmi

w = wmi.WMI()

admins = None
for group in w.Win32_Group():
    if group.Name == "Administrators":
        users = group.associators(wmi_result_class="Win32_UserAccount")
        admins = [user.Name for user in users]
        # ic(type(users[0]), type(admins))

for user in w.Win32_UserAccount():  # Get-WmiObject Win32_UserAccount | Select-Object *
    print(f"Username: {user.Name}")
    print(f"Administrator: {user.Name in admins}")  # ty:ignore[unsupported-operator]
    print(f"Disabled: {user.Disabled}")
    print(f"Domain: {user.Domain}")
    print(f"Local: {user.LocalAccount}")
    print(f"Password Changeable: {user.PasswordChangeable}")
    print(f"Password Expires: {user.PasswordExpires}")
    print(f"Password Required: {user.PasswordRequired}")
    print()

print("Password Policy:")
print(os.system("net accounts"))

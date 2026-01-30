import os
import platform


def setWindowsPassword(username, password):
    # Active Directory Service Interfaces (ADSI) Component Object Model (COM) interface
    # from win32com import adsi
    # ads_object = adsi.ADSGetObject(f"WinNT://localhost/{username},user")
    # The above doesn't work...

    from win32com import client

    ads_object = client.GetObject(f"WinNT://localhost/{username},user")
    ads_object.Getinfo()
    ads_object.SetPassword(password)


def setLinuxPassword(username, password):
    os.system(f"echo {username}:{password} | chpasswd")


def changeCriteria(username):
    if username in ["testuser", "user1", "python_user"]:
        return True
    else:
        return False


if platform.system() == "Windows":
    import wmi

    w = wmi.WMI()
    for user in w.Win32_UserAccount():
        username = user.Name
        if changeCriteria(username):
            print(f"Changing password: {username}")
            setWindowsPassword(username, "newpass")
else:
    import pwd

    for p in pwd.getpwall():  # ty:ignore[unresolved-attribute]
        if p.pw_uid == 0 or p.pw_uid > 1000:
            username = p.pw_name
            if changeCriteria(username):
                print(f"Changing password: {username}")
                setLinuxPassword(username, "newpass")

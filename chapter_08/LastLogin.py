# from icecream import ic
from subprocess import check_output, CalledProcessError, STDOUT
import re


def checkLastLogin(user: str):
    try:
        result = check_output(f"net user {user}", stderr=STDOUT)
    except CalledProcessError as _e:
        print(f"Command failed. Does user '{user}' exist?")
        # print(e)
        return
    # ic(result)
    logon = re.findall("Last logon\s*([^\r\n]+)", result.decode("utf-8"))[0]

    if logon != "Never":
        print(f"{user} last logged in {logon}")


decoy_accounts = ["tester", "testuser", "python_user"]
for user in decoy_accounts:
    checkLastLogin(user)

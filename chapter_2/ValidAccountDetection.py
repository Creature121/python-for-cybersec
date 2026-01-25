import win32evtlog

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ


def QueryEventLog(eventID):
    logs = []
    handle = win32evtlog.OpenEventLog(server, logtype)

    while True:
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if events:
            for event in events:
                if event.EventID == eventID:
                    logs.append(event)
        else:
            break
    return logs


def DetectBruteForce():
    failures = {}
    events = QueryEventLog(4625)  # Event code for failed login attempt.

    for event in events:
        if event.StringInserts[0].startswith("S-1-5-21"):
            account = event.StringInserts[1]
            if account in failures:
                failures[account] += 1
            else:
                failures[account] = 1

    for account in failures:
        print(f"{account}: {failures[account]} failed logins")


def CheckDefaultAccounts():
    with open("defaults.txt", "r") as f:
        # defaults = [[part for part in line.split(' ')][0] for line in f]
        defaults = [
            line.split(" ")[0] for line in f
        ]  # .split() already gives a list, no need to deconstruct it

    with open("allowlist.txt", "r") as f:
        allowed = f.read().splitlines()

    events = QueryEventLog(4624)  # Event code for successful login attempt
    for event in events:
        # i.e., 8 = LogonType
        # Logon types 10 (RemoteInteractive (=>RDP) ) and 3 (Network)
        if event.StringInserts[8] == ["10", "3"]:
            if event.StringInserts[5] in defaults:  # i.e., 5 = TargetUserName
                if event.StringInserts[18] not in allowed:  # i.e., 18 = IpAddress
                    print(
                        f"Unauthorized login to {event.StringInserts[5]} from {event.StringInserts[18]}"
                    )


DetectBruteForce()
CheckDefaultAccounts()

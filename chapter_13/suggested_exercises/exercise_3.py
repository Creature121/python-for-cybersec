def QueryEventLog(eventID):
    import win32evtlog  # ty:ignore[unresolved-import]

    server = "localhost"
    logtype = "Security"
    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    logs = []

    handle = win32evtlog.OpenEventLog(server, logtype)

    while events := win32evtlog.ReadEventLog(handle, flags, 0):
        logs.extend(event for event in events if event.EventID == eventID)

    return logs


def checkWindowsPasswordChange():
    events = QueryEventLog(4724)
    for event in events:
        if event.StringInserts[8] == ["10", "3"]: # "Logged into remotely"
            if event.StringInserts[5] == "Subject": # "Subject Account"
                changed = event.StringInserts[0]
                changer = event.StringInserts[4]
                time = event.TimeGenerated

                print(f"Password of {changed} changed by {changer} at {time}")


checkWindowsPasswordChange()

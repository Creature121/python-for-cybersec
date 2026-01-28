import win32evtlog  # ty:ignore[unresolved-import]

server = "localhost"
log_type = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ


def QueryEventLog(eventID, file_name=None):
    logs = []

    if not file_name:
        handle = win32evtlog.OpenEventLog(server, log_type)
    else:
        handle = win32evtlog.OpenEventLog(server, file_name)

    while True:
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if events:
            logs.extend([event for event in events if event.EventID == eventID])
        else:
            break

    return logs


def DetectAdminstratorLogin():
    events = QueryEventLog(4672)
    for event in events:
        if event.StringInserts[0].startswith("S-1-5-21"):
            print(f"Login attempt by {event.StringInserts[1]} at {event.TimeGenerated}")


DetectAdminstratorLogin()

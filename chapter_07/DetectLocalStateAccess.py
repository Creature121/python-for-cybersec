# from icecream import ic
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
            for event in events:
                if event.EventID == eventID:
                    # ic(event)
                    logs.append(event)
        else:
            break
    # ic(logs)
    return logs


def DetectLocalStateAccess():
    events = QueryEventLog(4663)
    if events:
        for event in events:
            if event.StringInserts[6].endswith("Local State"):
                print(
                    f"{event.StringInserts[11]} (PID {event.StringInserts[10]}) accessed Local State at {event.TimeGenerate}"
                )
    else:
        print("No Events Recorded.")


DetectLocalStateAccess()

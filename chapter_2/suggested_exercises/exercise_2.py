import win32evtlog  # ty:ignore[unresolved-import]

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
            print(type(event.TimeGenerated.timestamp()))
            if account in failures:
                failures[account][0] += 1
                failures[account][1].append(event.TimeGenerated.timestamp())
            else:
                failures[account] = [1, [event.TimeGenerated.timestamp()]]
                # failures[account][0] += 1
                # failures[account][1].append(event.TimeGenerated.timestamp())

    for account in failures:
        print(f"{account}:")
        print(f"{failures[account][0]} failed logins")

        times = failures[account][1]
        time_intervals = (
            [ts2 - ts1 for ts1, ts2 in zip(times, times[1:])] if len(times) >= 2 else []
        )
        avg_time_interval = (
            sum(time_intervals) / len(time_intervals) if time_intervals else 0
        )

        print(f"Average time between login attempts: {avg_time_interval}")


DetectBruteForce()

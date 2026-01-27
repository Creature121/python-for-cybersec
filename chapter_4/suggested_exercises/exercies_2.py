import win32evtlog  # ty:ignore[unresolved-import]

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ


def QueryEventLog(eventID, file_name=None):
    logs = []
    if not file_name:
        handle = win32evtlog.OpenEventLog(server, logtype)
    else:
        handle = win32evtlog.OpenEventLog(server, file_name)

    while True:
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if events:
            for event in events:
                if event.EventID == eventID:
                    logs.append(event)
        else:
            break
    return logs


def DetectPathModification():
    events = QueryEventLog(
        4657
    )

    for event in events:
        if event.StringInserts[5] == "Path":
            key = event.StringInserts[4]
            old_path = event.StringInserts[9].split(";")
            new_path = event.StringInserts[11].split(";")
            additions = [d for d in new_path if d not in old_path]
            deletions = [d for d in old_path if d not in new_path]

            process = event.StringInserts[-1]
            pid = event.StringInserts[-2]

            print(f"Path at {key} modified by {process} (PID: {pid})")
            if additions:
                print("\tAdditions: ")
                for a in additions:
                    print(f"\t\t{a}")
            if deletions:
                print("\tDeletions: ")
                for d in deletions:
                    print(f"\t\t{d}")
            if not (additions or deletions):
                print("Possible Reordering:")
                old_new_positions = zip(range(1, len(old_path)+1), old_path, new_path)
                for position, old_entry, new_entry in old_new_positions:
                    print("Index\tOld Entry\tNew Entry")
                    print(f"{position}.\t{old_entry}\t{new_entry}")


DetectPathModification()

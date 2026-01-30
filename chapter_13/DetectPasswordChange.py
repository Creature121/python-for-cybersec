import datetime
import platform
import subprocess

def QueryEventLog(eventID):
    import win32evtlog  # ty:ignore[unresolved-import]
    server = "localhost"
    logtype = "Security"
    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    logs = []

    handle = win32evtlog.OpenEventLog(server, logtype)

    # while True:
    #     events = win32evtlog.ReadEventLog(handle, flags, 0)
    #     if events:
    #         for event in events:
    #             if event.EventID == eventID:
    #                 logs.append(event)
    #     else:
    #         break
    
    while events := win32evtlog.ReadEventLog(handle, flags, 0):
        logs.extend(event for event in events if event.EventID == eventID)

    return logs

def checkWindowsPasswordChange():
    events = QueryEventLog(4724)
    for event in events:
        changed = event.StringInserts[0]
        changer = event.StringInserts[4]
        time = event.TimeGenerated

        print(f"Password of {changed} changed by {changer} at {time}")

def compareDates(date_1, date_2):
    date_1_parts = [int(part) for part in date_1.split("/")]
    date_2_parts = [int(part) for part in date_2.split("/")]

    d1 = datetime.datetime(date_1_parts[2], date_1_parts[0], date_1_parts[1])
    d2 = datetime.datetime(date_2_parts[2], date_2_parts[0], date_2_parts[1])

    return d2 >= d1

threshold = "01/01/2021"
def checkLinuxPasswordChange():
    import pwd
    # import grp

    for p in pwd.getpwall():  # ty:ignore[unresolved-attribute]
        user = p[0]
        results = subprocess.check_output(["passwd", user, "-S"]).decode("utf-8")
        date = results.split(" ")[2]
        if compareDates(threshold, date):
            print(f"Password of {user} changed on {date}")
    
if platform.system() == "Windows":
    checkWindowsPasswordChange()
else:
    checkLinuxPasswordChange()
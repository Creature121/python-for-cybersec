import win32evtlog
import xml.etree.ElementTree as ET
import psutil
import datetime

server = "localhost"
logtype = "Microsoft-Windows-WMI-Activity/Trace"
flags = win32evtlog.EvtQueryForwardDirection
query = "*[System[EventID=23]]"


def GetEventLogs():
    query_object = win32evtlog.EvtQuery(logtype, flags, query)
    events = ()

    while True:
        events_object = win32evtlog.EvtNext(query_object, 100, -1, 0)

        if events_object:
            events = events + events_object
        else:
            break

    return events


def ParseEvents(events):
    for event in events:
        xml = win32evtlog.EvtRender(event, 1)
        root = ET.fromstring(xml)
        path = "./{*}UserData/{*}ProcessCreate/{*}"
        name = root.findall(f"{path}Commandline")[0].text
        pid = root.findall(f"{path}CreatedProcessId")[0].text
        print(f"Process {name} launched with PID {pid}")
        if psutil.pid_exists(int(pid)):
            print("It is currently running.")
            print("Details:")
            process = psutil.Process(int(pid))
            print(
                f"Creation Time: {datetime.datetime.fromtimestamp(process.create_time())}"
            )  # Process's creation time
            print(
                f"Parent PID: {process.parent().pid}"
            )  # Process's parent process's pid.


events = GetEventLogs()
ParseEvents(events)

import win32evtlog  # ty:ignore[unresolved-import]
import xml.etree.ElementTree as ET

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


events = GetEventLogs()
ParseEvents(events)

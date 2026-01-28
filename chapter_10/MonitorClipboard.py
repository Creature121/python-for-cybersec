import win32gui  # ty:ignore[unresolved-import]
import win32api  # ty:ignore[unresolved-import]
import ctypes
from win32clipboard import GetClipboardOwner  # ty:ignore[unresolved-import]
from win32process import GetWindowThreadProcessId  # ty:ignore[unresolved-import]
from psutil import Process


allow_list = []


def processEvent(window_handle, msg, wparam, lparam):
    if msg == 0x031D:
        try:
            win = GetClipboardOwner()
            pid = GetWindowThreadProcessId(win)[1]
            process = Process(pid)
            name = process.name()
            if name not in allow_list:
                print(f"Clipboard modified by {name}")
        except Exception as e:
            print("Clipboard modified by unknown process.")
            print(e)


def createWindow():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = processEvent
    wc.lpszClassName = "clipboardListner"
    wc.hInstance = win32api.GetModuleHandle(None)
    class_atom = win32gui.RegisterClass(wc)

    return win32gui.CreateWindow(
        class_atom, "clipboardListener", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None
    )


def setupListener():
    window_handle = createWindow()
    ctypes.windll.user32.AddClipboardFormatListener(window_handle)
    win32gui.PumpMessages()


setupListener()

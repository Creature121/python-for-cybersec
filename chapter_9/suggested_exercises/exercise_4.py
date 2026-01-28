# from icecream import ic
import sqlite3
import os

chrome_path = os.path.join(
    "C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"
)

# ic(firefox_path)
connection = sqlite3.connect(chrome_path)
cursor = connection.cursor()
cursor.execute("SELECT * FROM cookies")

data = cursor.fetchall()

cookie_map = [
    ".amazon.com",
    ".google.com",
    ".microsoftonline.com",
    ".facebook.com",
    ".github.com",
    ".live.com",
    ".fake.com",
]

# ic(data)

cookies = {}
for cookie in data:
    for domain in cookie_map:
        cookies.setdefault(f"{cookie[1]}", set()).add(cookie[3])
for cookie, names in cookies.items():
    print(f"{cookie}:")
    for name in names:
        print(f"\t{name}")

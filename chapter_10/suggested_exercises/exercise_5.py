from libratom.lib.pff import PffArchive
import glob
import os
from zipfile import ZipFile
from sys import platform


# archive_files: list[str] = ["zip"]
email_files: list[str] = ["pst", "ost"]


def searchArchiveFile(file_name: str) -> bool:
    try:
        for file in ZipFile(file_name, "r").namelist():
            email = True in [file.endswith(ext) for ext in email_files]
            if email:
                return True
    except Exception as _:
        return False
    return False


def findFiles(extensions: list[str]) -> list[str]:
    files = []
    for ext in extensions:
        if platform == "win32":
            pattern = rf"~\**\*.{ext}"
        else:
            pattern = rf"~/**/*.{ext}"
        pattern = os.path.expanduser(pattern)
        print("Searching...")
        found = glob.glob(pattern, recursive=True)
        print("Done.")
        # if ext in archive_files:
        #     for a in found:
        #         if searchArchiveFile(a):
        #             files.append(a)
        # else:
        files += found
    return files


extensions = email_files  # + archive_files

# file_name = "sample.pst"

for file_name in findFiles(extensions):
    archive = PffArchive(file_name)
    print("-")
    print(file_name)
    for folder in archive.folders():
        if folder.get_number_of_sub_messages() != 0:
            for message in folder.sub_messages:
                print(f"Sender: {message.get_sender_name()}")
                print(f"Subject: {message.get_subject()}")
                print(f"Message: {message.get_plain_text_body()}")
    print("-")

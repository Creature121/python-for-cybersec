from pprint import pprint
import glob
import os
from zipfile import ZipFile
from sys import platform
from tarfile import TarFile

archive_files: list[str] = ["zip", "tar"]
email_files: list[str] = ["pst", "ost"]


def searchArchiveFile(file_name: str) -> bool:
    try:
        if file_name.endswith("zip"):
            for file in ZipFile(file_name, "r").namelist():
                email = True in [file.endswith(ext) for ext in email_files]
                if email:
                    return True
        elif file_name.endswith("tar"):
            for file in TarFile(file_name, "r").getnames():
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
        # print(pattern)
        print("Beginning search...")
        found = glob.glob(pattern, recursive=True)
        print("Search complete.")
        if ext in archive_files:
            for a in found:
                if searchArchiveFile(a):
                    files.append(a)
        else:
            files += found
    return files


extensions = email_files + archive_files
pprint(findFiles(extensions))

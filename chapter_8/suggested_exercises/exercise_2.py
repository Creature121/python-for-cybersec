import os
import re
from zipfile import ZipFile

email_regex = "[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}"
phone_regex = "[(]?[0-9]{3}[)]?-[0-9]{3}-[0-9]{4}"
ssn_regex = "[0-9]{3}-[0-9]{2}-[0-9]{4}"
regexes = [email_regex, phone_regex, ssn_regex]


def findPII(data):
    matches = []
    for regex in regexes:
        match_list = re.findall(regex, data)
        matches += match_list
    return matches


def printMatches(file_dir, matches):
    if len(matches) > 0:
        print(file_dir)
        for match in matches:
            print(f"\t{match}")


def parseDocx(root, docs):
    for doc in docs:
        matches = None
        file_dir = os.path.join(root, doc)

        with ZipFile(file_dir, "r") as zip:
            data = zip.read("word/document.xml")

        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError as _:
            print(
                "Failed to decode data (utf-8). Trying alternate encoding scheme (utf-16le)..."
            )
            data = data.decode("utf-16le")  # ty:ignore[possibly-missing-attribute]

        matches = findPII(data)

        print("-")
        printMatches(file_dir, matches)
        print("-")


def parseText(root, txts):
    for txt in txts:
        file_dir = os.path.join(root, txt)
        with open(file_dir, "r") as f:
            data = f.read()
            matches = findPII(data)
        printMatches(file_dir, matches)


txt_ext = [".txt", ".py", ".csv"]


def findFiles(directory):
    for root, directories, files in os.walk(directory):
        parseDocx(root, [file for file in files if file.endswith(".docx")])
        for ext in txt_ext:
            parseText(root, [file for file in files if file.endswith(ext)])


directory = os.path.join(os.getcwd(), "../Documents")
findFiles(directory)

from pandas import Series
from scipy.stats import entropy
from pathlib import Path


def calcEntropy(data):
    s = Series(data)
    counts = s.value_counts()
    return entropy(counts)


def calcFileEntropy(file_name):
    with open(file_name, "rb") as f:
        b = list(f.read())
    file_len = len(b)
    return calcEntropy(b)


def getFiles(directory, ext):
    paths = list(Path(directory).rglob(f"*{ext}*"))
    return paths


threshold = 0


def checkFiles(directory, ext):
    files = getFiles(directory, ext)
    for f in files:
        entropy = calcFileEntropy(f)
        if entropy > threshold:
            print(f"{f} is potentially encrypted (entropy {entropy})")


directory = "Documents"
ext = ".docx"
checkFiles(directory, ext)

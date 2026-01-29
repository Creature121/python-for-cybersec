import pathlib


def getTimestamps(file_name):
    file_path = pathlib.Path(file_name)
    stats = file_path.stat()

    if not file_path.exists():
        return []

    return (stats.st_ctime, stats.st_mtime, stats.st_atime)


def createDecoyFiles(file_names):
    with open("decoys.txt", "w") as f:
        for file in file_names:
            (ctime, mtime, atime) = getTimestamps(file)
            f.write(f"{file},{ctime},{mtime},{atime}\n")


decoys = [r"Documents\clients.csv", r"Documents\Resume.docx"]
createDecoyFiles(decoys)

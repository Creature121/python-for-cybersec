import pathlib


def getTimestamps(file_name):
    file_path = pathlib.Path(file_name)
    stats = file_path.stat()

    if not file_path.exists():  # File got deleted.
        return []

    return (stats.st_ctime, stats.st_mtime, stats.st_atime)


def checkTimestamps(file_name, create, modify, access):
    stats = getTimestamps(file_name)

    if len(stats) == 0:
        return False  # File deleted.

    (creation_time, modification_time, access_time) = stats

    if float(create) != float(creation_time):
        return False
    elif float(modify) != float(modification_time):
        return False
    elif float(access) != float(access_time):
        return False

    return True


def checkDecoyFiles():
    with open("decoys.txt", "r") as f:
        for line in f:
            vals = line.rstrip().split(",")
            if not checkTimestamps(vals[0], vals[1], vals[2], vals[3]):
                print(f"{vals[0]} has modified attributes.")


checkDecoyFiles()

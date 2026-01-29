import os
import re  # Unused import?  # noqa: F401
import subprocess


def findADS(directory: str):
    for dir_path, dir_names, file_names in os.walk(directory):
        for file in file_names:
            file_name = os.path.join(dir_path, file)
            cmd = f"Get-Item -path {file_name} -stream * "
            cmd += '| Format-Table -Property "Stream" -HideTableHeaders'

            results = subprocess.run(
                ["powershell", "-Command", cmd], capture_output=True
            )

            streams = results.stdout.decode("utf-8").split("\r\n")
            streams: list[str] = [s.strip() for s in streams]
            streams = [s for s in streams if len(s) > 1]

            if len(streams) > 1:
                print(f"ADS detected for {file_name}")
                for s in streams[1:]:
                    print(f"\t{s}")


findADS(".")

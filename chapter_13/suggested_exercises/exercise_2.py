import psutil

for process in psutil.process_iter():
    try:
        if files := process.open_files():
            if file_names := [
                file.path for file in files if file.path.endswith("docx")
            ]:
                print("-")
                print(f"{process.name()} (PID {process.pid}):")
                for file_name in file_names:
                    print(f"\t{file_name}")
                print("-")
    except psutil.AccessDenied:
        pass
        # print("Access Denied")

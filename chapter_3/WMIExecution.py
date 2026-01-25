import subprocess
import wmi


def WMIProcessCreation(name):
    contoller = wmi.WMI()
    processID, returnValue = contoller.Win32_Process.Create(CommandLine=name)
    print(f"Process {name} created with PID {processID}")


def PSProcessCreation(name):
    command = [
        "powershell",
        f"& {{invoke-wmimethod win32_process -name create -argumentlist {name} | select ProcessId | % {{ $_.ProcessId }} | Write-Host }}",
    ]

    process = subprocess.run(command, shell=True, capture_output=True)

    if process.returncode == 0:
        print(
            f"Process {name} created with Powershell, PID {process.stdout.decode('utf-8')}"
        )


command = "notepad.exe"
WMIProcessCreation(command)
PSProcessCreation(command)

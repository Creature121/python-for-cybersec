- Chapter 2 is concerned about the "Initial Access" phase of the MITRE ATT&CK framework.
    - We will be working with 2 techniques:
        - Valid Accounts
            - Attempts to take advantage of default accounts
                - [TestDefaultCredentials.py](TestDefaultCredentials.py)
            - Detect Window login attempts
                - [ValidAccountDetection.py](ValidAccountDetection.py)
                    - Uses Windows Event Logs to detect failed login attempts.
                    - Checks for unauthorized access to default accounts.
            - > ...potentially vulnerable to detection and prevention by network-based security solutions.

        - Replication Through Removable Media
            - > When a user inserts removable media into a drive, it is possible for malicious content on the media to run on their computer.
            - Exploiting Autorun
                - [AutorunSetup.py](AutorunSetup.py)
            - [AutorunDetection.py](AutorunDetection.py)
---
---
# Windows Logon Types
| LOGON TYPE | LOGON TITLE | DESCRIPTION |
|------------|-------------|-------------|
| 0 | System | Used only by the System account, for example at system startup. |
| 2 | Interactive | A user logged on to this computer. |
| 3 | Network | A user or computer logged on to this computer from the network. |
| 4 | Batch | Batch logon type is used by batch servers, where processes may be executing on behalf of a user without their direct intervention. |
| 5 | Service | A service was started by the Service Control Manager. |
| 7 | Unlock | This workstation was unlocked. |
| 8 | NetworkCleartext | A user logged on to this computer from the network. The user’s password was passed to the authentication package in its unhashed form. The built-in authentication packages all hash credentials before sending them across the network. The credentials do not traverse the network in plaintext (also called cleartext). |
| 9 | NewCredentials | A caller cloned its current token and specified new credentials for outbound connections. The new logon session has the same local identity, but uses different credentials for other network connections. |
| 10 | RemoteInteractive | A user logged on to this computer remotely using Terminal Services or Remote Desktop. |
| 11 | CachedInteractive | A user logged on to this computer with network credentials that were stored locally on the computer. The domain controller was not contacted to verify the credentials. |
| 12 | CachedRemoteInteractive | Same as RemoteInteractive. This is used for internal auditing. |
| 13 | CachedUnlock | Workstation logon |
---
---
- Downloaded from author's site:
    - [defaults.txt](defaults.txt)
    - [allowlist.txt](allowlist.txt)
    - [malicious.py](malicious.py)
    - [Firefox.ico](Firefox.ico)
- paramiko
    - low-level SSH handling library
- telnetlib
    - Telnet handling library
- Windows Event Logs
    - Event Codes
    - Logon Types
    - The values in the `EventData` field are called `StringInserts` in Python
- pyinstaller
    - packages Python scripts into exe
- shutil
    - copying/moving/archiving files


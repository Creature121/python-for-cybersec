- This chapter is concerned with the "Persistence" phase of the MITRE ATT&CK framework.
- We will be covering 2 techniques:
    - Boot or Logon Autostart Execution
        - OSs allow users to define their own scripts that run on boot/user logon.
        - Under HKEY_USERS, you can get access to other users
            - through their Windows Security Identifier (SID)
        - [RegAutorun.py](RegAutorun.py)
        - [DetectRegistryAutorun.py](DetectRegistryAutorun.py)
        - > A call to QueryInfoKey returns an array of three values:
                ■ The number of subkeys that the key has
                ■ The number of values that the key has
                ■ The time that the key was last modified in hundreds of nanoseconds since
January 1, 1601
    - Hijack Execution Flow
---
---
- Downloaded from [the author's site](https://www.wiley.com/en-us/Python+for+Cybersecurity%3A+Using+Python+for+Cyber+Offense+and+Defense-p-9781119850649#downloadstab-section):
    - [BuildExe.py](payload/BuildExe.py)
    - [Firefox.ico](payload/Firefox.ico)
    - [malicious.py](payload/malicious.py)
    - Very similar to the stuff we needed in chapter 2.
- Use the Windows Registry to enable persistence through Autorun.
- `pathlib` package can be *really* useful in path related stuff.
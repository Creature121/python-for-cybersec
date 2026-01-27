- Chapter 6 focuses in the "Defense Evasion" phase of the MITRE ATT&CK framework.
    - Focusing on 2 techniques:
        - Hide Artifacts
            - Hide Artifacts technique is passive Defense Evasion
                - Attempts to conceal the attack from cybersecurity products.
            - > Alternate data streams are a more effective means of hiding data on the Windows file system.
                - Example: [benign.txt](benign.txt)
            - [AlternateDataStreams.py](AlternateDataStreams.py)
                - The last line that runs the `wmic` command fails to show the notepad windwow because of how Windows work.
                    - WMIC (a service) runs in Session 0, user logins run in subsequent sessions.
                        - Which basically means any process that has a UI created by WMIC can't be seen by any user.
            -  [DetectADS.py](DetectADS.py)
        - Impair Defenses
            - > The Impair Defenses technique is an example of active Defense Evasion
            - Fully disabling anti-virus software requires:
                - disabling Autorun features
                - terminating existing processes
            - "Services" are another way for programs to auto run.
                - Managed by Windows Service Control Manager (SCM)
            - Many antivirus programs define themselves as services at `HKLM\SYSTEM\CurrentControlSet\Services`
            - [DetectAntivirusService.py](DetectAntivirusService.py)
                - While this only detects, it can be easily changed to deactivate.
                    - Use admin -> SetValueEx -> set value to 0x04
                - On the flip side, can be used by defender instead to detect deactivated antivirus
                    - Search of 0x04 instead of 0x02
            - [TerminateAntivirus.py](TerminateAntivirus.py)
---
---
| VALUE | START TYPE | MEANING |
|-|-|-|
| 0x00 | Boot | This service is needed to use the boot volume device. |
| 0x01 | System | This service is loaded by the I/O subsystem. |
| 0x02 | Autoload | The service is always loaded and run. |
| 0x03 | Manual | This service must be started manually by the user. |
| 0x04 | Disabled | The service is disabled and should not be started. |
---
---
- Alternate Data Streams
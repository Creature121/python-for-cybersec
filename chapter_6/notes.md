- Chapter 6 focuses in the "Defense Evasion" phase of the MITRE ATT&CK framework.
    - Focusing on 2 techniques:
        - Hide Artifacts
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
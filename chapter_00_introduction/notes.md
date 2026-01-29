- Why Python for cybersecurity?
    - Supports automation in the management of cyber risk (prevent malware, d&r attacks, ensure compliance)
    - It's popular/easy/powerful.
---
- MITRE ATT&CK Framework
    - Shows how a cyber attack works;
        > ...breaks it into objectives that the attacker may need to achieve on their way to their final goal.
    - Hierarchy
        - Tactics
            - Techniques / Sub-techniques
    ---
    1. Reconnaisence
    2. Resource Development
    3. Initial Access
    4. Execution
    5. Persistence
    6. Privilege Escalation
    7. Defense Evasion
    8. Credential Access
    9. Discovery
    10. Lateral Movement
    11. Collection
    12. Command and Control
    13. Exfiltration
    14. Impact
---
- Each tactic has its own chapter
    - Except first 2; combined into MITRE Pre-ATT&CK
    - Each chapter explores 2 attack techniques, and how they can be implemented in Python.
        - Followed by a defensive section showing how Python can be used to defend against those techniques.
---
- I will be using Windows 11, no VMs.
- I will be using the UV package manager, not pip.
- I will be writing the code sample from the book by myself.
- I downloaded the `requirements.txt` from https://www.wiley.com/go/pythonforcybersecurity.

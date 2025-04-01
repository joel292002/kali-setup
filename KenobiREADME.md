# TryHackMe - Kenobi Write-Up

## *1. Overview*
- *Target Machine:* Kenobi (TryHackMe)
- *Objective:* Gain root access and retrieve the flag
- *Techniques Used:* Enumeration, NFS Exploitation, Privilege Escalation

---

## *2. Enumeration*
### *2.1 - Nmap Scan*
```bash
nmap -sC -sV -p- -oN scan.txt <Target_IP>

Findings:
![WhatsApp Image 2025-04-01 at 9 18 16 PM](https://github.com/user-attachments/assets/498dd7f2-2361-4a60-a79d-bb9dee3197a6)

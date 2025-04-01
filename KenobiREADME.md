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
![Image](https://github.com/user-attachments/assets/b5b8441f-08f9-45f9-89eb-e9f1275f903e)


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
![Image](https://github.com/user-attachments/assets/24c71557-1cc3-44bb-9676-12f77cc493b0)






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
![Kenobi Write-Up](https://raw.githubusercontent.com/joel292002/kali-setup/main/kenobi-image.png)







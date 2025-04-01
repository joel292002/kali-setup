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
![Image alt ](https://github.com/joel292002/kali-setup/blob/4c690d28c70e172e6b95219890205da1afa86583/WhatsApp%20Image%202025-04-01%20at%209.18.16%20PM.jpeg)

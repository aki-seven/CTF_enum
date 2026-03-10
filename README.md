# CTF_enum
An automation script I developed to help me in CTF recon and enumeration.

### FEATURES ###
Automated Nmap full port scanning
Automatic open port extraction
Service and version detection
Nmap vulnerability script scanning
Web directory enumeration using Feroxbuster

Additional tools menu including:
Gobuster
Recursive Feroxbuster
Nikto
FFUF with extension fuzzing
Automatic result organization by target IP

### REQUIREMENTS ###
python3
nmap
feroxbuster
gobuster
ffuf
nikto

###  INSTALLATION ###
```bash
git clone https://github.com/aki-seven/CTF_enum.git
```

### USAGE ###
```bash
python3 ctf_enum.py --ip <TARGET IP>
```

--- Start Options ---
1) Run port scanning
2) Run web enumeration
3) Open tools menu
 Anything else to Exit
Select an option: 

Select an option in the menu.
1 - To run port scan, service scan, & script=vuln scan
2 - To run an enumeration using Feroxbuster.
3 - To run additional web enumeration

### OUTPUT STRUCTURE ###

The script automatically organizes results into a folder named after the target IP:

TARGET_IP/
 ├── nmap_portscan.txt
 ├── nmap_service_scan.txt
 ├── nmap_vuln_scan.txt
 ├── ferox_common.json
 ├── ferox_raft_medium.json
 ├── ferox_dirbuster_medium.json
 ├── gobuster_common.txt
 ├── ffuf_raft_medium.json
 └── ffuf_extension_raft_medium.json

 

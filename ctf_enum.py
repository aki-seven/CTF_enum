import subprocess
import os
import argparse 

# import cmd # Optional Upgrade
# class QuickShell(cmd.Cmd):
#     prompt = "quickscan> "
#     def do_ferox(self, arg):
#         subprocess.run(f"feroxbuster -u http://{options.ip}", shell=True)
#     def do_nmap(self, arg):
#         subprocess.run(f"nmap {arg}", shell=True)
#     def do_exit(self, arg):
#         return True
# QuickShell().cmdloop()

parser = argparse.ArgumentParser(
    prog='Quick Commands',
    description='Quick Commands: Handy tool for OSCP boxes',
    epilog='ip'
)

parser.add_argument("--ip", help="ip", required=True)# positional arg
options = parser.parse_args()
os.makedirs(options.ip, exist_ok=True)

def nmap_scan():
    # PORT SCAN
    print("[+] Running initial port scan")
    subprocess.run(f"nmap -p- --min-rate 1000  -v -oN {options.ip}/nmap_portscan.txt {options.ip}", shell=True)

    ports = [] 

    with open(f"{options.ip}/nmap_portscan.txt") as f:
        for line in f:
            if "open" in line:
                port = line.split("/")[0]
                ports.append(port)

    ports = ",".join(ports)
    print("[+] Open ports:", ports)

    if not ports:
        print("[-] No open ports found.")
        exit() 

    # SERVICE SCAN
    service_scan = f"nmap -Pn -A -T4 -p{ports} -v -oN {options.ip}/nmap_service_scan.txt {options.ip}"
    print("[+] Running service scan")
    subprocess.run(service_scan, shell=True)

    # --SCRIPT=VULN SCAN
    vuln_script_scan = f"nmap -Pn -A -T4 -p{ports} --script=vuln -v -oN {options.ip}/nmap_vuln_scan.txt {options.ip}"
    print("[+] Running script vuln scan")
    subprocess.run(vuln_script_scan, shell=True) #  Removed , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL

# WEB Enumeration

# Ferox
def web_enumeration():
   
    print("[+] Running web directory scan with common") # used popen instead of run to deduct enuemration time in half or less
    subprocess.run(f"feroxbuster -u {web_url} -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -t 100 -v -o {options.ip}/ferox_common.json", shell=True)
    print("[+] Running web directory scan with raft-medium")
    subprocess.run(f"feroxbuster -u {web_url} -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-words.txt -t 100 -v -o {options.ip}/ferox_raft_medium.json", shell=True)
    print("[+] Running web directory scan with dirbuster-medium")
    subprocess.run(f"feroxbuster -u {web_url} -w /usr/share/wordlists/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt -t 100 -v -o {options.ip}/ferox_dirbuster_medium.json", shell=True)


def additional_tools():
 # NEED TO FIND A WAY TO SKIP TO ADDITIONAL COMMANDS IN CASE ABOVE ONES ARE NOT REQUIRED.
    while True:
        print("\n--- Additional Options ---")
        print("1) Run Gobuster with common.txt")
        print("2) Feroxbuster -r ")
        print("3) Run Nikto")
        print("4) Run ffuf with options filter code 404 and -e .php,.txt,.bak,.zip ")
        print("5) Exit")

        choice = input("Select an option: ")

        if choice == "1":
            print("[+] Running scan with gobuster using common.txt")
            subprocess.run(f"gobuster dir -u {web_url} -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -o {options.ip}/gobuster_common.txt", shell=True)
                        
        elif choice =="2":
            print("[+] Running scan with feroxbuster using recursion")  # temporary solution
            wordlists = ["common.txt", "raft-medium-words.txt","DirBuster-2007_directory-list-2.3-medium.txt"]
            flags="-r"
            for wl in wordlists:
                subprocess.run(f"feroxbuster -u {web_url} -w /usr/share/wordlists/seclists/Discovery/Web-Content/{wl} -t 100 -v {flags} -o {options.ip}/ferox_recursion_{wl}.json", shell=True)


        elif choice == "3":  
            print("[+] Running scan with nikto")
            subprocess.run(f"nikto -h {web_url}", shell=True)

        elif choice == "4":
            print("[+] Running scan with ffuf with raft-medium-words")
            clean_url = web_url.rstrip("/")
            subprocess.run(f" ffuf -u {clean_url}/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-words.txt -fc 404 -o {options.ip}/ffuf_raft_medium.json", shell=True)
            subprocess.run(f" ffuf -u {clean_url}/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-words.txt -e .php,.txt,.bak,.zip -fc 404 -o {options.ip}/ffuf_extension_raft_medium.json", shell=True)

        elif choice == "5":
            print("Exiting...")
            break # instead of break, loop back to additional options after completion of one of adn options until preses 5 for exit
        else:
            print("Invalid option") 

while True:
    print("\n--- Start Options ---")
    print("1) Run port scanning")
    print("2) Run web enumeration")
    print("3) Open tools menu")
    print(" Anything else to Exit")

    choice = input("Select an option: ")
    if choice == "1":
        nmap_scan()
    elif choice == "2":
        web_url = input("Enter web url(http://TARGET:PORT/): ")
        web_enumeration()
    elif choice == "3":
        web_url = input("Enter web url(http://TARGET:PORT/): ")
        additional_tools()
    else:
       print("Exiting...")

       break

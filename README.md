## Automated Nmap Scanner

This script automates the process of scanning IP addresses or ranges using Nmap with seven powerful scanning techniques. It features color-coded output for improved readability:

    Red: Errors and command details
    Green: User prompts and descriptions
    Blue: IP addresses, ports, and service details

### Features

    Select from seven scanning methods
    Enter IP addresses or ranges
    Color-coded output for easy reading
    Breaks between different IP reports for clarity

### Requirements

    Python 3.x
    Nmap installed on the system

### Usage

    Clone the Repository:

    bash

git clone https://github.com/yourusername/nmap-scanner.git
cd nmap-scanner

Run the Script:

    python nmap_scanner.py

    ### Follow the Prompts:
        Enter the IP address or range you want to scan. Here are some examples:
            Single IP Address: 192.168.1.1
            IP Range: 192.168.1.1-192.168.1.10
            Subnet Range: 192.168.1.0/24
        Choose the scan method by entering the corresponding number.

### Scan Methods

    1. SYN Scan (-sS): A stealthy scan that only sends SYN packets.
    2. TCP Connect Scan (-sT): A more reliable scan that completes the TCP handshake.
    3. UDP Scan (-sU): Scans UDP ports, which can be slower and less reliable.
    4. Aggressive Scan (-A): Enables OS detection, version detection, script scanning, and traceroute.
    5. Service Version Detection (-sV): Attempts to determine service versions.
    6. OS Detection (-O): Attempts to determine the operating system of the target.
    7. Full Scan (-p-): Scans all 65,535 TCP ports.

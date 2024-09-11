import os
import subprocess
import re

def print_colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"

def print_ascii_art():
    art = """
⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀
⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣆⠉⠉⢉⣿⣿⣿⣷⣦⣄⡀⠀
⠀⠚⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⣿⡇
⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠈⠃
⠸⠁⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠹⣿⣿⡇⠈⠻⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⡇⠀⠀⠈⠙⠿⣿⠀⠀⠀

Automated Nmap Scanner
"""
    print(print_colored(art, 'red'))

def is_valid_ip_or_range(ip):
    # Pattern to match valid IP address or CIDR notation
    ip_pattern = re.compile(
        r'^(\d{1,3}\.){3}\d{1,3}(/(3[0-2]|[12][0-9]|[0-9]))?$'
    )
    # Validate the IP or CIDR notation
    if ip_pattern.match(ip):
        # Split IP and CIDR parts
        parts = ip.split('/')
        if len(parts) == 2:
            ip_part, cidr_part = parts
            # Validate CIDR part
            if not (0 <= int(cidr_part) <= 32):
                return False
        return True
    return False

def process_nmap_output(output):
    """Process the Nmap output and print the entire IP report in blue, with breaks between IP addresses."""
    lines = output.splitlines()
    ip_start = False  # Track if are at the start of a new IP section

    for line in lines:
        if "Nmap scan report for" in line:
            if ip_start:
                print("\n" + "-" * 40 + "\n")  # Print a break between different IP addresses
            ip_start = True
            print(print_colored(line, 'blue'))  # IP address in blue

        elif ip_start:
            if "open" in line or "Host is up" in line or "MAC Address" in line or "Not shown" in line:
                print(print_colored(line, 'blue'))  # Rest of the IP-related report in blue
            else:
                print(line)  # For other lines, keep default colors

def main():
    print_ascii_art()
    while True:
        print(print_colored("Please enter a valid IP address or IP range:", 'green'))
        ip = input()
        if is_valid_ip_or_range(ip):
            break
        else:
            print(print_colored("Invalid IP address or range. Please try again.", 'red'))

    print(print_colored("Choose a scan method (1-7):", 'green'))
    methods = [
        ("SYN Scan", "-sS", "A stealthy scan that only sends SYN packets."),
        ("TCP Connect Scan", "-sT", "A more reliable scan that completes the TCP handshake."),
        ("UDP Scan", "-sU", "Scans UDP ports, which can be slower and less reliable."),
        ("Aggressive Scan", "-A", "Enables OS detection, version detection, script scanning, and traceroute."),
        ("Service Version Detection", "-sV", "Attempts to determine service versions."),
        ("OS Detection", "-O", "Attempts to determine the operating system of the target."),
        ("Full Scan", "-p-", "Scans all 65,535 TCP ports.")
    ]

    for idx, (name, _, description) in enumerate(methods, 1):
        print(print_colored(f"{idx}. {name}: {description}", 'green'))

    choice = int(input("Enter the number of the scan method you want to use: "))
    if choice < 1 or choice > len(methods):
        print(print_colored("Invalid choice. Exiting.", 'red'))
        return

    method_name, method_flag, _ = methods[choice - 1]
    print(print_colored(f"You selected: {method_name}", 'green'))

    # Execute the selected scan method and capture the output
    command = f"nmap {method_flag} {ip}"
    print(print_colored(f"Executing command: {command}", 'red'))
    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

    # Process and display Nmap output with colored IP addresses and port details
    process_nmap_output(result.stdout)

main()

import os
import subprocess

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
███╗   ██╗███╗   ███╗ █████╗ ██████╗ 
████╗  ██║████╗ ████║██╔══██╗██╔══██╗
██╔██╗ ██║██╔████╔██║███████║██║  ██║
██║╚██╗██║██║╚██╔╝██║██╔══██║██║  ██║
██║ ╚████║██║ ╚═╝ ██║██║  ██║██████╔╝
╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ 

Automated Nmap Scanner
"""
    print(print_colored(art, 'red'))

def process_nmap_output(output):
    """Process the Nmap output and print the entire IP report in blue, with breaks between IP addresses."""
    lines = output.splitlines()
    ip_start = False  # Track if we're at the start of a new IP section

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
    print(print_colored("Please enter an IP address or IP range:", 'green'))
    ip = input()

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

import subprocess
import string
import random
import re

def mac_address_randomgen():
    """Generate and return a Linux Mac address"""
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    mac = ""

    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")

def get_actualmac(iface):
    """Get the actual MAC address"""
    ifconf = subprocess.check_output(f"ifconfig {iface}",shell=True).decode()
    return re.search("ether (.+) ", ifconf).group().split()[1].strip()

def mac_address_specific(iface, new_mac):
    """Change the actual MAC address by"""
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac}", shell=True)
    subprocess.check_output(f"ifconfig {iface} up", shell=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python Mac Changer on Linux")
    parser.add_argument("interface", help="The network interface name on Linux")
    parser.add_argument("-r", "--random", action="store_true", help="Generates a random MAC address")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change to")
    args = parser.parse_args()
    iface = args.interface

    if args.random:
        new_mac_address = mac_address_randomgen()
    elif args.mac:
        new_mac_address = args.mac
    
    old_mac_address = get_actualmac(iface)
    print("[*] Old MAC address:", old_mac_address)
    mac_address_specific(iface, new_mac_address)
    new_mac_address = get_actualmac(iface)
    print("[+] New MAC address:", new_mac_address)

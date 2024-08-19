#!/usr/bin/env python3
import subprocess
from colorama import Fore
import argparse

def get_wireless_interface():
    try:
        result = subprocess.run(['iw', 'dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None

        for line in result.stdout.split('\n'):
            if 'Interface' in line:
                interface_name = line.split()[1]
                return interface_name

    except Exception as e:
        print(Fore.RED + 'An error occurred: ' + Fore.LIGHTRED_EX + str(e) + Fore.WHITE)
        return None

def get_interface_mode(interface):
    try:
        result = subprocess.run(['iwconfig', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None

        for line in result.stdout.split('\n'):
            if 'Mode:' in line:
                mode = line.split('Mode:')[1].split()[0]
                return mode.lower()

    except Exception as e:
        print(Fore.RED + 'An error occurred: ' + Fore.LIGHTRED_EX + str(e) + Fore.WHITE)
        return None

def start_monitor_mode():
    interface_name = get_wireless_interface()
    new_interface_name = 'wlan0'

    if interface_name is None:
        print(Fore.RED + 'No wireless interface found' + Fore.WHITE)
        return

    mode = get_interface_mode(interface_name)
    if mode == 'monitor':
        print(Fore.YELLOW + 'Interface is already in monitor mode' + Fore.WHITE)
        return

    try:
        subprocess.run(f'ifconfig {interface_name} name {new_interface_name}', shell=True)
        subprocess.run(f'ifconfig {new_interface_name} down', shell=True)
        subprocess.run(f'iwconfig {new_interface_name} mode monitor', shell=True)
        subprocess.run(f'ifconfig {new_interface_name} up', shell=True)
        print(Fore.LIGHTGREEN_EX + 'Monitor Mode Enabled Successfully, New Interface Name: ' + Fore.BLUE + new_interface_name + Fore.WHITE)
    except:
        print(Fore.RED + 'Failed To Enable Monitor Mode' + Fore.WHITE)

def stop_monitor_mode():
    new_interface_name = 'wlan0'

    mode = get_interface_mode(new_interface_name)
    if mode == 'managed':
        print(Fore.YELLOW + 'Interface is already in managed mode' + Fore.WHITE)
        return

    try:
        subprocess.run(f'ifconfig {new_interface_name} down', shell=True)
        subprocess.run(f'iwconfig {new_interface_name} mode managed', shell=True)
        subprocess.run(f'ifconfig {new_interface_name} up', shell=True)
        print(Fore.LIGHTGREEN_EX + 'Monitor Mode Disabled, Interface Name: ' + Fore.BLUE + new_interface_name + Fore.WHITE)
    except:
        print(Fore.RED + 'Failed To Disable Monitor Mode' + Fore.WHITE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wireless Interface Monitor Mode Script')
    parser.add_argument('-start', action='store_true', help='Enable monitor mode')
    parser.add_argument('-stop', action='store_true', help='Disable monitor mode')

    args = parser.parse_args()

    if args.start:
        start_monitor_mode()
    elif args.stop:
        stop_monitor_mode()
    else:
        parser.print_help()

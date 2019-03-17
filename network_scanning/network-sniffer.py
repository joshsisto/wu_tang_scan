
import os
import re
import sys
import speedtest


def spd_tst():
    get_ip_addr()
    print()
    speedtester = speedtest.Speedtest()
    speedtester.get_best_server()
    speedtester.download()
    speedtester.upload()
    res = speedtester.results.dict()
    print(res["download"] / 1000000, "⬇️ Down️", res["upload"] / 1000000, "⬆️ Up", "Ping", res["ping"], "ms")


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


platform = get_platform()
print(f'Platform:{platform}')

# Terminal Commands
get_ip_cmd = """ ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' """
get_pub_ip_cmd = """ curl 'https://api.ipify.org?format=json' """
nmap_net_scan_cmd = """ sudo -S nmap -sS -O -PI -PT -oX nmap_scan.xml 192.168.88.1/24 """
nmap_web_scan_cmd = """ nmap """
# Regex
regex_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"


def get_ip_addr():
    ip_addresses = os.popen(get_ip_cmd).read()
    ip_addr_list = re.findall(regex_ip, ip_addresses)
    print("IP Addresses")
    print(ip_addr_list)
    print()
    public_ip = os.popen(get_pub_ip_cmd).read()
    print()
    print(f'Public IP:{public_ip}')


def nmap_net_scan():
    net_scan = os.popen(nmap_net_scan_cmd).read()
    print(net_scan)


def scan_website():
    site = input("what site would you like to scan?\n")
    scan = os.popen(nmap_web_scan_cmd + site).read()
    return print(scan)


# nmap_results = open("nmap.txt", 'r').read()
# nmap_results = nmap_results.split('\n\n')
# print(nmap_results[3])
# print(len(nmap_results))


# spd_tst()
# scan_website()
# get_ip_addr()
nmap_net_scan()





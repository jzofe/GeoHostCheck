#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Geo Host Checker – Ender Topluluk  |  <scriptkidsensei> 

import os
import random
import requests
import sys
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)
kalin = Style.BRIGHT
kirmizi = Fore.RED
yesil = Fore.GREEN
mavi = Fore.BLUE
sari = Fore.YELLOW
sil = Style.RESET_ALL

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/129 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 Firefox/131.0",
]

filename = "proxy_list.txt"

def yslx(msg): print(f"{kalin}{yesil}[{datetime.now().strftime('%H:%M:%S')}]{sil}  {msg}")
def kirx(msg): print(f"{kalin}{kirmizi}[{datetime.now().strftime('%H:%M:%S')}]{sil} ! {msg}")
def sarx(msg): print(f"{kalin}{sari}[{datetime.now().strftime('%H:%M:%S')}]{sil} * {msg}")
def user2(msg): print(f"{kalin}{mavi}[USER-AGENT]{sil} X {msg}")

def get_location(ip):
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,city,regionName,message", 
            timeout=8
        )
        r.raise_for_status() 
        j = r.json()
        
        if j.get("status") == "success":
            city = j.get('city') if j.get('city') else 'N/A City'
            region = j.get('regionName') if j.get('regionName') else 'N/A Region'
            country = j.get('country') if j.get('country') else 'N/A Country'
            return f"{country} • {city} • {region}"
        
        elif j.get("status") == "fail" and j.get("message"):
            return f"API Failed: {j['message']}"

    except requests.exceptions.Timeout:
        return "Location Timeout"
    except requests.exceptions.RequestException as e:
        return "Location Error" 
    except Exception:
        return "Location Error"
    
    return "Location Error"

def load_proxy_list():
    try:
        with open(filename, "r") as f:
            proxies = [p.strip() for p in f if p.strip()]
        if not proxies: raise
        return proxies
    except:
        kirx("proxy_list.txt is empty")
        return []

def save_proxy_list(proxies):
    with open(filename, "w") as f:
        for p in proxies:
            f.write(p + "\n")

def get_proxy_list():
    sarx("Proxies are being downloaded auto from the internet, please wait...")
    url = "https://free.redscrape.com/api/proxies?&protocol=http&max_timeout=1500&format=txt"
    try:
        r = requests.get(url, timeout=20)
        proxies = [line.strip() for line in r.text.splitlines() if line.strip()]
        save_proxy_list(proxies)
        yslx(f"{len(proxies)} Finished! -> proxy_list.txt")
        return proxies
    except:
        kirx("Something is wrong")
        return []

def count_proxies(): 
    return len(load_proxy_list())

def check_http_tls(target, proxy):
    ip = proxy.split(":")[0]
    location = get_location(ip) 
    ua = random.choice(user_agents)
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    headers = {"User-Agent": ua}

    for proto in ["http", "https"]:
        try:
            r = requests.get(f"{proto}://{target}", headers=headers, proxies=proxies, timeout=12, allow_redirects=True)
            status_code = str(r.status_code)
            
            if r.status_code < 400:
                yslx(f"{'UP!':^5} | {target:^25} | {proto.upper():^8} | {proxy:^22} | {location:^35} | {status_code:^6}")
                return True
            else:
                kirx(f"{'DOWN':^5} | {target:^25} | {proto.upper():^8} | {proxy:^22} | {location:^35} | {status_code:^6}")
        except requests.exceptions.Timeout:
            kirx(f"{'DOWN':^5} | {target:^25} | {proto.upper():^8} | {proxy:^22} | {location:^35} | {'Timeout':^6}")
        except requests.exceptions.RequestException:
            kirx(f"{'DOWN':^5} | {target:^25} | {proto.upper():^8} | {proxy:^22} | {location:^35} | {'Error':^6}")
    
    return False

def check_tcp(target, port, proxy):
    ip = proxy.split(":")[0]
    location = get_location(ip)
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        with requests.Session() as s:
            s.proxies.update(proxies)
            resp = s.send(requests.Request("CONNECT", f"{target}:{port}").prepare(), timeout=10)
            
            status_code = str(resp.status_code)

            proto_str = f"TCP:{port}"

            if resp.status_code in [200, 201]:
                yslx(f"{'UP!':^5} | {target:^25} | {proto_str:^8} | {proxy:^22} | {location:^35} | {status_code:^6}")
                return True
            else:
                kirx(f"{'DOWN':^5} | {target:^25} | {proto_str:^8} | {proxy:^22} | {location:^35} | {status_code:^6}")
                return False
    except requests.exceptions.Timeout:
        proto_str = f"TCP:{port}"
        kirx(f"{'DOWN':^5} | {target:^25} | {proto_str:^8} | {proxy:^22} | {location:^35} | {'Timeout':^6}")
    except requests.exceptions.RequestException:
        proto_str = f"TCP:{port}"
        kirx(f"{'DOWN':^5} | {target:^25} | {proto_str:^8} | {proxy:^22} | {location:^35} | {'Error':^6}")
    return False

def start_check(target, protocol, tcp_ports=None): 
    os.system('clear && cfonts GeoHC -f 3d -c red')
    proxy_list = load_proxy_list()
    if not proxy_list:
        kirx("Proxy list is empty. Try [3]")
        time.sleep(2)
        return

    print(f"""
                     [Geo Host Checker] by Fyks {Fore.MAGENTA}<scriptkidsensei>{sil}

                      HOST: >{target}< | Total proxy : {kalin}{sari}{len(proxy_list)}{sil} | {protocol.upper()}

                                      Exit : {Fore.RED}Q{sil}
    """)
    
    print(f"{'STATUS':^5} | {'TARGET':^25} | {'PROTO':^8} | {'PROXY':^22} | {'LOCATION':^35} | {'RESULT':^6}\n" + "─"*120)

    used = set()
    for proxy in proxy_list:
        if proxy in used: continue
        used.add(proxy)

        is_up = False
        if protocol.upper() in ["HTTP", "TLS", "ALL"]:
            if check_http_tls(target, proxy):
                is_up = True

        if protocol.upper() in ["TCP", "ALL"] and not is_up and tcp_ports: 
            for port in tcp_ports:
                if check_tcp(target, port, proxy):
                    is_up = True
                    break

        time.sleep(0.8)  

    input(f"\n{kalin}{yesil} finish. press enter for back to menu.{sil}")


def get_tcp_ports():
    default_ports = "80,443,8080,8443"
    
    print(f"\n> Enter ports to check (e.g., 80,443,21,22).")
    ports_input = input(f"> Press Enter for default ({default_ports}): ").strip()
    
    if not ports_input:
        ports_input = default_ports

    try:
        ports_list = [int(p.strip()) for p in ports_input.split(',') if p.strip().isdigit() and 1 <= int(p.strip()) <= 65535]
        if not ports_list:
            kirx("Invalid port list. Default ports will be used.")
            return [80, 443, 8080, 8443]
        return ports_list
    except:
        kirx("Error: Ports must be numbers. Default ports will be used.")
        return [80, 443, 8080, 8443]


def main():
    while True:
        os.system('clear && cfonts GeoHC -f 3d -c red')
        proxy_count = count_proxies()
        print(f"""
              [Geo {Fore.RED}H{Style.RESET_ALL}ost {Fore.RED}C{Style.RESET_ALL}hecker] by Fyks {Fore.MAGENTA}<scriptkidsensei>{Style.RESET_ALL} | Proxies {kalin}{sari}{proxy_count}{sil}
                                {Style.BRIGHT}Web{Style.RESET_ALL} - endertopluluk.com
      [X] Main
      |
      ├── [1] Start
      ├── [2] IP Lookup
      ├── [3] Search Proxies [AUTO]
      └── [4] Delete proxies

              | {Fore.RED}[5] Exit{Style.RESET_ALL} |
                ────────
        """)
        choice = input(f"{kalin}{yesil}root{sil}@geohc >_ ")

        if choice == "1":
            os.system('clear && cfonts GeoHC -f 3d -c red')
            target = input(f" {yesil}root{sil}@geohc/host IP/Domain >_ ")
            if not target: continue
            print("\nPROTOCOLS")
            print("HTTP, TLS, TCP, ALL")
            proto = input("\n> Select a protocol : ").strip()
            
            tcp_ports = None
            if proto.upper() in ["TCP", "ALL"]:
                tcp_ports = get_tcp_ports() 

            if proto.upper() not in ["HTTP","TLS","TCP","ALL"]:
                proto = "ALL"

            start_check(target, proto, tcp_ports) 

        elif choice == "2":
            os.system('clear && cfonts GeoHC -f 3d -c red')
            ip = input("IP >_ ")
            infoxx(ip)

        elif choice == "3":
            get_proxy_list()

        elif choice == "4":
            open(filename, "w").close()
            yslx("proxy_list.txt deleted!")

        elif choice == "5":
            yslx("Goodbye!")
            break

if __name__ == "__main__":
    main()

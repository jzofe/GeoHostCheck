import os
import time
import argparse
import sys
import requests
from requests import get
import bs4
from bs4 import BeautifulSoup
import subprocess
import scapy
from datetime import datetime
import signal
from colorama import init, Fore, Style
from scapy.all import *
from urllib.parse import urlparse
import socket
import tkinter as tk
import random
from requests.exceptions import RequestException

os.system('clear')
os.system('echo -e "\033]0;GeoHostChecker \007"')
ping_listener = None

user_agents =  [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/52.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 5.1.1; ASUS_X00BD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 9; SM-A530W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 5.0; SM-N900) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 11; SM-N770F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.101 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 7.0; LGMP450) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36"
        "Dalvik/2.1.0 (Linux; U; Android 8.1.0; GOME 2018X38A Build/O11019)"
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/129.0.336390422 Mobile/15E148 Safari/604.1"
        "Mozilla/5.0 (Linux; Android 9; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36"
        "Mozilla/5.0 (Linux; Android 9; SM-N976N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.90 Mobile Safari/537.36"
        "Dalvik/1.6.0 (Linux; U; Android 8.1.0; E100 Build/KOT49H)"
]


def get_user_agent():
    return random.choice(user_agents)

def get_ip_info(target_ip):
    url = f"https://ipinfo.io/{target_ip}/json"
    response = requests.get(url)
    data = response.json()
    return data

def check():
    def on_key_release(key):
        if key == keyboard.Key.esc:
            return_to_main_menu()
        elif hasattr(key, 'char') and key.char.upper() == 'Q':
            return_to_main_menu()

    proxy_count = count_proxies(filename)

    ip_menu = f"""
                     [Geo Host Checker] by Fyks {Fore.MAGENTA}<scriptkidsensei>{Style.RESET_ALL}

        Total proxy : {kalin}{sari}{proxy_count}{sil}
    """
    os.system('clear')
    os.system('clear && cfonts GeoHC -f 3d -c red')
    print(ip_menu)
    target_ip = input(f" {Fore.GREEN}root{Style.RESET_ALL}@geohc/host IP/Domain >_ ")
    print("")
    print("PROTOCOLS")
    print("HTTP, TLS, UDP, TCP, ICMP | DNS")
    print("")
    protocol = input("> Select a protocol : ")
    ping_menu = f"""
                     [Geo Host Checker] by Fyks {Fore.MAGENTA}<scriptkidsensei>{Style.RESET_ALL}

                      IP : >{target_ip}< | Total proxy : {kalin}{sari}{proxy_count}{sil} | {protocol}

                                      Exit : {Fore.RED}Q{Style.RESET_ALL}

    """
    os.system('clear')
    os.system('clear && cfonts GeoHC -f 3d -c red')
    print(ping_menu)

    proxy_list = load_proxy_list("proxy_list.txt")
    current_proxy_index = 0

    while current_proxy_index < len(proxy_list):
        proxy = proxy_list[current_proxy_index]
        proxy_address, proxy_port = proxy.split(':')
        user_agent = get_user_agent()
        result = ping_with_proxy(target_ip, proxy_list, proxy_address, proxy_port, protocol, user_agent)

        if not result:
            current_proxy_index += 1
        else:
            current_proxy_index = (current_proxy_index + 1) % len(proxy_list)

    return_to_main_menu()

def check_dependencies():
    try:
        import requests
        from requests import get
    except ImportError:
        print("Some modules are missing. loading...")
        subprocess.check_call(["pip", "install", "requests"])

    try:
        import bs4
        from bs4 import BeautifulSoup
    except ImportError:
        print("Some modules are missing. loading...")
        subprocess.check_call(["pip", "install", "bs4"])

    try:
        import colorama
        from colorama import init, Fore, Style
    except ImportError:
        print("Some modules are missing. loading...")
        subprocess.check_call(["pip", "install", "colorama"])

check_dependencies()

init(autoreset=True)

kalin = Style.BRIGHT
kirmizi = Fore.RED
yesil = Fore.GREEN
mavi = Fore.BLUE
sari = Fore.YELLOW
sil = Style.RESET_ALL

def yslx(message):
    current_time = datetime.now().strftime(' INFO ')
    formatted_message = f"{kalin}{yesil}[{current_time}]{sil}  {message}"
    print(formatted_message)
def exit(message):
    current_time = datetime.now().strftime(' GOODBYE! ')
    formatted_message = f"{kalin}{yesil}[{current_time}]{sil}  {message}"
    print(formatted_message)

def sarx(message):
    current_time = datetime.now().strftime('CHECKING')
    formatted_message = f"{kalin}{sari}[{current_time}]{sil} * {message}"
    print(formatted_message)

def max(message):
    current_time = datetime.now().strftime(' INFO ')
    formatted_message = f"{kalin}{mavi}[{current_time}]{sil} * {message}"
    print(formatted_message)

def max1(message):
    current_time = datetime.now().strftime(' INFO ')
    formatted_message = f"{kalin}{sari}[{current_time}]{sil} * {message}"
    print(formatted_message)

def kirx(message):
    current_time = datetime.now().strftime('ERROR : %H:%M:%S')
    formatted_message = f"{kalin}{kirmizi}[{current_time}]{sil} ! {message}"
    print(formatted_message)

def user2(message):
    current_time = datetime.now().strftime(' USER-AGENT ')
    formatted_message = f"{kalin}{mavi}[{current_time}]{sil} X {message}"
    print(formatted_message)



def calculate_checksum(source_string):
    sum = 0
    countTo = (len(source_string) // 2) * 2

    count = 0
    while count < countTo:
        thisVal = source_string[count+1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2

    if countTo < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

def add_root_prompt():
    print(f"{Style.BRIGHT}{Fore.GREEN}root{Style.RESET_ALL}@geohc >_ ")

def get_proxy_list():
    url = "https://free-proxy-list.net/#list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }

    response = get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        proxy_list = []

        for row in soup.find_all("tr")[1:]:
            columns = row.find_all("td")
            if len(columns) >= 8:
                ip = columns[0].get_text()
                port = columns[1].get_text()
                proxy = f"{ip}:{port}"
                proxy_list.append(proxy)

        return proxy_list
    else:
        kirx("ERROR :", response.status_code)
        return []


def load_proxy_list(file_path):
    try:
        with open(file_path, 'r') as file:
            proxy_list = file.read().splitlines()
            if not proxy_list:
                raise ValueError("Proxy list is empty")
        return proxy_list
    except FileNotFoundError:
        yslx("Proxy list file not found. being created...")
        os.system('sudo touch proxy_list.txt')
        sys.exit(1)
    except PermissionError:
        kirx("You need root permissions to run this script. Try running with 'sudo su' command.")
        sys.exit(1)
    except ValueError as e:
        kirx(f"Error: {str(e)}")
        sys.exit(1)

def send_tcp_request(target_ip, tcp_port, protocol, proxy_address, user_agent):
    location_info = get_location_info(proxy_address)
    location_str = f"{Fore.MAGENTA}LOCATION: Unknown{Style.RESET_ALL}"
    if location_info:
        location_str = f"{Fore.MAGENTA}LOCATION: {location_info['country']}, {location_info['city']}, {location_info['region']}{Style.RESET_ALL}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((target_ip, tcp_port))
        request = "Hello!"
        request_bytes = request.encode()
        client_socket.send(request_bytes)
        response = client_socket.recv(1024)
        client_socket.sendto(request_bytes, (target_ip, tcp_port))
        yslx(f"UP! | {target_ip} {location_str} | {protocol}")
    except ConnectionRefusedError:
        kirx("DOWN | Connection refused | LOCATION {location_str}")
        print("")
        time.sleep(2)
    except ConnectionResetError as e:
        kirx("Connection reset by peer. Retrying...")
        retries += 1
        time.sleep(1)
    except Exception as e:
        print("An error occurred:", str(e))
        print("")
        time.sleep(2)
    finally:
        client_socket.close()

def save_to_file(proxy_list):

    with open("proxy_list.txt", "w") as file:
        for proxy in proxy_list:
            file.write(proxy + "\n")

def get_location_info(proxy_address):
    url = f"http://ip-api.com/json/{proxy_address}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def follow_redirects(client_socket, request, max_redirects=5):
    redirects = 0
    while redirects < max_redirects:
        client_socket.send(request.encode())
        response = client_socket.recv(4096).decode()

        if "HTTP/1.1 301 Moved Permanently" in response:
            redirects += 1
            new_location = response.split('Location: ')[1].split('\r\n')[0]
            new_host = urlparse(new_location).netloc
            new_request = f"GET {new_location} HTTP/1.1\r\nHost: {new_host}\r\n\r\n"
            request = new_request
        else:
            if not response.strip():
                print("Empty response. No content received.")
                print("")
                time.sleep(1.1)
            else:
                print(response)
            break

def custom_print(message):
    print(message)
    print(f"{Style.BRIGHT}{Fore.GREEN}root{Style.RESET_ALL}@geohc >_ ")

def send_udp_packet(target_ip, target_port, protocol, proxy_address):
    location_info = get_location_info(proxy_address)
    location_str = f"{Fore.MAGENTA}LOCATION: Unknown{Style.RESET_ALL}"
    if location_info:
            location_str = f"{Fore.MAGENTA}LOCATION: {location_info['country']}, {location_info['city']}, {location_info['region']}{Style.RESET_ALL}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "UDP"
    message_bytes = message.encode()

    try:
        client_socket.sendto(message_bytes, (target_ip, target_port))
        yslx(f"UP! | {target_ip} {location_str} | {protocol}")
        print("")
    except Exception as e:
        kirx(f"An error occurred:", str(e))
        print("")
        time.sleep(1.1)
    finally:
        client_socket.close()

def send_tls_request(target_ip, tls_port, protocol, proxy_address, user_agent):
    location_info = get_location_info(proxy_address)
    location_str = f"{Fore.MAGENTA}LOCATION: Unknown{Style.RESET_ALL}"

    if location_info:
        location_str = f"{Fore.MAGENTA}LOCATION: {location_info['country']}, {location_info['city']}, {location_info['region']}{Style.RESET_ALL}"

    try:
        response = requests.get(f"https://{target_ip}", headers=headers, proxies={"http": f"http://{proxy_address}:{tls_port}"}, timeout=10)

        if response.status_code == 200:
            response_text = response.text
            yslx(f"UP! | {target_ip} | {location_str} | {protocol}")
            return response_text
        else:
            kirx("DOWN! | LOCATION {location_str}")
            print("")
            user2(f"Host DOWN. User-agent changed to: {user_agent}")
            print("")
            time.sleep(1.1)
            return None

    except RequestException as e:
        kirx(f"An error occurred: {str(e)}")
        kirx(f"DOWN | {target_ip} | {location_str} | {protocol}")
        print("")
        user2(f"Host DOWN. User-agent changed to: {user_agent}")
        print("")
        time.sleep(1.1)
        return None

def send_http_request(target_ip, port, protocol, proxy_address, user_agent):
    location_info = get_location_info(proxy_address)
    location_str = f"{Fore.MAGENTA}LOCATION: Unknown{Style.RESET_ALL}"

    if location_info:
        location_str = f"{Fore.MAGENTA}LOCATION: {location_info['country']}, {location_info['city']}, {location_info['region']}{Style.RESET_ALL}"

    request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"

    try:
        response = requests.get(f"http://{target_ip}", headers=headers)

        if response.status_code == 200:
            response_text = response.text
            yslx(f"UP! | {target_ip} | {location_str} | {protocol}")
            return response_text
        else:
            kirx(f"DOWN! | LOCATION {location_str}")
            print("")
            user2(f"Host DOWN. User-agent changed to: {user_agent}")
            print("")
            time.sleep(1.1)
            return None

    except Exception as e:
        kirx(f"An error occurred: {str(e)}")
        kirx(f"DOWN | {target_ip} | {location_str} | {protocol}")
        print("")
        print(f"Host DOWN. User-agent changed to: {user_agent}")
        print("")
        time.sleep(1.1)
        return None
headers = {
    "User-Agent": get_user_agent(),
}

def resolve_ip_to_hostname(target_ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(target_ip)
        return hostname
    except socket.herror as e:
        kirx(f"Failed to resolve IP address {target_ip} to hostname: {str(e)}")
        return None

def send_tls_request_to_dns(target_ip, tls_port, protocol, proxy_address, user_agent):
    location_info = get_location_info(proxy_address)
    location_str = f"{Fore.MAGENTA}LOCATION: Unknown{Style.RESET_ALL}"

    if location_info:
        location_str = f"{Fore.MAGENTA}LOCATION: {location_info['country']}, {location_info['city']}, {location_info['region']}{Style.RESET_ALL}"

    url = f"https://{target_ip}"
    try:
        response = requests.get(f"https://{target_ip}", headers=headers, proxies={"http": f"http://{proxy_address}:{tls_port}"}, timeout=10)

        if response.status_code == 200:
            response_text = response.text
            yslx(f"UP! | {target_ip} | {location_str} | {protocol}")
            return response_text
        else:
            kirx("DOWN! | LOCATION {location_str}")
            print("")
            user2(f"Host DOWN. User-agent changed to: {user_agent}")
            print("")
            time.sleep(1.1)
            return None

    except RequestException as e:
        kirx(f"An error occurred: {str(e)}")
        kirx(f"DOWN | {target_ip} | {location_str} | {protocol}")
        print("")
        user2(f"Host DOWN. User-agent changed to: {user_agent}")
        print("")
        time.sleep(1.1)
        return None

def get_ip_info2(infoxb):
    url = f"https://ipinfo.io/{infoxb}/json"
    response = requests.get(url)
    data = response.json()
    return data

def ping_with_proxy(target_ip, proxy_list, proxy_address, proxy_port, protocol, user_agent):
    ping_count = 0
    down_count = 0
    info = get_ip_info(target_ip)
    print(f" {Style.BRIGHT}{Fore.GREEN}< IP INFO >{sil}")
    print(f"| >>> Location:", info.get("country"))
    print(f"| >> ISP:", info.get("org"))
    print("")

    while True:
        if down_count >= 2:
            user_agent = get_user_agent()
            print(f"Host DOWN. User-agent changed to: {user_agent}")
            print("")
            down_count = 0

        random_proxy = random.choice(proxy_list)
        proxy_address, proxy_port = random_proxy.split(':')

        sarx(f"CHECKING {target_ip} | PROXY | {proxy_address} | PORT | {proxy_port} | PROTOCOL | {protocol}" )
        location_info = get_location_info(proxy_address)
        location_str = f"{Fore.MAGENTA}LOCATION: Unknown{Style.RESET_ALL}"

        if location_info and 'country' in location_info and 'city' in location_info and 'region' in location_info:
            location_str = f"{Fore.MAGENTA}LOCATION: {location_info['country']}, {location_info['city']}, {location_info['region']}{Style.RESET_ALL}"

        try:
            if protocol == "ICMP":
                response = sr1(IP(dst=target_ip) / ICMP(), verbose=0, timeout=2)
                if response:
                    if response.haslayer(ICMP):
                        if response[ICMP].type == 0:
                            yslx(f"UP! | {target_ip} | {location_str} | {protocol}")
                            print("")
                            if "DOWN" in response:
                                down_count += 1
                                if down_count >= 2:
                                    user_agent = get_user_agent()
                                    user2(f"Host DOWN. User-agent changed to: {user_agent}")
                            else:
                                down_count = 0
                        else:
                            kirx(f"DOWN! | {target_ip} | LOCATION : {location_str}")
                            print("")
                            time.sleep(1.1)
                    else:
                        kirx(f"DOWN! | LOCATION {location_str}")
                        print("")
                        user2t(f"Host DOWN. User-agent changed to: {user_agent}")
                        print("")
                else:
                    kirx(f"DOWN! | LOCATION {location_str}")
                    print("")
                    user2(f"Host DOWN. User-agent changed to: {user_agent}")
                    print("")
            elif protocol == "HTTP":
                response = send_http_request(target_ip, port, protocol, proxy_address, user_agent)
                if response:
                    if "DOWN" in response:
                        down_count += 1
                        if down_count >= 2:
                            new_user_agent = get_user_agent()
                            if new_user_agent != user_agent:
                                print(f"Host DOWN. User-agent changed from {user_agent} to {new_user_agent}")
                            user_agent = new_user_agent
                            print(f"Host DOWN. User-agent changed to: {user_agent}")
                    else:
                        down_count = 0
            elif protocol == "UDP":
                send_udp_packet(target_ip, udp_port, protocol, proxy_address)
            elif protocol == "DNS":
                send_tls_request_to_dns(target_ip, tls_port, protocol, proxy_address, user_agent)
            elif protocol == "TCP":
                send_tcp_request(target_ip, tcp_port, protocol, proxy_address, user_agent)
            elif protocol == "TLS":
                send_tls_request(target_ip, tls_port, protocol, proxy_address, user_agent)
            else:
                kirx("Invalid protocol. Press 'CTRL+C'")
        except KeyboardInterrupt:
            kirx("GeoHC Stopped by user.")
        except socket.gaierror as e:
            kirx("Name or service not known")
            return_to_main_menu()
        except PermissionError:
            print("You need root permissions to run this script. Try running with 'sudo su' command.")
            sys.exit(1)

        ping_count += 1
        if ping_count >= 1:
            time.sleep(1.1)

        time.sleep(1.1)


def return_to_main_menu():
    main()

def handle_interrupt(signal, frame):
    sarx("Connection stopped by user.")
    sys.exit(0)

def count_proxies(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        proxy_count = len(lines)
        return proxy_count
    except FileNotFoundError:
        return 0

filename = "proxy_list.txt"

proxy_count = count_proxies(filename)

class MenuItem:
    def __init__(self, name):
        self.name = name
        self.submenu = {}

    def add_submenu(self, name, submenu):
        self.submenu[name] = submenu

    def display(self, depth=0):
        print("  " * depth + self.name)
        for key, submenu in self.submenu.items():
            submenu.display(depth + 1)

def infoxx(infoxb):
    ip_info = get_ip_info2(infoxb)
    os.system('cfonts GeoHC -f 3d -c "#FE0000" --align center')
    if "ip" in ip_info:
        print(f"                            - IP: {ip_info['ip']}")
        print("")
    if "hostname" in ip_info:
        print(f"                            > {Style.BRIGHT}HOSTNAME{sil}: {ip_info['hostname']}")
    if "city" in ip_info:
        print(f"                            > {Style.BRIGHT}CITY{sil}: {ip_info['city']}")
    if "region" in ip_info:
        print(f"                            > {Style.BRIGHT}REGION{sil}: {ip_info['region']}")
    if "country" in ip_info:
        print(f"                            > {Style.BRIGHT}COUNTRY{sil}: {ip_info['country']}")
    if "org" in ip_info:
        print(f"                            > {Style.BRIGHT}ISP{sil}: {ip_info['org']}")


menu = f"""
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
"""
menu2 = f"""
             [Geo {Fore.RED}H{Style.RESET_ALL}ost {Fore.RED}C{Style.RESET_ALL}hecker] by Fyks {Fore.MAGENTA}<scriptkidsensei>{Style.RESET_ALL} | Proxies {kalin}{sari}{proxy_count}{sil}


         | [1] Check
         | [2] Search Proxies [AUTO]
         | [3] Delete proxies

                  | {Fore.RED}[3] Exit{Style.RESET_ALL} |
                   ───────────
"""
def main():
    os.system('clear')
    os.system('clear && cfonts GeoHC -f 3d -c red')
    print(menu)
    choice = input(f"{Style.BRIGHT}{Fore.GREEN}root{Style.RESET_ALL}@geohc >_ ")

    if choice == "1":
        check()
    elif choice == "3":
        max1("Proxies are being downloaded automatically from the internet, please wait...")
        proxy_list = get_proxy_list()

        if proxy_list:
            save_to_file(proxy_list)
            yslx("Finished! proxy_list.txt")
            time.sleep(1)
        else:
            kirx("ERROR")
    elif choice == "4":
        yslx("Proxies deleted.")
        with open(filename, "r+") as file:
            file.truncate(0)
    elif choice == "2":
        os.system('clear')
        os.system('clear && cfonts GeoHC -f 3d -c red')
        print("                                   IP LOOKUP                  ")
        infoxb = input(f"IP >_ ")
        os.system('clear')
        infoxx(infoxb)
    elif choice == "5":
        yslx("Goodbye!")
        sys.exit(0)

def clis():
    parser = argparse.ArgumentParser(description="GeoHostChecker")
    parser.add_argument("ip", type=str, nargs='?', help="IP address or domain name")
    parser.add_argument("protocol", type=str, nargs='?', help="Protocol to check (e.g., HTTP, ICMP)")
    parser.add_argument("--delete-proxy-list", action="store_true", help="Delete proxy list")
    parser.add_argument("--install-proxy-list", action="store_true", help="Install proxy list from the internet")
    parser.add_argument("--info", action="store_true", help="IP Lookup")

    args = parser.parse_args()

    if args.install_proxy_list:
        max1("Proxies are being downloaded automatically from the internet, please wait...")
        proxy_list = get_proxy_list()

        if proxy_list:
            save_to_file(proxy_list)
            yslx("Finished! proxy_list.txt")
            time.sleep(1)
        else:
            kirx("ERROR")
        sys.exit(0)

    elif args.delete_proxy_list:
         max1("Proxy list deleted")
         with open(filename, "r+") as file:
            file.truncate(0)

    elif args.info:
        infoxb = args.ip
        os.system('clear')
        infoxx(infoxb)

    if (not args.ip or not args.protocol) and not args.install_proxy_list and not args.delete_proxy_list:
        print("")
        print("Usage: python3 geohc.py <ip> <protocol>")
        sys.exit(1)

    target_ip = args.ip
    protocol = args.protocol
    check_ip_protocol_from_args(target_ip, protocol)

def check_ip_protocol_from_args(target_ip, protocol):
    try:
        proxy_list = load_proxy_list("proxy_list.txt")
        proxy_count = count_proxies("proxy_list.txt")
        user_agent = get_user_agent()

        ping_menu = """
                         [Geo Host Checker] by Fyks {}<scriptkidsensei>{}{}

                          IP : >{}< | Total proxy : {}{}{} | {}

                                          Exit : {}Q{}
        """.format(Fore.MAGENTA, Style.RESET_ALL, target_ip, kalin, Fore.MAGENTA, Style.RESET_ALL, proxy_count, sil, protocol, Fore.RED, Style.RESET_ALL)

        os.system('clear && cfonts GeoHC -f 3d -c red')
        print(ping_menu)

        current_proxy_index = 0

        while current_proxy_index < len(proxy_list):
            proxy = proxy_list[current_proxy_index]
            proxy_address, proxy_port = proxy.split(':')
            user_agent = get_user_agent()
            result = ping_with_proxy(target_ip, proxy_list, proxy_address, proxy_port, protocol, user_agent)

            if not result:
                current_proxy_index += 1
            else:
                current_proxy_index = (current_proxy_index + 1) % len(proxy_list)
        ping_with_proxy(target_ip, proxy_list, proxy_address, proxy_port, protocol, user_agent)
    except PermissionError:
        print("You need root permissions to run this script. Try running with 'sudo su' command.")
        sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    tcp_port = 58200 
    udp_port = 53
    port = 80
    tls_port = 443
    filename = "proxy_list.txt"

    if "--install-proxy-list" in sys.argv:
        os.system('clear && cfonts GeoHC -f 3d -c red')
        clis()
    else:
        if len(sys.argv) == 3:
            clis()
        elif len(sys.argv) > 3:
            kirx("Too many arguments. Usage: python3 geohc.py <ip> <protocol>")
        elif "--delete-proxy-list" in sys.argv:
            os.system('clear && cfonts GeoHC -f 3d -c red')
            clis()
        elif "--info" in sys.argv:
            clis()
        elif "-h" in sys.argv:
            clis()
        else:
            main()

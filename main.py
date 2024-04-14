from time import sleep
from datetime import *
from os import name
import subprocess
import threading
import requests
import socket
import json

with open('settings.json') as f:
    settings = json.load(f)
    base_ip = settings.get("base_ip")
    start_ip = settings.get("start_ip")
    end_ip = settings.get("end_ip")
    max_threads = settings.get("max_threads")
    ports = settings.get("ports")
    timeout = settings.get("timeout")

class Ip_tools:
    def dns(self, domain):
        try:
            print(socket.gethostbyname(domain))
        except Exception as e:
            print(f"An error occurred: {e}")

    def ip_to_location(self, ip_address):
        try:
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            location_data = {
                "latitude": response.get("latitude"),
                "longitude": response.get("longitude")
            }
            
            latitude = location_data.get("latitude")
            longitude = location_data.get("longitude")

            location_data = {
                "ip": ip_address,
                "city": response.get("city"),
                "region": response.get("region"),
                "country": response.get("country_name"),
                "latitude": response.get("latitude"),
                "longitude": response.get("longitude"),
                "Google Maps": f"https://maps.google.com/?q={latitude},{longitude}"
            }
            for x in location_data:
                print(f"{x} : {location_data[x]}")
        except Exception as e:
            print(f"An error occurred: {e}")

class Ip_scanner:
    def __init__(self, base_ip, start_ip, end_ip, max_threads, ports, timeout):
        self.base_ip = base_ip
        self.current_ip = start_ip
        self.end_ip = end_ip

        self.max_threads = max_threads
        self.ports = ports
        self.timeout = timeout

        self.current_thread = 0
        self.running_threads = 0
        self.done_threads = 0
        self.worked_ips = []

        self.start_time = None

    def prep(self):
        self.start_time = datetime.now()
        print("Launching all threads. This might take a while...")

    def loop(self):
        while self.current_ip == self.end_ip:
            if self.running_threads != self.max_threads and self.running_threads < self.max_threads or self.max_threads == 0:
            
                self.current_thread += 1
                threading.Thread(target=self.ping, args=(self.base_ip, self.current_ip, self.ports, self.timeout)).start()
                self.current_ip += 1
            else:
                sleep(0.1)
        print("", flush=True)

        if self.done_threads != self.end_ip:
            print("Waiting for threads to finish...")

        while self.done_threads != self.end_ip:
            sleep(1)
            progressbar = "[" + "#" * (self.max_threads - self.running_threads) + "." * self.running_threads + "]"
            print("\r" + progressbar, end="", flush=True)

    def ping(self, base_ip, current_ip, ports, timeout):
        self.running_threads += 1
        put_in_ip = f"{base_ip}.{current_ip}"
        timeout_windows = timeout * 1000

        if name == 'nt':
            ping_command = f"ping -n 1 -w {timeout_windows} {put_in_ip}"
        else:
            ping_command = f"ping -c 1 -W {timeout} {put_in_ip}"

        try:
            ping_result = str(subprocess.check_output(ping_command, shell=True))
        except:
            ping_result = ""
        
        if 'ttl' in ping_result.lower():
            if len(self.ports) > 0:
                for port in ports:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(self.timeout)
                        port_works = s.connect_ex((put_in_ip, int(port)))
                    if port_works == 0:
                        ip_with_port = f"{put_in_ip}:{port}"
                        self.worked_ips.append(ip_with_port)

            else:
                self.worked_ips.append(put_in_ip)

        self.done_threads += 1
        self.running_threads -= 1

    def return_info(self):
        print("\n")
        end_time = datetime.now()
        execution_time = end_time - self.start_time
        execution_time = (datetime.min + execution_time).strftime("%Mm:%Ss")

        self.worked_ips.sort()
        print("Working ips:")
        for ip in self.worked_ips:
            print(ip)

        print("")
        print(f"It took {execution_time} to scan.")
        print(f"Scanned {self.done_threads} ip-adresses.")


ip_tools = Ip_tools()
ip_scanner = Ip_scanner(base_ip=base_ip, start_ip=start_ip, end_ip=end_ip, max_threads=max_threads, ports=ports, timeout=timeout)
ascii = '''
 ______  _______                                                                              
/      |/       \                                                                             
$$$$$$/ $$$$$$$  |        _______   _______   ______   _______   _______    ______    ______  
  $$ |  $$ |__$$ |       /       | /       | /      \ /       \ /       \  /      \  /      \ 
  $$ |  $$    $$/       /$$$$$$$/ /$$$$$$$/  $$$$$$  |$$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |
  $$ |  $$$$$$$/        $$      \ $$ |       /    $$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
 _$$ |_ $$ |             $$$$$$  |$$ \_____ /$$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$/ $$ |      
/ $$   |$$ |            /     $$/ $$       |$$    $$ |$$ |  $$ |$$ |  $$ |$$       |$$ |      
$$$$$$/ $$/             $$$$$$$/   $$$$$$$/  $$$$$$$/ $$/   $$/ $$/   $$/  $$$$$$$/ $$/       
                                                                                                                                                                                       
'''

print(ascii)

while True:
    print("Quick Ip scanner.")
    print("Made by Blnix.")

    print("1. Ip scanner")
    print("2. Domain to ip")
    print("3. Ip to location")
    print("4. Refresh settings")
    user = input()
    while user != "1" and user != "2" and user != "3" and user != "4":
        print("Invalid input...")
        user = input()

    if user == "1":
        ip_scanner.prep()
        ip_scanner.loop()
        ip_scanner.return_info()
        ip_scanner = Ip_scanner(base_ip=base_ip, start_ip=start_ip, end_ip=end_ip, max_threads=max_threads, ports=ports, timeout=timeout)

    elif user == "2":
        print("What Domain?")
        ip_tools_domain = input()
        ip_tools.dns(ip_tools_domain)

    elif user == "3":
        print("What Ip?")
        ip_tools_ip = input()
        ip_tools.ip_to_location(ip_tools_ip)

    elif user == "4":
        with open('settings.json') as f:
            settings = json.load(f)
            base_ip = settings.get("base_ip")
            start_ip = settings.get("start_ip")
            end_ip = settings.get("end_ip")
            max_threads = settings.get("max_threads")
            ports = settings.get("ports")
            timeout = settings.get("timeout")
        ip_scanner = Ip_scanner(base_ip=base_ip, start_ip=start_ip, end_ip=end_ip, max_threads=max_threads, ports=ports, timeout=timeout)
        print("Settings loaded.")

    print("\n" * 2)

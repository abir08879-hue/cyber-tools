import requests
import os
import sys

# ================= CONFIGURATION =================
# ANSI Color Codes for Red and Reset
RED = '\033[1;31m'
RESET = '\033[0m'

BANNER = f"""{RED}
   ██╗    ██╗███████╗     █████╗ ██████╗ ███████╗
   ██║    ██║██╔════╝    ██╔══██╗██╔══██╗██╔════╝
   ██║ █╗ ██║█████╗      ███████║██████╔╝█████╗  
   ██║███╗██║██╔══╝      ██╔══██║██╔══██╗██╔══╝  
   ╚███╔███╔╝███████╗    ██║  ██║██║  ██║███████╗
    ╚══╝╚══╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗ ██████╗ ██████╗  ██████╗███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    █████╗  ██║   ██║██████╔╝██║     █████╗  
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██║     ╚██████╔╝██║  ██║╚██████╗███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
{RESET}"""

DIV = f"{RED}────────────────────────────────────────────────────────{RESET}"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_own_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return None

def trace_ip(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'fail':
            return None, data.get('message', 'Unknown Error')
            
        return data, None
    except requests.exceptions.RequestException as e:
        return None, f"Network Error: {e}"

def display_results(data):
    print(f"\n{DIV}")
    print(f"🎯 TARGET IP: {data.get('query', 'N/A')}")
    print(f"{DIV}")
    print(f"📍 Country     : {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})")
    print(f"🏙️  City        : {data.get('city', 'N/A')}")
    print(f"🗺️  Region      : {data.get('regionName', 'N/A')}")
    print(f"📮 Zip Code    : {data.get('zip', 'N/A')}")
    print(f"🕒 Timezone    : {data.get('timezone', 'N/A')}")
    print(f"📡 ISP         : {data.get('isp', 'N/A')}")
    print(f"🏢 Organization: {data.get('org', 'N/A')}")
    print(f"🔢 AS          : {data.get('as', 'N/A')}")
    
    lat, lon = data.get('lat'), data.get('lon')
    if lat and lon:
        print(f"🗺️  Coordinates : {lat}, {lon}")
        print(f"🔗 Google Maps : https://www.google.com/maps?q={lat},{lon}")
    
    print(f"{DIV}\n")

def main():
    clear_screen()
    print(BANNER)
    print(f"          [ IP TRACER - BY KANHA ]\n")
    
    print("[+] Detecting your own IP...")
    own_ip = get_own_ip()
    if own_ip:
        print(f"[✓] Your Public IP: {own_ip}\n")
    else:
        print("[!] Could not detect your IP.\n")

    print("Options:")
    print("  [1] Trace your own IP")
    print("  [2] Trace a specific IP address")
    print("  [3] Exit")
    
    choice = input("\n[?] Enter your choice (1/2/3): ").strip()
    
    if choice == '1':
        if not own_ip:
            print("[-] Your IP could not be detected.")
            return
        target_ip = own_ip
    elif choice == '2':
        target_ip = input("[?] Enter target IP address: ").strip()
        if not target_ip:
            print("[-] IP address cannot be empty.")
            return
    elif choice == '3':
        print("[+] Exiting...")
        sys.exit(0)
    else:
        print("[-] Invalid choice.")
        return

    print(f"\n[+] Tracing IP: {target_ip}...")
    data, error = trace_ip(target_ip)
    
    if error:
        print(f"\n[!] Error: {error}")
    else:
        display_results(data)

if __name__ == "__main__":
    main()

import requests
import time
import random

def get_indian_proxies():
    """Fetches a list of free Indian proxies from ProxyScrape."""
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=IN&ssl=all&anonymity=anonymous"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        proxies = response.text.strip().split("\r\n")
        # Filter empty lines
        proxies = [p for p in proxies if p.strip()]
        return proxies
    except Exception as e:
        print(f"[WARNING] Failed to fetch proxy list: {e}")
        return []

def robust_get(url, headers=None, stream=False):
    """
    Tries to safely GET a URL directly first. 
    If it fails (like GitHub Actions being blocked by AKTU), 
    it rotates through free Indian Proxies until successful!
    """
    # Attempt direct connection first (Local Run)
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False, stream=stream)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"[WARNING] Direct connection failed ({e}). Engaging Indian Proxy Rotator for Bypassing Block...")

    # Attempt via VPN proxy routing (GitHub Actions Run)
    proxies = get_indian_proxies()
    random.shuffle(proxies)
    
    for proxy_ip in proxies[:5]: # Try up to 5 proxies to save time
        proxy_dict = {"http": f"http://{proxy_ip}", "https": f"http://{proxy_ip}"}
        print(f"   [INFO] Trying Proxy -> {proxy_ip}...")
        try:
            response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=15, verify=False, stream=stream)
            response.raise_for_status()
            print("   [SUCCESS] Connected securely through proxy!")
            return response
        except requests.RequestException:
            print("   [ERROR] Proxy connection failed. Trying next...")
            continue
            
    # Absolute failure
    raise Exception(f"Failed to access {url} directly and all proxies were blocked or offline.")

import requests
import ipaddress
from datetime import datetime, timezone

URL = "https://core.telegram.org/resources/cidr.txt"
HEADER = "# Original file: " + URL + "\n/ip firewall address-list\n"
OUTPUT_FILE = "vless/mikrotik/telegram_cidr_ipv4.rsc"

def main():
    resp = requests.get(URL)
    resp.raise_for_status()
    lines = resp.text.splitlines()
    cidrs = [line.strip() for line in lines if line.strip()]
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    result = "# Generated at: " + generated_at + "\n" + HEADER

    if not cidrs:
        raise ValueError("No cidrs found")

    for cidr in cidrs:
        try:
            net = ipaddress.ip_network(cidr.strip())

            if isinstance(net, ipaddress.IPv4Network):
                result += f"add list=TELEGRAM-CIDR comment=TELEGRAM-CIDR address={cidr}\n"
        except ValueError:
            pass

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    main()

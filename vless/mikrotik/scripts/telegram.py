import requests
from datetime import datetime, timezone

URL = "https://raw.githubusercontent.com/fernvenue/telegram-cidr-list/refs/heads/master/CIDRv4.txt"
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
        result += f"add list=TELEGRAM-CIDR comment=TELEGRAM-CIDR address={cidr}\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    main()

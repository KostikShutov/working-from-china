import requests
import ipaddress
from datetime import datetime, timezone


def get_lines(url: str) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    if not lines:
        raise ValueError("No lines found")

    return lines


def is_ipv4(ip: str) -> bool:
    try:
        return isinstance(ipaddress.ip_network(ip), ipaddress.IPv4Network)
    except ValueError:
        return False


def strip(line: str) -> str:
    return line.strip(' ,#/')


def generate_file(lines: list[str], listName: str, url: str, outputFile: str) -> None:
    result = ""

    for line in lines:
        line = strip(line)

        if is_ipv4(line):
            result += f"add list={listName}-CIDR comment={listName}-CIDR address={line}\n"

    if not result:
        raise ValueError("No cidrs generated")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    result = f"# Generated at: {now}\n# Original file: {url}\n/ip firewall address-list\n" + result

    with open(outputFile, "w", encoding="utf-8") as f:
        f.write(result)

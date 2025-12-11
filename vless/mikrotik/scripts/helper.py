import requests
import ipaddress
from datetime import datetime, timezone


def get_lines(url: str) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    if not lines:
        raise ValueError(f"No lines received from url {url}")

    return lines


def is_ipv4(ip: str) -> bool:
    try:
        return isinstance(ipaddress.ip_network(ip), ipaddress.IPv4Network)
    except ValueError:
        return False


def strip(line: str) -> str:
    return line.strip(' ,#/_')


def generate_file(lines: list[str], list_name: str, url: str, output_file: str) -> None:
    cidrs = ""

    for line in lines:
        line = strip(line)

        if is_ipv4(line):
            cidrs += f"add list={list_name}-CIDR comment={list_name}-CIDR address={line}\n"

    if not cidrs:
        raise ValueError("No cidrs generated")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    result = f"# Generated at: {now}\n# Original file: {url}\n/ip firewall address-list\n" + cidrs

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

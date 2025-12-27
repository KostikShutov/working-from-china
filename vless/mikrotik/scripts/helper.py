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


def get_opencck_lines(url: str) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json().values()
    lines = []

    for cidr_list in data:
        for cidr in cidr_list:
            lines.append(strip(cidr))

    if not lines:
        raise ValueError(f"No lines received from url {url}")

    return lines


def is_ipv4(ip: str) -> bool:
    try:
        return isinstance(ipaddress.ip_network(ip, strict=False), ipaddress.IPv4Network)
    except ValueError:
        return False


def strip(line: str) -> str:
    return line.strip(' ,#/_')


def generate_file(name: str, lines: list[str], urls: list[str]) -> None:
    def covered(cidr: ipaddress.IPv4Network, kept: list[ipaddress.IPv4Network]) -> bool:
        for big in kept:
            if cidr.subnet_of(big):
                return True

        return False

    list_name = name.upper()
    lines = list(dict.fromkeys(lines))
    cidrs: list[ipaddress.IPv4Network] = []

    for line in lines:
        line = strip(line)

        if is_ipv4(line):
            cidrs.append(ipaddress.IPv4Network(line, strict=False))

    if not cidrs:
        raise ValueError("No cidrs generated")

    cidrs.sort(key=lambda n: n.prefixlen)
    kept: list[ipaddress.IPv4Network] = []

    for cidr in cidrs:
        if not covered(cidr, kept):
            kept.append(cidr)

    if not kept:
        raise ValueError("No cidrs after filtered")

    cidr_list: str = ""

    for address in kept:
        cidr_list += f"add list={list_name}-CIDR comment={list_name}-CIDR address={str(address)}\n"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    result = f"# Generated at: {now}\n"

    for url in urls:
        result += f"# Original file: {url}\n"

    result += "/ip firewall address-list\n" + cidr_list

    with open("vless/mikrotik/" + name + "_cidr_ipv4.rsc", "w", encoding="utf-8") as f:
        f.write(result)

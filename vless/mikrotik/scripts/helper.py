import requests
import ipaddress
from datetime import datetime, timezone
from config import ConfigUrls


def get_lines(url: str) -> list[str]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    lines = response.text.splitlines()

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


def generate_service_file(name: str, urls: list[str], others: list[str]) -> None:
    with_others: bool = others != []

    for url in urls:
        for line in get_lines(url):
            others.append(strip(line))

    if with_others:
        urls.append(ConfigUrls.OTHERS_URL)

    generate_file(name=name, lines=others, urls=urls)


def generate_file(name: str, lines: list[str], urls: list[str]) -> None:
    def get_cidrs(lines: list[str]) -> list[ipaddress.IPv4Network]:
        cidrs: list[ipaddress.IPv4Network] = []

        for line in lines:
            line = strip(line)

            if is_ipv4(line):
                cidrs.append(ipaddress.IPv4Network(line, strict=False))

        if not cidrs:
            raise ValueError("No cidrs generated")

        cidrs.sort(key=lambda n: n.prefixlen)

        return cidrs

    def filter_cidrs(cidrs: list[ipaddress.IPv4Network]) -> list[ipaddress.IPv4Network]:
        kept: list[ipaddress.IPv4Network] = []

        for cidr in cidrs:
            if not subnet_of(cidr, kept):
                kept.append(cidr)

        if not kept:
            raise ValueError("No cidrs after filtered")

        return kept

    def subnet_of(cidr: ipaddress.IPv4Network, kept: list[ipaddress.IPv4Network]) -> bool:
        for big in kept:
            if cidr.subnet_of(big):
                return True

        return False

    lines = list(dict.fromkeys(lines))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    result: str = f"# Generated at: {now}\n"

    for url in urls:
        result += f"# Original file: {url}\n"

    list_name = name.upper()
    cidr_list: str = ""

    for cidr in filter_cidrs(get_cidrs(lines)):
        cidr_list += f"add list={list_name}-CIDR comment={list_name}-CIDR address={str(cidr)}\n"

    result += "/ip firewall address-list\n" + cidr_list

    with open("vless/mikrotik/" + name + "_cidr_ipv4.rsc", "w", encoding="utf-8") as f:
        f.write(result)

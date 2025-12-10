import re
import requests
import ipaddress
from datetime import datetime, timezone

URL = "https://gist.githubusercontent.com/iamwildtuna/7772b7c84a11bf6e1385f23096a73a15/raw/9aa7c097b0721bac547fa26eb2cbf6c58d3cf22b/gistfile2.txt"
HEADER = "# Original file: " + URL + "\n/ip firewall address-list\n"
OUTPUT_DIR = "vless/mikrotik/"
STRIP = ' ,#/'


def clean_text(text: str) -> str:
    text = re.sub(r'[А-Яа-яЁё]', '', text)
    text = re.sub(r'[^A-Za-z0-9]', '_', text)
    text = re.sub(r'_+', '_', text)
    text = text.strip('_')

    return text.lower()


def filter_lines(lines: list[str]) -> list[str]:
    pattern = re.compile(r'route|узл|подс|адр', re.IGNORECASE)

    return [line for line in lines if line and not pattern.search(line)]


def is_ipv4(ip: str) -> bool:
    try:
        net = ipaddress.ip_network(ip)

        return isinstance(net, ipaddress.IPv4Network)
    except ValueError:
        return False


def prepare_services(lines: list[str]) -> dict[str, list[str]]:
    services: dict[str, list[str]] = {}
    current_service = ""

    for line in lines:
        cidrs = line.strip(STRIP).split()
        first = cidrs[0].strip(STRIP)

        if is_ipv4(first):
            if not current_service:
                raise ValueError("Current service can not be empty")

            for cidr in cidrs:
                cidr = cidr.strip(STRIP)

                if is_ipv4(cidr):
                    if current_service not in services:
                        services[current_service] = []

                    services[current_service].append(cidr)

        else:
            current_service = clean_text(first)

    return services


def main():
    resp = requests.get(URL)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    if not lines:
        raise ValueError("No lines found")

    lines = filter_lines(lines)

    if not lines:
        raise ValueError("No lines after filtering")

    services: dict[str, list[str]] = prepare_services(lines)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    for service, cidrs in services.items():
        if service not in ["chatgpt", "meta", "twitter", "medium_com"]:
            continue

        result = ""

        for cidr in cidrs:
            try:
                net = ipaddress.ip_network(cidr.strip())

                if isinstance(net, ipaddress.IPv4Network):
                    result += f"add list={service.upper()}-CIDR comment={service.upper()}-CIDR address={cidr}\n"
            except ValueError:
                pass

        result = "# Generated at: " + generated_at + "\n" + HEADER + result

        if not result:
            raise ValueError("No cidrs generated for " + service)

        with open(OUTPUT_DIR + service + "_cidr_ipv4.rsc", "w", encoding="utf-8") as f:
            f.write(result)


if __name__ == "__main__":
    main()

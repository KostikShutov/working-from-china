import re
from helper import get_lines, is_ipv4, strip, generate_file

URL = "https://gist.githubusercontent.com/iamwildtuna/7772b7c84a11bf6e1385f23096a73a15/raw/9aa7c097b0721bac547fa26eb2cbf6c58d3cf22b/gistfile2.txt"
HEADER = "# Original file: " + URL + "\n/ip firewall address-list\n"
OUTPUT_DIR = "vless/mikrotik/"
WHITE_LIST = ["chatgpt", "meta", "twitter", "medium_com"]


def clean_text(text: str) -> str:
    text = re.sub(r'[А-Яа-яЁё]', '', text)
    text = re.sub(r'[^A-Za-z0-9]', '_', text)
    text = re.sub(r'_+', '_', text)
    text = text.strip('_')

    return text.lower()


def filter_lines(lines: list[str]) -> list[str]:
    pattern = re.compile(r'route|узл|подс|адр', re.IGNORECASE)
    lines = [line for line in lines if line and not pattern.search(line)]

    if not lines:
        raise ValueError("No lines after filtering")

    return lines


def prepare_services(lines: list[str]) -> dict[str, list[str]]:
    services: dict[str, list[str]] = {}
    current_service = ""

    for line in lines:
        cidrs = strip(line).split()
        first = strip(cidrs[0])

        if is_ipv4(first):
            if not current_service:
                raise ValueError("Current service can not be empty")

            for cidr in cidrs:
                if current_service not in services:
                    services[current_service] = []

                services[current_service].append(cidr)
        else:
            current_service = clean_text(first)

    return services


def main():
    lines = get_lines(URL)
    lines = filter_lines(lines)
    services: dict[str, list[str]] = prepare_services(lines)

    for service, cidrs in services.items():
        if service not in WHITE_LIST:
            continue

        generate_file(
            lines=cidrs,
            listName=service.upper(),
            url=URL,
            outputFile=OUTPUT_DIR + service + "_cidr_ipv4.rsc",
        )


if __name__ == "__main__":
    main()

import re
from helper import get_lines, is_ipv4, strip, generate_file

URL = "https://gist.githubusercontent.com/iamwildtuna/7772b7c84a11bf6e1385f23096a73a15/raw/9aa7c097b0721bac547fa26eb2cbf6c58d3cf22b/gistfile2.txt"
OUTPUT_DIR = "vless/mikrotik/"
CHATGPT = "chatgpt"
META = "meta"
TWITTER = "twitter"
MEDIUM = "medium_com"
WHITE_LIST = [CHATGPT, META, TWITTER, MEDIUM]


def clean_text(text: str) -> str:
    text = re.sub(r'[А-Яа-яЁё]', '', text)
    text = re.sub(r'[^A-Za-z0-9]', '_', text)
    text = re.sub(r'_+', '_', text)

    return strip(text).lower()


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
        sublines = strip(line).split()
        first = strip(sublines[0])

        if is_ipv4(first):
            if not current_service:
                raise ValueError("Current service can not be empty")

            for subline in sublines:
                if current_service not in services:
                    services[current_service] = []

                services[current_service].append(subline)
        else:
            current_service = clean_text(first)

    return services


def main():
    lines = get_lines(URL)
    lines = filter_lines(lines)
    services: dict[str, list[str]] = prepare_services(lines)

    for white_service in WHITE_LIST:
        if white_service not in services:
            raise ValueError(f"Service {white_service} not found in white list")

        lines = services[white_service]

        generate_file(
            lines=lines,
            list_name=white_service.upper(),
            url=URL,
            output_file=OUTPUT_DIR + white_service + "_cidr_ipv4.rsc",
        )


if __name__ == "__main__":
    main()

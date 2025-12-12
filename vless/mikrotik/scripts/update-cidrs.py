import re
from helper import get_lines, is_ipv4, strip, generate_file

TELEGRAM_URL = "https://core.telegram.org/resources/cidr.txt"
WHATSAPP_URL = "https://raw.githubusercontent.com/HybridNetworks/whatsapp-cidr/refs/heads/main/WhatsApp/whatsapp_cidr_ipv4.txt"
META_URL = "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/meta.lst"
YOUTUBE_URL = "https://raw.githubusercontent.com/touhidurrr/iplist-youtube/refs/heads/main/lists/cidr4.txt"
OTHERS_URL = "https://gist.githubusercontent.com/iamwildtuna/7772b7c84a11bf6e1385f23096a73a15/raw/9aa7c097b0721bac547fa26eb2cbf6c58d3cf22b/gistfile2.txt"
JETBRAINS_URL = "https://raw.githubusercontent.com/KostikShutov/iplist-jetbrains/refs/heads/main/lists/cidr4.txt"
OUTPUT_DIR = "vless/mikrotik/"
CHATGPT = "chatgpt"
META = "meta"
TWITTER = "twitter"
MEDIUM = "medium_com"
YOUTUBE = "youtube"
WHITE_LIST = [CHATGPT, META, TWITTER, MEDIUM, YOUTUBE]


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


def merge_meta_files(meta: list[str]) -> list[str]:
    lines = get_lines(WHATSAPP_URL)

    for line in lines:
        meta.append(strip(line))

    lines = get_lines(META_URL)

    for line in lines:
        meta.append(strip(line))

    return meta


def merge_youtube_files(youtube: list[str]) -> list[str]:
    lines = get_lines(YOUTUBE_URL)

    for line in lines:
        youtube.append(strip(line))

    return youtube


def main():
    lines = get_lines(OTHERS_URL)
    lines = filter_lines(lines)
    services: dict[str, list[str]] = prepare_services(lines)
    services[META] = merge_meta_files(services[META])
    services[YOUTUBE] = merge_youtube_files(services[YOUTUBE])

    for white_service in WHITE_LIST:
        if white_service not in services:
            raise ValueError(f"Service {white_service} not found in white list")

        lines = services[white_service]

        if white_service == META:
            urls = [OTHERS_URL, WHATSAPP_URL, META_URL]
        elif white_service == YOUTUBE:
            urls = [OTHERS_URL, YOUTUBE_URL]
        else:
            urls = [OTHERS_URL]

        generate_file(
            lines=lines,
            list_name=white_service.upper(),
            urls=urls,
            output_file=OUTPUT_DIR + white_service + "_cidr_ipv4.rsc",
        )

    generate_file(
        lines=get_lines(TELEGRAM_URL),
        list_name="TELEGRAM",
        urls=[TELEGRAM_URL],
        output_file=OUTPUT_DIR + "telegram_cidr_ipv4.rsc",
    )

    generate_file(
        lines=get_lines(JETBRAINS_URL),
        list_name="JETBRAINS",
        urls=[JETBRAINS_URL],
        output_file=OUTPUT_DIR + "jetbrains_cidr_ipv4.rsc",
    )


if __name__ == "__main__":
    main()

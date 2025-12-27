import re
from helper import get_lines, is_ipv4, strip, generate_service_file
from config import ConfigUrls, ConfigNames


def prepare_others() -> dict[str, list[str]]:
    def filter_lines(lines: list[str]) -> list[str]:
        pattern = re.compile(r'route|узл|подс|адр', re.IGNORECASE)
        lines = [line for line in lines if line and not pattern.search(line)]

        if not lines:
            raise ValueError("No lines after filtering")

        return lines

    def clean_text(text: str) -> str:
        text = re.sub(r'[А-Яа-яЁё]', '', text)
        text = re.sub(r'[^A-Za-z0-9]', '_', text)
        text = re.sub(r'_+', '_', text)

        return strip(text).lower()

    lines = filter_lines(get_lines(ConfigUrls.OTHERS_URL))
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
    others: dict[str, list[str]] = prepare_others()

    for service in ConfigNames.OTHERS_LIST:
        if service not in others:
            raise ValueError(f"Service {service} not found in others list")

    generate_service_file(
        name=ConfigNames.CHATGPT,
        urls=[ConfigUrls.CHATGPT_URL_OPEN],
        others=others[ConfigNames.CHATGPT],
    )

    generate_service_file(
        name=ConfigNames.JETBRAINS,
        urls=[ConfigUrls.JETBRAINS_URL_OPEN, ConfigUrls.JETBRAINS_URL_OWN],
        others=[],
    )

    generate_service_file(
        name=ConfigNames.LINKEDIN,
        urls=[ConfigUrls.LINKEDIN_URL_OPEN],
        others=others[ConfigNames.LINKEDIN],
    )

    generate_service_file(
        name=ConfigNames.MEDIUM,
        urls=[ConfigUrls.MEDIUM_URL_OPEN],
        others=others[ConfigNames.MEDIUM],
    )

    generate_service_file(
        name=ConfigNames.META,
        urls=[ConfigUrls.WHATSAPP_URL, ConfigUrls.META_URL, ConfigUrls.META_URL_OPEN],
        others=others[ConfigNames.META],
    )

    generate_service_file(
        name=ConfigNames.TELEGRAM,
        urls=[ConfigUrls.TELEGRAM_URL],
        others=[]
    )

    generate_service_file(
        name=ConfigNames.TWITTER,
        urls=[ConfigUrls.TWITTER_URL_OPEN],
        others=others[ConfigNames.TWITTER],
    )

    generate_service_file(
        name=ConfigNames.YOUTUBE,
        urls=[ConfigUrls.YOUTUBE_URL, ConfigUrls.YOUTUBE_URL_OPEN],
        others=others[ConfigNames.YOUTUBE],
    )


if __name__ == "__main__":
    main()

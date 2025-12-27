import re
from helper import get_lines, get_opencck_lines, is_ipv4, strip
from config import ConfigUrls, ConfigNames
from chatgpt import merge_chatgpt_files, generate_chatgpt_file
from jetbrains import merge_jetbrains_files, generate_jetbrains_file
from medium import generate_medium_file
from meta import merge_meta_files, generate_meta_file
from telegram import generate_telegram_file
from twitter import merge_twitter_files, generate_twitter_file
from youtube import merge_youtube_files, generate_youtube_file


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
    lines = get_lines(ConfigUrls.OTHERS_URL)
    lines = filter_lines(lines)
    services: dict[str, list[str]] = prepare_services(lines)
    services[ConfigNames.CHATGPT] = merge_chatgpt_files(services[ConfigNames.CHATGPT])
    services[ConfigNames.META] = merge_meta_files(services[ConfigNames.META])
    services[ConfigNames.TWITTER] = merge_twitter_files(services[ConfigNames.TWITTER])
    services[ConfigNames.YOUTUBE] = merge_youtube_files(services[ConfigNames.YOUTUBE])
    services[ConfigNames.JETBRAINS] = merge_jetbrains_files(get_opencck_lines(ConfigUrls.JETBRAINS_URL_OPEN))
    services[ConfigNames.TELEGRAM] = get_lines(ConfigUrls.TELEGRAM_URL)

    for white_service in ConfigNames.WHITE_LIST:
        if white_service not in services:
            raise ValueError(f"Service {white_service} not found in white list")

    generate_chatgpt_file(services[ConfigNames.CHATGPT])
    generate_jetbrains_file(services[ConfigNames.JETBRAINS])
    generate_medium_file(services[ConfigNames.MEDIUM])
    generate_meta_file(services[ConfigNames.META])
    generate_telegram_file(services[ConfigNames.TELEGRAM])
    generate_twitter_file(services[ConfigNames.TWITTER])
    generate_youtube_file(services[ConfigNames.YOUTUBE])


if __name__ == "__main__":
    main()

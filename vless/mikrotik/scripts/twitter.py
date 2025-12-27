from helper import get_opencck_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_twitter_files(twitter: list[str]) -> list[str]:
    for line in get_opencck_lines(ConfigUrls.TWITTER_URL_OPEN):
        twitter.append(strip(line))

    return twitter


def generate_twitter_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.TWITTER,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL, ConfigUrls.TWITTER_URL_OPEN],
    )

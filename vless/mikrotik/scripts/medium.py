from helper import get_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_medium_files(medium: list[str]) -> list[str]:
    for line in get_lines(ConfigUrls.MEDIUM_URL_OPEN):
        medium.append(strip(line))

    return medium


def generate_medium_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.MEDIUM,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL, ConfigUrls.MEDIUM_URL_OPEN],
    )

from helper import get_opencck_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_chatgpt_files(medium: list[str]) -> list[str]:
    for line in get_opencck_lines(ConfigUrls.MEDIUM_URL_OPEN):
        medium.append(strip(line))

    return medium


def generate_medium_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.MEDIUM,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL],
    )

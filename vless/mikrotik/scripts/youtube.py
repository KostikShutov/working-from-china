from helper import get_lines, get_opencck_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_youtube_files(youtube: list[str]) -> list[str]:
    for line in get_lines(ConfigUrls.YOUTUBE_URL):
        youtube.append(strip(line))

    for line in get_opencck_lines(ConfigUrls.YOUTUBE_URL_OPEN):
        youtube.append(strip(line))

    return youtube


def generate_youtube_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.YOUTUBE,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL, ConfigUrls.YOUTUBE_URL, ConfigUrls.YOUTUBE_URL_OPEN],
    )

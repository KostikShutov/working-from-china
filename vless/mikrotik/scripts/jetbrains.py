from helper import get_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_jetbrains_files(jetbrains: list[str]) -> list[str]:
    for line in get_lines(ConfigUrls.JETBRAINS_URL_OWN):
        jetbrains.append(strip(line))

    return jetbrains


def generate_jetbrains_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.JETBRAINS,
        lines=lines,
        urls=[ConfigUrls.JETBRAINS_URL_OPEN, ConfigUrls.JETBRAINS_URL_OWN],
    )

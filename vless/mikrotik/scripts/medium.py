from helper import generate_file
from config import ConfigUrls, ConfigNames


def generate_medium_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.MEDIUM,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL],
    )

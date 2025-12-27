from helper import generate_file
from config import ConfigUrls, ConfigNames


def generate_telegram_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.TELEGRAM,
        lines=lines,
        urls=[ConfigUrls.TELEGRAM_URL],
    )

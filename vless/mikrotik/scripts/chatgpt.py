from helper import generate_file
from config import ConfigUrls, ConfigNames


def generate_chatgpt_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.CHATGPT,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL],
    )

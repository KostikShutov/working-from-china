from helper import get_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_chatgpt_files(chatgpt: list[str]) -> list[str]:
    for line in get_lines(ConfigUrls.CHATGPT_URL_OPEN):
        chatgpt.append(strip(line))

    return chatgpt


def generate_chatgpt_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.CHATGPT,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL, ConfigUrls.CHATGPT_URL_OPEN],
    )

from helper import get_lines, strip, generate_file
from config import ConfigUrls, ConfigNames


def merge_meta_files(meta: list[str]) -> list[str]:
    for line in get_lines(ConfigUrls.WHATSAPP_URL):
        meta.append(strip(line))

    for line in get_lines(ConfigUrls.META_URL):
        meta.append(strip(line))

    for line in get_lines(ConfigUrls.META_URL_OPEN):
        meta.append(strip(line))

    return meta


def generate_meta_file(lines: list[str]) -> None:
    generate_file(
        name=ConfigNames.META,
        lines=lines,
        urls=[ConfigUrls.OTHERS_URL, ConfigUrls.WHATSAPP_URL, ConfigUrls.META_URL, ConfigUrls.META_URL_OPEN],
    )

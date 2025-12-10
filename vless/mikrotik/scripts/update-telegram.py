from helper import get_lines, generate_file

URL = "https://core.telegram.org/resources/cidr.txt"
LIST_NAME = "TELEGRAM"
OUTPUT_FILE = "vless/mikrotik/telegram_cidr_ipv4.rsc"


def main():
    generate_file(
        lines=get_lines(URL),
        listName="TELEGRAM",
        url=URL,
        outputFile=OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()

# Установка и настройка на VPS сервере Wireguard

1. Обновляемся и готовимся

    ```bash
    sudo apt update
    sudo apt upgrade
    sudo apt install curl
    ```

2. Скачать скрипт

    ```bash
    curl -O https://raw.githubusercontent.com/angristan/wireguard-install/master/wireguard-install.sh
    chmod +x wireguard-install.sh
    ```

3. Запустить скрипт

    ```bash
    sudo ./wireguard-install.sh
    ```

Источник: <https://habr.com/ru/sandbox/189100/>

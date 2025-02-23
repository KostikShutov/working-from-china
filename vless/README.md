# Установка и настройка на VPS сервере VLESS

1. Устанавливаем пакеты:

    ```bash
    apt install curl mc htop nano
    ```

2. Устанавливаем v2ray (включает vless):

    ```bash
    bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
    ```

3. Останавливаем v2ray:

    ```bash
    systemctl stop xray.service
    ```

4. Генерируем uuid для конфигурации:

    ```bash
    /usr/local/bin/xray uuid
    ```

5. Генерируем ключи для конфигурации (ключи стоит записать, они нигде не сохранятся в виде файла):

    ```bash
    /usr/local/bin/xray x25519
    ```

6. Редактируем конфигурацию:

    ```bash
    nano /usr/local/etc/xray/config.json
    ```

    Пример конфига:

    ```json
    {
        "log": {
            "loglevel": "info"
        },
        "routing": {
            "rules": [],
            "domainStrategy": "AsIs"
        },
        "inbounds": [
            {
            "port": 443,
            "protocol": "vless",
            "tag": "vless_tls",
            "settings": {
                "clients": [
                {
                    "id": "сюда вставить ID из выхлопа ./usr/local/bin/xray uuid",
                    "email": "user@server",
                    "flow": "xtls-rprx-vision"
                }
                ],
                "decryption": "none"
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                "show": false,
                "dest": "www.microsoft.com:443",
                "xver": 0,
                "serverNames": ["www.microsoft.com"],
                "privateKey": "сюда вставить приватный ключ из выхлопа ./usr/local/bin/xray x25519",
                "minClientVer": "",
                "maxClientVer": "",
                "maxTimeDiff": 0,
                "shortIds": ["сюда вставить выхлоп команды openssl rand -hex 8"]
                }
            },
            "sniffing": {
                "enabled": true,
                "destOverride": ["http", "tls"]
            }
            }
        ],
        "outbounds": [
            {
            "protocol": "freedom",
            "tag": "direct"
            },
            {
            "protocol": "blackhole",
            "tag": "block"
            }
        ]
    }
    ```

7. Запускаем v2ray:

    ```bash
    systemctl start xray.service
    ```

Источник: <https://habr.com/ru/articles/844760/>

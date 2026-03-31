# Архитектура multi-hop

Конфиг первого сервера:

Пример конфига:

```json
{
    "log": {
        "loglevel": "info"
    },
    "routing": {
        "rules": [
            {
                "type": "field",
                "outboundTag": "to_remote",
                "network": "tcp,udp"
            }
        ],
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
                    "dest": "ya.ru:443",
                    "xver": 0,
                    "serverNames": ["ya.ru"],
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
        },
        {
            "protocol": "vless",
            "tag": "to_remote",
            "settings": {
                "vnext": [
                    {
                        "address": "REMOTE_SERVER_IP",
                        "port": 443,
                        "users": [
                            {
                                "id": "UUID_УДАЛЕННОГО_СЕРВЕРА",
                                "encryption": "none",
                                "flow": "xtls-rprx-vision"
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                    "serverName": "ya.ru",
                    "publicKey": "PUBLIC_KEY_УДАЛЕННОГО",
                    "shortId": "SHORT_ID_УДАЛЕННОГО",
                    "fingerprint": "chrome"
                }
            }
        }
    ]
}
```

Клиент (вы) подключаетесь к текущему серверу в inbounds, а middle сервер подключается к конечному серверу в outbounds. На конечном сервере [обычная настройка vless](../README.md).
